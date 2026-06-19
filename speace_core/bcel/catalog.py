"""Catalog of biological-to-digital equivalences used by the BCEL.

Each entry records the function, the likely accidental constraints, and the
functional constraints that must be preserved as mathematical rules.
"""

from typing import Dict, List

from speace_core.bcel.models import BiologicalComponent, CyberneticEquivalent, FunctionalConstraint


def _dna_rna_equivalent() -> CyberneticEquivalent:
    return CyberneticEquivalent(
        component_name="DNA-RNA expression",
        preserved_function="stable source code + isolated execution copy",
        removed_constraints=[
            "chemical instability of RNA",
            "macromolecular transport slowness",
            "transcription enzyme overhead",
        ],
        kept_constraints=[
            FunctionalConstraint(
                name="source_protection",
                invariant="identity_preservation_through_change",
                biological_form="DNA stays in nucleus; RNA is the disposable working copy",
                mathematical_form="immutable SharedGenome + volatile Transcriptome",
                parameters={"genome_write_governance": True},
            ),
            FunctionalConstraint(
                name="amplification_control",
                invariant="generative_variability_preservation",
                biological_form="thousands of mRNA copies from one gene",
                mathematical_form="context-dependent expression profiles; rate limiting",
                parameters={"max_expression_rate": 1.0},
            ),
        ],
        digital_implementation="Digital DNA -> Digital RNA -> Workspace",
        configuration={"rna_volatility": True, "dna_immutable": True},
    )


def _synapse_equivalent() -> CyberneticEquivalent:
    return CyberneticEquivalent(
        component_name="chemical synapse",
        preserved_function="directed, weighted, adaptive signal transmission",
        removed_constraints=[
            "neurotransmitter diffusion delay",
            "vesicle depletion",
            "thermal noise in ion channels",
        ],
        kept_constraints=[
            FunctionalConstraint(
                name="delay_as_lowpass_filter",
                invariant="coherence_preservation",
                biological_form="1-2 ms synaptic delay",
                mathematical_form="leaky integrator + rate limiter",
                parameters={"tau_ms": 5.0, "max_rate_hz": 100.0},
                stability_test="network_does_not_oscillate_when_delay_removed",
            ),
            FunctionalConstraint(
                name="short_term_depression",
                invariant="destructive_entropy_reduction",
                biological_form="vesicle depletion reduces gain on repeated firing",
                mathematical_form="activity-dependent synaptic gain decay",
                parameters={"decay_per_spike": 0.05, "recovery_tau": 10.0},
                stability_test="prevents_runaway_excitation",
            ),
        ],
        digital_implementation="SynapticBond regulated by PeriodicLaw",
        configuration={"bond_type": "weighted_directed"},
    )


def _memory_consolidation_equivalent() -> CyberneticEquivalent:
    return CyberneticEquivalent(
        component_name="slow long-term memory consolidation",
        preserved_function="move stable patterns from transient to persistent storage",
        removed_constraints=[
            "protein synthesis latency (hours/days)",
            "limited molecular storage capacity",
        ],
        kept_constraints=[
            FunctionalConstraint(
                name="statistical_sampling_gate",
                invariant="destructive_entropy_reduction",
                biological_form="slow consolidation acts as a noise filter",
                mathematical_form="workspace -> persistent memory only after recurrence threshold",
                parameters={"recurrence_threshold": 3, "observation_window_ticks": 100},
                stability_test="noise_does_not_persist",
            )
        ],
        digital_implementation="GlobalWorkspace -> SemanticMemoryStore with recurrence check",
        configuration={"persistence_delay": "statistical"},
    )


class BCELCatalog:
    """Registry of known biological-digital equivalences."""

    def __init__(self) -> None:
        self._entries: Dict[str, CyberneticEquivalent] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        for eq in (_dna_rna_equivalent(), _synapse_equivalent(), _memory_consolidation_equivalent()):
            self._entries[eq.component_name] = eq

    def register(self, equivalent: CyberneticEquivalent) -> None:
        self._entries[equivalent.component_name] = equivalent

    def get(self, component_name: str) -> CyberneticEquivalent | None:
        return self._entries.get(component_name)

    def list_components(self) -> List[str]:
        return sorted(self._entries.keys())

    def evaluate_component(
        self, component: BiologicalComponent
    ) -> CyberneticEquivalent:
        """Return the catalog equivalent, or a fresh unclassified one."""
        known = self.get(component.name)
        if known is not None:
            return known
        return CyberneticEquivalent(
            component_name=component.name,
            preserved_function=component.function,
            removed_constraints=[],
            kept_constraints=[],
            digital_implementation="unknown",
        )


def default_catalog() -> BCELCatalog:
    return BCELCatalog()
