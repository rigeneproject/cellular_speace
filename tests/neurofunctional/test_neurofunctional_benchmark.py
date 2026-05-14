import random

import pytest

from speace_core.cellular_brain.benchmark.neurofunctional_benchmark import (
    NeuroFunctionalBenchmark,
)
from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType
from speace_core.dna.parser import load_genome
from speace_core.orchestrator import CellularBrainOrchestrator


@pytest.fixture
def genome():
    return load_genome("speace_core/dna/genome/default_genome.yaml")


@pytest.fixture
def orchestrator(genome):
    random.seed(42)
    return CellularBrainOrchestrator.build_mvp(genome)


@pytest.fixture
def benchmark(orchestrator):
    return NeuroFunctionalBenchmark(orchestrator)


@pytest.mark.asyncio
async def test_benchmark_captures_baseline_state(benchmark):
    state = await benchmark.capture_state()
    assert state.neuron_count > 0
    assert state.synapse_count >= 0
    assert 0.0 <= state.coherence_phi <= 1.0
    assert 0.0 <= state.mean_energy <= 1.0
    assert 0.0 <= state.accuracy <= 1.0


@pytest.mark.asyncio
async def test_adaptation_after_error(benchmark, orchestrator):
    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    target = pattern

    result = await benchmark.run_case(
        "adaptation_after_error",
        input_pattern=pattern,
        target_output=target,
        n_ticks=3,
    )

    assert result.case_name == "adaptation_after_error"
    assert result.baseline_state.neuron_count > 0
    assert result.final_state.neuron_count > 0
    assert result.final_state.coherence_phi > 0.0
    assert result.final_state.mean_energy > 0.0
    assert 0.0 <= result.metrics.accuracy_score <= 1.0
    assert 0.0 <= result.metrics.speace_cognitive_score <= 1.0


@pytest.mark.asyncio
async def test_useful_neurogenesis(benchmark, orchestrator):
    # Force neurogenesis to fire deterministically
    orchestrator._neurogenesis.phi_threshold = 1.0
    orchestrator._neurogenesis.error_threshold = 1

    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "useful_neurogenesis",
        input_pattern=pattern,
        target_output=pattern,
        n_ticks=3,
    )

    assert result.case_name == "useful_neurogenesis"
    assert result.final_state.neuron_count > result.baseline_state.neuron_count
    assert result.metrics.neurogenesis_events >= 1
    assert result.final_state.coherence_phi > 0.0


@pytest.mark.asyncio
async def test_useful_apoptosis(benchmark, orchestrator):
    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "useful_apoptosis",
        input_pattern=pattern,
        target_output=pattern,
        n_ticks=3,
    )

    assert result.case_name == "useful_apoptosis"
    # The weak neuron should have been removed or synapses pruned
    assert (
        result.metrics.apoptosis_events >= 1
        or result.final_state.synapse_count < result.baseline_state.synapse_count
    )
    # No functional collapse
    assert result.final_state.accuracy >= 0.0
    assert result.final_state.neuron_count >= 5
    assert result.final_state.coherence_phi > 0.0


@pytest.mark.asyncio
async def test_differentiation_consistency(benchmark, orchestrator):
    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "differentiation_consistency",
        input_pattern=pattern,
        target_output=pattern,
    )

    assert result.case_name == "differentiation_consistency"
    assert result.metrics.cell_differentiation_events >= 1

    circuit = orchestrator.circuit
    hip = next((n for n in circuit.hidden_neurons if n.cell_id == "hip_001"), None)
    pfc = next((n for n in circuit.hidden_neurons if n.cell_id == "pfc_001"), None)
    if hip:
        assert hip.cell_type == "hippocampal_neuron"
        assert hip.differentiation_state == "differentiated"
    if pfc:
        assert pfc.cell_type == "prefrontal_neuron"
        assert pfc.differentiation_state == "differentiated"


