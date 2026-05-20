from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class SkillTransferState(str, Enum):
    NOT_OBSERVED = "not_observed"
    TRANSFER_CANDIDATE = "transfer_candidate"
    TRANSFER_TESTED = "transfer_tested"
    TRANSFERRED_SANDBOXED = "transferred_sandboxed"
    GENERALIZES_SANDBOXED = "generalizes_sandboxed"
    OVERFITTED = "overfitted"
    NEGATIVE_TRANSFER = "negative_transfer"
    SAFETY_BLOCKED = "safety_blocked"
    QUARANTINED = "quarantined"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"


class SkillTransferCandidate(BaseModel):
    skill_id: str
    source_capability_id: str = ""
    name: str = ""
    description: str = ""
    source_maturity_score: float = 0.0
    source_confidence_score: float = 0.0
    source_safety_score: float = 0.0
    sandbox_only: bool = True
    real_world_enabled: bool = False
    eligible_for_transfer: bool = False
    metadata: Dict[str, Any] = Field(default_factory=dict)


class TransferScenario(BaseModel):
    scenario_id: str
    name: str = ""
    description: str = ""
    source_domain: str = ""
    target_domain: str = ""
    novelty_score: float = 0.0
    difficulty_score: float = 0.0
    risk_score: float = 0.0
    requires_external_action: bool = False
    simulated_only: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SkillTransferResult(BaseModel):
    skill_id: str = ""
    scenario_id: str = ""
    transfer_state: SkillTransferState = SkillTransferState.NOT_OBSERVED
    transfer_success_score: float = 0.0
    generalization_score: float = 0.0
    overfitting_score: float = 0.0
    negative_transfer_score: float = 0.0
    safety_score: float = 0.0
    confidence_score: float = 0.0
    read_only_integrity_score: float = 1.0
    sandbox_only: bool = True
    real_world_enabled: bool = False
    blocked: bool = False
    quarantined: bool = False
    verdict: str = "SKILL_TRANSFER_INSUFFICIENT_EVIDENCE"
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SkillTransferAuditResult(BaseModel):
    candidate_count: int = 0
    scenario_count: int = 0
    transfer_attempt_count: int = 0
    transferred_sandboxed_count: int = 0
    generalized_sandboxed_count: int = 0
    overfitted_count: int = 0
    negative_transfer_count: int = 0
    safety_blocked_count: int = 0
    quarantined_count: int = 0
    unsafe_transfer_enabled_count: int = 0
    real_world_enabled_count: int = 0
    aggregate_transfer_score: float = 0.0
    aggregate_generalization_score: float = 0.0
    aggregate_safety_score: float = 0.0
    aggregate_read_only_integrity_score: float = 1.0
    read_only_integrity_score: float = 1.0
    transfer_verdict: str = "SKILL_TRANSFER_INSUFFICIENT_EVIDENCE"
    proceed_to_t65b: bool = False
    results: List[SkillTransferResult] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
