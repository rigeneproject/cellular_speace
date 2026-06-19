"""Stress-test framework for validating functional constraints."""

from dataclasses import dataclass
from typing import Callable, Dict

from speace_core.bcel.models import FunctionalConstraint


@dataclass
class StressTestResult:
    """Outcome of a constraint stress test."""

    test_name: str
    passed: bool
    metric_before: float
    metric_after: float
    interpretation: str


class ConstraintStressTester:
    """Check whether removing/accelerating a constraint destabilizes the system.

    A functional constraint should show that relaxing it increases oscillation,
    saturation, or decoherence. An accidental constraint should show that
    removing it improves performance without instability.
    """

    def __init__(self) -> None:
        self._tests: Dict[str, Callable[[FunctionalConstraint], StressTestResult]] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        self.register("default", self._default_test)

    def register(
        self,
        name: str,
        test_fn: Callable[[FunctionalConstraint], StressTestResult],
    ) -> None:
        self._tests[name] = test_fn

    def _default_test(self, constraint: FunctionalConstraint) -> StressTestResult:
        """Placeholder: real tests will run against the orchestrator / circuit."""
        return StressTestResult(
            test_name=f"default_{constraint.name}",
            passed=True,
            metric_before=0.0,
            metric_after=0.0,
            interpretation="Placeholder: integrate with runtime simulator for real validation.",
        )

    def run(self, constraint: FunctionalConstraint) -> StressTestResult:
        """Run the registered test for a functional constraint."""
        test_name = constraint.stability_test or "default"
        test_fn = self._tests.get(test_name, self._default_test)
        return test_fn(constraint)
