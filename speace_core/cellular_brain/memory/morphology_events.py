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
