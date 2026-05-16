import pytest

from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType
from speace_core.cellular_brain.regions.brain_region import BrainRegion
from speace_core.cellular_brain.regions.region_registry import RegionRegistry
from speace_core.cellular_brain.regions.region_stability_controller import (
    RegionLevelStabilityController,
    RegionStabilityAction,
    RegionStabilityResult,
    RegionStabilityState,
)


@pytest.fixture
def registry():
    reg = RegionRegistry()
    for rid in ["sensory", "limbic", "hippocampus", "prefrontal", "motor"]:
        reg.register(BrainRegion(
            region_id=rid,
            region_type=rid,
            neuron_ids=[f"n_{rid}_1", f"n_{rid}_2"],
            dominant_cell_types=[f"{rid}_neuron"],
            role_description=f"Role of {rid}",
        ))
    return reg


# ---------------------------------------------------------------------------
# 1. Importabilità e modelli
# ---------------------------------------------------------------------------

def test_stability_controller_importable():
    assert RegionLevelStabilityController is not None
    assert RegionStabilityState is not None
    assert RegionStabilityAction is not None
    assert RegionStabilityResult is not None


def test_compute_instability_score():
    score = RegionLevelStabilityController.compute_instability_score(
        phi_baseline=0.25,
        phi=0.20,
        activation_volatility=0.1,
        signal_overflow=0.05,
        energy_stress=0.0,
        negative_utility_pressure=0.0,
    )
    assert 0.0 <= score <= 1.0
    # phi regression contributes 0.35 * 0.05 = 0.0175
    # volatility contributes 0.25 * 0.1 = 0.025
    # overflow contributes 0.20 * 0.05 = 0.01
    assert score > 0.0


def test_compute_instability_score_clamped():
    score = RegionLevelStabilityController.compute_instability_score(
        phi_baseline=0.25,
        phi=0.0,
        activation_volatility=1.0,
        signal_overflow=1.0,
        energy_stress=1.0,
        negative_utility_pressure=1.0,
    )
    # Formula yields 0.35*0.25 + 0.25*1 + 0.20*1 + 0.10*1 + 0.10*1 = 0.7375
    # but clamped to [0,1]
    assert 0.0 <= score <= 1.0
    assert score > 0.5


def test_compute_instability_score_zero():
    score = RegionLevelStabilityController.compute_instability_score(
        phi_baseline=0.25,
        phi=0.30,
        activation_volatility=0.0,
        signal_overflow=0.0,
        energy_stress=0.0,
        negative_utility_pressure=0.0,
    )
    assert score == 0.0


# ---------------------------------------------------------------------------
# 2. Decide stability action
# ---------------------------------------------------------------------------

def test_decide_stability_action_none():
    state = RegionStabilityState(region_id="sensory", instability_score=0.1)
    action = RegionLevelStabilityController.decide_stability_action(state)
    assert action is None


def test_decide_stability_action_soft_damping():
    state = RegionStabilityState(region_id="sensory", instability_score=0.35)
    action = RegionLevelStabilityController.decide_stability_action(state)
    assert action is not None
    assert action.action_type == "soft_damping"
    assert action.routing_multiplier == 0.75


def test_decide_stability_action_hard_damping():
    state = RegionStabilityState(region_id="sensory", instability_score=0.60)
    action = RegionLevelStabilityController.decide_stability_action(state)
    assert action is not None
    assert action.action_type == "hard_damping"
    assert action.routing_multiplier == 0.40
    assert action.cooldown_ticks == 2


def test_decide_stability_action_routing_block():
    state = RegionStabilityState(region_id="sensory", instability_score=0.85)
    action = RegionLevelStabilityController.decide_stability_action(state)
    assert action is not None
    assert action.action_type == "routing_block"
    assert action.routing_multiplier == 0.0
    assert action.cooldown_ticks == 3


# ---------------------------------------------------------------------------
# 3. Apply stability action
# ---------------------------------------------------------------------------

