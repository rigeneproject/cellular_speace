from typing import Any, Dict, List

from pydantic import BaseModel, Field


class GenomeIdentity(BaseModel):
    entity_name: str = "SPEACE"
    nature: str = "cybernetic_evolutionary_entity"
    core_function: str = "increase_systemic_coherence"
    substrate: str = "digital_physical_hybrid"
    continuity_principle: str = "preserve_identity_through_adaptive_change"


class GenomeMorphology(BaseModel):
    allowed_cell_types: List[str] = []
    allowed_tissues: List[str] = []
    organs: List[str] = []


class CellExpressionRules(BaseModel):
    role: str
    express: List[str] = []
    threshold_defaults: Dict[str, float] = Field(default_factory=dict)


class HomeostasisParams(BaseModel):
    default_threshold: float = 0.5
    default_plasticity_rate: float = 0.05
    max_energy: float = 1.0
    overload_threshold: float = 0.85
    noise_suppression_rate: float = 0.2
    energy_recovery_rate: float = 0.01


class ImmuneParams(BaseModel):
    prune_threshold: float = 0.1
    quarantine_error_limit: int = 10
    myelination_success_threshold: float = 0.8
    latency_reduction: float = 0.3


class SharedGenome(BaseModel):
    identity: GenomeIdentity = Field(default_factory=GenomeIdentity)
    morphology: GenomeMorphology = Field(default_factory=GenomeMorphology)
    expression_rules: Dict[str, CellExpressionRules] = Field(default_factory=dict)
    homeostasis: HomeostasisParams = Field(default_factory=HomeostasisParams)
    immune: ImmuneParams = Field(default_factory=ImmuneParams)
    ilf_core: Dict[str, Any] = Field(default_factory=dict)
    edd_cvt_core: Dict[str, Any] = Field(default_factory=dict)

    def get_genes_for_role(self, role: str) -> List[str]:
        rules = self.expression_rules.get(role)
        if rules is None:
            return []
        return list(rules.express)
