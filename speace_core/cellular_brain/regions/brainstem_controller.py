from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType


class BrainstemFunctionalState(str, Enum):
    STABLE = "stable"
    WATCHFUL = "watchful"
    CORRECTIVE = "corrective"
    PROTECTIVE = "protective"
    EMERGENCY = "emergency"


class BrainstemState(BaseModel):
    state: BrainstemFunctionalState = BrainstemFunctionalState.STABLE
    mean_phi: float = 0.0
    mean_energy: float = 0.0
    instability_mean: float = 0.0
    unstable_region_count: int = 0
    mean_deep_activation: float = 0.0
    regional_signal_flow: float = 0.0
    deep_region_signal_flow: float = 0.0
    stability_actions: int = 0
    routing_blocks: int = 0
    cooldowns: int = 0
    mean_pathway_utility: float = 0.0
    energy_state: float = 0.0


class BrainstemDecision(BaseModel):
    state: BrainstemFunctionalState = BrainstemFunctionalState.STABLE
    reason: str = ""
    energy_recovery_multiplier: float = 1.0
    routing_suppression_multiplier: float = 1.0
    plasticity_suppression_multiplier: float = 1.0
    decay_boost_multiplier: float = 1.0
    cooldown_boost_multiplier: float = 1.0
    neurogenesis_suppression_multiplier: float = 1.0
    apoptosis_boost_multiplier: float = 1.0
    brainstem_priority_boost: float = 1.0


class BrainstemModulationResult(BaseModel):
    decision: BrainstemDecision = Field(default_factory=BrainstemDecision)
    state_changed: bool = False
    decisions_count: int = 0
    emergency_count: int = 0
    recovery_actions: int = 0
    homeostatic_gain: float = 0.0
    phi_recovery_contribution: float = 0.0


