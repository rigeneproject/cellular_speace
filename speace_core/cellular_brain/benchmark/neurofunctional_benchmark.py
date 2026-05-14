import json
import random
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from speace_core.cellular_brain.circuits.neural_circuit import NeuralCircuit
from speace_core.cellular_brain.memory.morphological_memory import MorphologicalMemory
from speace_core.cellular_brain.memory.morphology_events import MorphologyEventType
from speace_core.orchestrator import CellularBrainOrchestrator


class BenchmarkState(BaseModel):
    neuron_count: int = 0
    synapse_count: int = 0
    active_synapse_count: int = 0
    coherence_phi: float = 0.0
    mean_energy: float = 0.0
    accuracy: float = 0.0
    output_activations: List[float] = Field(default_factory=list)


class BenchmarkMetrics(BaseModel):
    accuracy_score: float = 0.0
    coherence_phi: float = 0.0
    phi_trend: float = 0.0
    mean_energy: float = 0.0
    energy_efficiency: float = 0.0
    neuron_count_delta: int = 0
    synapse_count_delta: int = 0
    neurogenesis_events: int = 0
    apoptosis_events: int = 0
    cell_differentiation_events: int = 0
    adaptation_gain: float = 0.0
    morphological_stability: float = 0.0
    morphological_adaptation: float = 0.0
    structural_complexity: float = 0.0
    functional_improvement: float = 0.0
    speace_cognitive_score: float = 0.0


class BenchmarkResult(BaseModel):
    case_name: str = ""
    baseline_state: BenchmarkState = Field(default_factory=BenchmarkState)
    final_state: BenchmarkState = Field(default_factory=BenchmarkState)
    metrics: BenchmarkMetrics = Field(default_factory=BenchmarkMetrics)
    json_report_path: Optional[str] = None
    markdown_report_path: Optional[str] = None


