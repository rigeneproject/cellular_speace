from typing import Dict, List

from pydantic import BaseModel, Field

from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron
from speace_core.cellular_brain.circuits.neural_circuit import NeuralCircuit
from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType


class RepairAction(BaseModel):
    """Single repair action applied to a cell."""

    cell_id: str
    action: str = ""
    success: bool = False
    energy_cost: float = 0.0
    damage_before: float = 0.0
    damage_after: float = 0.0


class CellularRepairResult(BaseModel):
    """Aggregate result of a repair pass."""

    actions: List[RepairAction] = Field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0
    total_energy_cost: float = 0.0
    repair_success_rate: float = 0.0


class CellularRepairEngine:
    """T42 — Repair damaged cells using energy-budgeted interventions.

    Repair efficacy depends on damage level and available energy.
    Reversible damage is cheap to fix; structural damage rarely heals.
    """

    def __init__(
        self,
        base_repair_cost: float = 0.05,
        reversible_heal_amount: float = 0.30,
        functional_heal_amount: float = 0.10,
        structural_heal_amount: float = 0.02,
        critical_heal_amount: float = 0.00,
        min_energy_to_repair: float = 0.20,
        max_repairs_per_cycle: int = 5,
    ):
        self.base_repair_cost = base_repair_cost
        self.reversible_heal_amount = reversible_heal_amount
        self.functional_heal_amount = functional_heal_amount
        self.structural_heal_amount = structural_heal_amount
        self.critical_heal_amount = critical_heal_amount
        self.min_energy_to_repair = min_energy_to_repair
        self.max_repairs_per_cycle = max_repairs_per_cycle

    def run(
        self,
        circuit: NeuralCircuit,
        damage_per_cell: Dict[str, "CellularDamageState"],
        memory: MorphologicalMemory | None = None,
    ) -> CellularRepairResult:
        from speace_core.cellular_brain.cells.cellular_damage import CellularDamageState

        all_neurons = {
            n.cell_id: n
            for n in circuit.input_neurons
            + circuit.hidden_neurons
            + circuit.output_neurons
        }
        actions: List[RepairAction] = []
        success_count = 0
        failure_count = 0
        total_energy_cost = 0.0
        repairs_done = 0

        # Prioritize by damage level (reversible first, then functional, etc.)
        sorted_cells = sorted(
            damage_per_cell.items(),
            key=lambda x: x[1].damage_score,
            reverse=True,
        )

        for cell_id, damage_state in sorted_cells:
            if repairs_done >= self.max_repairs_per_cycle:
                break
            neuron = all_neurons.get(cell_id)
            if neuron is None:
                continue
            action = self._attempt_repair(neuron, damage_state)
            actions.append(action)
            repairs_done += 1
            if action.success:
                success_count += 1
            else:
                failure_count += 1
            total_energy_cost += action.energy_cost

            if memory is not None:
                memory.create_event(
                    event_type=MorphologyEventType.CELLULAR_REPAIR_ATTEMPTED,
                    source_id="cellular_repair_engine",
                    target_id=cell_id,
                    metadata={
                        "action": action.action,
                        "success": action.success,
                        "energy_cost": action.energy_cost,
                        "damage_before": action.damage_before,
                        "damage_after": action.damage_after,
                    },
                )

        repair_success_rate = success_count / len(actions) if actions else 0.0
        return CellularRepairResult(
            actions=actions,
            success_count=success_count,
            failure_count=failure_count,
            total_energy_cost=round(total_energy_cost, 4),
            repair_success_rate=round(repair_success_rate, 4),
        )

    def _attempt_repair(
        self,
        neuron: DigitalNeuron,
        damage_state: "CellularDamageState",
    ) -> RepairAction:
        from speace_core.cellular_brain.cells.cellular_damage import CellularDamageState

        level = damage_state.level
        damage_before = damage_state.damage_score

        # Determine heal amount and cost
        if level == "reversible":
            heal = self.reversible_heal_amount
            cost = self.base_repair_cost
            action_name = "reversible_repair"
        elif level == "functional":
            heal = self.functional_heal_amount
            cost = self.base_repair_cost * 1.5
            action_name = "functional_repair"
        elif level == "structural":
            heal = self.structural_heal_amount
            cost = self.base_repair_cost * 3.0
            action_name = "structural_repair"
        elif level == "critical":
            heal = self.critical_heal_amount
            cost = self.base_repair_cost * 5.0
            action_name = "critical_repair"
        else:
            # No damage
            return RepairAction(
                cell_id=neuron.cell_id,
                action="no_damage",
                success=True,
                energy_cost=0.0,
                damage_before=damage_before,
                damage_after=damage_before,
            )

        # Budget check: neuron must have enough energy
        if neuron.energy < max(self.min_energy_to_repair, cost):
            return RepairAction(
                cell_id=neuron.cell_id,
                action=action_name,
                success=False,
                energy_cost=0.0,
                damage_before=damage_before,
                damage_after=damage_before,
            )

        neuron.energy = max(0.0, neuron.energy - cost)
        new_damage = max(0.0, damage_before - heal)

        return RepairAction(
            cell_id=neuron.cell_id,
            action=action_name,
            success=True,
            energy_cost=cost,
            damage_before=damage_before,
            damage_after=round(new_damage, 4),
        )
