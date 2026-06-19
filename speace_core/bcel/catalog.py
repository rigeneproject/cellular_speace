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




def _homeostasis_equivalent() -> CyberneticEquivalent:
    return CyberneticEquivalent(
        component_name="biological homeostasis",
        preserved_function="maintain stable internal state despite perturbations",
        removed_constraints=[
            "slow hormonal diffusion through bloodstream",
            "limited sensor coverage of the body",
            "allostatic wear and tear",
        ],
        kept_constraints=[
            FunctionalConstraint(
                name="negative_feedback_loop",
                invariant="coherence_preservation",
                biological_form="homeostatic set-points with negative feedback",
                mathematical_form="target tracking PID / error-correcting controller",
                parameters={"set_point": 0.5, "gain": 0.1, "decay": 0.9},
                stability_test="system_returns_to_set_point_after_perturbation",
            )
        ],
        digital_implementation="HomeostasisEngine with target tracking",
        configuration={"feedback_type": "negative"},
    )


def _immune_response_equivalent() -> CyberneticEquivalent:
    return CyberneticEquivalent(
        component_name="immune response",
        preserved_function="detect and neutralize threats while preserving self",
        removed_constraints=[
            "physical cell migration through tissue",
            "antibody production latency",
            "inflammation side-effects",
        ],
        kept_constraints=[
            FunctionalConstraint(
                name="self_nonself_discrimination",
                invariant="identity_preservation_through_change",
                biological_form="immune system distinguishes self from non-self",
                mathematical_form="allow-list / signature-based anomaly detection",
                parameters={"tolerance_threshold": 0.1, "quarantine_after_errors": 10},
                stability_test="does_not_attack_legitimate_components",
            ),
            FunctionalConstraint(
                name="controlled_inflammation",
                invariant="destructive_entropy_reduction",
                biological_form="localized inflammation isolates damage",
                mathematical_form="quarantine + resource throttling for misbehaving agents",
                parameters={"quarantine_duration_ticks": 50},
            ),
        ],
        digital_implementation="ImmuneEngine + quarantine policies",
        configuration={"detection": "signature_and_anomaly"},
    )


def _metabolism_equivalent() -> CyberneticEquivalent:
    return CyberneticEquivalent(
        component_name="cellular metabolism",
        preserved_function="allocate energy and resources to functions that need them",
        removed_constraints=[
            "ATP synthesis bottleneck",
            "mitochondrial spatial distribution",
            "limited substrate diffusion",
        ],
        kept_constraints=[
            FunctionalConstraint(
                name="resource_allocation_by_demand",
                invariant="interconnection_efficiency",
                biological_form="metabolism preferentially fuels active tissues",
                mathematical_form="energy budget allocator weighted by activity and coherence",
                parameters={"baseline_budget": 0.3, "activity_weight": 0.5, "coherence_weight": 0.2},
                stability_test="active_modules_receive_resources_without_starvation",
            )
        ],
        digital_implementation="MetabolismCoordinator / EnergyControlAgent",
        configuration={"allocator": "demand_weighted"},
    )


def _apoptosis_equivalent() -> CyberneticEquivalent:
    return CyberneticEquivalent(
        component_name="apoptosis",
        preserved_function="remove damaged or unnecessary components safely",
        removed_constraints=[
            "lysosomal enzyme cascade",
            "phagocyte cleanup latency",
            "irreversibility of cell death",
        ],
        kept_constraints=[
            FunctionalConstraint(
                name="programmed_removal_threshold",
                invariant="destructive_entropy_reduction",
                biological_form="cells self-destruct when damage exceeds a threshold",
                mathematical_form="prune components when error rate > threshold with audit trail",
                parameters={"damage_threshold": 0.8, "grace_period_ticks": 20},
                stability_test="removal_reduces_instead_of_creating_entropy",
            )
        ],
        digital_implementation="ApoptosisEngine with rollback-capable pruning",
        configuration={"rollback_enabled": True},
    )


def _refractory_period_equivalent() -> CyberneticEquivalent:
    return CyberneticEquivalent(
        component_name="neural refractory period",
        preserved_function="limit firing rate to prevent runaway excitation",
        removed_constraints=[
            "ion-channel recovery time",
            "sodium-potassium pump refractoriness",
        ],
        kept_constraints=[
            FunctionalConstraint(
                name="rate_limiter",
                invariant="coherence_preservation",
                biological_form="neuron cannot fire again immediately after a spike",
                mathematical_form="digital neuron enforces minimum inter-spike interval",
                parameters={"min_inter_spike_ticks": 2},
                stability_test="firing_rate_stays_bounded",
            )
        ],
        digital_implementation="DigitalNeuron refractory counter",
        configuration={"refractory_ticks": 2},
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
        for eq in (
            _dna_rna_equivalent(),
            _synapse_equivalent(),
            _memory_consolidation_equivalent(),
            _homeostasis_equivalent(),
            _immune_response_equivalent(),
            _metabolism_equivalent(),
            _apoptosis_equivalent(),
            _refractory_period_equivalent(),
        ):
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
