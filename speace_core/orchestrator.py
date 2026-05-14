import asyncio
import random
from typing import List

from pydantic import BaseModel

from speace_core.cellular_brain.base.digital_signal import DigitalSignal
from speace_core.cellular_brain.cells.digital_astrocyte import DigitalAstrocyte
from speace_core.cellular_brain.cells.digital_microglia import DigitalMicroglia
from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron
from speace_core.cellular_brain.cells.digital_oligodendrocyte import DigitalOligodendrocyte
from speace_core.cellular_brain.cells.digital_synapse import DigitalSynapse
from speace_core.cellular_brain.circuits.neural_circuit import NeuralCircuit
from speace_core.cellular_brain.regulation.homeostasis_engine import (
    HomeostasisEngine,
    SystemMetrics,
)
from speace_core.cellular_brain.regulation.plasticity_engine import PlasticityEngine
from speace_core.dna.models import SharedGenome


class CellularBrainOrchestrator(BaseModel):
    genome: SharedGenome
    circuit: NeuralCircuit
    tick_interval: float = 0.0
    current_tick: int = 0
    metrics_log: List[SystemMetrics] = []

    _homeostasis: HomeostasisEngine = None  # type: ignore[assignment]
    _plasticity: PlasticityEngine = None  # type: ignore[assignment]

    class Config:
        arbitrary_types_allowed = True

    def model_post_init(self, __context: object) -> None:
        self._homeostasis = HomeostasisEngine()
        self._plasticity = PlasticityEngine()

    async def run_ticks(self, n_ticks: int) -> None:
        for _ in range(n_ticks):
            await self._tick()
            if self.tick_interval > 0:
                await asyncio.sleep(self.tick_interval)

    async def _tick(self) -> None:
        self.current_tick += 1
        await self.circuit.tick()

        all_neurons = (
            self.circuit.input_neurons
            + self.circuit.hidden_neurons
            + self.circuit.output_neurons
        )
        metrics = self._homeostasis.compute_metrics(
            tick=self.current_tick,
            neurons=all_neurons,
            astrocytes=self.circuit.astrocytes,
            synapse_count=len(self.circuit.synapses),
            pruned_count=sum(1 for s in self.circuit.synapses if s.state == "pruned"),
        )
        self.metrics_log.append(metrics)

    def inject(self, pattern: List[float]) -> None:
        self.circuit.inject_input(pattern)

    def feedback(self, score: float) -> None:
        self.circuit.apply_feedback(score)

    def run_immune(self) -> None:
        self.circuit.run_immune()

    @property
    def latest_metrics(self) -> SystemMetrics | None:
        return self.metrics_log[-1] if self.metrics_log else None

    @classmethod
    def build_mvp(cls, genome: SharedGenome) -> "CellularBrainOrchestrator":
        n_inputs = 10
        n_hidden = 60
        n_outputs = 10
        n_synapses = 300
        n_astros = 5
        n_micro = 2
        n_oligo = 2

        input_neurons = [
            DigitalNeuron(cell_id=f"in_{i}", role="digital_neuron", threshold=0.5)
            for i in range(n_inputs)
        ]
        hidden_neurons = [
            DigitalNeuron(cell_id=f"hid_{i}", role="digital_neuron", threshold=0.5)
            for i in range(n_hidden)
        ]
        output_neurons = [
            DigitalNeuron(cell_id=f"out_{i}", role="digital_neuron", threshold=0.5)
            for i in range(n_outputs)
        ]

        all_neurons = input_neurons + hidden_neurons + output_neurons
        for n in all_neurons:
            n.bind_genome(genome)

        synapses: List[DigitalSynapse] = []
        for _ in range(n_synapses):
            src = random.choice(all_neurons)
            tgt = random.choice(all_neurons)
            if src.cell_id == tgt.cell_id:
                continue
            syn = DigitalSynapse(
                cell_id=f"syn_{src.cell_id}_{tgt.cell_id}",
                role="digital_synapse",
                source=src.cell_id,
                target=tgt.cell_id,
                weight=random.uniform(0.1, 0.9),
            )
            syn.bind_genome(genome)
            synapses.append(syn)
            src.targets.append(tgt.cell_id)

        astrocytes = [
            DigitalAstrocyte(cell_id=f"astro_{i}", role="digital_astrocyte")
            for i in range(n_astros)
        ]
        microglia = [
            DigitalMicroglia(cell_id=f"micro_{i}", role="digital_microglia")
            for i in range(n_micro)
        ]
        oligodendrocytes = [
            DigitalOligodendrocyte(cell_id=f"oligo_{i}", role="digital_oligodendrocyte")
            for i in range(n_oligo)
        ]

        circuit = NeuralCircuit(
            circuit_id="mvp_circuit",
            input_neurons=input_neurons,
            hidden_neurons=hidden_neurons,
            output_neurons=output_neurons,
            synapses=synapses,
            astrocytes=astrocytes,
            microglia=microglia,
            oligodendrocytes=oligodendrocytes,
        )

        return cls(genome=genome, circuit=circuit)