def test_apply_stability_action(registry):
    controller = RegionLevelStabilityController()
    region = registry.regions["sensory"]
    controller._region_states["sensory"] = RegionStabilityState(region_id="sensory")
    action = RegionStabilityAction(
        region_id="sensory",
        action_type="hard_damping",
        reason="test",
        damping_factor=0.6,
        cooldown_ticks=2,
        routing_multiplier=0.4,
    )
    controller.apply_stability_action(region, action)
    state = controller._region_states["sensory"]
    assert state.damping_factor == 0.6
    assert state.cooldown_remaining == 2
    assert state.routing_allowed is True


def test_apply_routing_block(registry):
    controller = RegionLevelStabilityController()
    region = registry.regions["sensory"]
    controller._region_states["sensory"] = RegionStabilityState(region_id="sensory")
    action = RegionStabilityAction(
        region_id="sensory",
        action_type="routing_block",
        reason="test",
        damping_factor=0.3,
        routing_multiplier=0.0,
        cooldown_ticks=3,
    )
    controller.apply_stability_action(region, action)
    state = controller._region_states["sensory"]
    assert state.routing_allowed is False


# ---------------------------------------------------------------------------
# 4. Pre / post routing stability check
# ---------------------------------------------------------------------------

def test_pre_routing_stability_check(registry):
    controller = RegionLevelStabilityController()
    mem = MorphologicalMemory()
    result = controller.pre_routing_stability_check(registry, circuit=None, memory=mem)
    assert isinstance(result, RegionStabilityResult)
    assert result.regions_checked == 5


def test_post_routing_stability_check(registry):
    controller = RegionLevelStabilityController()
    mem = MorphologicalMemory()
    result = controller.post_routing_stability_check(registry, circuit=None, memory=mem)
    assert isinstance(result, RegionStabilityResult)


# ---------------------------------------------------------------------------
# 5. Brainstem override
# ---------------------------------------------------------------------------

def test_brainstem_override_triggered(registry):
    controller = RegionLevelStabilityController(
        enable_brainstem_override=True,
        brainstem_override_threshold=0.75,
    )
    mem = MorphologicalMemory()
    # Force instability on all regions by setting previous state with high-stress values
    for rid in registry.regions:
        controller._region_states[rid] = RegionStabilityState(
            region_id=rid,
            phi=0.0,
            energy=1.0,
            activation=1.0,
            signal_inflow=1.0,
            signal_outflow=0.0,
            instability_score=0.9,
        )
    result = controller.pre_routing_stability_check(registry, circuit=None, memory=mem)
    assert result.brainstem_override_triggered is True
    assert controller._brainstem_override_active is True
    assert controller._global_routing_multiplier == 0.5


def test_brainstem_override_not_triggered(registry):
    controller = RegionLevelStabilityController(
        enable_brainstem_override=True,
        brainstem_override_threshold=0.75,
    )
    mem = MorphologicalMemory()
    result = controller.pre_routing_stability_check(registry, circuit=None, memory=mem)
    assert result.brainstem_override_triggered is False


# ---------------------------------------------------------------------------
# 6. Get multipliers
# ---------------------------------------------------------------------------

def test_get_routing_multiplier_default():
    controller = RegionLevelStabilityController()
    assert controller.get_routing_multiplier("sensory") == 1.0


def test_get_routing_multiplier_blocked():
    controller = RegionLevelStabilityController()
    controller._region_states["sensory"] = RegionStabilityState(
        region_id="sensory", damping_factor=0.5, routing_allowed=False
    )
    assert controller.get_routing_multiplier("sensory") == 0.0


def test_get_routing_multiplier_damped():
    controller = RegionLevelStabilityController()
    controller._global_routing_multiplier = 0.5
    controller._region_states["sensory"] = RegionStabilityState(
        region_id="sensory", damping_factor=0.8, routing_allowed=True
    )
    assert controller.get_routing_multiplier("sensory") == 0.4


def test_get_plasticity_multiplier_default():
    controller = RegionLevelStabilityController()
    assert controller.get_plasticity_multiplier("sensory") == 1.0


# ---------------------------------------------------------------------------
# 7. Memory events
# ---------------------------------------------------------------------------

