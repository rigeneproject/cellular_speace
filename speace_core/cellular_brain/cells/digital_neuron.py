from typing import List

from speace_core.cellular_brain.base.digital_cell import DigitalCell
from speace_core.cellular_brain.base.digital_signal import DigitalSignal


class DigitalNeuron(DigitalCell):
    threshold: float = 0.5
    activation: float = 0.0
    plasticity_rate: float = 0.05
    targets: List[str] = []
    error_history: List[float] = []

    async def receive(self, signal: DigitalSignal) -> None:
        self.activation += signal.strength

    async def tick(self) -> List[DigitalSignal]:
        signals: List[DigitalSignal] = []
        if self.activation >= self.threshold and self.energy > 0.1:
            self.energy = max(0.0, self.energy - 0.05)
            for target_id in self.targets:
                signals.append(
                    DigitalSignal(
                        source=self.cell_id,
                        target=target_id,
                        strength=self.activation,
                    )
                )
            self.activation = 0.0
        else:
            self.activation *= 0.5
        return signals

    def adapt(self, feedback_score: float) -> None:
        self.threshold -= self.plasticity_rate * feedback_score
        self.threshold = max(0.1, min(1.0, self.threshold))
        self.local_memory.append(feedback_score)
        if feedback_score < 0:
            self.error_history.append(feedback_score)