@pytest.mark.asyncio
async def test_morphological_memory_trace(benchmark, orchestrator):
    # Force neurogenesis deterministically
    orchestrator._neurogenesis.phi_threshold = 1.0
    orchestrator._neurogenesis.error_threshold = 1

    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "morphological_memory_trace",
        input_pattern=pattern,
        target_output=pattern,
        n_ticks=3,
    )

    assert result.case_name == "morphological_memory_trace"
    mem = orchestrator.memory
    assert mem.count_events(MorphologyEventType.NEURON_CREATED) >= 1
    assert len(mem.snapshots) > 1
    assert mem.phi_trend() is not None


@pytest.mark.asyncio
async def test_report_generation(benchmark, orchestrator):
    # Force neurogenesis deterministically
    orchestrator._neurogenesis.phi_threshold = 1.0
    orchestrator._neurogenesis.error_threshold = 1

    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "morphological_memory_trace",
        input_pattern=pattern,
        target_output=pattern,
        n_ticks=3,
    )

    json_path = benchmark.generate_json_report(result)
    md_path = benchmark.generate_markdown_report(result)

    assert json_path.exists()
    assert md_path.exists()
    assert result.json_report_path is not None
    assert result.markdown_report_path is not None

    md_text = md_path.read_text(encoding="utf-8")
    assert "SPEACE NeuroFunctional Benchmark Report" in md_text
    assert result.case_name in md_text
    assert "SPEACE Cognitive Score" in md_text

    latest_md = benchmark.reports_dir / "latest_report.md"
    latest_json = benchmark.reports_dir / "latest_report.json"
    assert latest_md.exists()
    assert latest_json.exists()


@pytest.mark.asyncio
async def test_cognitive_score_bounds(benchmark, orchestrator):
    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "adaptation_after_error",
        input_pattern=pattern,
        target_output=pattern,
        n_ticks=3,
    )

    score = result.metrics.speace_cognitive_score
    assert 0.0 <= score <= 1.0


@pytest.mark.asyncio
async def test_adaptation_in_burst_mode(benchmark, orchestrator):
    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "adaptation_after_error",
        execution_mode="event_driven_burst",
        input_pattern=pattern,
        target_output=pattern,
        n_ticks=3,
    )

    assert result.case_name == "adaptation_after_error"
    assert result.baseline_state.neuron_count > 0
    assert result.final_state.neuron_count > 0
    assert result.final_state.coherence_phi > 0.0
    assert 0.0 <= result.metrics.speace_cognitive_score <= 1.0


@pytest.mark.asyncio
async def test_adaptation_in_burst_mode_with_stdp(benchmark, orchestrator):
    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "adaptation_after_error",
        execution_mode="event_driven_burst",
        stdp_enabled=True,
        input_pattern=pattern,
        target_output=pattern,
        n_ticks=3,
    )

    assert result.case_name == "adaptation_after_error"
    assert result.baseline_state.neuron_count > 0
    assert result.final_state.neuron_count > 0
    assert result.final_state.coherence_phi > 0.0
    assert 0.0 <= result.metrics.speace_cognitive_score <= 1.0


@pytest.mark.asyncio
async def test_adaptation_in_burst_mode_with_stdp_and_inhibition(benchmark, orchestrator):
    pattern = [1.0 if i % 2 == 0 else 0.0 for i in range(10)]
    result = await benchmark.run_case(
        "adaptation_after_error",
        execution_mode="event_driven_burst",
        stdp_enabled=True,
        inhibition_enabled=True,
        input_pattern=pattern,
        target_output=pattern,
        n_ticks=3,
    )

    assert result.case_name == "adaptation_after_error"
    assert result.baseline_state.neuron_count > 0
    assert result.final_state.neuron_count > 0
    assert result.final_state.coherence_phi > 0.0
    assert 0.0 <= result.metrics.speace_cognitive_score <= 1.0
