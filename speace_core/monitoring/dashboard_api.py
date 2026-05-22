"""DashboardAPI — FastAPI application for SPEACE Local Organism Monitor.

Serves read-only HTTP endpoints and WebSocket live updates.
"""

import time
from pathlib import Path
from typing import Any, Dict

from speace_core.cli import SPEACE_VERSION
from speace_core.monitoring.alert_engine import AlertEngine
from speace_core.monitoring.anomaly_panel import AnomalyPanel
from speace_core.monitoring.metrics_bus import MetricsBus
from speace_core.monitoring.organism_state_collector import OrganismStateCollector
from speace_core.monitoring.safety_status import SafetyStatus
from speace_core.monitoring.websocket_server import create_websocket_router

from contextlib import asynccontextmanager

try:
    from fastapi import FastAPI
    from fastapi.staticfiles import StaticFiles

    _HAS_FASTAPI = True
except Exception as exc:  # pragma: no cover
    _HAS_FASTAPI = False
    FastAPI = Any  # type: ignore[misc,assignment]
    StaticFiles = Any  # type: ignore[misc,assignment]
    raise SystemExit(
        "FastAPI / Uvicorn are not installed.\n"
        "Install with: pip install \"speace-core[monitoring]\"\n"
        "or:          pip install fastapi uvicorn websockets"
    ) from exc

# --------------------------------------------------------------------------- #
# Bootstrap
# --------------------------------------------------------------------------- #
_start_time = time.time()

_data_root = Path("data")
_collector = OrganismStateCollector(data_root=str(_data_root))
_safety = SafetyStatus(data_root=str(_data_root))
_anomaly = AnomalyPanel()
_alert_engine = AlertEngine()

# Load genome thresholds if available
_genome_path = Path(__file__).resolve().parent.parent / "dna" / "genome" / "monitoring_dashboard.yaml"
if _genome_path.exists():
    try:
        import yaml

        _cfg = yaml.safe_load(_genome_path.read_text(encoding="utf-8"))
        _md = _cfg.get("monitoring_dashboard", {})
        _thresh = _md.get("anomaly_thresholds", {})
        if _thresh:
            _anomaly = AnomalyPanel(
                coherence_phi_min=_thresh.get("coherence_phi_min", 0.1),
                energy_min=_thresh.get("energy_min", 0.2),
                severity_max=_thresh.get("severity_max", 2.0),
                branching_ratio_deviation=_thresh.get("branching_ratio_deviation", 0.3),
            )
        _alert_thresh = _md.get("alert_thresholds", {})
        if _alert_thresh:
            _alert_engine = AlertEngine(thresholds=_alert_thresh)
    except Exception:
        pass

def _post_process(state: Dict[str, Any]) -> Dict[str, Any]:
    try:
        state["anomaly_panel"] = _anomaly.analyze(state)
    except Exception:
        state["anomaly_panel"] = {"anomalies": [], "overall_status": "unknown", "anomaly_count": 0}
    try:
        alerts = _alert_engine.evaluate(state)
        state["alert_engine"] = {
            "alerts": alerts,
            "health_score": _alert_engine.health_score(state),
        }
    except Exception:
        state["alert_engine"] = {"alerts": [], "health_score": 0.0}
    return state


_metrics_bus = MetricsBus(collector=_collector, interval_ms=1000.0, post_process=_post_process)

_static_dir = Path(__file__).resolve().parent.parent.parent / "web" / "dashboard"
if not _static_dir.exists():
    # Fallback for editable installs where cwd might differ
    _static_dir = Path("web") / "dashboard"

# --------------------------------------------------------------------------- #
# Lifecycle
# --------------------------------------------------------------------------- #


@asynccontextmanager
async def _lifespan(_app: FastAPI):
    _metrics_bus.start()
    yield
    _metrics_bus.stop()


app = FastAPI(
    title="SPEACE Local Organism Monitor",
    description="T101 — Read-only organismic monitoring dashboard",
    version=SPEACE_VERSION,
    lifespan=_lifespan,
)


# --------------------------------------------------------------------------- #
# API — read-only granular endpoints
# --------------------------------------------------------------------------- #


@app.get("/api/health")
async def api_health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "uptime_seconds": int(time.time() - _start_time),
        "speace_version": SPEACE_VERSION,
    }


@app.get("/api/state")
async def api_state() -> Dict[str, Any]:
    state = _metrics_bus.latest()
    if not state:
        state = _collector.collect_all()
        state["timestamp"] = time.time()
    anomalies = _anomaly.analyze(state)
    return {
        **state,
        "anomaly_panel": anomalies,
    }


@app.get("/api/body")
async def api_body() -> Dict[str, Any]:
    return _collector.collect_body()


@app.get("/api/cognition")
async def api_cognition() -> Dict[str, Any]:
    return _collector.collect_cognition()


@app.get("/api/dynamics")
async def api_dynamics() -> Dict[str, Any]:
    return _collector.collect_dynamics()


@app.get("/api/identity")
async def api_identity() -> Dict[str, Any]:
    return _collector.collect_identity()


@app.get("/api/drives")
async def api_drives() -> Dict[str, Any]:
    return _collector.collect_drives()


@app.get("/api/safety")
async def api_safety() -> Dict[str, Any]:
    safety = _safety.evaluate()
    safety["governance_mode"] = "observation_only"
    safety["allow_actuator_commands"] = False
    return safety


# --------------------------------------------------------------------------- #
# T102 — Alerts and Health Score
# --------------------------------------------------------------------------- #


@app.get("/api/alerts")
async def api_alerts(limit: int = 20) -> Dict[str, Any]:
    state = _metrics_bus.latest()
    if not state:
        state = _collector.collect_all()
        state["timestamp"] = time.time()
    alerts = _alert_engine.evaluate(state)
    recent = _alert_engine.recent_alerts(limit=limit)
    return {
        "alerts": alerts,
        "recent_alerts": recent,
        "health_score": _alert_engine.health_score(state),
        "timestamp": time.time(),
    }


@app.get("/api/health_score")
async def api_health_score() -> Dict[str, Any]:
    state = _metrics_bus.latest()
    if not state:
        state = _collector.collect_all()
        state["timestamp"] = time.time()
    return {
        "health_score": _alert_engine.health_score(state),
        "timestamp": time.time(),
    }


# --------------------------------------------------------------------------- #
# WebSocket
# --------------------------------------------------------------------------- #

app.include_router(create_websocket_router(_metrics_bus))

# --------------------------------------------------------------------------- #
# Static frontend (mounted last so API routes take precedence)
# --------------------------------------------------------------------------- #

if _static_dir.exists():
    app.mount("/", StaticFiles(directory=str(_static_dir), html=True), name="dashboard")
