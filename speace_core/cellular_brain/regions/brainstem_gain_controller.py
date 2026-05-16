from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType


class BrainstemGainState(BaseModel):
    global_brainstem_gain: float = 1.0
    routing_gain: float = 1.0
    plasticity_gain: float = 1.0
    decay_gain: float = 1.0
    energy_recovery_gain: float = 1.0
    cooldown_gain: float = 1.0
    emergency_gain: float = 1.0
    cognitive_preservation_gain: float = 1.0


class BrainstemGainDecision(BaseModel):
    global_brainstem_gain: float = 1.0
    routing_gain: float = 1.0
    plasticity_gain: float = 1.0
    decay_gain: float = 1.0
    energy_recovery_gain: float = 1.0
    cooldown_gain: float = 1.0
    emergency_gain: float = 1.0
    cognitive_preservation_gain: float = 1.0
    adjustment_applied: bool = False
    reason: str = ""


class BrainstemGainUpdateResult(BaseModel):
    decision: BrainstemGainDecision = Field(default_factory=BrainstemGainDecision)
    brainstem_gain_reward: float = 0.0
    over_suppression_detected: bool = False
    useful_stabilization_detected: bool = False
    true_instability_detected: bool = False
    gain_adjustments_count: int = 0
    gain_stability_score: float = 0.0


