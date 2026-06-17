"""AssociativeRecallEnvironment - external memory task for SPEACE.

This environment tests associative memory by presenting stimulus-response
pairs and then probing recall:

    study phase:   show (cue, target) pairs repeatedly
    test phase:    show cue alone, measure whether SPEACE output
                   resembles the previously associated target.

Reward is based on cosine similarity between the emitted output pattern
and the correct target. The task exercises:
  - Hebbian / heterosynaptic plasticity
  - latent-state superposition (COR)
  - lazy functional activation driven by DNA rules
  - simulator-backend synchronization
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

import numpy as np


@dataclass
class RecallStep:
    phase: str  # study or test
    cue: List[float]
    target: Optional[List[float]]
    emitted: List[float]
    reward: float
    error: float
    cor_collapsed: bool = False


class AssociativeRecallEnvironment:
    """Associative recall / paired-associate task for SPEACE.

    Args:
        input_size: dimension of cue vector (must fit orchestrator inputs).
        output_size: dimension of target vector (must fit orchestrator outputs).
        num_pairs: number of distinct cue-target associations.
        study_repetitions: how many times each pair is shown during study.
        test_length: number of test probes.
        seed: RNG seed.
    """

    def __init__(
        self,
        input_size: int = 10,
        output_size: int = 10,
        num_pairs: int = 4,
        study_repetitions: int = 3,
        test_length: int = 20,
        seed: Optional[int] = None,
    ):
        self.input_size = input_size
        self.output_size = output_size
        self.num_pairs = num_pairs
        self.study_repetitions = study_repetitions
        self.test_length = test_length
        self._rng = random.Random(seed)
        self._np_rng = np.random.default_rng(seed)

        self._pairs: List[Tuple[List[float], List[float]]] = []
        self._study_steps: int = 0
        self._test_steps: int = 0
        self._history: List[RecallStep] = []
        self._episode: int = 0

        self._build_pairs()

    def _build_pairs(self) -> None:
        """Generate orthogonal-ish cue-target associations."""
        self._pairs = []
        for i in range(self.num_pairs):
            cue = [0.0] * self.input_size
            target = [0.0] * self.output_size
            cue[i % self.input_size] = 1.0
            target[(i + 3) % self.output_size] = 1.0
            cue = [v + self._np_rng.normal(0, 0.02) for v in cue]
            target = [v + self._np_rng.normal(0, 0.02) for v in target]
            self._pairs.append((cue, target))

    def reset_episode(self) -> None:
        """Shuffle pairs and reset counters."""
        self._episode += 1
        self._study_steps = 0
        self._test_steps = 0
        self._history.clear()
        self._rng.shuffle(self._pairs)

    def _read_output(self, orchestrator: Any) -> List[float]:
        """Read output-neuron activations as a prediction vector."""
        outs = orchestrator.circuit.output_neurons
        return [float(n.activation) for n in outs[: self.output_size]]

    def _inject(self, orchestrator: Any, pattern: List[float]) -> None:
        """Inject a pattern into the orchestrator's input neurons."""
        orchestrator.inject(pattern)

    def _similarity_reward(self, emitted: List[float], target: List[float]) -> Tuple[float, float]:
        """Return (reward, error) using cosine similarity."""
        e = np.array(emitted, dtype=float)
        t = np.array(target, dtype=float)
        size = min(len(e), len(t))
        e = e[:size]
        t = t[:size]
        norm_e = np.linalg.norm(e)
        norm_t = np.linalg.norm(t)
        if norm_e == 0 or norm_t == 0:
            return 0.0, 1.0
        cosine = float(np.dot(e, t) / (norm_e * norm_t))
        reward = max(0.0, (cosine + 1.0) / 2.0)
        error = 1.0 - reward
        return reward, error

    def _tick_orchestrator(self, orchestrator: Any) -> bool:
        """Advance orchestrator and return whether COR collapsed this tick."""
        import asyncio
        try:
            asyncio.run(orchestrator._tick())
        except Exception:
            pass
        last = getattr(orchestrator, "_last_cor_result", None)
        return bool(last and last.collapsed)

    def run_study_phase(self, orchestrator: Any) -> List[RecallStep]:
        """Present each pair repeatedly."""
        steps: List[RecallStep] = []
        for _ in range(self.study_repetitions):
            for cue, target in self._pairs:
                self._inject(orchestrator, cue)
                collapsed = self._tick_orchestrator(orchestrator)
                emitted = self._read_output(orchestrator)
                reward, error = self._similarity_reward(emitted, target)
                if reward > 0.3:
                    for syn in orchestrator.circuit.synapses:
                        if syn.weight > 0.0:
                            syn.reinforce(reward * 0.5)
                step = RecallStep(
                    phase="study",
                    cue=list(cue),
                    target=list(target),
                    emitted=emitted,
                    reward=reward,
                    error=error,
                    cor_collapsed=collapsed,
                )
                steps.append(step)
                self._history.append(step)
                self._study_steps += 1
        return steps

    def run_test_phase(self, orchestrator: Any) -> List[RecallStep]:
        """Probe recall by presenting cues alone."""
        steps: List[RecallStep] = []
        for _ in range(self.test_length):
            cue, target = self._rng.choice(self._pairs)
            self._inject(orchestrator, cue)
            collapsed = self._tick_orchestrator(orchestrator)
            emitted = self._read_output(orchestrator)
            reward, error = self._similarity_reward(emitted, target)
            step = RecallStep(
                phase="test",
                cue=list(cue),
                target=list(target),
                emitted=emitted,
                reward=reward,
                error=error,
                cor_collapsed=collapsed,
            )
            steps.append(step)
            self._history.append(step)
            self._test_steps += 1
        return steps

    def run_episode(self, orchestrator: Any) -> Dict[str, Any]:
        """Run a full study+test episode and return summary."""
        self.reset_episode()
        study_steps = self.run_study_phase(orchestrator)
        test_steps = self.run_test_phase(orchestrator)

        study_rewards = [s.reward for s in study_steps]
        test_rewards = [s.reward for s in test_steps]
        cor_collapses = sum(1 for s in self._history if s.cor_collapsed)

        return {
            "episode": self._episode,
            "num_pairs": self.num_pairs,
            "study_steps": len(study_steps),
            "test_steps": len(test_steps),
            "mean_study_reward": float(np.mean(study_rewards)) if study_rewards else 0.0,
            "mean_test_reward": float(np.mean(test_rewards)) if test_rewards else 0.0,
            "learning_gain": (
                float(np.mean(test_rewards)) - float(np.mean(study_rewards))
                if study_rewards and test_rewards else 0.0
            ),
            "cor_collapses": cor_collapses,
            "history_sample": [
                {
                    "phase": s.phase,
                    "reward": round(s.reward, 4),
                    "error": round(s.error, 4),
                    "cor_collapsed": s.cor_collapsed,
                }
                for s in self._history[:5]
            ],
        }
