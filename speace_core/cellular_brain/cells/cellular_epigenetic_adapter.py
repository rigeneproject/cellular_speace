from typing import Dict, List

from pydantic import BaseModel, Field

from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron
from speace_core.cellular_brain.circuits.neural_circuit import NeuralCircuit
from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType


class GeneExpressionProfile(BaseModel):
    """Local gene expression profile for a single cell."""

    cell_id: str
    stress_response_genes: List[str] = Field(default_factory=list)
    repair_genes: List[str] = Field(default_factory=list)
    defense_genes: List[str] = Field(default_factory=list)
    metabolic_genes: List[str] = Field(default_factory=list)
    expression_shift_count: int = 0
    last_shift_tick: int = 0


class EpigeneticShift(BaseModel):
    """Record of a single epigenetic shift."""

    cell_id: str
    tick: int
    trigger: str = ""
    genes_added: List[str] = Field(default_factory=list)
    genes_removed: List[str] = Field(default_factory=list)


class CellularEpigeneticResult(BaseModel):
    """Aggregate result of an epigenetic adaptation pass."""

    profiles: Dict[str, GeneExpressionProfile] = Field(default_factory=dict)
    shifts: List[EpigeneticShift] = Field(default_factory=list)
    epigenetic_shift_count: int = 0
    mean_gene_count: float = 0.0


class CellularEpigeneticAdapter:
    """T42 — Local epigenetic adaptation per cell.

    Each cell maintains its own gene expression profile. Stress and damage
    triggers shift expression toward stress-response, repair, defense, or
    metabolic genes. Shifts are recorded and influence downstream behavior.
    """

    def __init__(
        self,
        stress_response_threshold: float = 0.50,
        repair_trigger_threshold: float = 0.40,
        defense_trigger_threshold: float = 0.60,
        metabolic_boost_threshold: float = 0.30,
    ):
        self.stress_response_threshold = stress_response_threshold
        self.repair_trigger_threshold = repair_trigger_threshold
        self.defense_trigger_threshold = defense_trigger_threshold
        self.metabolic_boost_threshold = metabolic_boost_threshold

    def adapt(
        self,
        circuit: NeuralCircuit,
        stress_per_cell: Dict[str, "CellularStressState"],
        damage_per_cell: Dict[str, "CellularDamageState"],
        current_tick: int,
        memory: MorphologicalMemory | None = None,
    ) -> CellularEpigeneticResult:
        from speace_core.cellular_brain.cells.cellular_stress import CellularStressState
        from speace_core.cellular_brain.cells.cellular_damage import CellularDamageState

        all_neurons = (
            circuit.input_neurons
            + circuit.hidden_neurons
            + circuit.output_neurons
        )
        profiles: Dict[str, GeneExpressionProfile] = {}
        shifts: List[EpigeneticShift] = []

        for neuron in all_neurons:
            stress = stress_per_cell.get(neuron.cell_id)
            damage = damage_per_cell.get(neuron.cell_id)
            profile, shift = self._adapt_cell(
                neuron, stress, damage, current_tick
            )
            profiles[neuron.cell_id] = profile
            if shift is not None:
                shifts.append(shift)
                if memory is not None:
                    memory.create_event(
                        event_type=MorphologyEventType.CELLULAR_EPIGENETIC_SHIFT,
                        source_id="cellular_epigenetic_adapter",
                        target_id=neuron.cell_id,
                        metadata={
                            "trigger": shift.trigger,
                            "genes_added": shift.genes_added,
                            "genes_removed": shift.genes_removed,
                            "tick": current_tick,
                        },
                    )

        total_genes = sum(
            len(p.stress_response_genes)
            + len(p.repair_genes)
            + len(p.defense_genes)
            + len(p.metabolic_genes)
            for p in profiles.values()
        )
        mean_gene_count = total_genes / len(profiles) if profiles else 0.0

        return CellularEpigeneticResult(
            profiles=profiles,
            shifts=shifts,
            epigenetic_shift_count=len(shifts),
            mean_gene_count=round(mean_gene_count, 4),
        )

    def _adapt_cell(
        self,
        neuron: DigitalNeuron,
        stress: "CellularStressState | None",
        damage: "CellularDamageState | None",
        current_tick: int,
    ) -> tuple[GeneExpressionProfile, EpigeneticShift | None]:
        # Start from existing epigenetic marks if present
        existing_genes: List[str] = list(getattr(neuron, "epigenetic_marks", {}).keys())
        stress_score = stress.stress_score if stress else 0.0
        damage_score = damage.damage_score if damage else 0.0

        stress_genes: List[str] = []
        repair_genes: List[str] = []
        defense_genes: List[str] = []
        metabolic_genes: List[str] = []

        # Baseline metabolic genes
        if stress_score < self.metabolic_boost_threshold and damage_score < self.repair_trigger_threshold:
            metabolic_genes = ["metabolic_baseline", "energy_efficiency"]
        else:
            metabolic_genes = ["metabolic_baseline"]

        if stress_score >= self.stress_response_threshold:
            stress_genes = ["hsp70_like", "oxidative_stress_response", "calcium_buffering"]
        if damage_score >= self.repair_trigger_threshold:
            repair_genes = ["dna_repair_like", "proteostasis", "autophagy_like"]
        if stress_score >= self.defense_trigger_threshold or damage_score >= 0.50:
            defense_genes = ["immune_like_response", "inflammatory_dampening", "barrier_reinforcement"]

        added: List[str] = []
        removed: List[str] = []

        all_new = stress_genes + repair_genes + defense_genes + metabolic_genes
        for g in all_new:
            if g not in existing_genes:
                added.append(g)

        for g in existing_genes:
            if g not in all_new and g.startswith(("hsp", "dna_repair", "immune_like", "inflammatory")):
                removed.append(g)

        existing_marks = getattr(neuron, "epigenetic_marks", {}) or {}
        existing_shift_count = existing_marks.get("__shift_count", 0)
        existing_last_tick = existing_marks.get("__last_shift_tick", 0)

        new_shift_count = existing_shift_count + (1 if added or removed else 0)
        new_last_tick = current_tick if (added or removed) else existing_last_tick

        profile = GeneExpressionProfile(
            cell_id=neuron.cell_id,
            stress_response_genes=stress_genes,
            repair_genes=repair_genes,
            defense_genes=defense_genes,
            metabolic_genes=metabolic_genes,
            expression_shift_count=new_shift_count,
            last_shift_tick=new_last_tick,
        )

        # Persist onto neuron for continuity
        neuron.epigenetic_marks = {g: 1.0 for g in all_new}
        neuron.epigenetic_marks["__shift_count"] = new_shift_count
        neuron.epigenetic_marks["__last_shift_tick"] = new_last_tick

        if added or removed:
            shift = EpigeneticShift(
                cell_id=neuron.cell_id,
                tick=current_tick,
                trigger=self._determine_trigger(stress_score, damage_score),
                genes_added=added,
                genes_removed=removed,
            )
        else:
            shift = None

        return profile, shift

    def _determine_trigger(self, stress_score: float, damage_score: float) -> str:
        if stress_score >= self.defense_trigger_threshold or damage_score >= 0.50:
            return "defense_priority"
        if damage_score >= self.repair_trigger_threshold:
            return "repair_priority"
        if stress_score >= self.stress_response_threshold:
            return "stress_response"
        return "metabolic_baseline"