class AdaptiveBrainstemGainController:
    """T37 — Adaptive gain layer atop BrainstemFunctionalController.

    Dynamically modulates the intensity of brainstem modulations based on
    observed cognitive, energetic, and stability outcomes.

    Principles:
    - If suppression hurts cognition without helping Φ, reduce suppressive gains.
    - If stabilization improves Φ while preserving cognition, maintain or slightly increase.
    - If true instability (Φ collapse, critical energy), increase protective gains.
    - If chronic emergency/protective without benefit, relax emergency gain.
    """

    # Safe ranges
    MIN_GENERAL_GAIN: float = 0.50
    MAX_GENERAL_GAIN: float = 1.50
    MIN_EMERGENCY_GAIN: float = 0.40
    MAX_EMERGENCY_GAIN: float = 1.20
    MIN_COGNITIVE_PRESERVATION_GAIN: float = 1.00
    MAX_COGNITIVE_PRESERVATION_GAIN: float = 1.50

    # Learning rate for gain EMA updates
    LEARNING_RATE: float = 0.05

    def __init__(self) -> None:
        self._gain = BrainstemGainState()
        self._gain_adjustments_count: int = 0
        self._last_reward: float = 0.0
        self._last_over_suppression: bool = False
        self._last_useful_stabilization: bool = False
        self._last_true_instability: bool = False

    # ------------------------------------------------------------------ #
    # Reward computation
    # ------------------------------------------------------------------ #

    def compute_reward(self, metrics: Dict[str, Any]) -> float:
        """Compute scalar reward in [-1, 1] from observed deltas."""
        cog_delta = metrics.get("cognitive_score_delta", 0.0)
        phi_delta = metrics.get("coherence_phi_delta", 0.0)
        energy_delta = metrics.get("energy_efficiency_delta", 0.0)
        func_delta = metrics.get("functional_improvement_delta", 0.0)
        suppression_cost = metrics.get("suppression_cost", 0.0)
        total_ticks = max(1, metrics.get("total_ticks", 5))
        emergency_ticks = metrics.get("emergency_ticks", 0)
        emergency_tick_ratio = emergency_ticks / total_ticks

        reward = (
            0.35 * max(0.0, cog_delta)
            + 0.25 * max(0.0, phi_delta)
            + 0.20 * max(0.0, energy_delta)
            + 0.10 * max(0.0, func_delta)
            - 0.25 * suppression_cost
            - 0.15 * emergency_tick_ratio
        )
        return round(max(-1.0, min(1.0, reward)), 4)

    # ------------------------------------------------------------------ #
    # Adaptive rules
    # ------------------------------------------------------------------ #

    def evaluate(
        self,
        metrics: Dict[str, Any],
    ) -> BrainstemGainUpdateResult:
        cog_delta = metrics.get("cognitive_score_delta", 0.0)
        phi_delta = metrics.get("coherence_phi_delta", 0.0)
        energy_delta = metrics.get("energy_efficiency_delta", 0.0)
        func_delta = metrics.get("functional_improvement_delta", 0.0)
        suppression_cost = metrics.get("suppression_cost", 0.0)
        emergency_ticks = metrics.get("emergency_ticks", 0)
        protective_ticks = metrics.get("protective_ticks", 0)
        total_ticks = max(1, metrics.get("total_ticks", 5))
        mean_region_energy = metrics.get("mean_region_energy", metrics.get("mean_energy", 0.0))
        mean_region_phi = metrics.get("mean_region_phi", 0.0)

        decision = BrainstemGainDecision()
        decision.global_brainstem_gain = self._gain.global_brainstem_gain
        decision.routing_gain = self._gain.routing_gain
        decision.plasticity_gain = self._gain.plasticity_gain
        decision.decay_gain = self._gain.decay_gain
        decision.energy_recovery_gain = self._gain.energy_recovery_gain
        decision.cooldown_gain = self._gain.cooldown_gain
        decision.emergency_gain = self._gain.emergency_gain
        decision.cognitive_preservation_gain = self._gain.cognitive_preservation_gain

        reward = self.compute_reward(metrics)
        reasons: list[str] = []
        adjustment = False

        self._last_over_suppression = False
        self._last_useful_stabilization = False
        self._last_true_instability = False

        # Rule 1: Over-suppression detection
        # Cognitive regression without Φ benefit → reduce suppression
        if cog_delta < -0.02 and phi_delta >= -0.02:
            self._last_over_suppression = True
            adjustment = True
            reasons.append("over_suppression")
            # Reduce suppressive gains
            self._gain.routing_gain = self._clamp(
                self._gain.routing_gain - self.LEARNING_RATE, self.MIN_GENERAL_GAIN, self.MAX_GENERAL_GAIN
            )
            self._gain.plasticity_gain = self._clamp(
                self._gain.plasticity_gain - self.LEARNING_RATE, self.MIN_GENERAL_GAIN, self.MAX_GENERAL_GAIN
            )
            self._gain.emergency_gain = self._clamp(
                self._gain.emergency_gain - self.LEARNING_RATE, self.MIN_EMERGENCY_GAIN, self.MAX_EMERGENCY_GAIN
            )
            # Boost cognitive preservation
            self._gain.cognitive_preservation_gain = self._clamp(
                self._gain.cognitive_preservation_gain + self.LEARNING_RATE,
                self.MIN_COGNITIVE_PRESERVATION_GAIN,
                self.MAX_COGNITIVE_PRESERVATION_GAIN,
            )

        # Rule 2: Useful stabilization
        # Φ improves and cognition preserved → maintain or slightly increase
        if phi_delta > 0.02 and cog_delta >= -0.03:
            self._last_useful_stabilization = True
            adjustment = True
            reasons.append("useful_stabilization")
            self._gain.global_brainstem_gain = self._clamp(
                self._gain.global_brainstem_gain + self.LEARNING_RATE * 0.5,
                self.MIN_GENERAL_GAIN,
                self.MAX_GENERAL_GAIN,
            )

        # Rule 3: Energy recovery without cognitive damage
        # Good energy recovery → reduce only suppressive routing/plasticity
        if energy_delta > 0.01 and cog_delta >= -0.03:
            adjustment = True
            reasons.append("energy_recovery_safe")
            self._gain.routing_gain = self._clamp(
                self._gain.routing_gain - self.LEARNING_RATE * 0.5, self.MIN_GENERAL_GAIN, self.MAX_GENERAL_GAIN
            )
            self._gain.plasticity_gain = self._clamp(
                self._gain.plasticity_gain - self.LEARNING_RATE * 0.5, self.MIN_GENERAL_GAIN, self.MAX_GENERAL_GAIN
            )

        # Rule 4: Chronic emergency/protective without Φ collapse
        # Too much time in high-alert states without benefit → relax emergency
        if (emergency_ticks > 3 or protective_ticks > 6) and phi_delta >= -0.03:
            adjustment = True
            reasons.append("chronic_high_alert")
            self._gain.emergency_gain = self._clamp(
                self._gain.emergency_gain - self.LEARNING_RATE, self.MIN_EMERGENCY_GAIN, self.MAX_EMERGENCY_GAIN
            )
            self._gain.decay_gain = self._clamp(
                self._gain.decay_gain - self.LEARNING_RATE * 0.5, self.MIN_GENERAL_GAIN, self.MAX_GENERAL_GAIN
            )
            self._gain.cognitive_preservation_gain = self._clamp(
                self._gain.cognitive_preservation_gain + self.LEARNING_RATE,
                self.MIN_COGNITIVE_PRESERVATION_GAIN,
                self.MAX_COGNITIVE_PRESERVATION_GAIN,
            )

        # Rule 5: True instability escalation
        # Φ collapse or critically low energy → increase protection
        if phi_delta < -0.05 or mean_region_energy < 0.12 or mean_region_phi < 0.10:
            self._last_true_instability = True
            adjustment = True
            reasons.append("true_instability")
            self._gain.global_brainstem_gain = self._clamp(
                self._gain.global_brainstem_gain + self.LEARNING_RATE, self.MIN_GENERAL_GAIN, self.MAX_GENERAL_GAIN
            )
            self._gain.energy_recovery_gain = self._clamp(
                self._gain.energy_recovery_gain + self.LEARNING_RATE, self.MIN_GENERAL_GAIN, self.MAX_GENERAL_GAIN
            )
            self._gain.decay_gain = self._clamp(
                self._gain.decay_gain + self.LEARNING_RATE, self.MIN_GENERAL_GAIN, self.MAX_GENERAL_GAIN
            )

        if adjustment:
            self._gain_adjustments_count += 1

        # Apply global gain scaling (soft)
        if adjustment:
            global_factor = self._gain.global_brainstem_gain
            decision.routing_gain = round(self._gain.routing_gain * global_factor, 4)
            decision.plasticity_gain = round(self._gain.plasticity_gain * global_factor, 4)
            decision.decay_gain = round(self._gain.decay_gain * global_factor, 4)
            decision.energy_recovery_gain = round(self._gain.energy_recovery_gain * global_factor, 4)
            decision.cooldown_gain = round(self._gain.cooldown_gain * global_factor, 4)
            decision.emergency_gain = round(self._gain.emergency_gain * global_factor, 4)
            decision.cognitive_preservation_gain = round(self._gain.cognitive_preservation_gain, 4)
            decision.adjustment_applied = True
        else:
            decision.routing_gain = round(self._gain.routing_gain, 4)
            decision.plasticity_gain = round(self._gain.plasticity_gain, 4)
            decision.decay_gain = round(self._gain.decay_gain, 4)
            decision.energy_recovery_gain = round(self._gain.energy_recovery_gain, 4)
            decision.cooldown_gain = round(self._gain.cooldown_gain, 4)
            decision.emergency_gain = round(self._gain.emergency_gain, 4)
            decision.cognitive_preservation_gain = round(self._gain.cognitive_preservation_gain, 4)

        decision.reason = "; ".join(reasons) if reasons else "no_adjustment"

        # Gain stability score: how close gains are to 1.0 (neutral)
        all_gains = [
            decision.routing_gain,
            decision.plasticity_gain,
            decision.decay_gain,
            decision.energy_recovery_gain,
            decision.emergency_gain,
            decision.cognitive_preservation_gain,
        ]
        gain_stability = 1.0 - sum(abs(g - 1.0) for g in all_gains) / len(all_gains)
        gain_stability = max(0.0, min(1.0, gain_stability))

        return BrainstemGainUpdateResult(
            decision=decision,
            brainstem_gain_reward=reward,
            over_suppression_detected=self._last_over_suppression,
            useful_stabilization_detected=self._last_useful_stabilization,
            true_instability_detected=self._last_true_instability,
            gain_adjustments_count=self._gain_adjustments_count,
            gain_stability_score=round(gain_stability, 4),
        )

    def apply(
        self,
        metrics: Dict[str, Any],
        memory: Optional[MorphologicalMemory] = None,
    ) -> BrainstemGainUpdateResult:
        result = self.evaluate(metrics)

        if memory is not None:
            memory.create_event(
                event_type=MorphologyEventType.BRAINSTEM_GAIN_EVALUATED,
                region_id="brainstem_homeostatic",
                metadata={
                    "reward": result.brainstem_gain_reward,
                    "gain_stability_score": result.gain_stability_score,
                    "gain_adjustments_count": result.gain_adjustments_count,
                },
            )
            if result.decision.adjustment_applied:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_GAIN_ADJUSTED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "reason": result.decision.reason,
                        "routing_gain": result.decision.routing_gain,
                        "plasticity_gain": result.decision.plasticity_gain,
                        "decay_gain": result.decision.decay_gain,
                        "energy_recovery_gain": result.decision.energy_recovery_gain,
                        "emergency_gain": result.decision.emergency_gain,
                        "cognitive_preservation_gain": result.decision.cognitive_preservation_gain,
                    },
                )
            if result.over_suppression_detected:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_OVER_SUPPRESSION_DETECTED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "cognitive_score_delta": metrics.get("cognitive_score_delta", 0.0),
                        "coherence_phi_delta": metrics.get("coherence_phi_delta", 0.0),
                    },
                )
            if result.useful_stabilization_detected:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_USEFUL_STABILIZATION_DETECTED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "coherence_phi_delta": metrics.get("coherence_phi_delta", 0.0),
                        "cognitive_score_delta": metrics.get("cognitive_score_delta", 0.0),
                    },
                )
            if result.true_instability_detected:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_TRUE_INSTABILITY_DETECTED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "mean_region_energy": metrics.get("mean_region_energy", metrics.get("mean_energy", 0.0)),
                        "coherence_phi_delta": metrics.get("coherence_phi_delta", 0.0),
                    },
                )
            if result.decision.adjustment_applied and "over_suppression" in result.decision.reason:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_EMERGENCY_GAIN_REDUCED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "emergency_gain": result.decision.emergency_gain,
                    },
                )
            if result.decision.adjustment_applied and "useful_stabilization" in result.decision.reason:
                memory.create_event(
                    event_type=MorphologyEventType.BRAINSTEM_COGNITIVE_GAIN_BOOSTED,
                    region_id="brainstem_homeostatic",
                    metadata={
                        "cognitive_preservation_gain": result.decision.cognitive_preservation_gain,
                    },
                )

        return result

    def get_gain_summary(self) -> Dict[str, Any]:
        return {
            "global_brainstem_gain": self._gain.global_brainstem_gain,
            "routing_gain": self._gain.routing_gain,
            "plasticity_gain": self._gain.plasticity_gain,
            "decay_gain": self._gain.decay_gain,
            "energy_recovery_gain": self._gain.energy_recovery_gain,
            "cooldown_gain": self._gain.cooldown_gain,
            "emergency_gain": self._gain.emergency_gain,
            "cognitive_preservation_gain": self._gain.cognitive_preservation_gain,
            "gain_adjustments_count": self._gain_adjustments_count,
            "last_reward": self._last_reward,
            "last_over_suppression": self._last_over_suppression,
            "last_useful_stabilization": self._last_useful_stabilization,
            "last_true_instability": self._last_true_instability,
        }

    @staticmethod
    def _clamp(value: float, min_val: float, max_val: float) -> float:
        return max(min_val, min(max_val, value))
