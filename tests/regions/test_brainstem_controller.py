import pytest

from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType
from speace_core.cellular_brain.regions.brainstem_controller import (
    BrainstemFunctionalController,
    BrainstemFunctionalState,
    BrainstemDecision,
    BrainstemModulationResult,
    BrainstemState,
)


# ---------------------------------------------------------------------------
# 1. Importabilità e modelli
# ---------------------------------------------------------------------------

def test_brainstem_importable():
    assert BrainstemFunctionalController is not None
    assert BrainstemFunctionalState is not None
    assert BrainstemDecision is not None
    assert BrainstemModulationResult is not None
    assert BrainstemState is not None


def test_brainstem_state_defaults():
    state = BrainstemState()
    assert state.state == BrainstemFunctionalState.STABLE
    assert state.mean_phi == 0.0


def test_brainstem_decision_defaults():
    dec = BrainstemDecision()
    assert dec.state == BrainstemFunctionalState.STABLE
    assert dec.routing_suppression_multiplier == 1.0
    assert dec.energy_recovery_multiplier == 1.0


def test_brainstem_modulation_result_defaults():
    res = BrainstemModulationResult()
    assert res.state_changed is False
    assert res.decisions_count == 0


# ---------------------------------------------------------------------------
# 2. State evaluation
# ---------------------------------------------------------------------------

def test_evaluate_state_stable():
    ctrl = BrainstemFunctionalController()
    assert ctrl.evaluate_state({"mean_region_phi": 0.30, "mean_energy": 0.50}) == BrainstemFunctionalState.STABLE


def test_evaluate_state_watchful_low_phi():
    ctrl = BrainstemFunctionalController()
    assert ctrl.evaluate_state({"mean_region_phi": 0.18, "mean_energy": 0.50}) == BrainstemFunctionalState.WATCHFUL


