import asyncio
import random
from typing import List

from pydantic import BaseModel

from speace_core.cellular_brain.base.digital_signal import DigitalSignal
from speace_core.cellular_brain.cells.digital_astrocyte import DigitalAstrocyte
from speace_core.cellular_brain.cells.digital_microglia import DigitalMicroglia
from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron
from speace_core.cellular_brain.cells.digital_oligodendrocyte import DigitalOligodendrocyte
from speace_core.cellular_brain.cells.digital_synapse import DigitalSynapse
from speace_core.cellular_brain.circuits.neural_circuit import NeuralCircuit
from speace_core.cellular_brain.regulation.apoptosis_engine import ApoptosisEngine
from speace_core.cellular_brain.regulation.cell_differentiation_engine import (
    CellDifferentiationEngine,
)
from speace_core.cellular_brain.regulation.homeostasis_engine import (
    HomeostasisEngine,
    SystemMetrics,
)
from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_snapshot import MorphologySnapshot
from speace_core.cellular_brain.execution.burst_engine import EventDrivenBurstEngine
from speace_core.cellular_brain.regulation.neurogenesis_engine import NeurogenesisEngine
from speace_core.cellular_brain.regulation.plasticity_engine import PlasticityEngine
from speace_core.cellular_brain.analysis.community_detection_engine import (
    CommunityDetectionEngine,
    CommunityDetectionResult,
)
from speace_core.cellular_brain.metacognition.confidence_engine import (
    ConfidenceEngine,
    ConfidenceState,
)
from speace_core.cellular_brain.regulation.energy_control_agent import EnergyControlAgent
from speace_core.cellular_brain.regulation.inhibition_engine import InhibitionEngine
from speace_core.cellular_brain.regulation.stdp_plasticity_engine import STDPPlasticityEngine
from speace_core.cellular_brain.regions.region_registry import RegionRegistry
from speace_core.cellular_brain.regions.region_factory import RegionFactory
from speace_core.cellular_brain.regions.inter_region_plasticity import InterRegionPlasticityEngine
from speace_core.cellular_brain.regions.region_signal_router import (
    RegionSignalRouter,
    RegionRoutingResult,
)
from speace_core.cellular_brain.regions.region_stability_controller import (
    RegionLevelStabilityController,
)
from speace_core.cellular_brain.regions.deep_region_routing_calibrator import (
    DeepRegionRoutingCalibrator,
    DeepRegionRoutingProfile,
)
from speace_core.cellular_brain.regions.brainstem_controller import BrainstemFunctionalController
from speace_core.cellular_brain.regions.brainstem_gain_controller import (
    AdaptiveBrainstemGainController,
    BrainstemGainUpdateResult,
)
from speace_core.cellular_brain.cells.cellular_stress import CellularStressEngine
from speace_core.cellular_brain.cells.cellular_damage import CellularDamageEngine
from speace_core.cellular_brain.cells.cellular_repair_engine import CellularRepairEngine
from speace_core.cellular_brain.cells.cellular_defense_engine import CellularDefenseEngine
from speace_core.cellular_brain.cells.cellular_epigenetic_adapter import CellularEpigeneticAdapter
from speace_core.dna.models import SharedGenome