class BrainstemFunctionalController:
    """Active homeostatic arbiter for the cellular brain.

    T35 transforms brainstem_homeostatic from a passive deep-region target
    into a systemic regulator of energy, routing, plasticity, decay,
    cooldown, and recovery.
    """

    def __init__(
        self,
        phi_threshold_stable: float = 0.25,
        phi_threshold_watchful: float = 0.20,
        phi_threshold_corrective: float = 0.15,
        phi_threshold_protective: float = 0.10,
        energy_threshold_emergency: float = 0.15,
        instability_threshold_watchful: float = 0.15,
        instability_threshold_corrective: float = 0.30,
        instability_threshold_protective: float = 0.50,
        instability_threshold_emergency: float = 0.70,
    ):
        self.phi_threshold_stable = phi_threshold_stable
        self.phi_threshold_watchful = phi_threshold_watchful
        self.phi_threshold_corrective = phi_threshold_corrective
        self.phi_threshold_protective = phi_threshold_protective
        self.energy_threshold_emergency = energy_threshold_emergency
        self.instability_threshold_watchful = instability_threshold_watchful
        self.instability_threshold_corrective = instability_threshold_corrective
        self.instability_threshold_protective = instability_threshold_protective
        self.instability_threshold_emergency = instability_threshold_emergency
        self._previous_state: Optional[BrainstemFunctionalState] = None
        self._decisions_count: int = 0
        self._emergency_count: int = 0
        self._recovery_actions: int = 0
        self._last_phi: float = 0.0

    # ------------------------------------------------------------------ #
    # State evaluation
    # ------------------------------------------------------------------ #

    def evaluate_state(self, metrics: Dict[str, Any]) -> BrainstemFunctionalState:
        phi = metrics.get("mean_region_phi", 0.0)
        energy = metrics.get("mean_energy", 0.0)
        instability = metrics.get("region_instability_mean", 0.0)
        unstable_count = metrics.get("unstable_region_count", 0)
        deep_activation = metrics.get("mean_deep_region_activation", 0.0)

        # Emergency: critical energy or extreme instability
        if energy < self.energy_threshold_emergency or instability >= self.instability_threshold_emergency:
            return BrainstemFunctionalState.EMERGENCY

        # Protective: strong instability or many unstable regions or very high deep activation
        if (
            instability >= self.instability_threshold_protective
            or unstable_count >= 3
            or deep_activation > 2.0
        ):
            return BrainstemFunctionalState.PROTECTIVE

        # Corrective: moderate instability
        if instability >= self.instability_threshold_corrective or phi < self.phi_threshold_corrective:
            return BrainstemFunctionalState.CORRECTIVE

        # Watchful: mild instability or phi slightly low
        if instability >= self.instability_threshold_watchful or phi < self.phi_threshold_watchful:
            return BrainstemFunctionalState.WATCHFUL

        return BrainstemFunctionalState.STABLE

    # ------------------------------------------------------------------ #
    # Decision computation
    # ------------------------------------------------------------------ #

    def decide(
        self,
        metrics: Dict[str, Any],
        memory: Optional[MorphologicalMemory] = None,
    ) -> BrainstemDecision:
        state = self.evaluate_state(metrics)
        phi = metrics.get("mean_region_phi", 0.0)
        energy = metrics.get("mean_energy", 0.0)
        instability = metrics.get("region_instability_mean", 0.0)
        deep_activation = metrics.get("mean_deep_region_activation", 0.0)
        signal_flow = metrics.get("regional_signal_flow", 0.0)
        utility = metrics.get("mean_pathway_utility", 0.0)

        reasons: List[str] = []
        if state == BrainstemFunctionalState.STABLE:
            reasons.append("system_stable")
        if state == BrainstemFunctionalState.WATCHFUL:
            reasons.append("mild_instability_or_low_phi")
        if state == BrainstemFunctionalState.CORRECTIVE:
            reasons.append("moderate_instability_or_low_phi")
        if state == BrainstemFunctionalState.PROTECTIVE:
            reasons.append("strong_instability_or_high_deep_activation")
        if state == BrainstemFunctionalState.EMERGENCY:
            reasons.append("critical_energy_or_extreme_instability")

        # Default: no suppression
        decision = BrainstemDecision(
            state=state,
            reason="; ".join(reasons),
        )

        if state == BrainstemFunctionalState.STABLE:
            return decision

        if state == BrainstemFunctionalState.WATCHFUL:
            decision.routing_suppression_multiplier = 0.90
            decision.decay_boost_multiplier = 1.10
            decision.brainstem_priority_boost = 1.05
            return decision

        if state == BrainstemFunctionalState.CORRECTIVE:
            decision.routing_suppression_multiplier = 0.75
            decision.plasticity_suppression_multiplier = 0.80
            decision.decay_boost_multiplier = 1.25
            decision.cooldown_boost_multiplier = 1.20
            decision.brainstem_priority_boost = 1.10
            return decision

        if state == BrainstemFunctionalState.PROTECTIVE:
            decision.routing_suppression_multiplier = 0.55
            decision.plasticity_suppression_multiplier = 0.50
            decision.decay_boost_multiplier = 1.50
            decision.cooldown_boost_multiplier = 1.40
            decision.neurogenesis_suppression_multiplier = 0.30
            decision.apoptosis_boost_multiplier = 1.30
            decision.brainstem_priority_boost = 1.25
            return decision

        if state == BrainstemFunctionalState.EMERGENCY:
            decision.routing_suppression_multiplier = 0.30
            decision.plasticity_suppression_multiplier = 0.20
            decision.decay_boost_multiplier = 2.00
            decision.cooldown_boost_multiplier = 2.00
            decision.neurogenesis_suppression_multiplier = 0.10
            decision.apoptosis_boost_multiplier = 1.60
            decision.energy_recovery_multiplier = 1.50
            decision.brainstem_priority_boost = 1.50
            return decision

        return decision

    # ------------------------------------------------------------------ #
    # Apply modulation
    # ------------------------------------------------------------------ #

    def apply(
        self,
        metrics: Dict[str, Any],
        memory: Optional[MorphologicalMemory] = None,
    ) -> BrainstemModulationResult:
        decision = self.decide(metrics, memory)
        state = decision.state
        state_changed = self._previous_state != state
        self._previous_state = state
        self._decisions_count += 1

        if state == BrainstemFunctionalState.EMERGENCY:
            self._emergency_count += 1

        phi = metrics.get("mean_region_phi", 0.0)
        phi_recovery = max(0.0, phi - self._last_phi)
        self._last_phi = phi

        recovery_actions = 0
        if state in {BrainstemFunctionalState.CORRECTIVE, BrainstemFunctionalState.PROTECTIVE, BrainstemFunctionalState.EMERGENCY}:
            recovery_actions = 1
            self._recovery_actions += 1

        # Compute a simple homeostatic gain score
        homeostatic_gain = 0.0
        if state == BrainstemFunctionalState.STABLE:
            homeostatic_gain = 0.05
        elif state == BrainstemFunctionalState.WATCHFUL:
            homeostatic_gain = 0.02
        elif state == BrainstemFunctionalState.CORRECTIVE:
            homeostatic_gain = -0.05
        elif state == BrainstemFunctionalState.PROTECTIVE:
            homeostatic_gain = -0.10
        elif state == BrainstemFunctionalState.EMERGENCY:
            homeostatic_gain = -0.20

        result = BrainstemModulationResult(
            decision=decision,
            state_changed=state_changed,
            decisions_count=self._decisions_count,
            emergency_count=self._emergency_count,
            recovery_actions=recovery_actions,
            homeostatic_gain=homeostatic_gain,
            phi_recovery_contribution=phi_recovery,
        )

        if memory is not None:
            if state_changed:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_STATE_CHANGED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "new_state": state.value,
                        "previous_state": self._previous_state.value if self._previous_state else None,
                        "reason": decision.reason,
                    },
                )
            memory.create_event(
                event_type=MorphologyEventType.BRAINSTEM_MODULATION_APPLIED,
                region_id="brainstem_homeostatic",
                metadata={
                    "state": state.value,
                    "routing_suppression_multiplier": decision.routing_suppression_multiplier,
                    "plasticity_suppression_multiplier": decision.plasticity_suppression_multiplier,
                    "energy_recovery_multiplier": decision.energy_recovery_multiplier,
                    "decay_boost_multiplier": decision.decay_boost_multiplier,
                    "brainstem_priority_boost": decision.brainstem_priority_boost,
                },
            )
            if state == BrainstemFunctionalState.EMERGENCY:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_EMERGENCY_TRIGGERED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "reason": decision.reason,
                        "routing_suppression_multiplier": decision.routing_suppression_multiplier,
                        "energy_recovery_multiplier": decision.energy_recovery_multiplier,
                    },
                )
            if recovery_actions > 0:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_RECOVERY_APPLIED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "state": state.value,
                        "phi_recovery_contribution": phi_recovery,
                    },
                )
            if decision.routing_suppression_multiplier < 1.0:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_ROUTING_SUPPRESSED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "routing_suppression_multiplier": decision.routing_suppression_multiplier,
                    },
                )
            if decision.plasticity_suppression_multiplier < 1.0:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_PLASTICITY_SUPPRESSED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "plasticity_suppression_multiplier": decision.plasticity_suppression_multiplier,
                    },
                )
            if decision.energy_recovery_multiplier > 1.0:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_ENERGY_RECOVERY_BOOSTED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "energy_recovery_multiplier": decision.energy_recovery_multiplier,
                    },
                )

        return result

    # ------------------------------------------------------------------ #
    # Getters for benchmark/orchestrator integration
    # ------------------------------------------------------------------ #

    def get_modulation_summary(self) -> Dict[str, Any]:
        return {
            "previous_state": self._previous_state.value if self._previous_state else None,
            "decisions_count": self._decisions_count,
            "emergency_count": self._emergency_count,
            "recovery_actions": self._recovery_actions,
        }