def test_stability_check_records_events(registry):
    controller = RegionLevelStabilityController()
    mem = MorphologicalMemory()
    controller.pre_routing_stability_check(registry, circuit=None, memory=mem)
    types = [e.event_type for e in mem.events]
    assert MorphologyEventType.REGION_STABILITY_CHECKED in types


def test_damping_records_event(registry):
    controller = RegionLevelStabilityController()
    mem = MorphologicalMemory()
    region = registry.regions["sensory"]
    controller._region_states["sensory"] = RegionStabilityState(region_id="sensory")
    action = RegionStabilityAction(
        region_id="sensory",
        action_type="hard_damping",
        reason="test",
        damping_factor=0.6,
        cooldown_ticks=2,
    )
    controller.apply_stability_action(region, action, memory=mem)
    types = [e.event_type for e in mem.events]
    assert MorphologyEventType.REGION_DAMPING_APPLIED in types


def test_routing_block_records_event(registry):
    controller = RegionLevelStabilityController()
    mem = MorphologicalMemory()
    region = registry.regions["sensory"]
    controller._region_states["sensory"] = RegionStabilityState(region_id="sensory")
    action = RegionStabilityAction(
        region_id="sensory",
        action_type="routing_block",
        reason="test",
        damping_factor=0.3,
        routing_multiplier=0.0,
        cooldown_ticks=3,
    )
    controller.apply_stability_action(region, action, memory=mem)
    types = [e.event_type for e in mem.events]
    assert MorphologyEventType.REGION_ROUTING_BLOCKED in types


def test_brainstem_override_records_event(registry):
    controller = RegionLevelStabilityController(enable_brainstem_override=True)
    mem = MorphologicalMemory()
    for rid in registry.regions:
        controller._region_states[rid] = RegionStabilityState(
            region_id=rid,
            phi=0.0,
            energy=1.0,
            activation=1.0,
            signal_inflow=1.0,
            signal_outflow=0.0,
            instability_score=0.9,
        )
    controller.pre_routing_stability_check(registry, circuit=None, memory=mem)
    types = [e.event_type for e in mem.events]
    assert MorphologyEventType.BRAINSTEM_STABILITY_OVERRIDE in types


# ---------------------------------------------------------------------------
# 8. Cooldown recovery
# ---------------------------------------------------------------------------

def test_cooldown_recovery(registry):
    controller = RegionLevelStabilityController()
    mem = MorphologicalMemory()
    controller._region_states["sensory"] = RegionStabilityState(
        region_id="sensory", cooldown_remaining=1, routing_allowed=False, damping_factor=0.5
    )
    controller.pre_routing_stability_check(registry, circuit=None, memory=mem)
    state = controller._region_states["sensory"]
    assert state.cooldown_remaining == 0
    assert state.routing_allowed is True
    assert state.damping_factor == 1.0
    types = [e.event_type for e in mem.events]
    assert MorphologyEventType.REGION_STABILITY_RECOVERED in types


# ---------------------------------------------------------------------------
# 9. Summarize stability
# ---------------------------------------------------------------------------

def test_summarize_stability():
    controller = RegionLevelStabilityController()
    controller._region_states["sensory"] = RegionStabilityState(region_id="sensory", instability_score=0.3)
    summary = controller.summarize_stability()
    assert "region_states" in summary
    assert summary["global_routing_multiplier"] == 1.0
    assert summary["brainstem_override_active"] is False


# ---------------------------------------------------------------------------
# 10. RegionStabilityState model defaults
# ---------------------------------------------------------------------------

def test_region_stability_state_defaults():
    state = RegionStabilityState(region_id="test")
    assert state.phi == 0.0
    assert state.energy == 0.0
    assert state.instability_score == 0.0
    assert state.damping_factor == 1.0
    assert state.routing_allowed is True


def test_region_stability_action_model():
    action = RegionStabilityAction(
        region_id="test",
        action_type="soft_damping",
        reason="volatility_high",
    )
    assert action.damping_factor == 1.0
    assert action.cooldown_ticks == 0


def test_region_stability_result_model():
    result = RegionStabilityResult()
    assert result.regions_checked == 0
    assert result.unstable_regions == 0
    assert result.mean_damping_factor == 1.0
    assert result.phi_guard_triggered is False
