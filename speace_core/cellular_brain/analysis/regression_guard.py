from typing import Any, Dict, Optional

from pydantic import BaseModel, Field

from speace_core.cellular_brain.analysis.recovery_policy_selector import (
    RecoveryPolicy,
    RegressionGuardThresholds,
)


class RegressionGuardResult(BaseModel):
    """Result of a regression guard evaluation."""

    verdict: str = "POLICY_STABLE"
    cognitive_score_ok: bool = True
    phi_ok: bool = True
    energy_efficiency_ok: bool = True
    suppression_cost_ok: bool = True
    recovery_score_ok: bool = True
    emergency_ratio_ok: bool = True
    state_entropy_ok: bool = True
    violations: Dict[str, str] = Field(default_factory=dict)


class RegressionGuard:
    """T41 — Lightweight regression guard against the frozen canonical policy.

    Compares current benchmark/audit metrics against the thresholds
    stored in RecoveryPolicy and returns a verdict.
    """

    @staticmethod
    def evaluate(
        metrics: Dict[str, Any],
        policy: Optional[RecoveryPolicy] = None,
        thresholds: Optional[RegressionGuardThresholds] = None,
    ) -> RegressionGuardResult:
        """Evaluate metrics against regression thresholds.

        `metrics` can be a BenchmarkMetrics dict, a LongHorizonProfileResult dict,
        or any flat dictionary containing the relevant keys.
        """
        def _safe(val):
            return float(val) if val is not None else 0.0

        thr = thresholds or (policy.regression_guard_thresholds if policy else RegressionGuardThresholds())
        result = RegressionGuardResult()
        violations: Dict[str, str] = {}

        # Cognitive score
        cog = _safe(metrics.get("cognitive_score", metrics.get("speace_cognitive_score", 0.0)))
        if cog < thr.min_cognitive_score:
            result.cognitive_score_ok = False
            violations["cognitive_score"] = f"{cog:.4f} < {thr.min_cognitive_score:.4f}"

        # Phi
        phi = _safe(metrics.get("coherence_phi", metrics.get("phi", 0.0)))
        if phi < thr.min_phi:
            result.phi_ok = False
            violations["phi"] = f"{phi:.4f} < {thr.min_phi:.4f}"

        # Energy
        energy = _safe(metrics.get("energy_efficiency", metrics.get("mean_energy", 0.0)))
        if energy < thr.min_energy_efficiency:
            result.energy_efficiency_ok = False
            violations["energy_efficiency"] = f"{energy:.4f} < {thr.min_energy_efficiency:.4f}"

        # Suppression cost
        sup = _safe(metrics.get("suppression_cost", 0.0))
        if sup > thr.max_suppression_cost:
            result.suppression_cost_ok = False
            violations["suppression_cost"] = f"{sup:.4f} > {thr.max_suppression_cost:.4f}"

        # Recovery score
        rec = _safe(metrics.get("long_horizon_recovery_score", 0.0))
        if rec < thr.min_long_horizon_recovery_score:
            result.recovery_score_ok = False
            violations["recovery_score"] = f"{rec:.4f} < {thr.min_long_horizon_recovery_score:.4f}"

        # Emergency ratio
        emg = _safe(metrics.get("emergency_state_ratio", metrics.get("emergency_state_ratio_over_time", 0.0)))
        if emg > thr.max_emergency_state_ratio:
            result.emergency_ratio_ok = False
            violations["emergency_ratio"] = f"{emg:.4f} > {thr.max_emergency_state_ratio:.4f}"

        # State entropy
        ent = _safe(metrics.get("state_entropy", 0.0))
        if ent < thr.min_state_entropy:
            result.state_entropy_ok = False
            violations["state_entropy"] = f"{ent:.4f} < {thr.min_state_entropy:.4f}"

        result.violations = violations

        # Unsafe override: if phi or energy below critical absolute thresholds
        if phi < 0.05 or energy < 0.05:
            result.verdict = "POLICY_UNSAFE"
            return result

        # Verdict logic
        if not violations:
            result.verdict = "POLICY_STABLE"
        elif any(k in violations for k in ("cognitive_score", "phi", "energy_efficiency", "suppression_cost")):
            # Major regression if core metric fails
            result.verdict = "POLICY_MAJOR_REGRESSION"
        else:
            result.verdict = "POLICY_MINOR_REGRESSION"

        return result

    @classmethod
    def evaluate_benchmark_metrics(cls, metrics: Any, policy: Optional[RecoveryPolicy] = None) -> RegressionGuardResult:
        """Convenience wrapper that accepts a BenchmarkMetrics object directly."""
        if hasattr(metrics, "model_dump"):
            d = metrics.model_dump()
        elif hasattr(metrics, "__dict__"):
            d = metrics.__dict__
        else:
            d = dict(metrics) if metrics is not None else {}
        return cls.evaluate(d, policy=policy)