def test_evaluate_state_watchful_mild_instability():
    ctrl = BrainstemFunctionalController()
    assert ctrl.evaluate_state({"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.20}) == BrainstemFunctionalState.WATCHFUL


def test_evaluate_state_corrective():
    ctrl = BrainstemFunctionalController()
    assert ctrl.evaluate_state({"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.35}) == BrainstemFunctionalState.CORRECTIVE


def test_evaluate_state_protective():
    ctrl = BrainstemFunctionalController()
    assert ctrl.evaluate_state({"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.55, "unstable_region_count": 1}) == BrainstemFunctionalState.PROTECTIVE


def test_evaluate_state_emergency_energy():
    ctrl = BrainstemFunctionalController()
    assert ctrl.evaluate_state({"mean_region_phi": 0.30, "mean_energy": 0.10, "region_instability_mean": 0.0}) == BrainstemFunctionalState.EMERGENCY


def test_evaluate_state_emergency_instability():
    ctrl = BrainstemFunctionalController()
    assert ctrl.evaluate_state({"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.80}) == BrainstemFunctionalState.EMERGENCY


# ---------------------------------------------------------------------------
# 3. Decision computation
# ---------------------------------------------------------------------------

def test_decide_stable_no_suppression():
    ctrl = BrainstemFunctionalController()
    dec = ctrl.decide({"mean_region_phi": 0.30, "mean_energy": 0.50})
    assert dec.state == BrainstemFunctionalState.STABLE
    assert dec.routing_suppression_multiplier == 1.0
    assert dec.plasticity_suppression_multiplier == 1.0


def test_decide_watchful_mild():
    ctrl = BrainstemFunctionalController()
    dec = ctrl.decide({"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.20})
    assert dec.state == BrainstemFunctionalState.WATCHFUL
    assert dec.routing_suppression_multiplier == 0.90
    assert dec.decay_boost_multiplier == 1.10


def test_decide_corrective():
    ctrl = BrainstemFunctionalController()
    dec = ctrl.decide({"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.40})
    assert dec.state == BrainstemFunctionalState.CORRECTIVE
    assert dec.routing_suppression_multiplier == 0.75
    assert dec.plasticity_suppression_multiplier == 0.80
    assert dec.decay_boost_multiplier == 1.25


def test_decide_protective():
    ctrl = BrainstemFunctionalController()
    dec = ctrl.decide({"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.60})
    assert dec.state == BrainstemFunctionalState.PROTECTIVE
    assert dec.routing_suppression_multiplier == 0.55
    assert dec.plasticity_suppression_multiplier == 0.50
    assert dec.neurogenesis_suppression_multiplier == 0.30


def test_decide_emergency():
    ctrl = BrainstemFunctionalController()
    dec = ctrl.decide({"mean_region_phi": 0.30, "mean_energy": 0.10, "region_instability_mean": 0.0})
    assert dec.state == BrainstemFunctionalState.EMERGENCY
    assert dec.routing_suppression_multiplier == 0.30
    assert dec.plasticity_suppression_multiplier == 0.20
    assert dec.energy_recovery_multiplier == 1.50
    assert dec.decay_boost_multiplier == 2.00


# ---------------------------------------------------------------------------
# 4. Apply modulation with memory events
# ---------------------------------------------------------------------------

def test_apply_emergency_records_events():
    ctrl = BrainstemFunctionalController()
    mem = MorphologicalMemory()
    metrics = {"mean_region_phi": 0.30, "mean_energy": 0.10, "region_instability_mean": 0.0}
    result = ctrl.apply(metrics, memory=mem)
    assert result.decision.state == BrainstemFunctionalState.EMERGENCY
    assert result.state_changed is True
    types = [e.event_type for e in mem.events]
    assert MorphologyEventType.BRAINSTEM_STATE_CHANGED in types
    assert MorphologyEventType.BRAINSTEM_MODULATION_APPLIED in types
    assert MorphologyEventType.BRAINSTEM_EMERGENCY_TRIGGERED in types
    assert MorphologyEventType.BRAINSTEM_RECOVERY_APPLIED in types
    assert MorphologyEventType.BRAINSTEM_ROUTING_SUPPRESSED in types
    assert MorphologyEventType.BRAINSTEM_PLASTICITY_SUPPRESSED in types
    assert MorphologyEventType.BRAINSTEM_ENERGY_RECOVERY_BOOSTED in types


def test_apply_stable_no_suppression_events():
    ctrl = BrainstemFunctionalController()
    mem = MorphologicalMemory()
    metrics = {"mean_region_phi": 0.30, "mean_energy": 0.50}
    result = ctrl.apply(metrics, memory=mem)
    assert result.decision.state == BrainstemFunctionalState.STABLE
    assert result.state_changed is True
    types = [e.event_type for e in mem.events]
    assert MorphologyEventType.BRAINSTEM_STATE_CHANGED in types
    assert MorphologyEventType.BRAINSTEM_MODULATION_APPLIED in types
    assert MorphologyEventType.BRAINSTEM_EMERGENCY_TRIGGERED not in types
    assert MorphologyEventType.BRAINSTEM_ROUTING_SUPPRESSED not in types


def test_apply_watchful_records_routing_suppressed():
    ctrl = BrainstemFunctionalController()
    mem = MorphologicalMemory()
    metrics = {"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.20}
    result = ctrl.apply(metrics, memory=mem)
    assert result.decision.state == BrainstemFunctionalState.WATCHFUL
    types = [e.event_type for e in mem.events]
    assert MorphologyEventType.BRAINSTEM_ROUTING_SUPPRESSED in types


def test_apply_recovery_actions_count():
    ctrl = BrainstemFunctionalController()
    mem = MorphologicalMemory()
    metrics = {"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.40}
    result = ctrl.apply(metrics, memory=mem)
    assert result.recovery_actions == 1
    assert result.homeostatic_gain == -0.05


def test_apply_no_state_change_on_second_call():
    ctrl = BrainstemFunctionalController()
    mem = MorphologicalMemory()
    metrics = {"mean_region_phi": 0.30, "mean_energy": 0.50, "region_instability_mean": 0.40}
    r1 = ctrl.apply(metrics, memory=mem)
    assert r1.state_changed is True
    r2 = ctrl.apply(metrics, memory=mem)
    assert r2.state_changed is False


# ---------------------------------------------------------------------------
# 5. Modulation summary
# ---------------------------------------------------------------------------

def test_get_modulation_summary():
    ctrl = BrainstemFunctionalController()
    ctrl.apply({"mean_region_phi": 0.30, "mean_energy": 0.10, "region_instability_mean": 0.0})
    summary = ctrl.get_modulation_summary()
    assert summary["decisions_count"] == 1
    assert summary["emergency_count"] == 1
    assert summary["recovery_actions"] == 1


# ---------------------------------------------------------------------------
# 6. Orchestrator integration
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_orchestrator_brainstem_enabled():
    from speace_core.dna.parser import load_genome
    from speace_core.orchestrator import CellularBrainOrchestrator

    genome = load_genome("speace_core/dna/genome/default_genome.yaml")
    orch = CellularBrainOrchestrator.build_mvp(genome)
    orch.brainstem_controller_enabled = True
    # Re-initialize to pick up the new flag
    orch.model_post_init(None)
    assert orch._brainstem_controller is not None


@pytest.mark.asyncio
async def test_orchestrator_brainstem_applies_modulations():
    from speace_core.dna.parser import load_genome
    from speace_core.orchestrator import CellularBrainOrchestrator
    from speace_core.cellular_brain.benchmark.neurofunctional_benchmark import NeuroFunctionalBenchmark

    genome = load_genome("speace_core/dna/genome/default_genome.yaml")
    orch = CellularBrainOrchestrator.build_mvp(genome)
    orch.brainstem_controller_enabled = True
    orch.model_post_init(None)

    bench = NeuroFunctionalBenchmark(orch)
    result = await bench.run_case(
        "morphological_memory_trace",
        execution_mode="event_driven_burst",
        n_ticks=3,
    )
    m = result.metrics
    assert hasattr(m, "brainstem_state")
    assert hasattr(m, "brainstem_decisions_count")
    assert m.brainstem_decisions_count >= 0


# ---------------------------------------------------------------------------
# 7. Metric enrichment from stability controller
# ---------------------------------------------------------------------------

def test_apply_enriches_instability_from_stability_summary():
    ctrl = BrainstemFunctionalController()
    mem = MorphologicalMemory()
    # Simulate stability-like metrics
    metrics = {
        "mean_region_phi": 0.30,
        "mean_energy": 0.50,
        "region_instability_mean": 0.60,
        "unstable_region_count": 0,
    }
    result = ctrl.apply(metrics, memory=mem)
    assert result.decision.state == BrainstemFunctionalState.PROTECTIVE


# ---------------------------------------------------------------------------
# 8. Benchmark metrics presence
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_benchmark_brainstem_metrics_present():
    from speace_core.dna.parser import load_genome
    from speace_core.orchestrator import CellularBrainOrchestrator
    from speace_core.cellular_brain.benchmark.neurofunctional_benchmark import NeuroFunctionalBenchmark

    genome = load_genome("speace_core/dna/genome/default_genome.yaml")
    orch = CellularBrainOrchestrator.build_mvp(genome)
    orch.brainstem_controller_enabled = True
    orch.model_post_init(None)

    bench = NeuroFunctionalBenchmark(orch)
    result = await bench.run_case(
        "morphological_memory_trace",
        execution_mode="event_driven_burst",
        n_ticks=2,
    )
    m = result.metrics
    assert isinstance(m.brainstem_state, str)
    assert m.brainstem_energy_modulation > 0.0
    assert m.brainstem_routing_modulation > 0.0
    assert m.brainstem_plasticity_modulation > 0.0
    assert m.brainstem_decay_modulation > 0.0
