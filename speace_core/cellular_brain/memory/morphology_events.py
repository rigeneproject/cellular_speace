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
