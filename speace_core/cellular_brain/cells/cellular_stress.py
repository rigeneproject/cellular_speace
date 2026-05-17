from typing import Dict, List, Literal

from pydantic import BaseModel, Field

from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron
from speace_core.cellular_brain.circuits.neural_circuit import NeuralCircuit


StressLevel = Literal["low", "medium", "high", "critical"]


class CellularStressState(BaseModel):
    """Per-cell stress snapshot computed by the CellularStressEngine."""

    cell_id: str
    stress_score: float = 0.0
    level: StressLevel = "low"
    energy_contribution: float = 0.0
    activation_contribution: float = 0.0
    firing_rate_contribution: float = 0.0
    apoptosis_risk_contribution: float = 0.0


class CellularStressResult(BaseModel):
    """Aggregate result of a stress evaluation pass."""

    per_cell: Dict[str, CellularStressState] = Field(default_factory=dict)
    mean_stress: float = 0.0
    max_stress: float = 0.0
    critical_count: int = 0
    high_count: int = 0
    medium_count: int = 0


class CellularStressEngine:
    """T42 — Evaluate per-cell stress from energy, activation, and history.

    Stress accumulates when a neuron is energetically depleted, hyperactive,
    or carries high apoptosis risk. Stress levels drive downstream damage,
    repair, defense, and epigenetic adaptation.
    """

    def __init__(
        self,
        energy_weight: float = 0.35,
        activation_weight: float = 0.25,
        firing_weight: float = 0.20,
        apoptosis_risk_weight: float = 0.20,
        critical_threshold: float = 0.75,
        high_threshold: float = 0.50,
        medium_threshold: float = 0.25,
    ):
        self.energy_weight = energy_weight
        self.activation_weight = activation_weight
        self.firing_weight = firing_weight
        self.apoptosis_risk_weight = apoptosis_risk_weight
        self.critical_threshold = critical_threshold
        self.high_threshold = high_threshold
        self.medium_threshold = medium_threshold

    def evaluate(self, circuit: NeuralCircuit) -> CellularStressResult:
        all_neurons = (
            circuit.input_neurons
            + circuit.hidden_neurons
            + circuit.output_neurons
        )
        per_cell: Dict[str, CellularStressState] = {}
        scores: List[float] = []
        critical_count = 0
        high_count = 0
        medium_count = 0

        for neuron in all_neurons:
            state = self._compute_stress(neuron)
            per_cell[neuron.cell_id] = state
            scores.append(state.stress_score)
            if state.level == "critical":
                critical_count += 1
            elif state.level == "high":
                high_count += 1
            elif state.level == "medium":
                medium_count += 1

        mean_stress = sum(scores) / len(scores) if scores else 0.0
        max_stress = max(scores) if scores else 0.0
        return CellularStressResult(
            per_cell=per_cell,
            mean_stress=round(mean_stress, 4),
            max_stress=round(max_stress, 4),
            critical_count=critical_count,
            high_count=high_count,
            medium_count=medium_count,
        )

    def _compute_stress(self, neuron: DigitalNeuron) -> CellularStressState:
        # Energy depletion stress (inverse of energy)
        energy_stress = max(0.0, 1.0 - neuron.energy)
        # Activation stress (high sustained activation)
        activation_stress = min(1.0, abs(neuron.activation) / 2.0)
        # Firing rate stress (consecutive fires)
        firing_stress = min(1.0, neuron.consecutive_fires / 5.0)
        # Apoptosis risk stress
        apoptosis_stress = min(1.0, getattr(neuron, "apoptosis_risk", 0.0))

        stress_score = (
            self.energy_weight * energy_stress
            + self.activation_weight * activation_stress
            + self.firing_weight * firing_stress
            + self.apoptosis_risk_weight * apoptosis_stress
        )
        stress_score = min(1.0, stress_score)

        if stress_score >= self.critical_threshold:
            level: StressLevel = "critical"
        elif stress_score >= self.high_threshold:
            level = "high"
        elif stress_score >= self.medium_threshold:
            level = "medium"
        else:
            level = "low"

        return CellularStressState(
            cell_id=neuron.cell_id,
            stress_score=round(stress_score, 4),
            level=level,
            energy_contribution=round(energy_stress, 4),
            activation_contribution=round(activation_stress, 4),
            firing_rate_contribution=round(firing_stress, 4),
            apoptosis_risk_contribution=round(apoptosis_stress, 4),
        )
