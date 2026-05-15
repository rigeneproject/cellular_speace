import math
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from speace_core.cellular_brain.circuits.neural_circuit import NeuralCircuit
from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType
from speace_core.cellular_brain.regions.region_connectome import RegionConnectome
from speace_core.cellular_brain.regulation.homeostasis_engine import SystemMetrics


class RegionSignal(BaseModel):
    source_region_id: str
    target_region_id: str
    signal_strength: float = 0.0
    pathway_strength: float = 0.0
    energy_cost: float = 0.0
    confidence_weight: float = 1.0
    delivered: bool = False
    reason: Optional[str] = None


class RegionRoutingResult(BaseModel):
    routed_signals: int = 0
    delivered_signals: int = 0
    blocked_signals: int = 0
    total_signal_strength: float = 0.0
    mean_signal_strength: float = 0.0
    total_energy_cost: float = 0.0
    active_pathways: int = 0
    regional_signal_flow_score: float = 0.0
    signals: List[RegionSignal] = Field(default_factory=list)


class RegionSignalRouter:
    """Routes signals between brain regions using soft activation and energy-aware gating.

    T25 makes inter-region pathways causally active so that T23 plasticity has
    meaningful activation pairs to observe (LTP/LTD).
    """

    def __init__(
        self,
        min_source_activation: float = 0.05,
        min_pathway_strength: float = 0.01,
        signal_gain: float = 1.0,
        energy_cost_per_signal: float = 0.001,
        max_signals_per_tick: int = 16,
    ):
        self.min_source_activation = min_source_activation
        self.min_pathway_strength = min_pathway_strength
        self.signal_gain = signal_gain
        self.energy_cost_per_signal = energy_cost_per_signal
        self.max_signals_per_tick = max_signals_per_tick

    # ------------------------------------------------------------------ #
    # Soft activation
    # ------------------------------------------------------------------ #

    def compute_soft_region_activation(
        self, region_id: str, circuit: NeuralCircuit
    ) -> float:
        """Return a sensitive activation score for a region.

        Formula:
            mean(|activation|)
            + 0.5 * max(|activation|)
            + 0.25 * active_fraction
        where active_fraction = neurons with |activation| > 0.05 / total.
        """
        all_neurons = circuit.input_neurons + circuit.hidden_neurons + circuit.output_neurons
        region_neurons = [
            n for n in all_neurons if getattr(n, "region", None) == region_id
        ]
        if not region_neurons:
            return 0.0

        activations = [abs(getattr(n, "activation", 0.0)) for n in region_neurons]
        mean_act = sum(activations) / len(activations)
        max_act = max(activations) if activations else 0.0
        active_frac = sum(1 for a in activations if a > 0.05) / len(activations)

        return mean_act + 0.5 * max_act + 0.25 * active_frac

    # ------------------------------------------------------------------ #
    # Signal construction
    # ------------------------------------------------------------------ #

    def build_region_signal(
        self,
        source_region_id: str,
        target_region_id: str,
        connection,
        circuit: NeuralCircuit,
        confidence_weight: float = 1.0,
    ) -> RegionSignal:
        source_activation = self.compute_soft_region_activation(source_region_id, circuit)
        signal_strength = (
            source_activation
            * connection.strength
            * self.signal_gain
            * confidence_weight
        )
        energy_cost = self.energy_cost_per_signal

        return RegionSignal(
            source_region_id=source_region_id,
            target_region_id=target_region_id,
            signal_strength=signal_strength,
            pathway_strength=connection.strength,
            energy_cost=energy_cost,
            confidence_weight=confidence_weight,
        )

    # ------------------------------------------------------------------ #
    # Signal delivery
    # ------------------------------------------------------------------ #

    def route_signal(
        self, signal: RegionSignal, target_region_id: str, circuit: NeuralCircuit
    ) -> bool:
        """Deliver signal to target region neurons. Returns True if delivered."""
        all_neurons = circuit.input_neurons + circuit.hidden_neurons + circuit.output_neurons
        target_neurons = [
            n for n in all_neurons if getattr(n, "region", None) == target_region_id
        ]
        if not target_neurons:
            signal.delivered = False
            signal.reason = "no_target_neurons"
            return False

        increment = signal.signal_strength / len(target_neurons)
        for n in target_neurons:
            n.activation = getattr(n, "activation", 0.0) + increment

        signal.delivered = True
        signal.reason = "delivered"
        return True

    # ------------------------------------------------------------------ #
    # Batch routing
    # ------------------------------------------------------------------ #

    def route_all(
        self,
        region_connectome: RegionConnectome,
        circuit: NeuralCircuit,
        metrics: Optional[SystemMetrics] = None,
        memory: Optional[MorphologicalMemory] = None,
        confidence_score: float = 0.0,
    ) -> RegionRoutingResult:
        result = RegionRoutingResult()
        if region_connectome is None or not region_connectome.connections:
            return result

        confidence_weight = max(0.5, 1.0 - confidence_score) if confidence_score > 0.6 else 1.0
        global_energy = metrics.mean_energy if metrics else 0.5

        signals_routed = 0
        for conn in region_connectome.connections:
            if signals_routed >= self.max_signals_per_tick:
                break

            source_activation = self.compute_soft_region_activation(
                conn.source_region_id, circuit
            )

            # Block: source too weak
            if source_activation < self.min_source_activation:
                result.blocked_signals += 1
                if memory is not None:
                    memory.create_event(
                        event_type=MorphologyEventType.REGION_SIGNAL_BLOCKED,
                        source_id=conn.source_region_id,
                        target_id=conn.target_region_id,
                        metadata={
                            "reason": "source_activation_below_threshold",
                            "source_activation": source_activation,
                            "threshold": self.min_source_activation,
                        },
                    )
                continue

            # Block: pathway too weak
            if conn.strength < self.min_pathway_strength:
                result.blocked_signals += 1
                if memory is not None:
                    memory.create_event(
                        event_type=MorphologyEventType.REGION_SIGNAL_BLOCKED,
                        source_id=conn.source_region_id,
                        target_id=conn.target_region_id,
                        metadata={
                            "reason": "pathway_strength_below_threshold",
                            "pathway_strength": conn.strength,
                            "threshold": self.min_pathway_strength,
                        },
                    )
                continue

            # Block: insufficient energy (soft gate)
            if global_energy < 0.1:
                result.blocked_signals += 1
                if memory is not None:
                    memory.create_event(
                        event_type=MorphologyEventType.REGION_SIGNAL_BLOCKED,
                        source_id=conn.source_region_id,
                        target_id=conn.target_region_id,
                        metadata={
                            "reason": "global_energy_depleted",
                            "global_energy": global_energy,
                        },
                    )
                continue

            signal = self.build_region_signal(
                conn.source_region_id,
                conn.target_region_id,
                conn,
                circuit,
                confidence_weight=confidence_weight,
            )

            if memory is not None:
                memory.create_event(
                    event_type=MorphologyEventType.REGION_SIGNAL_ROUTED,
                    source_id=conn.source_region_id,
                    target_id=conn.target_region_id,
                    metadata={
                        "signal_strength": signal.signal_strength,
                        "pathway_strength": conn.strength,
                        "confidence_weight": confidence_weight,
                    },
                )

            delivered = self.route_signal(signal, conn.target_region_id, circuit)

            if delivered:
                result.delivered_signals += 1
                result.total_signal_strength += signal.signal_strength
                result.total_energy_cost += signal.energy_cost
                if memory is not None:
                    memory.create_event(
                        event_type=MorphologyEventType.REGION_SIGNAL_DELIVERED,
                        source_id=conn.source_region_id,
                        target_id=conn.target_region_id,
                        metadata={
                            "signal_strength": signal.signal_strength,
                            "energy_cost": signal.energy_cost,
                        },
                    )
            else:
                result.blocked_signals += 1

            result.signals.append(signal)
            signals_routed += 1
            result.routed_signals += 1

        if result.delivered_signals > 0:
            result.mean_signal_strength = (
                result.total_signal_strength / result.delivered_signals
            )

        result.active_pathways = sum(
            1 for c in region_connectome.connections if c.strength >= self.min_pathway_strength
        )
        result.regional_signal_flow_score = self.compute_regional_signal_flow_score(result)

        if memory is not None and result.routed_signals > 0:
            memory.create_event(
                event_type=MorphologyEventType.REGIONAL_SIGNAL_FLOW_UPDATED,
                source_id="region_signal_router",
                metadata={
                    "routed_signals": result.routed_signals,
                    "delivered_signals": result.delivered_signals,
                    "blocked_signals": result.blocked_signals,
                    "total_signal_strength": result.total_signal_strength,
                    "mean_signal_strength": result.mean_signal_strength,
                    "regional_signal_flow_score": result.regional_signal_flow_score,
                },
            )

        return result

    # ------------------------------------------------------------------ #
    # Scoring
    # ------------------------------------------------------------------ #

    @staticmethod
    def compute_regional_signal_flow_score(result: RegionRoutingResult) -> float:
        """Score in [0, 1] measuring effective inter-region communication."""
        if result.routed_signals == 0:
            return 0.0
        delivery_ratio = result.delivered_signals / result.routed_signals
        strength_component = min(1.0, result.mean_signal_strength)
        return max(0.0, min(1.0, delivery_ratio * strength_component))
