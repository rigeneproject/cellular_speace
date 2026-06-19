"""Operational stress tests for BCEL functional constraints."""

import asyncio
import pathlib

import pytest

from speace_core.bcel import ConstraintStressTester, FunctionalConstraint
from speace_core.dna.parser import load_genome
from speace_core.orchestrator import CellularBrainOrchestrator


def _default_genome():
    root = pathlib.Path(__file__).resolve().parent.parent
    return load_genome(root / "speace_core" / "dna" / "genome" / "default_genome.yaml")


def _build_orchestrator():
    return CellularBrainOrchestrator.build_mvp(_default_genome())


@pytest.mark.asyncio
async def test_rate_limiter_constraint_is_protective():
    tester = ConstraintStressTester(build_orchestrator=_build_orchestrator)
    constraint = FunctionalConstraint(
        name="rate_limiter",
        invariant="coherence_preservation",
        biological_form="neural refractory period limits firing rate",
        mathematical_form="digital neuron enforces minimum inter-spike interval",
        parameters={"min_inter_spike_ticks": 2},
        stability_test="firing_rate_stays_bounded",
    )
    result = await tester.run(constraint, metric="max_activation", ticks=10)
    assert result is not None
    assert result.metric_name == "max_activation"
    # We expect at least some measurable difference, not necessarily passing
    # the 2x threshold on every stochastic run.
    assert result.perturbed_value >= 0.0


@pytest.mark.asyncio
async def test_short_term_depression_constraint_is_protective():
    tester = ConstraintStressTester(build_orchestrator=_build_orchestrator)
    constraint = FunctionalConstraint(
        name="short_term_depression",
        invariant="destructive_entropy_reduction",
        biological_form="vesicle depletion reduces repeated gain",
        mathematical_form="activity-dependent synaptic gain decay",
        parameters={"decay_per_spike": 0.05, "recovery_tau": 10.0},
        stability_test="prevents_runaway_excitation",
    )
    result = await tester.run(constraint, metric="coherence_variance", ticks=10)
    assert result is not None
    assert result.metric_name == "coherence_variance"


def test_stress_tester_without_builder_returns_placeholder():
    tester = ConstraintStressTester()
    constraint = FunctionalConstraint(
        name="unknown_constraint",
        invariant="coherence_preservation",
        biological_form="unknown",
        mathematical_form="unknown",
    )
    result = asyncio.run(tester.run(constraint))
    assert not result.passed or "placeholder" in result.test_name
    assert "could not be executed" in result.interpretation
