import random
from typing import List

from pydantic import BaseModel

from speace_core.cellular_brain.base.digital_signal import DigitalSignal
from speace_core.cellular_brain.cells.digital_astrocyte import DigitalAstrocyte
from speace_core.cellular_brain.cells.digital_microglia import DigitalMicroglia
from speace_core.cellular_brain.cells.digital_neuron import DigitalNeuron
from speace_core.cellular_brain.cells.digital_oligodendrocyte import DigitalOligodendrocyte
from speace_core.cellular_brain.cells.digital_synapse import DigitalSynapse


class NeuralCircuit(BaseModel):
    circuit_id: str
    input_neurons: List[DigitalNeuron] = []
    hidden_neurons: List[DigitalNeuron] = []
    output_neurons: List[DigitalNeuron] = []
    synapses: List[DigitalSynapse] = []
    astrocytes: List[DigitalAstrocyte] = []
    microglia: List[DigitalMicroglia] = []
    oligodendrocytes: List[DigitalOligodendrocyte] = []
    feedback_buffer: List[float] = []

    class Config:
        arbitrary_types_allowed = True

    def inject_input(self, pattern: List[float]) -> None:
        for neuron, strength in zip(self.input_neurons, pattern):
            neuron.activation += strength

    async def tick(self) -> List[DigitalSignal]:
        all_neurons = self.input_neurons + self.hidden_neurons + self.output_neurons
        outbound: List[DigitalSignal] = []

        # Astrocyte regulation
        for astro in self.astrocytes:
            astro.regulate(all_neurons)

        # Neuron firing
        for neuron in all_neurons:
            neuron_signals = await neuron.tick()
            for sig in neuron_signals:
                syn = self._find_synapse(sig.source, sig.target)
                if syn and syn.state != "pruned":
                    transmitted = syn.transmit(sig)
                    outbound.append(transmitted)

        # Route signals to targets
        for sig in outbound:
            target = self._find_neuron(sig.target)
            if target:
                await target.receive(sig)

        return outbound

    def apply_feedback(self, score: float) -> None:
        for syn in self.synapses:
            if syn.state == "pruned":
                continue
            if score > 0:
                syn.reinforce(score)
            else:
                syn.weaken(abs(score))
        for neuron in self.hidden_neurons + self.output_neurons:
            neuron.adapt(score)
        self.feedback_buffer.append(score)

    def run_immune(self) -> None:
        all_neurons = self.input_neurons + self.hidden_neurons + self.output_neurons
        for mg in self.microglia:
            mg.inspect(all_neurons, self.synapses)

    def _find_synapse(self, source: str, target: str) -> DigitalSynapse | None:
        for syn in self.synapses:
            if syn.source == source and syn.target == target:
                return syn
        return None

    def _find_neuron(self, cell_id: str) -> DigitalNeuron | None:
        for n in self.input_neurons + self.hidden_neurons + self.output_neurons:
            if n.cell_id == cell_id:
                return n
        return None

    @property
    def output_activations(self) -> List[float]:
        return [n.activation for n in self.output_neurons]
