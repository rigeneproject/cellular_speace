from enum import Enum
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class MorphologyEventType(str, Enum):
    SYNAPSE_REINFORCED = "synapse_reinforced"
    SYNAPSE_WEAKENED = "synapse_weakened"
    SYNAPSE_PRUNED = "synapse_pruned"
    PATHWAY_MYELINATED = "pathway_myelinated"
    PHI_CHANGED = "phi_changed"
    ENERGY_CHANGED = "energy_changed"
    ASTROCYTE_REGULATION = "astrocyte_regulation"
    MICROGLIA_PRUNING = "microglia_pruning"
    NEURON_CREATED = "neuron_created"
    NEURON_APOPTOSIS = "neuron_apoptosis"
    NEURON_SNOOZED = "neuron_snoozed"
    CELL_DIFFERENTIATED = "cell_differentiated"
    COMMUNITY_DETECTED = "community_detected"
    GENOME_SAVED = "genome_saved"
    GENOME_MUTATED = "genome_mutated"
    GENOME_CROSSED = "genome_crossed"
    GENOME_SELECTED = "genome_selected"
    EVOLUTION_STEP_COMPLETED = "evolution_step_completed"
    CONFIDENCE_EVALUATED = "confidence_evaluated"
    REGION_PATHWAY_REINFORCED = "region_pathway_reinforced"
    REGION_PATHWAY_WEAKENED = "region_pathway_weakened"
    REGION_PATHWAY_STABILIZED = "region_pathway_stabilized"
    INTER_REGION_PLASTICITY_APPLIED = "inter_region_plasticity_applied"
    REGION_SIGNAL_ROUTED = "region_signal_routed"
    REGION_SIGNAL_BLOCKED = "region_signal_blocked"
    REGION_SIGNAL_DELIVERED = "region_signal_delivered"
    REGIONAL_SIGNAL_FLOW_UPDATED = "regional_signal_flow_updated"
    REGION_PLASTICITY_TRIGGERED = "region_plasticity_triggered"
    REGION_PLASTICITY_TRIGGER_SKIPPED = "region_plasticity_trigger_skipped"
    REGION_CAUSAL_CORRELATION_DETECTED = "region_causal_correlation_detected"
    REGION_SOFT_ACTIVATION_TRACE = "region_soft_activation_trace"
    # T29 — Pathway Plasticity Sensitivity Tuning
    REGION_PLASTICITY_UPDATE_ACCEPTED = "region_plasticity_update_accepted"
    REGION_PLASTICITY_UPDATE_SKIPPED = "region_plasticity_update_skipped"
    REGION_PLASTICITY_UPDATE_ROLLED_BACK = "region_plasticity_update_rolled_back"
    REGION_PATHWAY_UTILITY_UPDATED = "region_pathway_utility_updated"
    PATHWAY_TUNING_PROFILE_APPLIED = "pathway_tuning_profile_applied"
    # T30 — Pathway Utility Learning
    PATHWAY_REWARD_COMPUTED = "pathway_reward_computed"
    PATHWAY_UTILITY_UPDATED = "pathway_utility_updated"
    PATHWAY_UTILITY_POSITIVE = "pathway_utility_positive"
    PATHWAY_UTILITY_NEGATIVE = "pathway_utility_negative"
    PATHWAY_UTILITY_GATE_APPLIED = "pathway_utility_gate_applied"
    # T31 — Deep Region Specialization
    DEEP_REGION_SPECIALIZATION_APPLIED = "deep_region_specialization_applied"
    DEEP_REGION_PATHWAY_CREATED = "deep_region_pathway_created"
    DEEP_REGION_METRICS_COMPUTED = "deep_region_metrics_computed"
    # T33 — Region-Level Stability Controller
    REGION_STABILITY_CHECKED = "region_stability_checked"
    REGION_INSTABILITY_DETECTED = "region_instability_detected"
    REGION_DAMPING_APPLIED = "region_damping_applied"
    REGION_ROUTING_BLOCKED = "region_routing_blocked"
    REGION_COOLDOWN_STARTED = "region_cooldown_started"
    BRAINSTEM_STABILITY_OVERRIDE = "brainstem_stability_override"
    REGION_STABILITY_RECOVERED = "region_stability_recovered"
    # T34 — Deep Region Routing Calibration
    DEEP_REGION_ROUTING_CALIBRATED = "deep_region_routing_calibrated"
    TOP_K_ROUTING_APPLIED = "top_k_routing_applied"
    REGIONAL_GAIN_APPLIED = "regional_gain_applied"
    DEEP_REGION_SIGNAL_BOOSTED = "deep_region_signal_boosted"
    FLOW_MEMORY_RECORDED = "flow_memory_recorded"
    STABILITY_AWARE_ROUTING_CORRECTED = "stability_aware_routing_corrected"
    # T34B-FIX — Activation explosion detection
    REGION_ACTIVATION_EXPLOSION_DETECTED = "region_activation_explosion_detected"
    REGION_ACTIVATION_CLAMPED = "region_activation_clamped"
    # T35 — Brainstem Functional Integration
    BRAINSTEM_STATE_CHANGED = "brainstem_state_changed"
    BRAINSTEM_MODULATION_APPLIED = "brainstem_modulation_applied"
    BRAINSTEM_EMERGENCY_TRIGGERED = "brainstem_emergency_triggered"
    BRAINSTEM_RECOVERY_APPLIED = "brainstem_recovery_applied"
    BRAINSTEM_ROUTING_SUPPRESSED = "brainstem_routing_suppressed"
    BRAINSTEM_PLASTICITY_SUPPRESSED = "brainstem_plasticity_suppressed"
    BRAINSTEM_ENERGY_RECOVERY_BOOSTED = "brainstem_energy_recovery_boosted"
    # T36 — Cognitive/Autonomic Balance Tuning
    BRAINSTEM_BALANCE_EVALUATED = "brainstem_balance_evaluated"
    BRAINSTEM_COGNITIVE_ACTIVITY_PRESERVED = "brainstem_cognitive_activity_preserved"
    BRAINSTEM_EMERGENCY_HYSTERESIS_APPLIED = "brainstem_emergency_hysteresis_applied"
    BRAINSTEM_SUPPRESSION_SOFTENED = "brainstem_suppression_softened"
    BRAINSTEM_STATE_EXITED_EMERGENCY = "brainstem_state_exited_emergency"
    # T37 — Adaptive Brainstem Gain Controller
    BRAINSTEM_GAIN_EVALUATED = "brainstem_gain_evaluated"
    BRAINSTEM_GAIN_ADJUSTED = "brainstem_gain_adjusted"
    BRAINSTEM_OVER_SUPPRESSION_DETECTED = "brainstem_over_suppression_detected"
    BRAINSTEM_USEFUL_STABILIZATION_DETECTED = "brainstem_useful_stabilization_detected"
    BRAINSTEM_TRUE_INSTABILITY_DETECTED = "brainstem_true_instability_detected"
    BRAINSTEM_COGNITIVE_GAIN_BOOSTED = "brainstem_cognitive_gain_boosted"
    BRAINSTEM_EMERGENCY_GAIN_REDUCED = "brainstem_emergency_gain_reduced"
    # T38 — Gain Sensitivity Tuning
    BRAINSTEM_GAIN_REWARD_V2_COMPUTED = "brainstem_gain_reward_v2_computed"
    BRAINSTEM_GAIN_LR_ADAPTED = "brainstem_gain_lr_adapted"
    BRAINSTEM_GAIN_DIVERSITY_PRESSURE_APPLIED = "brainstem_gain_diversity_pressure_applied"
    BRAINSTEM_GAIN_CONVERGENCE_DETECTED = "brainstem_gain_convergence_detected"
    BRAINSTEM_SUPPRESSION_COST_REDUCED = "brainstem_suppression_cost_reduced"
    BRAINSTEM_COGNITIVE_RECOVERY_IMPROVED = "brainstem_cognitive_recovery_improved"
    # T39 — Gain Input Coupling Redesign
    BRAINSTEM_GAIN_INPUT_COUPLED = "brainstem_gain_input_coupled"
    BRAINSTEM_STATE_THRESHOLD_ADJUSTED = "brainstem_state_threshold_adjusted"
    BRAINSTEM_PROTECTIVE_ESCAPE = "brainstem_protective_escape"
    BRAINSTEM_OUTPUT_COUPLED = "brainstem_output_coupled"
    BRAINSTEM_COUPLING_TRACE_RECORDED = "brainstem_coupling_trace_recorded"
    BRAINSTEM_SUPPRESSION_RELEASED = "brainstem_suppression_released"
    # T42 — Cellular Adaptive Defense & Repair
    CELLULAR_STRESS_EVALUATED = "cellular_stress_evaluated"
    CELLULAR_DAMAGE_EVALUATED = "cellular_damage_evaluated"
    CELLULAR_REPAIR_ATTEMPTED = "cellular_repair_attempted"
    CELLULAR_REPAIR_SUCCEEDED = "cellular_repair_succeeded"
    CELLULAR_REPAIR_FAILED = "cellular_repair_failed"
    CELLULAR_DEFENSE_APPLIED = "cellular_defense_applied"
    CELL_QUARANTINED = "cell_quarantined"
    CELL_QUARANTINE_RELEASED = "cell_quarantine_released"
    CELLULAR_IMMUNE_ALERT = "cellular_immune_alert"
    CELLULAR_EPIGENETIC_SHIFT = "cellular_epigenetic_shift"
    # T43 — Semantic Cell Assembly Memory
    CELL_ASSEMBLY_CREATED = "cell_assembly_created"
    CELL_ASSEMBLY_REINFORCED = "cell_assembly_reinforced"
    CELL_ASSEMBLY_CONSOLIDATED = "cell_assembly_consolidated"
    CELL_ASSEMBLY_DECAYED = "cell_assembly_decayed"
    CELL_ASSEMBLY_REACTIVATED = "cell_assembly_reactivated"
    SEMANTIC_RECALL_SUCCEEDED = "semantic_recall_succeeded"
    SEMANTIC_RECALL_FAILED = "semantic_recall_failed"
    # T45 — Autonomous Limitation Detection & Architecture Rewriting Loop
    LIMITATION_DETECTED = "limitation_detected"
    LIMITATION_DIAGNOSED = "limitation_diagnosed"
    ARCHITECTURE_PROPOSAL_CREATED = "architecture_proposal_created"
    ARCHITECTURE_PROPOSAL_SIMULATED = "architecture_proposal_simulated"
    ARCHITECTURE_PROPOSAL_ACCEPTED = "architecture_proposal_accepted"
    ARCHITECTURE_PROPOSAL_REJECTED = "architecture_proposal_rejected"
    SELF_IMPROVEMENT_CYCLE_COMPLETED = "self_improvement_cycle_completed"


class MorphologyEvent(BaseModel):
    event_id: str
    event_type: MorphologyEventType
    timestamp: float = 0.0
    source_id: Optional[str] = None
    target_id: Optional[str] = None
    region_id: Optional[str] = None
    phi_before: Optional[float] = None
    phi_after: Optional[float] = None
    energy_before: Optional[float] = None
    energy_after: Optional[float] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
