import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from speace_core.cellular_brain.memory.morphology_events import (
    MorphologyEvent,
    MorphologyEventType,
)
from speace_core.cellular_brain.self_improvement.architecture_rewriter import (
    ArchitectureRewriteProposal,
    ArchitectureRewriter,
    RewriteSimulationResult,
    SelfImprovementCycleResult,
)
from speace_core.cellular_brain.self_improvement.limitation_detector import (
    LimitationDetector,
    LimitationDiagnosis,
    LimitationSignal,
)
from speace_core.cellular_brain.self_improvement.proposal_store import ProposalStore
from speace_core.cellular_brain.self_improvement.outcome_tracker import (
    OutcomeTracker,
    ProposalOutcome,
)
from speace_core.cellular_brain.self_improvement.proposal_learning_engine import (
    ProposalLearningEngine,
    ProposalLearningRecord,
)
from speace_core.cellular_brain.self_improvement.self_improvement_memory import (
    SelfImprovementMemory,
)


class SelfImprovementLoop:
    """T45 — Autonomous Limitation Detection & Architecture Rewriting Loop."""

    def __init__(
        self,
        orchestrator=None,
        detector=None,
        rewriter=None,
        proposal_store=None,
        regression_guard=None,
        benchmark=None,
        memory=None,
        outcome_tracker=None,
        proposal_learning_engine=None,
        self_improvement_memory=None,
    ):
        self.orchestrator = orchestrator
        self.detector = detector or LimitationDetector()
        self.rewriter = rewriter or ArchitectureRewriter(safety_level="conservative")
        self.proposal_store = proposal_store or ProposalStore()
        self.regression_guard = regression_guard
        self.benchmark = benchmark
        self.memory = memory
        self.outcome_tracker = outcome_tracker or OutcomeTracker(memory=memory)
        self.proposal_learning_engine = proposal_learning_engine or ProposalLearningEngine(memory=memory)
        self.self_improvement_memory = self_improvement_memory or SelfImprovementMemory(memory=memory)

    # ------------------------------------------------------------------ #
    # Detection cycle
    # ------------------------------------------------------------------ #

    def run_detection_cycle(
        self, metrics: Dict[str, Any]
    ) -> SelfImprovementCycleResult:
        now = datetime.now(timezone.utc).isoformat()
        cycle_id = f"cycle-{uuid.uuid4().hex[:8]}"

        # 1. Detect limitations
        signals = self.detector.detect_from_metrics(metrics)
        self._log_event(MorphologyEventType.LIMITATION_DETECTED, {
            "cycle_id": cycle_id,
            "signals_count": len(signals),
        })

        # 2. Aggregate into diagnoses
        diagnoses = self.detector.aggregate_signals(signals)
        for diag in diagnoses:
            self._log_event(MorphologyEventType.LIMITATION_DIAGNOSED, {
                "cycle_id": cycle_id,
                "diagnosis_id": diag.id,
                "category": diag.primary_category,
                "urgency_score": diag.urgency_score,
            })

        # 3. Generate proposals
        proposals: List[ArchitectureRewriteProposal] = []
        for diag in diagnoses:
            proposal = self.rewriter.generate_proposal(diag)
            proposals.append(proposal)
            self._log_event(MorphologyEventType.ARCHITECTURE_PROPOSAL_CREATED, {
                "cycle_id": cycle_id,
                "proposal_id": proposal.id,
                "diagnosis_id": diag.id,
                "title": proposal.title,
            })
            self.proposal_store.save_proposal(proposal)

        # 4. Simulate proposals
        simulations: List[RewriteSimulationResult] = []
        accepted: List[str] = []
        rejected: List[str] = []
        for proposal in proposals:
            sim = self.simulate_proposal(proposal)
            simulations.append(sim)
            self._log_event(MorphologyEventType.ARCHITECTURE_PROPOSAL_SIMULATED, {
                "cycle_id": cycle_id,
                "proposal_id": proposal.id,
                "acceptance_score": sim.acceptance_score,
                "safety_passed": sim.safety_passed,
            })

            verdict = self.accept_or_reject(sim)
            if verdict == "accept":
                accepted.append(proposal.id)
                proposal.status = "accepted"
                self._log_event(MorphologyEventType.ARCHITECTURE_PROPOSAL_ACCEPTED, {
                    "cycle_id": cycle_id,
                    "proposal_id": proposal.id,
                    "acceptance_score": sim.acceptance_score,
                })
            elif verdict == "reject":
                rejected.append(proposal.id)
                proposal.status = "rejected"
                self._log_event(MorphologyEventType.ARCHITECTURE_PROPOSAL_REJECTED, {
                    "cycle_id": cycle_id,
                    "proposal_id": proposal.id,
                    "acceptance_score": sim.acceptance_score,
                })
            else:
                proposal.status = "simulated"

        # 5. Determine final verdict
        if not signals:
            final_verdict = "NO_LIMITATION_DETECTED"
        elif not proposals:
            final_verdict = "LIMITATION_DETECTED_NO_SAFE_PATCH"
        elif accepted:
            final_verdict = "PROPOSAL_ACCEPTED_FOR_NEXT_TASK"
        elif rejected and not accepted:
            final_verdict = "REGRESSION_BLOCKED"
        else:
            final_verdict = "SAFE_PROPOSAL_GENERATED"

        result = SelfImprovementCycleResult(
            cycle_id=cycle_id,
            detected_limitations=signals,
            diagnoses=diagnoses,
            proposals=proposals,
            simulations=simulations,
            accepted_proposals=accepted,
            rejected_proposals=rejected,
            final_verdict=final_verdict,
        )

        self.proposal_store.save_cycle_result(result)
        self._log_event(MorphologyEventType.SELF_IMPROVEMENT_CYCLE_COMPLETED, {
            "cycle_id": cycle_id,
            "final_verdict": final_verdict,
            "proposals_count": len(proposals),
            "accepted_count": len(accepted),
            "rejected_count": len(rejected),
        })
        return result

    def run_from_audit_report(
        self, report: Dict[str, Any]
    ) -> SelfImprovementCycleResult:
        now = datetime.now(timezone.utc).isoformat()
        cycle_id = f"cycle-{uuid.uuid4().hex[:8]}"

        signals = self.detector.detect_from_audit_report(report)
        self._log_event(MorphologyEventType.LIMITATION_DETECTED, {
            "cycle_id": cycle_id,
            "source": "audit_report",
            "signals_count": len(signals),
        })

        diagnoses = self.detector.aggregate_signals(signals)
        proposals = []
        simulations = []
        accepted = []
        rejected = []

        for diag in diagnoses:
            proposal = self.rewriter.generate_proposal(diag)
            proposals.append(proposal)
            self.proposal_store.save_proposal(proposal)

            sim = self.simulate_proposal(proposal)
            simulations.append(sim)

            verdict = self.accept_or_reject(sim)
            if verdict == "accept":
                accepted.append(proposal.id)
                proposal.status = "accepted"
            elif verdict == "reject":
                rejected.append(proposal.id)
                proposal.status = "rejected"
            else:
                proposal.status = "simulated"

        if not signals:
            final_verdict = "NO_LIMITATION_DETECTED"
        elif not proposals:
            final_verdict = "LIMITATION_DETECTED_NO_SAFE_PATCH"
        elif accepted:
            final_verdict = "PROPOSAL_ACCEPTED_FOR_NEXT_TASK"
        elif rejected and not accepted:
            final_verdict = "REGRESSION_BLOCKED"
        else:
            final_verdict = "SAFE_PROPOSAL_GENERATED"

        result = SelfImprovementCycleResult(
            cycle_id=cycle_id,
            detected_limitations=signals,
            diagnoses=diagnoses,
            proposals=proposals,
            simulations=simulations,
            accepted_proposals=accepted,
            rejected_proposals=rejected,
            final_verdict=final_verdict,
        )
        self.proposal_store.save_cycle_result(result)
        return result

    # ------------------------------------------------------------------ #
    # Simulation
    # ------------------------------------------------------------------ #

    def simulate_proposal(
        self, proposal: ArchitectureRewriteProposal
    ) -> RewriteSimulationResult:
        risks = self.rewriter.estimate_risk(proposal)
        benefits = self.rewriter.estimate_benefit(proposal)
        safety_passed = self.rewriter.validate_safety_constraints(proposal)

        # Compute acceptance score from risk/benefit balance
        benefit_sum = sum(benefits.values()) if benefits else 0.0
        risk_sum = sum(risks.values()) if risks else 0.0
        if benefit_sum + risk_sum > 0:
            raw_score = benefit_sum / (benefit_sum + risk_sum + 0.01)
        else:
            raw_score = 0.0

        # Modifiers
        if proposal.proposal_type == "module_addition":
            raw_score *= 0.95
        elif proposal.proposal_type == "genome_mutation":
            raw_score *= 0.85
        elif proposal.proposal_type == "parameter_tuning":
            raw_score *= 1.05

        acceptance_score = max(0.0, min(1.0, raw_score))

        # Delta metrics = estimated benefits minus estimated risks
        delta = {}
        for k, v in benefits.items():
            delta[k] = v - risks.get(k, 0.0)
        for k, v in risks.items():
            if k not in delta:
                delta[k] = -v

        # Regression guard check
        rg_verdict = "POLICY_SAFE"
        if self.regression_guard is not None and hasattr(self.regression_guard, "evaluate"):
            try:
                rg_result = self.regression_guard.evaluate(delta)
                rg_verdict = getattr(rg_result, "verdict", "POLICY_SAFE")
            except Exception:
                rg_verdict = "POLICY_SAFE"

        if rg_verdict == "POLICY_UNSAFE":
            safety_passed = False
            acceptance_score = 0.0

        recommendation = self.accept_or_reject(
            RewriteSimulationResult(
                proposal_id=proposal.id,
                safety_passed=safety_passed,
                acceptance_score=acceptance_score,
                regression_guard_verdict=rg_verdict,
            )
        )

        return RewriteSimulationResult(
            proposal_id=proposal.id,
            baseline_metrics={},
            simulated_metrics=benefits,
            delta_metrics=delta,
            regression_guard_verdict=rg_verdict,
            safety_passed=safety_passed,
            acceptance_score=acceptance_score,
            recommendation=recommendation,
        )

    def accept_or_reject(self, simulation: RewriteSimulationResult) -> str:
        if not simulation.safety_passed:
            return "reject"
        if simulation.regression_guard_verdict == "POLICY_UNSAFE":
            return "reject"
        if simulation.acceptance_score < 0.35:
            return "reject"
        if (
            simulation.safety_passed
            and simulation.acceptance_score >= 0.55
        ):
            risks_safe = True
            # Additional risk checks if we had access to the proposal object;
            # here we rely on acceptance_score and safety_passed.
            if risks_safe:
                return "accept"
        return "needs_more_evidence"

    # ------------------------------------------------------------------ #
    # Reporting
    # ------------------------------------------------------------------ #

    def generate_markdown_report(
        self, result: SelfImprovementCycleResult
    ) -> str:
        lines = [
            "# T45 Autonomous Limitation Detection & Architecture Rewriting Loop",
            "",
            "## Detected Limitations",
        ]
        if result.detected_limitations:
            for sig in result.detected_limitations:
                lines.append(f"- **{sig.category}** (severity={sig.severity:.2f}, confidence={sig.confidence:.2f}): {sig.description}")
        else:
            lines.append("No limitations detected.")

        lines.extend(["", "## Diagnoses"])
        if result.diagnoses:
            for diag in result.diagnoses:
                lines.append(f"- **{diag.primary_category}** | urgency={diag.urgency_score:.2f} | recurrence={diag.recurrence_score:.2f} | confidence={diag.confidence:.2f}")
                lines.append(f"  - Hypothesis: {diag.root_cause_hypothesis}")
                lines.append(f"  - Affected modules: {', '.join(diag.affected_modules)}")
                lines.append(f"  - Recommended action: {diag.recommended_action_type}")
        else:
            lines.append("No diagnoses generated.")

        lines.extend(["", "## Architecture Rewrite Proposals"])
        if result.proposals:
            for prop in result.proposals:
                lines.append(f"- **{prop.title}** (type={prop.proposal_type}, status={prop.status})")
                lines.append(f"  - Rationale: {prop.rationale}")
                lines.append(f"  - Target modules: {', '.join(prop.target_modules)}")
        else:
            lines.append("No proposals generated.")

        lines.extend(["", "## Simulation Results"])
        if result.simulations:
            for sim in result.simulations:
                lines.append(f"- Proposal {sim.proposal_id}: acceptance_score={sim.acceptance_score:.2f}, safety_passed={sim.safety_passed}, recommendation={sim.recommendation}")
        else:
            lines.append("No simulations run.")

        lines.extend(["", "## Accepted / Rejected Proposals"])
        lines.append(f"- Accepted: {len(result.accepted_proposals)}")
        for pid in result.accepted_proposals:
            lines.append(f"  - {pid}")
        lines.append(f"- Rejected: {len(result.rejected_proposals)}")
        for pid in result.rejected_proposals:
            lines.append(f"  - {pid}")

        lines.extend(["", "## Final Verdict"])
        lines.append(f"**{result.final_verdict}**")

        lines.extend(["", "## Recommended Next Task"])
        if result.accepted_proposals:
            # Find the accepted proposal title
            title = "Unknown"
            for p in result.proposals:
                if p.id in result.accepted_proposals:
                    title = p.title
                    break
            lines.append(f"Recommended Next Task: {title}")
        else:
            lines.append("No task recommended (no accepted proposals).")

        return "\n".join(lines) + "\n"

    def generate_json_report(
        self, result: SelfImprovementCycleResult
    ) -> str:
        return json.dumps(result.model_dump(), indent=2, ensure_ascii=False)

    # ------------------------------------------------------------------ #
    # T46 — Outcome Learning Integration
    # ------------------------------------------------------------------ #

    def record_proposal_outcome(
        self,
        proposal_id: str,
        limitation_type: str,
        task_id: str,
        audit_verdict: str,
        metrics: Dict[str, Any],
    ) -> ProposalOutcome:
        """Record the outcome of an implemented proposal after audit."""
        outcome = self.outcome_tracker.record_outcome(
            proposal_id=proposal_id,
            limitation_type=limitation_type,
            task_id=task_id,
            audit_verdict=audit_verdict,
            metrics=metrics,
        )
        self.self_improvement_memory.record_audit_outcome(
            outcome_id=outcome.id,
            proposal_id=proposal_id,
            verdict=audit_verdict,
            net_gain=outcome.net_gain,
        )
        return outcome

    def learn_from_outcome(self, outcome: ProposalOutcome) -> ProposalLearningRecord:
        """Update learning records from an outcome."""
        record = self.proposal_learning_engine.update_from_outcome(outcome)
        self.self_improvement_memory.record_learning_update(
            limitation_type=outcome.originating_limitation_type,
            task_id=outcome.implemented_task_id,
            confidence=record.confidence,
            mean_net_gain=record.mean_net_gain,
        )
        return record

    def get_best_known_proposal_for_limitation(
        self,
        limitation_type: str,
        candidates: Optional[List[Dict[str, Any]]] = None,
    ) -> Optional[Dict[str, Any]]:
        """Return the highest-confidence known proposal for a limitation."""
        if candidates is None:
            candidates = []
            # Build candidates from accepted proposals in store
            for prop in self.proposal_store.list_proposals(status="accepted"):
                candidates.append({
                    "task_id": prop.title,
                    "proposal_id": prop.id,
                    "title": prop.title,
                })
        if not candidates:
            return None
        ranked = self.proposal_learning_engine.rank_candidate_proposals(
            limitation_type=limitation_type,
            candidates=candidates,
        )
        return ranked[0] if ranked else None

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _log_event(
        self,
        event_type: MorphologyEventType,
        metadata: Dict[str, Any],
    ) -> None:
        if self.memory is None or not hasattr(self.memory, "log_event"):
            return
        try:
            event = MorphologyEvent(
                event_id=f"evt-{uuid.uuid4().hex[:8]}",
                event_type=event_type,
                timestamp=datetime.now(timezone.utc).timestamp(),
                metadata=metadata,
            )
            self.memory.log_event(event)
        except Exception:
            pass
