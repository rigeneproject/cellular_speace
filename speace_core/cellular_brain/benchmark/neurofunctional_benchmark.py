import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from speace_core.cellular_brain.circuits.neural_circuit import NeuralCircuit
from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType
from speace_core.cellular_brain.memory.episode_summarizer import EpisodeSummarizer
from speace_core.orchestrator import CellularBrainOrchestrator


class BenchmarkState(BaseModel):
    neuron_count: int = 0
    synapse_count: int = 0
    active_synapse_count: int = 0
    coherence_phi: float = 0.0
    mean_energy: float = 0.0
    accuracy: float = 0.0
    output_activations: List[float] = Field(default_factory=list)


class BenchmarkMetrics(BaseModel):
    accuracy_score: float = 0.0
    coherence_phi: float = 0.0
    phi_trend: float = 0.0
    mean_energy: float = 0.0
    energy_efficiency: float = 0.0
    neuron_count_delta: int = 0
    synapse_count_delta: int = 0
    neurogenesis_events: int = 0
    apoptosis_events: int = 0
    cell_differentiation_events: int = 0
    adaptation_gain: float = 0.0
    morphological_stability: float = 0.0
    morphological_adaptation: float = 0.0
    structural_complexity: float = 0.0
    functional_improvement: float = 0.0
    speace_cognitive_score: float = 0.0
    # T17 — Community metrics
    community_count: int = 0
    modularity_proxy: float = 0.0
    isolated_neuron_count: int = 0
    weak_community_count: int = 0
    overloaded_community_count: int = 0
    # T19 — Meta-cognitive metrics
    confidence_score: float = 0.0
    uncertainty_score: float = 0.0
    output_entropy: float = 0.0
    decision_stability: float = 0.0
    error_risk: float = 0.0
    recommended_action: str = "maintain"
    meta_cognitive_score: float = 0.0
    # T21 — Regional metrics
    region_count: int = 0
    connectome_density: float = 0.0
    mean_region_energy: float = 0.0
    mean_region_phi: float = 0.0
    # T23 — Inter-region plasticity metrics
    mean_pathway_strength: float = 0.0
    reinforced_pathways: int = 0
    weakened_pathways: int = 0
    inter_region_plasticity_events: int = 0
    pathway_energy_cost: float = 0.0
    regional_signal_flow_score: float = 0.0
    # T25 — Regional signal routing metrics
    routed_signals: int = 0
    delivered_signals: int = 0
    blocked_signals: int = 0
    total_routed_signal_strength: float = 0.0
    mean_routed_signal_strength: float = 0.0
    routing_energy_cost: float = 0.0
    active_inter_region_pathways: int = 0
    # T29 — Pathway tuning metrics
    pathway_tuning_accepted_updates: int = 0
    pathway_tuning_skipped_updates: int = 0
    pathway_tuning_rolled_back_updates: int = 0
    pathway_tuning_profile_id: str = ""
    # T30 — Pathway utility metrics
    mean_pathway_utility: float = 0.0
    best_pathway_utility: float = 0.0
    worst_pathway_utility: float = 0.0
    rewarded_pathways: int = 0
    penalized_pathways: int = 0
    pathway_reward_mean: float = 0.0
    pathway_cost_mean: float = 0.0
    utility_gated_updates: int = 0
    utility_skipped_updates: int = 0
    # T31 — Deep region specialization metrics
    deep_region_count: int = 0
    limbic_salience_score: float = 0.0
    cerebellar_error_correction_score: float = 0.0
    default_mode_consolidation_score: float = 0.0
    brainstem_homeostatic_stability_score: float = 0.0
    deep_region_signal_flow: float = 0.0
    region_specialization_diversity: float = 0.0
    region_role_alignment_score: float = 0.0
    # T33 — Region stability metrics
    region_instability_mean: float = 0.0
    unstable_region_count: int = 0
    stability_actions_applied: int = 0
    routing_blocks_applied: int = 0
    cooldowns_started: int = 0
    mean_region_damping_factor: float = 1.0
    brainstem_override_count: int = 0
    phi_recovery_score: float = 0.0
    stability_controller_active: bool = False
    # T34 — Deep Region Routing Calibration metrics
    top_k_routing_active: bool = False
    mean_deep_region_activation: float = 0.0
    deep_region_routing_efficiency: float = 0.0
    regional_gain_applied: bool = False
    flow_memory_enabled: bool = False
    stability_aware_routing_active: bool = False
    deep_region_targeted_signals: int = 0
    mean_regional_signal_gain: float = 0.0
    deep_region_phi_recovery: float = 0.0
    # T35 — Brainstem Functional Integration metrics
    brainstem_state: str = "stable"
    brainstem_decisions_count: int = 0
    brainstem_energy_modulation: float = 1.0
    brainstem_routing_modulation: float = 1.0
    brainstem_plasticity_modulation: float = 1.0
    brainstem_decay_modulation: float = 1.0
    brainstem_recovery_actions: int = 0
    brainstem_emergency_count: int = 0
    brainstem_homeostatic_gain: float = 0.0
    brainstem_phi_recovery_contribution: float = 0.0
    # T36 — Cognitive/Autonomic Balance Tuning metrics
    cognitive_vitality_score: float = 0.0
    autonomic_risk_score: float = 0.0
    balance_pressure: float = 0.0
    brainstem_state_distribution: Dict[str, int] = Field(default_factory=dict)
    emergency_ticks: int = 0
    protective_ticks: int = 0
    watchful_ticks: int = 0
    corrective_ticks: int = 0
    cognitive_preservation_score: float = 0.0
    autonomic_balance_score: float = 0.0
    suppression_cost: float = 0.0
    useful_activity_preserved: bool = False
    # T37 — Adaptive Brainstem Gain Controller metrics
    brainstem_gain_reward: float = 0.0
    global_brainstem_gain: float = 1.0
    routing_gain: float = 1.0
    plasticity_gain: float = 1.0
    decay_gain: float = 1.0
    energy_recovery_gain: float = 1.0
    emergency_gain: float = 1.0
    cognitive_preservation_gain: float = 1.0
    gain_adjustments_count: int = 0
    over_suppression_detected: bool = False
    useful_stabilization_detected: bool = False
    true_instability_detected: bool = False
    gain_stability_score: float = 0.0
    # T38 — Gain Sensitivity Tuning metrics
    brainstem_gain_reward_v2: float = 0.0
    adaptive_gain_learning_rate: float = 0.05
    gain_profile_divergence: float = 0.0
    gain_convergence_detected: bool = False
    diversity_pressure_applied: bool = False
    suppression_cost_reduction: float = 0.0
    cognitive_recovery_margin: float = 0.0
    phi_preservation_margin: float = 0.0
    net_gain_vs_t36: float = 0.0
    net_gain_vs_t34b: float = 0.0
    gain_vector_distance: float = 0.0
    # T39 — Gain Input Coupling Redesign metrics
    gain_input_coupling_strength: float = 0.0
    adjusted_cognitive_vitality_score: float = 0.0
    adjusted_autonomic_risk_score: float = 0.0
    adjusted_balance_pressure: float = 0.0
    protective_escape_count: int = 0
    protective_state_ratio: float = 0.0
    corrective_state_ratio: float = 0.0
    emergency_state_ratio: float = 0.0
    coupling_delta_mean: float = 0.0
    suppression_cost_after_coupling: float = 0.0
    brainstem_state_transition_count: int = 0
    # T42 — Cellular Adaptive Defense & Repair metrics
    mean_cellular_stress: float = 0.0
    max_cellular_stress: float = 0.0
    mean_damage_score: float = 0.0
    max_damage_score: float = 0.0
    repair_success_rate: float = 0.0
    repair_failure_rate: float = 0.0
    defense_activation_count: int = 0
    quarantined_cell_count: int = 0
    epigenetic_shift_count: int = 0
    cellular_resilience_score: float = 0.0
    cellular_survival_score: float = 0.0
    cellular_self_repair_score: float = 0.0
    cellular_defense_score: float = 0.0
    epigenetic_adaptation_score: float = 0.0
    # T43 — Semantic Cell Assembly Memory metrics
    semantic_assembly_count: int = 0
    semantic_active_assembly_count: int = 0
    semantic_consolidated_assembly_count: int = 0
    mean_assembly_strength: float = 0.0
    mean_assembly_stability: float = 0.0
    semantic_recall_success_rate: float = 0.0
    semantic_memory_density: float = 0.0
    semantic_memory_utility: float = 0.0
    semantic_consolidation_rate: float = 0.0
    semantic_memory_score: float = 0.0
    # T45 — Self-Improvement metrics
    limitations_detected: int = 0
    diagnoses_created: int = 0
    architecture_proposals_created: int = 0
    architecture_proposals_accepted: int = 0
    architecture_proposals_rejected: int = 0
    self_improvement_acceptance_score: float = 0.0
    self_improvement_safety_passed: bool = False
    # T44 — Associative Learning metrics
    assembly_association_count: int = 0
    assembly_associations_created: int = 0
    assembly_associations_reinforced: int = 0
    assembly_associations_weakened: int = 0
    assembly_associations_pruned: int = 0
    mean_association_strength: float = 0.0
    max_association_strength: float = 0.0
    association_density: float = 0.0
    associative_recall_success_rate: float = 0.0
    associative_recall_partial_success_rate: float = 0.0
    associative_memory_effect_score: float = 0.0
    # T46 — Self-Improvement Outcome Learning metrics
    self_improvement_outcome_count: int = 0
    self_improvement_success_rate: float = 0.0
    self_improvement_regression_rate: float = 0.0
    self_improvement_mean_net_gain: float = 0.0
    self_improvement_learning_confidence: float = 0.0
    validated_proposal_count: int = 0
    failed_proposal_count: int = 0
    # T47 — Episodic Memory metrics
    episode_count: int = 0
    episode_event_count: int = 0
    recovery_episode_count: int = 0
    regression_episode_count: int = 0
    self_improvement_episode_count: int = 0
    semantic_learning_episode_count: int = 0
    episodic_recall_success_rate: float = 0.0
    recovery_pattern_count: int = 0
    regression_precursor_count: int = 0
    # T48 — Episodic-Guided Self-Improvement Policy metrics
    episodic_policy_enabled: bool = False
    episodic_context_episode_count: int = 0
    episodic_recovery_context_count: int = 0
    episodic_regression_context_count: int = 0
    episodic_policy_bonus_mean: float = 0.0
    episodic_policy_penalty_mean: float = 0.0
    episodic_adjusted_confidence: float = 0.0
    episodic_policy_selected_proposal_score: float = 0.0
    # T49 — Counterfactual Architecture Sandbox metrics
    counterfactual_scenarios_tested: int = 0
    counterfactual_accepted_count: int = 0
    counterfactual_rejected_count: int = 0
    counterfactual_unsafe_count: int = 0
    counterfactual_best_delta_score: float = 0.0
    counterfactual_mean_delta_score: float = 0.0
    counterfactual_best_confidence: float = 0.0
    counterfactual_policy_safe: bool = False
    # T50 — Safe Architecture Patch Execution metrics
    architecture_patch_count: int = 0
    architecture_patch_applied_count: int = 0
    architecture_patch_confirmed_count: int = 0
    architecture_patch_rollback_count: int = 0
    architecture_patch_failure_count: int = 0
    architecture_patch_mean_delta_score: float = 0.0
    architecture_patch_last_delta_phi: float = 0.0
    architecture_patch_last_delta_energy: float = 0.0
    architecture_patch_safety_pass_rate: float = 0.0
    # T51 — Patch Outcome Audit metrics
    patch_audit_cycles_run: int = 0
    patch_audit_confirmed_count: int = 0
    patch_audit_rollback_count: int = 0
    patch_audit_rejected_count: int = 0
    patch_audit_unsafe_blocks: int = 0
    patch_audit_success_rate: float = 0.0
    patch_audit_regression_rate: float = 0.0
    patch_audit_cumulative_delta_score: float = 0.0
    patch_audit_cumulative_delta_phi: float = 0.0
    patch_audit_learning_confidence_delta: float = 0.0
    autonomous_improvement_readiness_score: float = 0.0