class NeuroFunctionalBenchmark:
    """Reproducible neuro-functional benchmark for SPEACE v0.2."""

    def __init__(self, orchestrator: CellularBrainOrchestrator):
        self.orch = orchestrator
        self.reports_dir = Path("reports/neurofunctional")
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    async def capture_state(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
    ) -> BenchmarkState:
        """Capture current circuit state, optionally after injecting a pattern."""
        if input_pattern is not None:
            self.orch.inject(input_pattern)
            await self.orch.run_ticks(1)

        circuit = self.orch.circuit
        metrics = self.orch.latest_metrics

        neuron_count = len(
            circuit.input_neurons + circuit.hidden_neurons + circuit.output_neurons
        )
        synapse_count = len(circuit.synapses)
        active_synapse_count = sum(1 for s in circuit.synapses if s.state != "pruned")
        coherence_phi = metrics.coherence_phi if metrics else 0.0
        mean_energy = metrics.mean_energy if metrics else 0.0

        output_activations = [n.activation for n in circuit.output_neurons]
        accuracy = 0.0
        if target_output is not None and output_activations:
            clamped = [min(1.0, max(0.0, a)) for a in output_activations]
            mae = sum(abs(t - o) for t, o in zip(target_output, clamped)) / len(
                target_output
            )
            accuracy = max(0.0, 1.0 - mae)

        return BenchmarkState(
            neuron_count=neuron_count,
            synapse_count=synapse_count,
            active_synapse_count=active_synapse_count,
            coherence_phi=coherence_phi,
            mean_energy=mean_energy,
            accuracy=accuracy,
            output_activations=output_activations,
        )

    async def run_adaptation_cycle(
        self,
        input_pattern: List[float],
        target_output: List[float],
        n_ticks: int = 5,
        n_feedback: int = 3,
    ) -> BenchmarkResult:
        """Run a generic adaptation cycle and return benchmark result."""
        baseline = await self.capture_state(input_pattern, target_output)

        for _ in range(n_feedback):
            self.orch.inject(input_pattern)
            await self.orch.run_ticks(n_ticks)
            # Alternate negative / positive feedback to simulate learning
            score = random.choice([-0.3, 0.5])
            self.orch.feedback(score)

        final = await self.capture_state(input_pattern, target_output)
        metrics = self._compute_metrics(baseline, final)

        result = BenchmarkResult(
            case_name="adaptation_cycle",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )
        return result

    async def run_case(
        self,
        case_name: str,
        execution_mode: str = "global_tick",
        stdp_enabled: bool = True,
        inhibition_enabled: bool = True,
        **kwargs: Any,
    ) -> BenchmarkResult:
        """Dispatcher for predefined benchmark scenarios."""
        original_mode = self.orch.execution_mode
        original_stdp = self.orch.stdp_enabled
        original_inhibition = self.orch.inhibition_enabled
        self.orch.execution_mode = execution_mode
        self.orch.stdp_enabled = stdp_enabled
        self.orch.inhibition_enabled = inhibition_enabled
        try:
            if case_name == "adaptation_after_error":
                result = await self._case_adaptation_after_error(**kwargs)
            elif case_name == "useful_neurogenesis":
                result = await self._case_useful_neurogenesis(**kwargs)
            elif case_name == "useful_apoptosis":
                result = await self._case_useful_apoptosis(**kwargs)
            elif case_name == "differentiation_consistency":
                result = await self._case_differentiation_consistency(**kwargs)
            elif case_name == "morphological_memory_trace":
                result = await self._case_morphological_memory_trace(**kwargs)
            else:
                raise ValueError(f"Unknown benchmark case: {case_name}")
        finally:
            self.orch.execution_mode = original_mode
            self.orch.stdp_enabled = original_stdp
            self.orch.inhibition_enabled = original_inhibition
        return result

    async def _case_adaptation_after_error(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
        n_ticks: int = 5,
    ) -> BenchmarkResult:
        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        baseline = await self.capture_state(pattern, target)

        # Negative feedback phase
        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.feedback(-0.5)

        # Positive feedback phase
        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.feedback(0.8)

        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="adaptation_after_error",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    async def _case_useful_neurogenesis(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
        n_ticks: int = 5,
    ) -> BenchmarkResult:
        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        baseline = await self.capture_state(pattern, target)

        # Force neurogenesis conditions
        self.orch.negative_feedback_count = 5
        # Ensure hidden neurons have high energy so mean_energy stays above min
        for n in self.orch.circuit.hidden_neurons:
            n.energy = 1.0

        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.run_neurogenesis()

        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="useful_neurogenesis",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    async def _case_useful_apoptosis(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
        n_ticks: int = 5,
    ) -> BenchmarkResult:
        from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron

        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        # Add a weak, expensive, isolated neuron to hidden layer
        weak = DigitalNeuron(
            cell_id="weak_001",
            role="digital_neuron",
            threshold=0.5,
            energy=1.0,
            utility_score=0.0,
        )
        weak.is_critical = False
        weak.neuron_role = "excitatory"
        self.orch.circuit.hidden_neurons.append(weak)

        baseline = await self.capture_state(pattern, target)

        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.run_apoptosis()

        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="useful_apoptosis",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    async def _case_differentiation_consistency(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
    ) -> BenchmarkResult:
        from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron

        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        # Add undifferentiated neurons in distinct regions
        hip = DigitalNeuron(cell_id="hip_001", role="digital_neuron")
        hip.region = "hippocampus"
        hip.differentiation_state = "undifferentiated"
        pfc = DigitalNeuron(cell_id="pfc_001", role="digital_neuron")
        pfc.region = "prefrontal"
        pfc.differentiation_state = "undifferentiated"

        self.orch.circuit.hidden_neurons.append(hip)
        self.orch.circuit.hidden_neurons.append(pfc)

        baseline = await self.capture_state(pattern, target)
        self.orch.run_differentiation()
        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="differentiation_consistency",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    async def _case_morphological_memory_trace(
        self,
        input_pattern: Optional[List[float]] = None,
        target_output: Optional[List[float]] = None,
        n_ticks: int = 5,
    ) -> BenchmarkResult:
        pattern = input_pattern or self._default_pattern()
        target = target_output or pattern

        baseline = await self.capture_state(pattern, target)

        # Full adaptive cycle
        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.feedback(-0.3)

        self.orch.negative_feedback_count = 5
        for n in self.orch.circuit.hidden_neurons:
            n.energy = 1.0
        self.orch.run_neurogenesis()
        self.orch.run_apoptosis()
        self.orch.run_differentiation()

        self.orch.inject(pattern)
        await self.orch.run_ticks(n_ticks)
        self.orch.feedback(0.6)

        final = await self.capture_state(pattern, target)
        metrics = self._compute_metrics(baseline, final)

        return BenchmarkResult(
            case_name="morphological_memory_trace",
            baseline_state=baseline,
            final_state=final,
            metrics=metrics,
        )

    def _compute_metrics(
        self, baseline: BenchmarkState, final: BenchmarkState
    ) -> BenchmarkMetrics:
        phi_trend = final.coherence_phi - baseline.coherence_phi
        neuron_count_delta = final.neuron_count - baseline.neuron_count
        synapse_count_delta = final.synapse_count - baseline.synapse_count
        structural_delta = abs(neuron_count_delta) + abs(synapse_count_delta)
        adaptation_gain = final.accuracy - baseline.accuracy

        energy_efficiency = max(0.0, min(1.0, final.mean_energy))
        structural_complexity = (
            final.active_synapse_count / final.neuron_count
            if final.neuron_count > 0
            else 0.0
        )
        morphological_stability = 1.0 / (
            1.0 + 0.1 * abs(neuron_count_delta) + 0.01 * abs(synapse_count_delta)
        )
        functional_improvement = max(0.0, adaptation_gain) + max(0.0, phi_trend)
        morphological_adaptation = (
            1.0
            if functional_improvement > 0 and structural_delta > 0
            else 0.0
        )
        safety_score = (
            1.0
            if final.neuron_count >= 5 and final.coherence_phi > 0.0
            else 0.0
        )

        mem = self.orch.memory
        neurogenesis_events = mem.count_events(MorphologyEventType.NEURON_CREATED)
        apoptosis_events = mem.count_events(MorphologyEventType.NEURON_APOPTOSIS)
        cell_diff_events = mem.count_events(MorphologyEventType.CELL_DIFFERENTIATED)

        score = (
            0.20 * final.accuracy
            + 0.20 * final.coherence_phi
            + 0.15 * max(0.0, adaptation_gain)
            + 0.15 * energy_efficiency
            + 0.10 * morphological_stability
            + 0.10 * max(0.0, phi_trend)
            + 0.10 * safety_score
        )
        speace_cognitive_score = max(0.0, min(1.0, score))

        return BenchmarkMetrics(
            accuracy_score=final.accuracy,
            coherence_phi=final.coherence_phi,
            phi_trend=phi_trend,
            mean_energy=final.mean_energy,
            energy_efficiency=energy_efficiency,
            neuron_count_delta=neuron_count_delta,
            synapse_count_delta=synapse_count_delta,
            neurogenesis_events=neurogenesis_events,
            apoptosis_events=apoptosis_events,
            cell_differentiation_events=cell_diff_events,
            adaptation_gain=adaptation_gain,
            morphological_stability=morphological_stability,
            morphological_adaptation=morphological_adaptation,
            structural_complexity=structural_complexity,
            functional_improvement=functional_improvement,
            speace_cognitive_score=speace_cognitive_score,
        )

    def generate_json_report(self, result: BenchmarkResult) -> Path:
        """Save a machine-readable JSON report and update latest links."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_{timestamp}.json"
        path = self.reports_dir / filename
        path.write_text(result.model_dump_json(indent=2), encoding="utf-8")

        latest = self.reports_dir / "latest_report.json"
        latest.write_text(result.model_dump_json(indent=2), encoding="utf-8")

        result.json_report_path = str(path)
        return path

    def generate_markdown_report(self, result: BenchmarkResult) -> Path:
        """Save a human-readable Markdown report and update latest links."""
        m = result.metrics
        lines = [
            "# SPEACE NeuroFunctional Benchmark Report",
            f"**Case:** {result.case_name}",
            f"**Date:** {datetime.now().isoformat()}",
            "",
            "## Baseline State",
            f"- Neurons: {result.baseline_state.neuron_count}",
            f"- Synapses: {result.baseline_state.synapse_count}",
            f"- Active synapses: {result.baseline_state.active_synapse_count}",
            f"- Coherence Φ: {result.baseline_state.coherence_phi:.4f}",
            f"- Mean energy: {result.baseline_state.mean_energy:.4f}",
            f"- Accuracy: {result.baseline_state.accuracy:.4f}",
            "",
            "## Final State",
            f"- Neurons: {result.final_state.neuron_count}",
            f"- Synapses: {result.final_state.synapse_count}",
            f"- Active synapses: {result.final_state.active_synapse_count}",
            f"- Coherence Φ: {result.final_state.coherence_phi:.4f}",
            f"- Mean energy: {result.final_state.mean_energy:.4f}",
            f"- Accuracy: {result.final_state.accuracy:.4f}",
            "",
            "## Metrics",
            f"| Metric | Value |",
            f"|---|---|",
            f"| Accuracy score | {m.accuracy_score:.4f} |",
            f"| Coherence Φ | {m.coherence_phi:.4f} |",
            f"| Φ trend | {m.phi_trend:.4f} |",
            f"| Mean energy | {m.mean_energy:.4f} |",
            f"| Energy efficiency | {m.energy_efficiency:.4f} |",
            f"| Neuron count delta | {m.neuron_count_delta} |",
            f"| Synapse count delta | {m.synapse_count_delta} |",
            f"| Neurogenesis events | {m.neurogenesis_events} |",
            f"| Apoptosis events | {m.apoptosis_events} |",
            f"| Differentiation events | {m.cell_differentiation_events} |",
            f"| Adaptation gain | {m.adaptation_gain:.4f} |",
            f"| Morphological stability | {m.morphological_stability:.4f} |",
            f"| Morphological adaptation | {m.morphological_adaptation:.4f} |",
            f"| Structural complexity | {m.structural_complexity:.4f} |",
            f"| Functional improvement | {m.functional_improvement:.4f} |",
            f"| **SPEACE Cognitive Score** | **{m.speace_cognitive_score:.4f}** |",
            "",
            "---",
            "*Generated by NeuroFunctionalBenchmark v0.2*",
        ]
        md = "\n".join(lines)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"benchmark_{timestamp}.md"
        path = self.reports_dir / filename
        path.write_text(md, encoding="utf-8")

        latest = self.reports_dir / "latest_report.md"
        latest.write_text(md, encoding="utf-8")

        result.markdown_report_path = str(path)
        return path

    @staticmethod
    def _default_pattern(length: int = 10) -> List[float]:
        return [1.0 if i % 2 == 0 else 0.0 for i in range(length)]
