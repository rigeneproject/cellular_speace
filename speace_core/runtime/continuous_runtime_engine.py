"""ContinuousRuntimeEngine — controlled persistent organism loop (T109).

Wraps CellularBrainOrchestrator in a long-running asyncio loop with
circadian phases, health monitoring, checkpointing, safe degradation,
and emergency halt. All governance flags are read-only; the runtime never
modifies source code, executes shell commands, or accesses the internet.
"""

import asyncio
import time
from typing import Any, Dict, Optional

from speace_core.cellular_brain.organism.organism_lifecycle import OrganismLifecycleManager
from speace_core.runtime.checkpoint_manager import CheckpointManager
from speace_core.runtime.circadian_scheduler import CircadianScheduler
from speace_core.runtime.emergency_halt_gate import EmergencyHaltGate
from speace_core.runtime.recovery_orchestrator import RecoveryOrchestrator
from speace_core.runtime.runtime_health_monitor import RuntimeHealthMonitor
from speace_core.runtime.safe_degradation_handler import SafeDegradationHandler
from speace_core.cellular_brain.experience.temporal_narrative_engine import TemporalNarrativeEngine
from speace_core.cellular_brain.experience.session_continuity_manager import SessionContinuityManager


class ContinuousRuntimeEngine:
    """Manages the persistent organism runtime loop."""

    STATES = ("initializing", "running", "paused", "sleeping", "halting", "halted")

    def __init__(
        self,
        orchestrator: Any,
        tick_interval: float = 1.0,
        checkpoint_interval_seconds: float = 300.0,
        awake_duration: float = 300.0,
        sleep_duration: float = 60.0,
        runtime_health_config: Optional[Dict[str, Any]] = None,
        emergency_halt_config: Optional[Dict[str, Any]] = None,
        degradation_config: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.orchestrator = orchestrator
        self.tick_interval = tick_interval
        self.checkpoint_interval_seconds = checkpoint_interval_seconds

        # Narrative / continuity
        self.narrative_engine = TemporalNarrativeEngine()
        self.session_continuity = SessionContinuityManager()

        # Subsystems
        self.checkpoint_manager = CheckpointManager()
        self.circadian = CircadianScheduler(
            awake_duration=awake_duration,
            sleep_duration=sleep_duration,
            narrative_engine=self.narrative_engine,
        )
        self.health_monitor = RuntimeHealthMonitor(
            target_tick_interval=tick_interval,
            **(runtime_health_config or {}),
        )
        self.degradation_handler = SafeDegradationHandler(
            narrative_engine=self.narrative_engine,
            **(degradation_config or {}),
        )
        self.halt_gate = EmergencyHaltGate(
            checkpoint_manager=self.checkpoint_manager,
            narrative_engine=self.narrative_engine,
            **(emergency_halt_config or {}),
        )
        self.recovery = RecoveryOrchestrator(
            checkpoint_manager=self.checkpoint_manager,
            narrative_engine=self.narrative_engine,
            session_continuity=self.session_continuity,
        )

        # Lifecycle (external to orchestrator)
        self.lifecycle = OrganismLifecycleManager(initial_state="initializing")

        # Runtime state
        self._state: str = "initializing"
        self._task: Optional[asyncio.Task] = None
        self._last_checkpoint_at: float = 0.0
        self._tick_count_since_start: int = 0
        self._started_at: float = 0.0

    # ------------------------------------------------------------------ #
    # Lifecycle control
    # ------------------------------------------------------------------ #

    async def start(self) -> Dict[str, Any]:
        """Initialize and begin the runtime loop."""
        self._state = "initializing"
        self._started_at = time.time()

        # Attempt recovery from checkpoint
        recovery_info = self.recovery.boot(self.orchestrator)
        if recovery_info["status"] == "recovered":
            self._tick_count_since_start = recovery_info.get("tick", 0)

        # Transition lifecycle to active
        self.lifecycle.transition_to("active", reason="runtime_start")

        # Enable key organismic subsystems for T109
        self.orchestrator.sleep_enabled = True
        self.orchestrator.brainstem_controller_enabled = True
        self.orchestrator.global_workspace_enabled = True
        self.orchestrator.temporal_dynamics_enabled = True
        self.orchestrator.neural_oscillator_enabled = True
        self.orchestrator.phase_coupling_enabled = True
        self.orchestrator.energy_field_enabled = True
        self.orchestrator.predictive_coding_enabled = True
        self.orchestrator.active_inference_enabled = True
        self.orchestrator.global_homeostatic_drive_enabled = True
        self.orchestrator.criticality_monitor_enabled = True

        self._state = "running"
        self._task = asyncio.create_task(self._loop())

        self.narrative_engine.record(
            event_type="runtime_start",
            description="Continuous runtime engine started.",
            importance=7,
            metadata={
                "tick_interval": self.tick_interval,
                "checkpoint_interval": self.checkpoint_interval_seconds,
                "recovery_status": recovery_info["status"],
            },
        )

        return {
            "state": self._state,
            "recovery": recovery_info,
            "resume_narrative": self.recovery.resume_narrative(),
        }

    async def pause(self) -> None:
        if self._state == "running":
            self._state = "paused"
            self.narrative_engine.record(
                event_type="runtime_pause",
                description="Runtime paused by operator.",
                importance=5,
            )

    async def resume(self) -> None:
        if self._state == "paused":
            self._state = "running"
            self.narrative_engine.record(
                event_type="runtime_resume",
                description="Runtime resumed by operator.",
                importance=5,
            )
        elif self._state == "halted":
            self.halt_gate.reset()
            self._state = "running"
            self.narrative_engine.record(
                event_type="runtime_resume",
                description="Runtime resumed from halted state by operator.",
                importance=6,
            )
            if self._task is None or self._task.done():
                self._task = asyncio.create_task(self._loop())

    async def halt(self) -> None:
        if self._state in ("running", "paused", "sleeping"):
            self._state = "halting"
            self.narrative_engine.record(
                event_type="runtime_halt_requested",
                description="Halt requested by operator.",
                importance=6,
            )
            # Let the loop handle graceful shutdown on next iteration

    async def force_checkpoint(self) -> Dict[str, Any]:
        cp = self.checkpoint_manager.save(
            orchestrator=self.orchestrator,
            runtime_state=self._state,
            circadian_phase=self.circadian.phase,
        )
        self._last_checkpoint_at = time.time()
        return cp

    async def stop(self) -> None:
        self._state = "halting"
        if self._task and not self._task.done():
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        # Final checkpoint
        try:
            self.checkpoint_manager.save(
                orchestrator=self.orchestrator,
                runtime_state="halted",
                circadian_phase=self.circadian.phase,
            )
        except Exception:
            pass
        self._state = "halted"
        self._task = None

    # ------------------------------------------------------------------ #
    # Main loop
    # ------------------------------------------------------------------ #

    async def _loop(self) -> None:
        try:
            while self._state not in ("halted", "halting"):
                if self._state == "paused":
                    await asyncio.sleep(self.tick_interval)
                    continue

                loop_start = time.time()

                # Circadian phase tick
                phase = self.circadian.tick()
                is_sleeping = self.circadian.is_sleeping()
                if is_sleeping and self._state != "sleeping":
                    self._state = "sleeping"
                elif not is_sleeping and self._state == "sleeping":
                    self._state = "running"

                # Orchestrator tick
                tick_latency_start = time.time()
                try:
                    await self.orchestrator._tick()
                    self._tick_count_since_start += 1
                    self.health_monitor.record_tick(
                        latency_ms=(time.time() - tick_latency_start) * 1000.0
                    )
                except Exception:
                    self.health_monitor.record_exception()

                # Memory RSS (best effort)
                try:
                    import psutil
                    proc = psutil.Process()
                    self.health_monitor.update_memory(proc.memory_info().rss / (1024 * 1024))
                except Exception:
                    pass

                # Brainstem state extraction
                brainstem_state = self._brainstem_state()

                # Emergency halt evaluation
                halt_reason = self.halt_gate.evaluate(
                    runtime_health=self.health_monitor.snapshot(),
                    brainstem_state=brainstem_state,
                    memory_rss_mb=self.health_monitor._peak_memory_rss_mb,
                    orchestrator=self.orchestrator,
                    runtime_state=self._state,
                    circadian_phase=phase,
                )
                if halt_reason is not None:
                    self._state = "halted"
                    break

                # Safe degradation
                if self.health_monitor.is_degraded():
                    self.degradation_handler.evaluate(
                        runtime_health=self.health_monitor.snapshot(),
                        brainstem_state=brainstem_state,
                        orchestrator=self.orchestrator,
                    )

                # Periodic checkpoint
                if (time.time() - self._last_checkpoint_at) >= self.checkpoint_interval_seconds:
                    try:
                        self.checkpoint_manager.save(
                            orchestrator=self.orchestrator,
                            runtime_state=self._state,
                            circadian_phase=phase,
                        )
                        self._last_checkpoint_at = time.time()
                    except Exception:
                        pass

                # Session continuity save
                try:
                    self.session_continuity.save({
                        "active_human": getattr(self, "_active_human", None),
                        "last_topic": getattr(self, "_last_topic", None),
                        "tick_count": self._tick_count_since_start,
                        "runtime_state": self._state,
                        "circadian_phase": phase,
                    })
                except Exception:
                    pass

                # Sleep until next tick
                elapsed = time.time() - loop_start
                sleep_time = max(0.0, self.tick_interval - elapsed)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)

        except asyncio.CancelledError:
            pass
        finally:
            if self._state == "halting":
                self._state = "halted"

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def _brainstem_state(self) -> str:
        ctrl = getattr(self.orchestrator, "_brainstem_controller", None)
        if ctrl is None:
            return "unknown"
        # BrainstemFunctionalController stores state in .last_state or ._current_state
        if hasattr(ctrl, "last_state"):
            return str(ctrl.last_state.state)
        if hasattr(ctrl, "_current_state"):
            return str(ctrl._current_state)
        return "unknown"

    # ------------------------------------------------------------------ #
    # Snapshot
    # ------------------------------------------------------------------ #

    def snapshot(self) -> Dict[str, Any]:
        return {
            "state": self._state,
            "tick_count": getattr(self.orchestrator, "current_tick", 0),
            "ticks_since_start": self._tick_count_since_start,
            "uptime_seconds": time.time() - self._started_at if self._started_at else 0,
            "tick_interval": self.tick_interval,
            "circadian": self.circadian.phase_context(),
            "health": self.health_monitor.snapshot(),
            "lifecycle": self.lifecycle.snapshot(),
            "halt": self.halt_gate.snapshot(),
            "degradation": self.degradation_handler.summary(),
            "recovery": self.recovery.snapshot(),
        }