class BenchmarkResult(BaseModel):
    case_name: str = ""
    baseline_state: BenchmarkState = Field(default_factory=BenchmarkState)
    final_state: BenchmarkState = Field(default_factory=BenchmarkState)
    metrics: BenchmarkMetrics = Field(default_factory=BenchmarkMetrics)
    json_report_path: Optional[str] = None
    markdown_report_path: Optional[str] = None


class NeuroFunctionalBenchmark:
    """Reproducible neuro-functional benchmark for SPEACE v0.2."""

    def __init__(self, orchestrator: CellularBrainOrchestrator):
        self.orch = orchestrator
        self.reports_dir = Path("reports/neurofunctional")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    async def capture_state(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
    ) -> BenchmarkState:
        """Capture current circuit state, optionally after injecting a pattern."""
        if input_pattern is not None:
            self.orch.inject(input_pattern)
            await self.orch.run_ticks(1)

        circuit = self.orch.circuit
        metrics = self.orch.latest_metrics

        neuron_count = len(
            circuit.input_neurons + circuit.hidden_neurons + circuit.output_neurons
        )
        synapse_count = len(circuit.synapses)
        active_synapse_count = sum(1 for s in circuit.synapses if s.state != "pruned")
        coherence_phi = metrics.coherence_phi if metrics else 0.0
        mean_energy = metrics.mean_energy if metrics else 0.0

        output_activations = [n.activation for n in circuit.output_neurons]
        accuracy = 0.0
        if target_output is not None and output_activations:
            clamped = [min(1.0, max(0.0, a)) for a in output_activations]
            mae = sum(abs(t - o) for t, o in zip(target_output, clamped)) / len(
                target_output
            )
            accuracy = max(0.0, 1.0 - mae)

        return BenchmarkState(
            neuron_count=neuron_count,
            synapse_count=synapse_count,
            active_synapse_count=active_synapse_count,
            coherence_phi=coherence_phi,
            mean_energy=mean_energy,
            accuracy=accuracy,
            output_activations=output_activations,
        )

    async def run_adaptation_cycle(
        self,
        input_pattern: List[float],
        target_output: List[float],
        n_ticks: int = 5,
        n_feedback: int = 3,
    ) -> BenchmarkResult:
        """Run a generic adaptation cycle and return benchmark result."""
        baseline = await self.capture_state(input_pattern, target_output)

        for _ in range(n_feedback):
            self.orch.inject(input_pattern)
            await self.orch.run_ticks(n_ticks)
            # Alternate negative / positive feedback to simulate learning
            score = random.choice([-0.3, 0.5])
            self.orch.feedback(score)

        final = await self.capture_state(input_pattern, target_output)
        metrics = self._compute_metrics(baseline, final)

        result = BenchmarkResult(
            case_name="adaptation_cycle",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )
        return result

    async def run_case(
        self,
        case_name: str,
        execution_mode: str = "global_tick",
        stdp_enabled: bool = True,
        inhibition_enabled: bool = True,
        energy_control_enabled: bool = True,
        community_detection_enabled: bool = True,
        confidence_enabled: bool = True,
        **kwargs: Any,
    ) -> BenchmarkResult:
        """Dispatcher for predefined benchmark scenarios."""
        original_mode = self.orch.execution_mode
        original_stdp = self.orch.stdp_enabled
        original_inhibition = self.orch.inhibition_enabled
        original_energy = self.orch.energy_control_enabled
        original_community = self.orch.community_detection_enabled
        original_confidence = self.orch.confidence_enabled
        original_irp = getattr(self.orch, "inter_region_plasticity_enabled", True)
        original_routing = getattr(self.orch, "region_signal_routing_enabled", True)
        self.orch.execution_mode = execution_mode
        self.orch.stdp_enabled = stdp_enabled
        self.orch.inhibition_enabled = inhibition_enabled
        self.orch.energy_control_enabled = energy_control_enabled
        self.orch.community_detection_enabled = community_detection_enabled
        self.orch.confidence_enabled = confidence_enabled
        self.orch.inter_region_plasticity_enabled = kwargs.pop("inter_region_plasticity_enabled", original_irp)
        self.orch.region_signal_routing_enabled = kwargs.pop("region_signal_routing_enabled", original_routing)
        try:
            if case_name == "adaptation_after_error":
                result = await self._case_adaptation_after_error(**kwargs)
            elif case_name == "useful_neurogenesis":
                result = await self._case_useful_neurogenesis(**kwargs)
            elif case_name == "useful_apoptosis":
                result = await self._case_useful_apoptosis(**kwargs)
            elif case_name == "differentiation_consistency":
                result = await self._case_differentiation_consistency(**kwargs)
            elif case_name == "morphological_memory_trace":
                result = await self._case_morphological_memory_trace(**kwargs)
            else:
                raise ValueError(f"Unknown benchmark case: {case_name}")
        finally:
            self.orch.execution_mode = original_mode
            self.orch.stdp_enabled = original_stdp
            self.orch.inhibition_enabled = original_inhibition
            self.orch.energy_control_enabled = original_energy
            self.orch.community_detection_enabled = original_community
            self.orch.confidence_enabled = original_confidence
            self.orch.inter_region_plasticity_enabled = original_irp
            self.orch.region_signal_routing_enabled = original_routing
        return result

    async def _case_adaptation_after_error(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
        n_ticks: int = 5,
    ) -> BenchmarkResult:
        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        baseline = await self.capture_state(pattern, target)

        # Negative feedback phase
        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.feedback(-0.5)

        # Positive feedback phase
        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.feedback(0.8)

        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="adaptation_after_error",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    async def _case_useful_neurogenesis(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
        n_ticks: int = 5,
    ) -> BenchmarkResult:
        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        baseline = await self.capture_state(pattern, target)

        # Force neurogenesis conditions
        self.orch.negative_feedback_count = 5
        # Ensure hidden neurons have high energy so mean_energy stays above min
        for n in self.orch.circuit.hidden_neurons:
            n.energy = 1.0

        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.run_neurogenesis()

        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="useful_neurogenesis",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    async def _case_useful_apoptosis(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
        n_ticks: int = 5,
    ) -> BenchmarkResult:
        from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron

        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        # Add a weak, expensive, isolated neuron to hidden layer
        weak = DigitalNeuron(
            cell_id="weak_001",
            role="digital_neuron",
            threshold=0.5,
            energy=1.0,
            utility_score=0.0,
        )
        weak.is_critical = False
        weak.neuron_role = "excitatory"
        self.orch.circuit.hidden_neurons.append(weak)

        baseline = await self.capture_state(pattern, target)

        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.run_apoptosis()

        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="useful_apoptosis",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    async def _case_differentiation_consistency(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
    ) -> BenchmarkResult:
        from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron

        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        # Add undifferentiated neurons in distinct regions
        hip = DigitalNeuron(cell_id="hip_001", role="digital_neuron")
        hip.region = "hippocampus"
        hip.differentiation_state = "undifferentiated"
        pfc = DigitalNeuron(cell_id="pfc_001", role="digital_neuron")
        pfc.region = "prefrontal"
        pfc.differentiation_state = "undifferentiated"

        self.orch.circuit.hidden_neurons.append(hip)
        self.orch.circuit.hidden_neurons.append(pfc)

        baseline = await self.capture_state(pattern, target)
        self.orch.run_differentiation()
        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="differentiation_consistency",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    async def _case_morphological_memory_trace(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
        n_ticks: int = 5,
    ) -> BenchmarkResult:
        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        baseline = await self.capture_state(pattern, target)

        # Full adaptive cycle
        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.feedback(-0.3)

        self.orch.negative_feedback_count = 5
        for n in self.orch.circuit.hidden_neurons:
            n.energy = 1.0
        self.orch.run_neurogenesis()
        self.orch.run_apoptosis()
        self.orch.run_differentiation()

        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.feedback(0.6)

        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="morphological_memory_trace",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    def _compute_metrics(
        self, baseline: BenchmarkState, final: BenchmarkState
    ) -> BenchmarkMetrics:
        phi_trend = final.coherence_phi - baseline.coherence_phi
        neuron_count_delta = final.neuron_count - baseline.neuron_count
        synapse_count_delta = final.synapse_count - baseline.synapse_count
        structural_delta = abs(neuron_count_delta) + abs(synapse_count_delta)
        adaptation_gain = final.accuracy - baseline.accuracy

        energy_efficiency = max(0.0, min(1.0, final.mean_energy))
        structural_complexity = (
            final.active_synapse_count / final.neuron_count
            if final.neuron_count > 0
            else 0.0
        )
        morphological_stability = 1.0 / (
            1.0 + 0.1 * abs(neuron_count_delta) + 0.01 * abs(synapse_count_delta)
        )
        functional_improvement = max(0.0, adaptation_gain) + max(0.0, phi_trend)
        morphological_adaptation = (
            1.0
            if functional_improvement > 0 and structural_delta > 0
            else 0.0
        )
        safety_score = (
            1.0
            if final.neuron_count >= 5 and final.coherence_phi > 0.0
            else 0.0
        )

        mem = self.orch.memory
        neurogenesis_events = mem.count_events(MorphologyEventType.NEURON_CREATED)
        apoptosis_events = mem.count_events(MorphologyEventType.NEURON_APOPTOSIS)
        cell_diff_events = mem.count_events(MorphologyEventType.CELL_DIFFERENTIATED)

        # T17 — Community metrics from orchestrator
        community_result = self.orch.last_community_result
        community_count = community_result.community_count if community_result else 0
        modularity_proxy = community_result.modularity_proxy if community_result else 0.0
        isolated_neuron_count = (
            len(community_result.isolated_neurons) if community_result else 0
        )
        weak_community_count = (
            len(community_result.weak_communities) if community_result else 0
        )
        overloaded_community_count = (
            len(community_result.overloaded_communities) if community_result else 0
        )

        score = (
            0.20 * final.accuracy
            + 0.20 * final.coherence_phi
            + 0.15 * max(0.0, adaptation_gain)
            + 0.15 * energy_efficiency
            + 0.10 * morphological_stability
            + 0.10 * max(0.0, phi_trend)
            + 0.10 * safety_score
        )
        speace_cognitive_score = max(0.0, min(1.0, score))

        # T19 — Confidence metrics from orchestrator
        confidence_state = self.orch.last_confidence_state
        confidence_score = confidence_state.confidence_score if confidence_state else 0.0
        uncertainty_score = confidence_state.uncertainty_score if confidence_state else 0.0
        output_entropy = confidence_state.output_entropy if confidence_state else 0.0
        decision_stability = confidence_state.decision_stability if confidence_state else 0.0
        error_risk = confidence_state.error_risk if confidence_state else 0.0
        recommended_action = (
            confidence_state.recommended_action if confidence_state else "maintain"
        )

        meta_cognitive_score = (
            0.40 * confidence_score
            + 0.30 * decision_stability
            + 0.20 * (1.0 - error_risk)
            + 0.10 * final.coherence_phi
        )
        meta_cognitive_score = max(0.0, min(1.0, meta_cognitive_score))

        # T21 — Regional metrics from orchestrator
        region_registry = self.orch.region_registry
        region_count = 0
        connectome_density = 0.0
        mean_region_energy = 0.0
        mean_region_phi = 0.0
        if region_registry is not None:
            region_count = len(region_registry.regions)
            connectome_density = region_registry.connectome.compute_connectome_density()
            global_metrics = region_registry.compute_global_metrics()
            mean_region_energy = global_metrics.get("mean_region_energy", 0.0)
            mean_region_phi = global_metrics.get("mean_region_phi", 0.0)

        # T23 — Inter-region plasticity metrics
        mean_pathway_strength = 0.0
        pathway_energy_cost = 0.0
        if region_registry is not None and region_registry.connectome is not None:
            conns = region_registry.connectome.connections
            if conns:
                mean_pathway_strength = sum(c.strength for c in conns) / len(conns)
        for e in reversed(mem.events):
            if e.event_type == MorphologyEventType.INTER_REGION_PLASTICITY_APPLIED:
                pathway_energy_cost = e.metadata.get("total_energy_cost", 0.0)
                break
        reinforced_pathways = mem.count_events(MorphologyEventType.REGION_PATHWAY_REINFORCED)
        weakened_pathways = mem.count_events(MorphologyEventType.REGION_PATHWAY_WEAKENED)
        inter_region_plasticity_events = mem.count_events(MorphologyEventType.INTER_REGION_PLASTICITY_APPLIED)

        # T24 — Regional signal flow score
        regional_signal_flow_score = 0.0
        if region_registry is not None and region_registry.connectome is not None:
            conns = region_registry.connectome.connections
            if conns:
                active_conns = sum(1 for c in conns if c.plasticity_enabled and c.strength > 0)
                normalized_active = active_conns / len(conns)
                regional_signal_flow_score = mean_pathway_strength * normalized_active * mean_region_phi

        # T25 — Regional signal routing metrics
        routed_signals = 0
        delivered_signals = 0
        blocked_signals = 0
        total_routed_signal_strength = 0.0
        mean_routed_signal_strength = 0.0
        routing_energy_cost = 0.0
        active_inter_region_pathways = 0
        last_routing = getattr(self.orch, "last_routing_result", None)
        if last_routing is not None:
            routed_signals = last_routing.routed_signals
            delivered_signals = last_routing.delivered_signals
            blocked_signals = last_routing.blocked_signals
            total_routed_signal_strength = last_routing.total_signal_strength
            mean_routed_signal_strength = last_routing.mean_signal_strength
            routing_energy_cost = last_routing.total_energy_cost
            active_inter_region_pathways = last_routing.active_pathways
            # Override T24 flow score with T25 value if available
            if last_routing.regional_signal_flow_score > 0:
                regional_signal_flow_score = last_routing.regional_signal_flow_score

        # T29 — Pathway tuning metrics from memory events
        pathway_tuning_accepted_updates = 0
        pathway_tuning_skipped_updates = 0
        pathway_tuning_rolled_back_updates = 0
        pathway_tuning_profile_id = ""
        for e in reversed(mem.events):
            if e.event_type == MorphologyEventType.PATHWAY_TUNING_PROFILE_APPLIED:
                pathway_tuning_accepted_updates = e.metadata.get("accepted", 0)
                pathway_tuning_skipped_updates = e.metadata.get("skipped", 0)
                pathway_tuning_rolled_back_updates = e.metadata.get("rolled_back", 0)
                pathway_tuning_profile_id = e.metadata.get("profile_id", "")
                break

        # T30 — Pathway utility metrics from memory events
        mean_pathway_utility = 0.0
        best_pathway_utility = 0.0
        worst_pathway_utility = 0.0
        rewarded_pathways = 0
        penalized_pathways = 0
        pathway_reward_mean = 0.0
        pathway_cost_mean = 0.0
        utility_gated_updates = 0
        utility_skipped_updates = 0
        utility_scores = []
        reward_values = []
        cost_values = []
        for e in mem.events:
            if e.event_type == MorphologyEventType.PATHWAY_REWARD_COMPUTED:
                reward_values.append(e.metadata.get("composite_reward", 0.0))
                cost_values.append(e.metadata.get("routing_cost", 0.0) + e.metadata.get("plasticity_cost", 0.0))
            elif e.event_type == MorphologyEventType.PATHWAY_UTILITY_POSITIVE:
                rewarded_pathways += 1
                utility_scores.append(e.metadata.get("utility_score", 0.0))
            elif e.event_type == MorphologyEventType.PATHWAY_UTILITY_NEGATIVE:
                penalized_pathways += 1
                utility_scores.append(e.metadata.get("utility_score", 0.0))
            elif e.event_type == MorphologyEventType.PATHWAY_UTILITY_GATE_APPLIED:
                utility_gated_updates += 1
        if utility_scores:
            mean_pathway_utility = sum(utility_scores) / len(utility_scores)
            best_pathway_utility = max(utility_scores)
            worst_pathway_utility = min(utility_scores)
        if reward_values:
            pathway_reward_mean = sum(reward_values) / len(reward_values)
        if cost_values:
            pathway_cost_mean = sum(cost_values) / len(cost_values)

        # T31 — Deep region specialization metrics
        deep_region_count = 0
        limbic_salience_score = 0.0
        cerebellar_error_correction_score = 0.0
        default_mode_consolidation_score = 0.0
        brainstem_homeostatic_stability_score = 0.0
        deep_region_signal_flow = 0.0
        region_specialization_diversity = 0.0
        region_role_alignment_score = 0.0
        if region_registry is not None:
            from speace_core.cellular_brain.regions.deep_region_specialization import DeepRegionSpecialization
            deep_metrics = DeepRegionSpecialization.compute_deep_region_metrics(region_registry)
            deep_region_count = deep_metrics.get("deep_region_count", 0)
            limbic_salience_score = deep_metrics.get("limbic_salience_score", 0.0)
            cerebellar_error_correction_score = deep_metrics.get("cerebellar_error_correction_score", 0.0)
            default_mode_consolidation_score = deep_metrics.get("default_mode_consolidation_score", 0.0)
            brainstem_homeostatic_stability_score = deep_metrics.get("brainstem_homeostatic_stability_score", 0.0)
            deep_region_signal_flow = deep_metrics.get("deep_region_signal_flow", 0.0)
            region_specialization_diversity = deep_metrics.get("region_specialization_diversity", 0.0)
            region_role_alignment_score = deep_metrics.get("region_role_alignment_score", 0.0)

        # T33 — Region stability metrics
        region_instability_mean = 0.0
        unstable_region_count = 0
        stability_actions_applied = 0
        routing_blocks_applied = 0
        cooldowns_started = 0
        mean_region_damping_factor = 1.0
        brainstem_override_count = 0
        phi_recovery_score = 0.0
        stability_controller_active = False
        if (
            self.orch.region_stability_controller_enabled
            and self.orch._region_stability_controller is not None
        ):
            controller = self.orch._region_stability_controller
            stability_controller_active = True
            states = list(controller._region_states.values())
            if states:
                region_instability_mean = sum(s.instability_score for s in states) / len(states)
                unstable_region_count = sum(1 for s in states if s.instability_score >= 0.25)
                mean_region_damping_factor = sum(s.damping_factor for s in states) / len(states)
            routing_blocks_applied = sum(
                1 for e in self.orch.memory.events
                if e.event_type == MorphologyEventType.REGION_ROUTING_BLOCKED
            )
            cooldowns_started = sum(
                1 for e in self.orch.memory.events
                if e.event_type == MorphologyEventType.REGION_COOLDOWN_STARTED
            )
            brainstem_override_count = sum(
                1 for e in self.orch.memory.events
                if e.event_type == MorphologyEventType.BRAINSTEM_STABILITY_OVERRIDE
            )
            stability_actions_applied = routing_blocks_applied + cooldowns_started + sum(
                1 for e in self.orch.memory.events
                if e.event_type == MorphologyEventType.REGION_DAMPING_APPLIED
            )
            # phi_recovery_score: max(0, phi_with_stability - phi_without_stability)
            # Approximate using baseline vs final if controller was active
            phi_recovery_score = max(0.0, final.coherence_phi - baseline.coherence_phi)

        # T34 — Deep Region Routing Calibration metrics
        top_k_routing_active = False
        mean_deep_region_activation = 0.0
        deep_region_routing_efficiency = 0.0
        regional_gain_applied = False
        flow_memory_enabled = False
        stability_aware_routing_active = False
        deep_region_targeted_signals = 0
        mean_regional_signal_gain = 0.0
        deep_region_phi_recovery = 0.0
        router = getattr(self.orch, "_region_signal_router", None)
        if router is not None:
            t34_profile = getattr(router, "_t34_profile", None)
            if t34_profile is not None:
                top_k_routing_active = t34_profile.top_k_routing_active
                flow_memory_enabled = t34_profile.flow_memory_enabled
                stability_aware_routing_active = t34_profile.stability_aware_routing
                regional_gain_applied = bool(t34_profile.regional_gain_map)
                gain_map = getattr(router, "_t34_gain_map", {})
                if gain_map:
                    mean_regional_signal_gain = sum(gain_map.values()) / len(gain_map)

        # Deep region activation proxy from last routing result
        last_routing = getattr(self.orch, "last_routing_result", None)
        if last_routing is not None:
            deep_region_targeted_signals = getattr(last_routing, "deep_region_targeted_signals", 0) or 0
            # Efficiency = delivered / (routed + 1e-12)
            if last_routing.routed_signals > 0:
                deep_region_routing_efficiency = last_routing.delivered_signals / last_routing.routed_signals

        # Deep region activation proxy: mean activation of deep-region neurons
        region_registry = self.orch.region_registry
        if region_registry is not None:
            deep_regions = {"limbic", "hippocampus", "default_mode", "prefrontal", "cerebellar", "brainstem_homeostatic"}
            all_neurons = self.orch.circuit.input_neurons + self.orch.circuit.hidden_neurons + self.orch.circuit.output_neurons
            deep_activations = [
                abs(getattr(n, "activation", 0.0))
                for n in all_neurons
                if getattr(n, "region", None) in deep_regions
            ]
            if deep_activations:
                mean_deep_region_activation = sum(deep_activations) / len(deep_activations)

        # Phi recovery specific to deep region calibration
        deep_region_phi_recovery = max(0.0, final.coherence_phi - baseline.coherence_phi)

        # T35 — Brainstem Functional Integration metrics
        brainstem_state = "stable"
        brainstem_decisions_count = 0
        brainstem_energy_modulation = 1.0
        brainstem_routing_modulation = 1.0
        brainstem_plasticity_modulation = 1.0
        brainstem_decay_modulation = 1.0
        brainstem_recovery_actions = 0
        brainstem_emergency_count = 0
        brainstem_homeostatic_gain = 0.0
        brainstem_phi_recovery_contribution = 0.0
        # T36 — Cognitive/Autonomic Balance Tuning metrics
        cognitive_vitality_score = 0.0
        autonomic_risk_score = 0.0
        balance_pressure = 0.0
        brainstem_state_distribution: Dict[str, int] = {}
        emergency_ticks = 0
        protective_ticks = 0
        watchful_ticks = 0
        corrective_ticks = 0
        cognitive_preservation_score = 0.0
        autonomic_balance_score = 0.0
        suppression_cost = 0.0
        useful_activity_preserved = False
        # T39 — defaults for gain input coupling metrics
        adjusted_cognitive_vitality_score = 0.0
        adjusted_autonomic_risk_score = 0.0
        adjusted_balance_pressure = 0.0
        protective_escape_count = 0
        protective_state_ratio = 0.0
        corrective_state_ratio = 0.0
        emergency_state_ratio = 0.0
        coupling_delta_mean = 0.0
        suppression_cost_after_coupling = 0.0
        brainstem_state_transition_count = 0
        gain_input_coupling_strength = 0.0
        bsc = getattr(self.orch, "_brainstem_controller", None)
        bsr = getattr(self.orch, "_last_brainstem_result", None)
        if bsc is not None and bsr is not None:
            brainstem_state = bsr.decision.state.value
            brainstem_decisions_count = bsr.decisions_count
            brainstem_energy_modulation = bsr.decision.energy_recovery_multiplier
            brainstem_routing_modulation = bsr.decision.routing_suppression_multiplier
            brainstem_plasticity_modulation = bsr.decision.plasticity_suppression_multiplier
            brainstem_decay_modulation = bsr.decision.decay_boost_multiplier
            brainstem_recovery_actions = bsr.recovery_actions
            brainstem_emergency_count = bsr.emergency_count
            brainstem_homeostatic_gain = bsr.homeostatic_gain
            brainstem_phi_recovery_contribution = bsr.phi_recovery_contribution
            # T36 extraction from controller state
            summary = bsc.get_modulation_summary()
            cognitive_vitality_score = summary.get("cognitive_vitality", 0.0)
            autonomic_risk_score = summary.get("autonomic_risk", 0.0)
            balance_pressure = summary.get("balance_pressure", 0.0)
            brainstem_state_distribution = summary.get("state_ticks", {})
            emergency_ticks = brainstem_state_distribution.get("emergency", 0)
            protective_ticks = brainstem_state_distribution.get("protective", 0)
            watchful_ticks = brainstem_state_distribution.get("watchful", 0)
            corrective_ticks = brainstem_state_distribution.get("corrective", 0)
            cognitive_preservation_score = 1.0 if summary.get("cognitive_preservation_applied", False) else 0.0
            autonomic_balance_score = max(0.0, 1.0 - balance_pressure)
            suppression_cost = summary.get("suppression_cost", 0.0)
            useful_activity_preserved = summary.get("useful_activity_preserved", False)
            # T39 — Gain Input Coupling metrics
            adjusted_cognitive_vitality_score = summary.get("adjusted_cognitive_vitality", 0.0)
            adjusted_autonomic_risk_score = summary.get("adjusted_autonomic_risk", 0.0)
            adjusted_balance_pressure = summary.get("adjusted_balance_pressure", 0.0)
            protective_escape_count = summary.get("protective_escape_count", 0)
            total_state_ticks = max(1, sum(brainstem_state_distribution.values()))
            protective_state_ratio = round(brainstem_state_distribution.get("protective", 0) / total_state_ticks, 4)
            corrective_state_ratio = round(brainstem_state_distribution.get("corrective", 0) / total_state_ticks, 4)
            emergency_state_ratio = round(brainstem_state_distribution.get("emergency", 0) / total_state_ticks, 4)
            coupling_delta_mean = summary.get("coupling_delta", 0.0)
            suppression_cost_after_coupling = summary.get("suppression_cost_after_coupling", 0.0)
            brainstem_state_transition_count = summary.get("state_transition_count", 0)
            gain_input_coupling_strength = round(
                abs(adjusted_cognitive_vitality_score - cognitive_vitality_score)
                + abs(adjusted_autonomic_risk_score - autonomic_risk_score), 4
            )

        # T37/T38 — Adaptive Brainstem Gain Controller metrics
        brainstem_gain_reward = 0.0
        brainstem_gain_reward_v2 = 0.0
        global_brainstem_gain = 1.0
        routing_gain = 1.0
        plasticity_gain = 1.0
        decay_gain = 1.0
        energy_recovery_gain = 1.0
        emergency_gain = 1.0
        cognitive_preservation_gain = 1.0
        gain_adjustments_count = 0
        over_suppression_detected = False
        useful_stabilization_detected = False
        true_instability_detected = False
        gain_stability_score = 0.0
        adaptive_gain_learning_rate = 0.05
        gain_profile_divergence = 0.0
        gain_convergence_detected = False
        diversity_pressure_applied = False
        suppression_cost_reduction = 0.0
        cognitive_recovery_margin = 0.0
        phi_preservation_margin = 0.0
        gain_vector_distance = 0.0
        bgc = getattr(self.orch, "_brainstem_gain_controller", None)
        if bgc is not None:
            gain_summary = bgc.get_gain_summary()
            global_brainstem_gain = gain_summary.get("global_brainstem_gain", 1.0)
            routing_gain = gain_summary.get("routing_gain", 1.0)
            plasticity_gain = gain_summary.get("plasticity_gain", 1.0)
            decay_gain = gain_summary.get("decay_gain", 1.0)
            energy_recovery_gain = gain_summary.get("energy_recovery_gain", 1.0)
            emergency_gain = gain_summary.get("emergency_gain", 1.0)
            cognitive_preservation_gain = gain_summary.get("cognitive_preservation_gain", 1.0)
            gain_adjustments_count = gain_summary.get("gain_adjustments_count", 0)
            adaptive_gain_learning_rate = gain_summary.get("adaptive_lr", 0.05)
            # Compute deltas from baseline for gain evaluation
            cog_delta = final.accuracy - baseline.accuracy
            phi_delta = final.coherence_phi - baseline.coherence_phi
            energy_delta = final.mean_energy - baseline.mean_energy
            func_delta = final.accuracy - baseline.accuracy
            flow_delta = regional_signal_flow_score - (baseline.coherence_phi if baseline.coherence_phi else 0.0)
            gain_metrics = {
                "cognitive_score_delta": cog_delta,
                "coherence_phi_delta": phi_delta,
                "energy_efficiency_delta": energy_delta,
                "functional_improvement_delta": func_delta,
                "regional_signal_flow_delta": flow_delta,
                "suppression_cost": suppression_cost,
                "emergency_ticks": emergency_ticks,
                "protective_ticks": protective_ticks,
                "total_ticks": getattr(self.orch, "current_tick", 5),
                "mean_region_energy": final.mean_energy,
                "mean_region_phi": final.coherence_phi,
            }
            gain_result = bgc.evaluate(gain_metrics)
            brainstem_gain_reward = gain_result.brainstem_gain_reward
            brainstem_gain_reward_v2 = gain_result.brainstem_gain_reward_v2
            over_suppression_detected = gain_result.over_suppression_detected
            useful_stabilization_detected = gain_result.useful_stabilization_detected
            true_instability_detected = gain_result.true_instability_detected
            gain_stability_score = gain_result.gain_stability_score
            gain_profile_divergence = gain_result.gain_profile_divergence
            gain_convergence_detected = gain_result.gain_convergence_detected
            diversity_pressure_applied = gain_result.diversity_pressure_applied
            suppression_cost_reduction = gain_result.suppression_cost_reduction
            cognitive_recovery_margin = gain_result.cognitive_recovery_margin
            phi_preservation_margin = gain_result.phi_preservation_margin
            # gain_vector_distance: distance from balanced preset
            preset_balanced = {
                "routing_gain": 1.0, "plasticity_gain": 1.0, "decay_gain": 1.0,
                "emergency_gain": 1.0, "cognitive_preservation_gain": 1.0, "global_brainstem_gain": 1.0,
            }
            current = {
                "routing_gain": routing_gain, "plasticity_gain": plasticity_gain, "decay_gain": decay_gain,
                "emergency_gain": emergency_gain, "cognitive_preservation_gain": cognitive_preservation_gain,
                "global_brainstem_gain": global_brainstem_gain,
            }
            keys = list(preset_balanced.keys())
            gain_vector_distance = round(sum(abs(current[k] - preset_balanced[k]) for k in keys) / len(keys), 4)

        # T42 — Cellular Adaptive Defense & Repair metrics
        mean_cellular_stress = 0.0
        max_cellular_stress = 0.0
        mean_damage_score = 0.0
        max_damage_score = 0.0
        repair_success_rate = 0.0
        repair_failure_rate = 0.0
        defense_activation_count = 0
        quarantined_cell_count = 0
        epigenetic_shift_count = 0
        cellular_resilience_score = 0.0
        cellular_survival_score = 0.0
        cellular_self_repair_score = 0.0
        cellular_defense_score = 0.0
        epigenetic_adaptation_score = 0.0
        orch = self.orch
        stress_result = getattr(orch, "_last_cellular_stress_result", None)
        damage_result = getattr(orch, "_last_cellular_damage_result", None)
        repair_result = getattr(orch, "_last_cellular_repair_result", None)
        defense_result = getattr(orch, "_last_cellular_defense_result", None)
        epigenetic_result = getattr(orch, "_last_cellular_epigenetic_result", None)
        if stress_result is not None:
            mean_cellular_stress = getattr(stress_result, "mean_stress", 0.0)
            max_cellular_stress = getattr(stress_result, "max_stress", 0.0)
        if damage_result is not None:
            mean_damage_score = getattr(damage_result, "mean_damage", 0.0)
            max_damage_score = getattr(damage_result, "max_damage", 0.0)
        if repair_result is not None:
            repair_success_rate = getattr(repair_result, "repair_success_rate", 0.0)
            repair_failure_rate = getattr(repair_result, "repair_failure_rate", 0.0)
        if defense_result is not None:
            defense_activation_count = getattr(defense_result, "defense_activation_count", 0)
            quarantined_cell_count = getattr(defense_result, "quarantined_count", 0)
        if epigenetic_result is not None:
            epigenetic_shift_count = getattr(epigenetic_result, "epigenetic_shift_count", 0)
            epigenetic_adaptation_score = getattr(epigenetic_result, "epigenetic_adaptation_score", 0.0)

        # T42B — Advanced cellular metrics
        all_neurons = orch.circuit.input_neurons + orch.circuit.hidden_neurons + orch.circuit.output_neurons
        neuron_count = len(all_neurons)
        if neuron_count > 0:
            # Survival: fraction of cells not critically damaged
            critical_cells = getattr(damage_result, "critical_count", 0) if damage_result else 0
            cellular_survival_score = round(1.0 - (critical_cells / neuron_count), 4)
            # Self-repair: repair success weighted by survival
            cellular_self_repair_score = round(repair_success_rate * cellular_survival_score, 4)
            # Defense: normalized defense activations per cell
            cellular_defense_score = round(min(1.0, defense_activation_count / neuron_count), 4)

        # Cellular resilience score: weighted composite
        cellular_resilience_score = round(
            0.30 * repair_success_rate
            + 0.25 * max(0.0, 1.0 - mean_damage_score)
            + 0.20 * max(0.0, 1.0 - mean_cellular_stress)
            + 0.15 * cellular_survival_score
            + 0.10 * epigenetic_adaptation_score,
            4,
        )

        # T43 — Semantic Cell Assembly Memory metrics
        semantic_assembly_count = 0
        semantic_active_assembly_count = 0
        semantic_consolidated_assembly_count = 0
        mean_assembly_strength = 0.0
        mean_assembly_stability = 0.0
        semantic_recall_success_rate = 0.0
        semantic_memory_density = 0.0
        semantic_memory_utility = 0.0
        semantic_consolidation_rate = 0.0
        semantic_memory_score = 0.0

        store = getattr(self.orch, "_semantic_memory_store", None)
        if store is not None:
            all_assemblies = list(store._assemblies.values())
            semantic_assembly_count = len(all_assemblies)
            active_asms = [a for a in all_assemblies if a.active]
            consolidated_asms = [a for a in all_assemblies if a.consolidated]
            semantic_active_assembly_count = len(active_asms)
            semantic_consolidated_assembly_count = len(consolidated_asms)
            if all_assemblies:
                mean_assembly_strength = sum(a.strength for a in all_assemblies) / len(all_assemblies)
                mean_assembly_stability = sum(a.stability for a in all_assemblies) / len(all_assemblies)
                semantic_memory_density = min(1.0, len(all_assemblies) / max(1, len(active_asms) * 2))
                semantic_memory_utility = sum(a.utility_score for a in all_assemblies) / len(all_assemblies)
                semantic_consolidation_rate = len(consolidated_asms) / len(all_assemblies)
            # recall success rate from metrics log
            if store._metrics_log:
                recalls = [getattr(m, "semantic_recall_success_rate", 0.0) for m in store._metrics_log]
                semantic_recall_success_rate = sum(recalls) / len(recalls)

            semantic_memory_score = round(
                0.25 * semantic_recall_success_rate
                + 0.20 * mean_assembly_stability
                + 0.15 * mean_assembly_strength
                + 0.15 * semantic_consolidation_rate
                + 0.10 * semantic_memory_utility
                + 0.10 * min(1.0, semantic_memory_density)
                + 0.05 * final.coherence_phi,
                4,
            )

        # T47 — Episodic Memory metrics
        episode_count = 0
        episode_event_count = 0
        recovery_episode_count = 0
        regression_episode_count = 0
        self_improvement_episode_count = 0
        semantic_learning_episode_count = 0
        episodic_recall_success_rate = 0.0
        recovery_pattern_count = 0
        regression_precursor_count = 0

        em = getattr(self.orch, "_episodic_memory", None)
        if em is not None:
            episodes = em.load_episodes()
            episode_count = len(episodes)
            episode_event_count = sum(len(ep.events) for ep in episodes)
            summarizer = EpisodeSummarizer()
            for ep in episodes:
                cls = summarizer.classify(ep)
                if cls == "RECOVERY_EPISODE":
                    recovery_episode_count += 1
                elif cls == "REGRESSION_EPISODE":
                    regression_episode_count += 1
                elif cls == "SELF_IMPROVEMENT_EPISODE":
                    self_improvement_episode_count += 1
                elif cls == "SEMANTIC_LEARNING_EPISODE":
                    semantic_learning_episode_count += 1
            recall_attempts = mem.count_events(MorphologyEventType.EPISODE_RECALLED)
            if recall_attempts > 0:
                pattern_detected = mem.count_events(MorphologyEventType.EPISODE_PATTERN_DETECTED)
                episodic_recall_success_rate = min(1.0, pattern_detected / recall_attempts)
            recall = getattr(self.orch, "_episodic_recall", None)
            if recall is not None:
                recovery_pattern_count = len(recall.find_recovery_patterns())
                regression_precursor_count = len(recall.find_regression_precursors())

        # T48 — Episodic-Guided Self-Improvement Policy metrics
        episodic_policy_enabled = getattr(self.orch, "episodic_policy_enabled", False)
        episodic_context_episode_count = 0
        episodic_recovery_context_count = 0
        episodic_regression_context_count = 0
        episodic_policy_bonus_mean = 0.0
        episodic_policy_penalty_mean = 0.0
        episodic_adjusted_confidence = 0.0
        episodic_policy_selected_proposal_score = 0.0
        if episodic_policy_enabled:
            context_events = [
                e for e in mem.events
                if e.event_type == MorphologyEventType.EPISODIC_POLICY_CONTEXT_BUILT
            ]
            episodic_context_episode_count = len(context_events)
            recovery_ctx = [
                e for e in context_events
                if e.metadata.get("recovery_episode_count", 0) > 0
            ]
            episodic_recovery_context_count = len(recovery_ctx)
            regression_ctx = [
                e for e in context_events
                if e.metadata.get("regression_episode_count", 0) > 0
            ]
            episodic_regression_context_count = len(regression_ctx)
            adj_events = [
                e for e in mem.events
                if e.event_type == MorphologyEventType.EPISODIC_POLICY_PROPOSAL_ADJUSTED
            ]
            if adj_events:
                bonuses = [e.metadata.get("bonus", 0.0) for e in adj_events]
                penalties = [e.metadata.get("penalty", 0.0) for e in adj_events]
                adjusted = [e.metadata.get("adjusted_confidence", 0.0) for e in adj_events]
                episodic_policy_bonus_mean = round(sum(bonuses) / len(bonuses), 4)
                episodic_policy_penalty_mean = round(sum(penalties) / len(penalties), 4)
                episodic_adjusted_confidence = round(max(adjusted), 4)
            sel_events = [
                e for e in mem.events
                if e.event_type == MorphologyEventType.EPISODIC_POLICY_PROPOSAL_SELECTED
            ]
            if sel_events:
                scores = [e.metadata.get("adjusted_confidence", 0.0) for e in sel_events]
                episodic_policy_selected_proposal_score = round(max(scores), 4)

        # T49 — Counterfactual Architecture Sandbox metrics
        counterfactual_scenarios_tested = 0
        counterfactual_accepted_count = 0
        counterfactual_rejected_count = 0
        counterfactual_unsafe_count = 0
        counterfactual_best_delta_score = 0.0
        counterfactual_mean_delta_score = 0.0
        counterfactual_best_confidence = 0.0
        counterfactual_policy_safe = False
        batch_events = [e for e in mem.events if e.event_type == MorphologyEventType.COUNTERFACTUAL_BATCH_COMPLETED]
        if batch_events:
            last_batch = batch_events[-1]
            counterfactual_scenarios_tested = last_batch.metadata.get("scenarios_tested", 0)
            counterfactual_accepted_count = last_batch.metadata.get("accepted_count", 0)
            counterfactual_rejected_count = last_batch.metadata.get("rejected_count", 0)
            counterfactual_unsafe_count = last_batch.metadata.get("unsafe_count", 0)
            counterfactual_best_delta_score = round(last_batch.metadata.get("best_delta_score", 0.0), 4)
        scenario_events = [e for e in mem.events if e.event_type == MorphologyEventType.COUNTERFACTUAL_SCENARIO_COMPLETED]
        if scenario_events:
            deltas = [e.metadata.get("delta_score", 0.0) for e in scenario_events]
            counterfactual_mean_delta_score = round(sum(deltas) / len(deltas), 4) if deltas else 0.0
            best_scenario = max(scenario_events, key=lambda e: e.metadata.get("delta_score", 0.0))
            counterfactual_best_confidence = round(best_scenario.metadata.get("confidence", 0.0), 4)
        accepted_events = [e for e in mem.events if e.event_type == MorphologyEventType.COUNTERFACTUAL_PROPOSAL_ACCEPTED]
        unsafe_events = [e for e in mem.events if e.event_type == MorphologyEventType.COUNTERFACTUAL_PROPOSAL_UNSAFE]
        counterfactual_policy_safe = len(unsafe_events) == 0 and len(accepted_events) > 0

        # T50 — Safe Architecture Patch Execution metrics
        architecture_patch_count = 0
        architecture_patch_applied_count = 0
        architecture_patch_confirmed_count = 0
        architecture_patch_rollback_count = 0
        architecture_patch_failure_count = 0
        architecture_patch_mean_delta_score = 0.0
        architecture_patch_last_delta_phi = 0.0
        architecture_patch_last_delta_energy = 0.0
        architecture_patch_safety_pass_rate = 0.0
        patch_events = [e for e in mem.events if e.event_type == MorphologyEventType.ARCHITECTURE_PATCH_APPLIED]
        architecture_patch_count = len(patch_events)
        architecture_patch_applied_count = architecture_patch_count
        confirmed_events = [e for e in mem.events if e.event_type == MorphologyEventType.ARCHITECTURE_PATCH_CONFIRMED]
        architecture_patch_confirmed_count = len(confirmed_events)
        rollback_events = [e for e in mem.events if e.event_type == MorphologyEventType.ARCHITECTURE_PATCH_ROLLED_BACK]
        architecture_patch_rollback_count = len(rollback_events)
        failed_events = [e for e in mem.events if e.event_type == MorphologyEventType.ARCHITECTURE_PATCH_FAILED]
        architecture_patch_failure_count = len(failed_events)
        if patch_events:
            last_patch = patch_events[-1]
            architecture_patch_last_delta_phi = round(last_patch.metadata.get("delta_phi", 0.0), 4)
            architecture_patch_last_delta_energy = round(last_patch.metadata.get("delta_energy", 0.0), 4)
        all_patch_results = confirmed_events + rollback_events + failed_events
        if all_patch_results:
            deltas = [e.metadata.get("delta_score", 0.0) for e in all_patch_results]
            architecture_patch_mean_delta_score = round(sum(deltas) / len(deltas), 4) if deltas else 0.0
            safe_count = len(confirmed_events)
            architecture_patch_safety_pass_rate = round(safe_count / len(all_patch_results), 4)

        # T51 — Patch Outcome Audit metrics (populated externally via audit)
        patch_audit_cycles_run = 0
        patch_audit_confirmed_count = 0
        patch_audit_rollback_count = 0
        patch_audit_rejected_count = 0
        patch_audit_unsafe_blocks = 0
        patch_audit_success_rate = 0.0
        patch_audit_regression_rate = 0.0
        patch_audit_cumulative_delta_score = 0.0
        patch_audit_cumulative_delta_phi = 0.0
        patch_audit_learning_confidence_delta = 0.0
        autonomous_improvement_readiness_score = 0.0

        return BenchmarkMetrics(
            accuracy_score=final.accuracy,
            coherence_phi=final.coherence_phi,
            phi_trend=phi_trend,
            mean_energy=final.mean_energy,
            energy_efficiency=energy_efficiency,
            neuron_count_delta=neuron_count_delta,
            synapse_count_delta=synapse_count_delta,
            neurogenesis_events=neurogenesis_events,
            apoptosis_events=apoptosis_events,
            cell_differentiation_events=cell_diff_events,
            adaptation_gain=adaptation_gain,
            morphological_stability=morphological_stability,
            morphological_adaptation=morphological_adaptation,
            structural_complexity=structural_complexity,
            functional_improvement=functional_improvement,
            speace_cognitive_score=speace_cognitive_score,
            community_count=community_count,
            modularity_proxy=modularity_proxy,
            isolated_neuron_count=isolated_neuron_count,
            weak_community_count=weak_community_count,
            overloaded_community_count=overloaded_community_count,
            confidence_score=confidence_score,
            uncertainty_score=uncertainty_score,
            output_entropy=output_entropy,
            decision_stability=decision_stability,
            error_risk=error_risk,
            recommended_action=recommended_action,
            meta_cognitive_score=meta_cognitive_score,
            region_count=region_count,
            connectome_density=connectome_density,
            mean_region_energy=mean_region_energy,
            mean_region_phi=mean_region_phi,
            mean_pathway_strength=mean_pathway_strength,
            reinforced_pathways=reinforced_pathways,
            weakened_pathways=weakened_pathways,
            inter_region_plasticity_events=inter_region_plasticity_events,
            pathway_energy_cost=pathway_energy_cost,
            regional_signal_flow_score=regional_signal_flow_score,
            routed_signals=routed_signals,
            delivered_signals=delivered_signals,
            blocked_signals=blocked_signals,
            total_routed_signal_strength=total_routed_signal_strength,
            mean_routed_signal_strength=mean_routed_signal_strength,
            routing_energy_cost=routing_energy_cost,
            active_inter_region_pathways=active_inter_region_pathways,
            pathway_tuning_accepted_updates=pathway_tuning_accepted_updates,
            pathway_tuning_skipped_updates=pathway_tuning_skipped_updates,
            pathway_tuning_rolled_back_updates=pathway_tuning_rolled_back_updates,
            pathway_tuning_profile_id=pathway_tuning_profile_id,
            mean_pathway_utility=mean_pathway_utility,
            best_pathway_utility=best_pathway_utility,
            worst_pathway_utility=worst_pathway_utility,
            rewarded_pathways=rewarded_pathways,
            penalized_pathways=penalized_pathways,
            pathway_reward_mean=pathway_reward_mean,
            pathway_cost_mean=pathway_cost_mean,
            utility_gated_updates=utility_gated_updates,
            utility_skipped_updates=utility_skipped_updates,
            deep_region_count=deep_region_count,
            limbic_salience_score=limbic_salience_score,
            cerebellar_error_correction_score=cerebellar_error_correction_score,
            default_mode_consolidation_score=default_mode_consolidation_score,
            brainstem_homeostatic_stability_score=brainstem_homeostatic_stability_score,
            deep_region_signal_flow=deep_region_signal_flow,
            region_specialization_diversity=region_specialization_diversity,
            region_role_alignment_score=region_role_alignment_score,
            region_instability_mean=region_instability_mean,
            unstable_region_count=unstable_region_count,
            stability_actions_applied=stability_actions_applied,
            routing_blocks_applied=routing_blocks_applied,
            cooldowns_started=cooldowns_started,
            mean_region_damping_factor=mean_region_damping_factor,
            brainstem_override_count=brainstem_override_count,
            phi_recovery_score=phi_recovery_score,
            stability_controller_active=stability_controller_active,
            top_k_routing_active=top_k_routing_active,
            mean_deep_region_activation=mean_deep_region_activation,
            deep_region_routing_efficiency=deep_region_routing_efficiency,
            regional_gain_applied=regional_gain_applied,
            flow_memory_enabled=flow_memory_enabled,
            stability_aware_routing_active=stability_aware_routing_active,
            deep_region_targeted_signals=deep_region_targeted_signals,
            mean_regional_signal_gain=mean_regional_signal_gain,
            deep_region_phi_recovery=deep_region_phi_recovery,
            # T35
            brainstem_state=brainstem_state,
            brainstem_decisions_count=brainstem_decisions_count,
            brainstem_energy_modulation=brainstem_energy_modulation,
            brainstem_routing_modulation=brainstem_routing_modulation,
            brainstem_plasticity_modulation=brainstem_plasticity_modulation,
            brainstem_decay_modulation=brainstem_decay_modulation,
            brainstem_recovery_actions=brainstem_recovery_actions,
            brainstem_emergency_count=brainstem_emergency_count,
            brainstem_homeostatic_gain=brainstem_homeostatic_gain,
            brainstem_phi_recovery_contribution=brainstem_phi_recovery_contribution,
            # T36
            cognitive_vitality_score=cognitive_vitality_score,
            autonomic_risk_score=autonomic_risk_score,
            balance_pressure=balance_pressure,
            brainstem_state_distribution=brainstem_state_distribution,
            emergency_ticks=emergency_ticks,
            protective_ticks=protective_ticks,
            watchful_ticks=watchful_ticks,
            corrective_ticks=corrective_ticks,
            cognitive_preservation_score=cognitive_preservation_score,
            autonomic_balance_score=autonomic_balance_score,
            suppression_cost=suppression_cost,
            useful_activity_preserved=useful_activity_preserved,
            # T37
            brainstem_gain_reward=brainstem_gain_reward,
            global_brainstem_gain=global_brainstem_gain,
            routing_gain=routing_gain,
            plasticity_gain=plasticity_gain,
            decay_gain=decay_gain,
            energy_recovery_gain=energy_recovery_gain,
            emergency_gain=emergency_gain,
            cognitive_preservation_gain=cognitive_preservation_gain,
            gain_adjustments_count=gain_adjustments_count,
            over_suppression_detected=over_suppression_detected,
            useful_stabilization_detected=useful_stabilization_detected,
            true_instability_detected=true_instability_detected,
            gain_stability_score=gain_stability_score,
            # T38
            brainstem_gain_reward_v2=brainstem_gain_reward_v2,
            adaptive_gain_learning_rate=adaptive_gain_learning_rate,
            gain_profile_divergence=gain_profile_divergence,
            gain_convergence_detected=gain_convergence_detected,
            diversity_pressure_applied=diversity_pressure_applied,
            suppression_cost_reduction=suppression_cost_reduction,
            cognitive_recovery_margin=cognitive_recovery_margin,
            phi_preservation_margin=phi_preservation_margin,
            net_gain_vs_t36=0.0,
            net_gain_vs_t34b=0.0,
            gain_vector_distance=gain_vector_distance,
            # T39
            gain_input_coupling_strength=gain_input_coupling_strength,
            adjusted_cognitive_vitality_score=adjusted_cognitive_vitality_score,
            adjusted_autonomic_risk_score=adjusted_autonomic_risk_score,
            adjusted_balance_pressure=adjusted_balance_pressure,
            protective_escape_count=protective_escape_count,
            protective_state_ratio=protective_state_ratio,
            corrective_state_ratio=corrective_state_ratio,
            emergency_state_ratio=emergency_state_ratio,
            coupling_delta_mean=coupling_delta_mean,
            suppression_cost_after_coupling=suppression_cost_after_coupling,
            brainstem_state_transition_count=brainstem_state_transition_count,
            # T42
            mean_cellular_stress=mean_cellular_stress,
            max_cellular_stress=max_cellular_stress,
            mean_damage_score=mean_damage_score,
            max_damage_score=max_damage_score,
            repair_success_rate=repair_success_rate,
            repair_failure_rate=repair_failure_rate,
            defense_activation_count=defense_activation_count,
            quarantined_cell_count=quarantined_cell_count,
            epigenetic_shift_count=epigenetic_shift_count,
            cellular_resilience_score=cellular_resilience_score,
            cellular_survival_score=cellular_survival_score,
            cellular_self_repair_score=cellular_self_repair_score,
            cellular_defense_score=cellular_defense_score,
            epigenetic_adaptation_score=epigenetic_adaptation_score,
            # T43
            semantic_assembly_count=semantic_assembly_count,
            semantic_active_assembly_count=semantic_active_assembly_count,
            semantic_consolidated_assembly_count=semantic_consolidated_assembly_count,
            mean_assembly_strength=mean_assembly_strength,
            mean_assembly_stability=mean_assembly_stability,
            semantic_recall_success_rate=semantic_recall_success_rate,
            semantic_memory_density=semantic_memory_density,
            semantic_memory_utility=semantic_memory_utility,
            semantic_consolidation_rate=semantic_consolidation_rate,
            semantic_memory_score=semantic_memory_score,
            # T47
            episode_count=episode_count,
            episode_event_count=episode_event_count,
            recovery_episode_count=recovery_episode_count,
            regression_episode_count=regression_episode_count,
            self_improvement_episode_count=self_improvement_episode_count,
            semantic_learning_episode_count=semantic_learning_episode_count,
            episodic_recall_success_rate=episodic_recall_success_rate,
            recovery_pattern_count=recovery_pattern_count,
            regression_precursor_count=regression_precursor_count,
            # T48
            episodic_policy_enabled=episodic_policy_enabled,
            episodic_context_episode_count=episodic_context_episode_count,
            episodic_recovery_context_count=episodic_recovery_context_count,
            episodic_regression_context_count=episodic_regression_context_count,
            episodic_policy_bonus_mean=episodic_policy_bonus_mean,
            episodic_policy_penalty_mean=episodic_policy_penalty_mean,
            episodic_adjusted_confidence=episodic_adjusted_confidence,
            episodic_policy_selected_proposal_score=episodic_policy_selected_proposal_score,
            # T49
            counterfactual_scenarios_tested=counterfactual_scenarios_tested,
            counterfactual_accepted_count=counterfactual_accepted_count,
            counterfactual_rejected_count=counterfactual_rejected_count,
            counterfactual_unsafe_count=counterfactual_unsafe_count,
            counterfactual_best_delta_score=counterfactual_best_delta_score,
            counterfactual_mean_delta_score=counterfactual_mean_delta_score,
            counterfactual_best_confidence=counterfactual_best_confidence,
            counterfactual_policy_safe=counterfactual_policy_safe,
            # T50
            architecture_patch_count=architecture_patch_count,
            architecture_patch_applied_count=architecture_patch_applied_count,
            architecture_patch_confirmed_count=architecture_patch_confirmed_count,
            architecture_patch_rollback_count=architecture_patch_rollback_count,
            architecture_patch_failure_count=architecture_patch_failure_count,
            architecture_patch_mean_delta_score=architecture_patch_mean_delta_score,
            architecture_patch_last_delta_phi=architecture_patch_last_delta_phi,
            architecture_patch_last_delta_energy=architecture_patch_last_delta_energy,
            architecture_patch_safety_pass_rate=architecture_patch_safety_pass_rate,
            # T51
            patch_audit_cycles_run=patch_audit_cycles_run,
            patch_audit_confirmed_count=patch_audit_confirmed_count,
            patch_audit_rollback_count=patch_audit_rollback_count,
            patch_audit_rejected_count=patch_audit_rejected_count,
            patch_audit_unsafe_blocks=patch_audit_unsafe_blocks,
            patch_audit_success_rate=patch_audit_success_rate,
            patch_audit_regression_rate=patch_audit_regression_rate,
            patch_audit_cumulative_delta_score=patch_audit_cumulative_delta_score,
            patch_audit_cumulative_delta_phi=patch_audit_cumulative_delta_phi,
            patch_audit_learning_confidence_delta=patch_audit_learning_confidence_delta,
            autonomous_improvement_readiness_score=autonomous_improvement_readiness_score,
        )

    def generate_json_report(self, result: BenchmarkResult) -> Path:
        """Save a machine-readable JSON report and update latest links."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_{timestamp}.json"
        path = self.reports_dir / filename
        path.write_text(result.model_dump_json(indent=2), encoding="utf-8")

        latest = self.reports_dir / "latest_report.json"
        latest.write_text(result.model_dump_json(indent=2), encoding="utf-8")

        result.json_report_path = str(path)
        return path

    def generate_markdown_report(self, result: BenchmarkResult) -> Path:
        """Save a human-readable Markdown report and update latest links."""
        m = result.metrics
        lines = [
            "# SPEACE NeuroFunctional Benchmark Report",
            f"**Case:** {result.case_name}",
            f"**Date:** {datetime.now().isoformat()}",
            "",
            "## Baseline State",
            f"- Neurons: {result.baseline_state.neuron_count}",
            f"- Synapses: {result.baseline_state.synapse_count}",
            f"- Active synapses: {result.baseline_state.active_synapse_count}",
            f"- Coherence Φ: {result.baseline_state.coherence_phi:.4f}",
            f"- Mean energy: {result.baseline_state.mean_energy:.4f}",
            f"- Accuracy: {result.baseline_state.accuracy:.4f}",
            "",
            "## Final State",
            f"- Neurons: {result.final_state.neuron_count}",
            f"- Synapses: {result.final_state.synapse_count}",
            f"- Active synapses: {result.final_state.active_synapse_count}",
            f"- Coherence Φ: {result.final_state.coherence_phi:.4f}",
            f"- Mean energy: {result.final_state.mean_energy:.4f}",
            f"- Accuracy: {result.final_state.accuracy:.4f}",
            "",
            "## Metrics",
            f"| Metric | Value |",
            f"|---|---|",
            f"| Accuracy score | {m.accuracy_score:.4f} |",
            f"| Coherence Φ | {m.coherence_phi:.4f} |",
            f"| Φ trend | {m.phi_trend:.4f} |",
            f"| Mean energy | {m.mean_energy:.4f} |",
            f"| Energy efficiency | {m.energy_efficiency:.4f} |",
            f"| Neuron count delta | {m.neuron_count_delta} |",
            f"| Synapse count delta | {m.synapse_count_delta} |",
            f"| Neurogenesis events | {m.neurogenesis_events} |",
            f"| Apoptosis events | {m.apoptosis_events} |",
            f"| Differentiation events | {m.cell_differentiation_events} |",
            f"| Adaptation gain | {m.adaptation_gain:.4f} |",
            f"| Morphological stability | {m.morphological_stability:.4f} |",
            f"| Morphological adaptation | {m.morphological_adaptation:.4f} |",
            f"| Structural complexity | {m.structural_complexity:.4f} |",
            f"| Functional improvement | {m.functional_improvement:.4f} |",
            f"| Community count | {m.community_count} |",
            f"| Modularity proxy | {m.modularity_proxy:.4f} |",
            f"| Isolated neurons | {m.isolated_neuron_count} |",
            f"| Weak communities | {m.weak_community_count} |",
            f"| Overloaded communities | {m.overloaded_community_count} |",
            f"| Confidence score | {m.confidence_score:.4f} |",
            f"| Uncertainty score | {m.uncertainty_score:.4f} |",
            f"| Output entropy | {m.output_entropy:.4f} |",
            f"| Decision stability | {m.decision_stability:.4f} |",
            f"| Error risk | {m.error_risk:.4f} |",
            f"| Recommended action | {m.recommended_action} |",
            f"| **Meta-Cognitive Score** | **{m.meta_cognitive_score:.4f}** |",
            f"| **SPEACE Cognitive Score** | **{m.speace_cognitive_score:.4f}** |",
            f"| Region count | {m.region_count} |",
            f"| Connectome density | {m.connectome_density:.4f} |",
            f"| Mean region energy | {m.mean_region_energy:.4f} |",
            f"| Mean region phi | {m.mean_region_phi:.4f} |",
            f"| Mean pathway strength | {m.mean_pathway_strength:.4f} |",
            f"| Reinforced pathways | {m.reinforced_pathways} |",
            f"| Weakened pathways | {m.weakened_pathways} |",
            f"| Inter-region plasticity events | {m.inter_region_plasticity_events} |",
            f"| Pathway energy cost | {m.pathway_energy_cost:.4f} |",
            f"| Regional signal flow score | {m.regional_signal_flow_score:.4f} |",
            f"| Routed signals | {m.routed_signals} |",
            f"| Delivered signals | {m.delivered_signals} |",
            f"| Blocked signals | {m.blocked_signals} |",
            f"| Total routed signal strength | {m.total_routed_signal_strength:.4f} |",
            f"| Mean routed signal strength | {m.mean_routed_signal_strength:.4f} |",
            f"| Routing energy cost | {m.routing_energy_cost:.4f} |",
            f"| Active inter-region pathways | {m.active_inter_region_pathways} |",
            f"| Tuning profile | {m.pathway_tuning_profile_id or 'none'} |",
            f"| Tuning accepted updates | {m.pathway_tuning_accepted_updates} |",
            f"| Tuning skipped updates | {m.pathway_tuning_skipped_updates} |",
            f"| Tuning rolled-back updates | {m.pathway_tuning_rolled_back_updates} |",
            f"| Mean pathway utility | {m.mean_pathway_utility:.4f} |",
            f"| Best pathway utility | {m.best_pathway_utility:.4f} |",
            f"| Worst pathway utility | {m.worst_pathway_utility:.4f} |",
            f"| Rewarded pathways | {m.rewarded_pathways} |",
            f"| Penalized pathways | {m.penalized_pathways} |",
            f"| Pathway reward mean | {m.pathway_reward_mean:.4f} |",
            f"| Pathway cost mean | {m.pathway_cost_mean:.4f} |",
            f"| Utility gated updates | {m.utility_gated_updates} |",
            f"| Utility skipped updates | {m.utility_skipped_updates} |",
            f"| Deep region count | {m.deep_region_count} |",
            f"| Limbic salience score | {m.limbic_salience_score:.4f} |",
            f"| Cerebellar error correction | {m.cerebellar_error_correction_score:.4f} |",
            f"| Default mode consolidation | {m.default_mode_consolidation_score:.4f} |",
            f"| Brainstem homeostatic stability | {m.brainstem_homeostatic_stability_score:.4f} |",
            f"| Deep region signal flow | {m.deep_region_signal_flow:.4f} |",
            f"| Region specialization diversity | {m.region_specialization_diversity:.4f} |",
            f"| Region role alignment | {m.region_role_alignment_score:.4f} |",
            f"| Stability controller active | {m.stability_controller_active} |",
            f"| Region instability mean | {m.region_instability_mean:.4f} |",
            f"| Unstable region count | {m.unstable_region_count} |",
            f"| Stability actions applied | {m.stability_actions_applied} |",
            f"| Routing blocks applied | {m.routing_blocks_applied} |",
            f"| Cooldowns started | {m.cooldowns_started} |",
            f"| Mean region damping factor | {m.mean_region_damping_factor:.4f} |",
            f"| Brainstem override count | {m.brainstem_override_count} |",
            f"| Phi recovery score | {m.phi_recovery_score:.4f} |",
            f"| Mean cellular stress | {m.mean_cellular_stress:.4f} |",
            f"| Max cellular stress | {m.max_cellular_stress:.4f} |",
            f"| Mean damage score | {m.mean_damage_score:.4f} |",
            f"| Max damage score | {m.max_damage_score:.4f} |",
            f"| Repair success rate | {m.repair_success_rate:.4f} |",
            f"| Defense activation count | {m.defense_activation_count} |",
            f"| Quarantined cell count | {m.quarantined_cell_count} |",
            f"| Epigenetic shift count | {m.epigenetic_shift_count} |",
            f"| Repair failure rate | {m.repair_failure_rate:.4f} |",
            f"| Cellular survival score | {m.cellular_survival_score:.4f} |",
            f"| Cellular self-repair score | {m.cellular_self_repair_score:.4f} |",
            f"| Cellular defense score | {m.cellular_defense_score:.4f} |",
            f"| Epigenetic adaptation score | {m.epigenetic_adaptation_score:.4f} |",
            "",
            "### T43 — Semantic Cell Assembly Memory",
            f"| Semantic assembly count | {m.semantic_assembly_count} |",
            f"| Semantic active assemblies | {m.semantic_active_assembly_count} |",
            f"| Semantic consolidated assemblies | {m.semantic_consolidated_assembly_count} |",
            f"| Mean assembly strength | {m.mean_assembly_strength:.4f} |",
            f"| Mean assembly stability | {m.mean_assembly_stability:.4f} |",
            f"| Semantic recall success rate | {m.semantic_recall_success_rate:.4f} |",
            f"| Semantic memory density | {m.semantic_memory_density:.4f} |",
            f"| Semantic memory utility | {m.semantic_memory_utility:.4f} |",
            f"| Semantic consolidation rate | {m.semantic_consolidation_rate:.4f} |",
            f"| **Semantic memory score** | **{m.semantic_memory_score:.4f}** |",
            "",
            "### T47 — Episodic Memory & Temporal Experience",
            f"| Episode count | {m.episode_count} |",
            f"| Episode event count | {m.episode_event_count} |",
            f"| Recovery episodes | {m.recovery_episode_count} |",
            f"| Regression episodes | {m.regression_episode_count} |",
            f"| Self-improvement episodes | {m.self_improvement_episode_count} |",
            f"| Semantic learning episodes | {m.semantic_learning_episode_count} |",
            f"| Episodic recall success rate | {m.episodic_recall_success_rate:.4f} |",
            f"| Recovery patterns | {m.recovery_pattern_count} |",
            f"| Regression precursors | {m.regression_precursor_count} |",
            "",
            "### T48 — Episodic-Guided Self-Improvement Policy",
            f"| Episodic policy enabled | {m.episodic_policy_enabled} |",
            f"| Context episode count | {m.episodic_context_episode_count} |",
            f"| Recovery context count | {m.episodic_recovery_context_count} |",
            f"| Regression context count | {m.episodic_regression_context_count} |",
            f"| Policy bonus mean | {m.episodic_policy_bonus_mean:.4f} |",
            f"| Policy penalty mean | {m.episodic_policy_penalty_mean:.4f} |",
            f"| Adjusted confidence | {m.episodic_adjusted_confidence:.4f} |",
            f"| Selected proposal score | {m.episodic_policy_selected_proposal_score:.4f} |",
            "",
            "### T49 — Counterfactual Architecture Sandbox",
            f"| Scenarios tested | {m.counterfactual_scenarios_tested} |",
            f"| Accepted count | {m.counterfactual_accepted_count} |",
            f"| Rejected count | {m.counterfactual_rejected_count} |",
            f"| Unsafe count | {m.counterfactual_unsafe_count} |",
            f"| Best delta score | {m.counterfactual_best_delta_score:.4f} |",
            f"| Mean delta score | {m.counterfactual_mean_delta_score:.4f} |",
            f"| Best confidence | {m.counterfactual_best_confidence:.4f} |",
            f"| Policy safe | {m.counterfactual_policy_safe} |",
            "",
            "### T50 — Safe Architecture Patch Execution",
            f"| Patches proposed | {m.architecture_patch_count} |",
            f"| Patches applied | {m.architecture_patch_applied_count} |",
            f"| Patches confirmed | {m.architecture_patch_confirmed_count} |",
            f"| Patches rolled back | {m.architecture_patch_rollback_count} |",
            f"| Patch failures | {m.architecture_patch_failure_count} |",
            f"| Mean delta score | {m.architecture_patch_mean_delta_score:.4f} |",
            f"| Last delta Φ | {m.architecture_patch_last_delta_phi:.4f} |",
            f"| Last delta energy | {m.architecture_patch_last_delta_energy:.4f} |",
            f"| Safety pass rate | {m.architecture_patch_safety_pass_rate:.4f} |",
            "",
            "### T51 — Patch Outcome Audit",
            f"| Audit cycles run | {m.patch_audit_cycles_run} |",
            f"| Patches confirmed | {m.patch_audit_confirmed_count} |",
            f"| Patches rolled back | {m.patch_audit_rollback_count} |",
            f"| Patches rejected | {m.patch_audit_rejected_count} |",
            f"| Unsafe blocks | {m.patch_audit_unsafe_blocks} |",
            f"| Success rate | {m.patch_audit_success_rate:.4f} |",
            f"| Regression rate | {m.patch_audit_regression_rate:.4f} |",
            f"| Cumulative delta score | {m.patch_audit_cumulative_delta_score:.4f} |",
            f"| Cumulative delta Φ | {m.patch_audit_cumulative_delta_phi:.4f} |",
            f"| Learning confidence delta | {m.patch_audit_learning_confidence_delta:.4f} |",
            f"| Readiness score | {m.autonomous_improvement_readiness_score:.4f} |",
            "",
            f"| **Cellular resilience score** | **{m.cellular_resilience_score:.4f}** |",



            "",
            "---",
            "*Generated by NeuroFunctionalBenchmark v0.3*",
        ]
        md = "\n".join(lines)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_{timestamp}.md"
        path = self.reports_dir / filename
        path.write_text(md, encoding="utf-8")

        latest = self.reports_dir / "latest_report.md"
        latest.write_text(md, encoding="utf-8")

        result.markdown_report_path = str(path)
        return path

    @staticmethod
    def _default_pattern(length: int = 10) -> List[float]:
        return [1.0 if i % 2 == 0 else 0.0 for i in range(length)]
