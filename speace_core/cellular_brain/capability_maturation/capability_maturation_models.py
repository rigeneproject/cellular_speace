from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class CapabilityMaturityState(str, Enum):
    UNOBSERVED = "unobserved"
    EMERGING = "emerging"
    IMMATURE = "immature"
    MATURING = "maturing"
    MATURE_SANDBOXED = "mature_sandboxed"
    REGRESSIVE = "regressive"
    SAFETY_BLOCKED = "safety_blocked"
    QUARANTINED = "quarantined"
    DEPRECATED = "deprecated"


class CapabilityRiskClass(str, Enum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


class CapabilityRecord(BaseModel):
    capability_id: str
    name: str = ""
    description: str = ""
    maturity_state: CapabilityMaturityState = CapabilityMaturityState.UNOBSERVED
    risk_class: CapabilityRiskClass = CapabilityRiskClass.UNKNOWN
    evidence_count: int = 0
    success_rate: float = 0.0
    regression_rate: float = 0.0
    safety_violation_count: int = 0
    human_review_required_count: int = 0
    sandbox_only: bool = True
    real_world_enabled: bool = False
    confidence_score: float = 0.0
    maturity_score: float = 0.0
    last_updated_at: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CapabilityMaturationResult(BaseModel):
    capability_count: int = 0
    mature_sandboxed_count: int = 0
    immature_count: int = 0
    regressive_count: int = 0
    safety_blocked_count: int = 0
    quarantined_count: int = 0
    aggregate_maturity_score: float = 0.0
    aggregate_safety_score: float = 0.0
    aggregate_confidence_score: float = 0.0
    read_only_integrity_score: float = 0.0
    unsafe_capability_enabled_count: int = 0
    real_world_capability_enabled_count: int = 0
    maturity_verdict: str = "CAPABILITY_MATURATION_INSUFFICIENT_EVIDENCE"
    proceed_to_t64b: bool = False
    capability_records: List[CapabilityRecord] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