class CellularBrainOrchestrator(BaseModel):
    genome: SharedGenome
    circuit: NeuralCircuit
    tick_interval: float = 0.0
    current_tick: int = 0
    metrics_log: List[SystemMetrics] = []

    _homeostasis: HomeostasisEngine = None  # type: ignore[assignment]
    _plasticity: PlasticityEngine = None  # type: ignore[assignment]
    _memory: MorphologicalMemory = None  # type: ignore[assignment]
    _neurogenesis: NeurogenesisEngine = None  # type: ignore[assignment]
    _apoptosis: ApoptosisEngine = None  # type: ignore[assignment]
    _differentiation: CellDifferentiationEngine = None  # type: ignore[assignment]
    _burst_engine: EventDrivenBurstEngine = None  # type: ignore[assignment]
    _stdp: STDPPlasticityEngine = None  # type: ignore[assignment]
    _inhibition: InhibitionEngine = None  # type: ignore[assignment]
    _energy_control: EnergyControlAgent = None  # type: ignore[assignment]
    _inter_region_plasticity: InterRegionPlasticityEngine = None  # type: ignore[assignment]
    _region_signal_router: RegionSignalRouter = None  # type: ignore[assignment]
    _community: CommunityDetectionEngine = None  # type: ignore[assignment]
    _confidence: ConfidenceEngine = None  # type: ignore[assignment]
    negative_feedback_count: int = 0
    execution_mode: str = "global_tick"
    stdp_enabled: bool = True
    inhibition_enabled: bool = True
    energy_control_enabled: bool = True
    inter_region_plasticity_enabled: bool = True
    region_signal_routing_enabled: bool = True
    community_detection_enabled: bool = True
    confidence_enabled: bool = True
    last_community_result: CommunityDetectionResult | None = None
    last_confidence_state: ConfidenceState | None = None
    last_routing_result: RegionRoutingResult | None = None
    neurogenesis_recommended: bool = False
    stabilization_recommended: bool = False
    plasticity_reduction_recommended: bool = False
    region_architecture_enabled: bool = True
    deep_regions_enabled: bool = True
    region_stability_controller_enabled: bool = False
    deep_region_routing_calibrator_enabled: bool = False
    brainstem_controller_enabled: bool = False
    brainstem_gain_controller_enabled: bool = False
    _region_registry: RegionRegistry | None = None
    _region_stability_controller: RegionLevelStabilityController | None = None
    _deep_region_routing_calibrator: DeepRegionRoutingCalibrator | None = None
    _deep_region_routing_profile: DeepRegionRoutingProfile | None = None
    _brainstem_controller: BrainstemFunctionalController | None = None
    _last_brainstem_result = None
    _brainstem_gain_controller = None
    _last_brainstem_gain_result = None
    # T42 — Cellular Adaptive Defense & Repair
    cellular_adaptive_defense_enabled: bool = False
    cellular_repair_enabled: bool = False
    cellular_epigenetics_enabled: bool = False
    _cellular_stress_engine: CellularStressEngine | None = None
    _cellular_damage_engine: CellularDamageEngine | None = None
    _cellular_repair_engine: CellularRepairEngine | None = None
    _cellular_defense_engine: CellularDefenseEngine | None = None
    _cellular_epigenetic_adapter: CellularEpigeneticAdapter | None = None
    _last_cellular_stress_result = None
    _last_cellular_damage_result = None
    _last_cellular_repair_result = None
    _last_cellular_defense_result = None
    _last_cellular_epigenetic_result = None
    _previous_damage_state: dict = {}

    class Config:
        arbitrary_types_allowed = True

    def model_post_init(self, __context: object) -> None:
        self._homeostasis = HomeostasisEngine()
        self._plasticity = PlasticityEngine()
        self._memory = MorphologicalMemory()
        self._memory.load()
        self.circuit.memory = self._memory
        self._neurogenesis = NeurogenesisEngine()
        self._apoptosis = ApoptosisEngine()
        self._differentiation = CellDifferentiationEngine(
            genome=self.genome,
            memory=self._memory,
        )
        self._burst_engine = EventDrivenBurstEngine()
        self._stdp = STDPPlasticityEngine()
        self._inhibition = InhibitionEngine()
        self._energy_control = EnergyControlAgent()
        self._inter_region_plasticity = InterRegionPlasticityEngine()
        self._region_signal_router = RegionSignalRouter()
        self._community = CommunityDetectionEngine()
        self._confidence = ConfidenceEngine()
        if self.region_architecture_enabled:
            self._region_registry = RegionFactory.build_from_genome(
                self.circuit, self.genome.model_dump(), seed=42, deep_regions_enabled=self.deep_regions_enabled
            )
        else:
            self._region_registry = None

        if self.region_stability_controller_enabled:
            self._region_stability_controller = RegionLevelStabilityController()
        else:
            self._region_stability_controller = None

        if self.deep_region_routing_calibrator_enabled:
            profile = self._deep_region_routing_profile or DeepRegionRoutingProfile(
                profile_id="orch_default",
                name="orchestrator_default",
            )
            self._deep_region_routing_calibrator = DeepRegionRoutingCalibrator(profile=profile)
            self._deep_region_routing_calibrator.apply_profile_to_router(self._region_signal_router)
        else:
            self._deep_region_routing_calibrator = None

        if self.brainstem_controller_enabled:
            self._brainstem_controller = BrainstemFunctionalController()
        else:
            self._brainstem_controller = None

        if self.brainstem_gain_controller_enabled:
            self._brainstem_gain_controller = AdaptiveBrainstemGainController()
        else:
            self._brainstem_gain_controller = None

        # T42 — Cellular Adaptive Defense & Repair
        if self.cellular_adaptive_defense_enabled:
            self._cellular_stress_engine = CellularStressEngine()
            self._cellular_damage_engine = CellularDamageEngine()
            self._cellular_defense_engine = CellularDefenseEngine()
        if self.cellular_repair_enabled:
            self._cellular_repair_engine = CellularRepairEngine()
        if self.cellular_epigenetics_enabled:
            self._cellular_epigenetic_adapter = CellularEpigeneticAdapter()

    async def run_ticks(self, n_ticks: int) -> None:
        for _ in range(n_ticks):
            await self._tick()
            if self.tick_interval > 0:
                await asyncio.sleep(self.tick_interval)

    async def _tick(self) -> None:
        self.current_tick += 1
        if self.execution_mode == "event_driven_burst":
            burst_results = self._burst_engine.run_event_cycle(self.circuit)
            if self.stdp_enabled:
                self._stdp.apply_stdp(self.circuit, self._memory)
            if self.inhibition_enabled:
                last_result = burst_results[-1] if burst_results else None
                self._inhibition.stabilize_after_burst(
                    self.circuit, last_result, self._memory
                )
            if self.energy_control_enabled:
                metrics = self.latest_metrics
                self._energy_control.regulate(
                    self.circuit,
                    metrics=metrics,
                    burst_engine=self._burst_engine,
                    memory=self._memory,
                )
        else:
            await self.circuit.tick()

        all_neurons = (
            self.circuit.input_neurons
            + self.circuit.hidden_neurons
            + self.circuit.output_neurons
        )
        metrics = self._homeostasis.compute_metrics(
            tick=self.current_tick,
            neurons=all_neurons,
            astrocytes=self.circuit.astrocytes,
            synapse_count=len(self.circuit.synapses),
            pruned_count=sum(1 for s in self.circuit.synapses if s.state == "pruned"),
        )
        self.metrics_log.append(metrics)

        # Community detection (observational only in T17)
        if self.community_detection_enabled:
            self.last_community_result = self._community.analyze(
                self.circuit, memory=self._memory
            )

        # Meta-learning confidence evaluation (T19)
        if self.confidence_enabled:
            self.last_confidence_state = self._confidence.evaluate(
                self.circuit,
                metrics=metrics,
                community_result=self.last_community_result,
                memory=self._memory,
            )
            self.neurogenesis_recommended = (
                self.last_confidence_state.neurogenesis_recommended
            )
            self.stabilization_recommended = (
                self.last_confidence_state.stabilization_recommended
            )
            self.plasticity_reduction_recommended = (
                self.last_confidence_state.plasticity_reduction_recommended
            )

        # Regional architecture regulation (T21)
        if self.region_architecture_enabled and self._region_registry is not None:
            for region in self._region_registry.regions.values():
                region.regulate_region(self.circuit)

        # T33 — Region-Level Stability Controller (pre-routing check)
        routing_multiplier_map = None
        plasticity_multiplier_map = None
        # T34B-FIX: Extract flow memory from router for stability controller
        flow_memory = None
        if self._region_signal_router is not None:
            flow_memory = getattr(self._region_signal_router, "_t34_flow_memory", None)
        if self.region_stability_controller_enabled and self._region_registry is not None:
            pre_result = self._region_stability_controller.pre_routing_stability_check(
                registry=self._region_registry,
                circuit=self.circuit,
                memory=self._memory,
                flow_memory=flow_memory,
            )
            routing_multiplier_map = {
                rid: self._region_stability_controller.get_routing_multiplier(rid)
                for rid in self._region_registry.regions
            }
            plasticity_multiplier_map = {
                rid: self._region_stability_controller.get_plasticity_multiplier(rid)
                for rid in self._region_registry.regions
            }

        # T35 — Brainstem Functional Integration
        if self.brainstem_controller_enabled and self._brainstem_controller is not None:
            # T36 — Compute mean deep-region activation from circuit at tick time
            deep_regions = {"limbic", "hippocampus", "default_mode", "prefrontal", "cerebellar", "brainstem_homeostatic"}
            deep_activations = [
                abs(getattr(n, "activation", 0.0))
                for n in all_neurons
                if getattr(n, "region", None) in deep_regions
            ]
            mean_deep_activation = sum(deep_activations) / len(deep_activations) if deep_activations else 0.0

            brainstem_metrics = {
                "mean_region_phi": metrics.coherence_phi,
                "mean_energy": metrics.mean_energy,
                "region_instability_mean": 0.0,
                "unstable_region_count": 0,
                "mean_deep_region_activation": mean_deep_activation,
                "regional_signal_flow": 0.0,
                "deep_region_signal_flow": 0.0,
                "stability_actions_applied": 0,
                "routing_blocks_applied": 0,
                "cooldowns_started": 0,
                "mean_pathway_utility": 0.0,
                "energy_state": metrics.mean_energy,
                "region_count": len(self._region_registry.regions) if self._region_registry is not None else 4,
                # T36 — placeholder for benchmark-level metrics; brainstem uses proxies when zero
                "cognitive_score": 0.0,
                "functional_improvement": 0.0,
            }
            # Enrich with stability controller data if available
            if self._region_stability_controller is not None:
                summary = self._region_stability_controller.summarize_stability()
                region_states = summary.get("region_states", {})
                instability_scores = [s.get("instability_score", 0.0) for s in region_states.values()]
                if instability_scores:
                    brainstem_metrics["region_instability_mean"] = sum(instability_scores) / len(instability_scores)
                brainstem_metrics["unstable_region_count"] = sum(
                    1 for s in region_states.values() if s.get("instability_score", 0.0) >= 0.25
                )
                brainstem_metrics["mean_region_damping_factor"] = summary.get("mean_damping_factor", 1.0)
            # Enrich with routing data if available
            if self.last_routing_result is not None:
                brainstem_metrics["regional_signal_flow"] = getattr(
                    self.last_routing_result, "regional_signal_flow_score", 0.0
                )
            # T39 — Evaluate gain controller BEFORE brainstem to pass gain vector into state selection
            gain_vector: dict | None = None
            if self.brainstem_gain_controller_enabled and self._brainstem_gain_controller is not None:
                gain_metrics = {
                    "cognitive_score_delta": 0.0,
                    "coherence_phi_delta": 0.0,
                    "energy_efficiency_delta": 0.0,
                    "functional_improvement_delta": 0.0,
                    "suppression_cost": getattr(self._brainstem_controller, "_last_suppression_cost", 0.0) if self._brainstem_controller else 0.0,
                    "emergency_ticks": getattr(self._brainstem_controller, "_state_ticks", {}).get("emergency", 0) if self._brainstem_controller else 0,
                    "protective_ticks": getattr(self._brainstem_controller, "_state_ticks", {}).get("protective", 0) if self._brainstem_controller else 0,
                    "total_ticks": self.current_tick,
                    "mean_region_energy": metrics.mean_energy,
                    "mean_region_phi": metrics.coherence_phi,
                }
                self._last_brainstem_gain_result = self._brainstem_gain_controller.evaluate(gain_metrics)
                gain_vector = self._last_brainstem_gain_result.decision.model_dump()

            self._last_brainstem_result = self._brainstem_controller.apply(
                metrics=brainstem_metrics,
                memory=self._memory,
                gain_vector=gain_vector,
            )
            # Compose brainstem modulations with stability multipliers
            decision = self._last_brainstem_result.decision
            if routing_multiplier_map is not None:
                for rid in routing_multiplier_map:
                    routing_multiplier_map[rid] *= decision.routing_suppression_multiplier
            else:
                routing_multiplier_map = {
                    rid: decision.routing_suppression_multiplier
                    for rid in self._region_registry.regions
                } if self._region_registry is not None else None
            if plasticity_multiplier_map is not None:
                for rid in plasticity_multiplier_map:
                    plasticity_multiplier_map[rid] *= decision.plasticity_suppression_multiplier
            else:
                plasticity_multiplier_map = {
                    rid: decision.plasticity_suppression_multiplier
                    for rid in self._region_registry.regions
                } if self._region_registry is not None else None
            # T37/T39 — Apply Adaptive Brainstem Gain Controller output coupling on top of T36 modulations
            if self.brainstem_gain_controller_enabled and self._brainstem_gain_controller is not None and gain_vector is not None:
                g = self._last_brainstem_gain_result.decision
                if routing_multiplier_map is not None:
                    for rid in routing_multiplier_map:
                        routing_multiplier_map[rid] = 1.0 - (1.0 - routing_multiplier_map[rid]) * g.routing_gain
                if plasticity_multiplier_map is not None:
                    for rid in plasticity_multiplier_map:
                        plasticity_multiplier_map[rid] = 1.0 - (1.0 - plasticity_multiplier_map[rid]) * g.plasticity_gain
                # Re-apply decay with adjusted gain
                adjusted_decay = 1.0 + (decision.decay_boost_multiplier - 1.0) * g.decay_gain
                if adjusted_decay > 1.0:
                    decay_factor = 1.0 / adjusted_decay
                    for n in all_neurons:
                        n.activation = getattr(n, "activation", 0.0) * decay_factor
                # If original decay was already applied, skip re-applying
            else:
                # Apply decay boost if requested (original T35/T36 path)
                if decision.decay_boost_multiplier > 1.0:
                    decay_factor = 1.0 / decision.decay_boost_multiplier
                    for n in all_neurons:
                        n.activation = getattr(n, "activation", 0.0) * decay_factor

        # Regional Signal Routing (T25)
        if self.region_signal_routing_enabled and self._region_registry is not None:
            confidence_score = 0.0
            if self.last_confidence_state is not None:
                confidence_score = self.last_confidence_state.confidence_score
            self.last_routing_result = self._region_signal_router.route_all(
                region_connectome=self._region_registry.connectome,
                circuit=self.circuit,
                metrics=metrics,
                memory=self._memory,
                confidence_score=confidence_score,
                routing_multiplier_map=routing_multiplier_map,
                current_tick=self.current_tick,
            )

        # Inter-Region Plasticity (T23)
        if self.inter_region_plasticity_enabled and self._region_registry is not None:
            confidence_score = 0.0
            if self.last_confidence_state is not None:
                confidence_score = self.last_confidence_state.confidence_score
            self._inter_region_plasticity.update_pathways(
                circuit=self.circuit,
                registry=self._region_registry,
                metrics=metrics,
                memory=self._memory,
                tick=self.current_tick,
                confidence_score=confidence_score,
                routing_result=self.last_routing_result,
                plasticity_multiplier_map=plasticity_multiplier_map,
            )

        # T33 — Region-Level Stability Controller (post-routing check)
        if self.region_stability_controller_enabled and self._region_registry is not None:
            self._region_stability_controller.post_routing_stability_check(
                registry=self._region_registry,
                circuit=self.circuit,
                memory=self._memory,
                flow_memory=flow_memory,
            )

        # T42 — Cellular Adaptive Defense & Repair
        self._run_cellular_adaptive_defense_and_repair()

        # Record morphological snapshot every tick
        snapshot = self._build_morphology_snapshot(metrics)
        self._memory.record_snapshot(snapshot)

    def inject(self, pattern: List[float]) -> None:
        self.circuit.inject_input(pattern)

    def feedback(self, score: float) -> None:
        self.circuit.apply_feedback(score)
        if score < 0:
            self.negative_feedback_count += 1

    def run_immune(self) -> None:
        self.circuit.run_immune()

    def run_neurogenesis(self) -> None:
        metrics = self.latest_metrics
        if metrics is None:
            return
        all_neurons = (
            self.circuit.input_neurons
            + self.circuit.hidden_neurons
            + self.circuit.output_neurons
        )
        energy = metrics.mean_energy
        phi = metrics.coherence_phi
        if self._neurogenesis.should_generate(
            self.negative_feedback_count, phi, energy
        ):
            self._neurogenesis.generate_neuron(
                self.circuit,
                phi_before=phi,
                reason="recurrent_negative_feedback_and_low_phi",
                differentiation_engine=self._differentiation,
            )
            self.negative_feedback_count = 0

    def run_differentiation(self) -> None:
        metrics = self.latest_metrics
        self._differentiation.differentiate_circuit(
            self.circuit, metrics=metrics
        )

    def run_apoptosis(self) -> None:
        metrics = self.latest_metrics
        self._apoptosis.run(self.circuit, metrics=metrics)

    def _run_cellular_adaptive_defense_and_repair(self) -> None:
        """T42 — Run stress, damage, repair, defense, and epigenetic adaptation."""
        # Stress evaluation
        if self.cellular_adaptive_defense_enabled and self._cellular_stress_engine is not None:
            self._last_cellular_stress_result = self._cellular_stress_engine.evaluate(self.circuit)
        else:
            self._last_cellular_stress_result = None

        # Damage evaluation (requires stress)
        if self.cellular_adaptive_defense_enabled and self._cellular_damage_engine is not None and self._last_cellular_stress_result is not None:
            self._last_cellular_damage_result = self._cellular_damage_engine.evaluate(
                self.circuit,
                stress_result=self._last_cellular_stress_result,
                previous_damage=getattr(self, "_previous_damage_state", None),
            )
            self._previous_damage_state = (
                self._last_cellular_damage_result.per_cell if self._last_cellular_damage_result else {}
            )
        else:
            self._last_cellular_damage_result = None

        # Defense (requires stress and damage)
        if self.cellular_adaptive_defense_enabled and self._cellular_defense_engine is not None:
            stress_per_cell = getattr(self._last_cellular_stress_result, "per_cell", {}) or {}
            damage_per_cell = getattr(self._last_cellular_damage_result, "per_cell", {}) or {}
            self._last_cellular_defense_result = self._cellular_defense_engine.run(
                self.circuit,
                stress_per_cell=stress_per_cell,
                damage_per_cell=damage_per_cell,
                memory=self._memory,
            )
        else:
            self._last_cellular_defense_result = None

        # Repair (requires damage)
        if self.cellular_repair_enabled and self._cellular_repair_engine is not None:
            damage_per_cell = getattr(self._last_cellular_damage_result, "per_cell", {}) or {}
            self._last_cellular_repair_result = self._cellular_repair_engine.run(
                self.circuit,
                damage_per_cell=damage_per_cell,
                memory=self._memory,
            )
        else:
            self._last_cellular_repair_result = None

        # Epigenetic adaptation (requires stress and damage)
        if self.cellular_epigenetics_enabled and self._cellular_epigenetic_adapter is not None:
            stress_per_cell = getattr(self._last_cellular_stress_result, "per_cell", {}) or {}
            damage_per_cell = getattr(self._last_cellular_damage_result, "per_cell", {}) or {}
            self._last_cellular_epigenetic_result = self._cellular_epigenetic_adapter.adapt(
                self.circuit,
                stress_per_cell=stress_per_cell,
                damage_per_cell=damage_per_cell,
                current_tick=self.current_tick,
                memory=self._memory,
            )
        else:
            self._last_cellular_epigenetic_result = None

    def _build_morphology_snapshot(self, metrics: SystemMetrics) -> MorphologySnapshot:
        active = sum(1 for s in self.circuit.synapses if s.state != "pruned")
        weights = [s.weight for s in self.circuit.synapses if s.state != "pruned"]
        trusts = [s.trust for s in self.circuit.synapses if s.state != "pruned"]
        energies = [n.energy for n in self.circuit.input_neurons + self.circuit.hidden_neurons + self.circuit.output_neurons]
        snapshot = MorphologySnapshot(
            snapshot_id=f"snap_{self.current_tick}",
            timestamp=metrics.tick,
            tick=self.current_tick,
            neuron_count=len(self.circuit.input_neurons + self.circuit.hidden_neurons + self.circuit.output_neurons),
            synapse_count=len(self.circuit.synapses),
            active_synapse_count=active,
            pruned_synapse_count=metrics.pruned_synapses,
            average_weight=sum(weights) / len(weights) if weights else 0.0,
            average_trust=sum(trusts) / len(trusts) if trusts else 0.0,
            average_energy=sum(energies) / len(energies) if energies else 0.0,
            coherence_phi=metrics.coherence_phi,
            execution_mode=self.execution_mode,
        )
        if self.execution_mode == "event_driven_burst":
            snapshot.burst_id = self._burst_engine.burst_counter
        return snapshot

    @property
    def latest_metrics(self) -> SystemMetrics | None:
        return self.metrics_log[-1] if self.metrics_log else None

    @property
    def memory(self) -> MorphologicalMemory:
        return self._memory

    @property
    def region_registry(self) -> RegionRegistry | None:
        return self._region_registry

    @classmethod
    def build_mvp(cls, genome: SharedGenome) -> "CellularBrainOrchestrator":
        n_inputs = 10
        n_hidden = 60
        n_outputs = 10
        n_synapses = 300
        n_astros = 5
        n_micro = 2
        n_oligo = 2

        input_neurons = [
            DigitalNeuron(cell_id=f"in_{i}", role="digital_neuron", threshold=0.5)
            for i in range(n_inputs)
        ]
        hidden_neurons = [
            DigitalNeuron(cell_id=f"hid_{i}", role="digital_neuron", threshold=0.5)
            for i in range(n_hidden)
        ]
        output_neurons = [
            DigitalNeuron(cell_id=f"out_{i}", role="digital_neuron", threshold=0.5)
            for i in range(n_outputs)
        ]

        all_neurons = input_neurons + hidden_neurons + output_neurons
        for n in all_neurons:
            n.bind_genome(genome)

        synapses: List[DigitalSynapse] = []
        for _ in range(n_synapses):
            src = random.choice(all_neurons)
            tgt = random.choice(all_neurons)
            if src.cell_id == tgt.cell_id:
                continue
            syn = DigitalSynapse(
                cell_id=f"syn_{src.cell_id}_{tgt.cell_id}",
                role="digital_synapse",
                source=src.cell_id,
                target=tgt.cell_id,
                weight=random.uniform(0.1, 0.9),
            )
            syn.bind_genome(genome)
            synapses.append(syn)
            src.targets.append(tgt.cell_id)

        astrocytes = [
            DigitalAstrocyte(cell_id=f"astro_{i}", role="digital_astrocyte")
            for i in range(n_astros)
        ]
        microglia = [
            DigitalMicroglia(cell_id=f"micro_{i}", role="digital_microglia")
            for i in range(n_micro)
        ]
        oligodendrocytes = [
            DigitalOligodendrocyte(cell_id=f"oligo_{i}", role="digital_oligodendrocyte")
            for i in range(n_oligo)
        ]

        circuit = NeuralCircuit(
            circuit_id="mvp_circuit",
            input_neurons=input_neurons,
            hidden_neurons=hidden_neurons,
            output_neurons=output_neurons,
            synapses=synapses,
            astrocytes=astrocytes,
            microglia=microglia,
            oligodendrocytes=oligodendrocytes,
        )

        return cls(genome=genome, circuit=circuit)
