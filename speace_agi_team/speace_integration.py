"""SPEACE Integration — avvia il team AGI automaticamente col cervello SPEACE.

Chiamata da ``LiveOrganism.run()`` nella fase di post-accensione,
avvia in background il web server FastAPI del team AGI (porta 8686)
e lo collega al contesto vivo dell'organismo.
"""

from __future__ import annotations

import logging
import threading
from typing import Any, Optional

_agi_thread: Optional[threading.Thread] = None
_server: Optional[Any] = None

logger = logging.getLogger("speace.agi_team")


def start_agi_team(
    host: str = "127.0.0.1",
    port: int = 8686,
    runtime: Any = None,
    orchestrator: Any = None,
) -> bool:
    """Avvia il team AGI in un thread background.

    Se il server e' gia' avviato, non fa nulla.

    Args:
        host: Host per il web server.
        port: Porta per il web server.
        runtime: Riferimento al runtime engine (per contesto vivo).
        orchestrator: Riferimento all'orchestrator (per contesto vivo).

    Returns:
        True se avviato, False se gia' in esecuzione.
    """
    global _agi_thread, _server

    if _agi_thread is not None and _agi_thread.is_alive():
        logger.info("AGI Team gia' attivo su http://%s:%d", host, port)
        return False

    try:
        import uvicorn
        from speace_agi_team.web_server import app

        # Espone il runtime e orchestrator sull'app per contesto vivo
        app.state.speace_runtime = runtime
        app.state.speace_orchestrator = orchestrator

        config = uvicorn.Config(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=False,
        )
        server = uvicorn.Server(config)
        _server = server  # salva riferimento per stop_agi_team()

        def _run():
            try:
                server.run()
            except Exception as exc:
                logger.error("AGI Team server fallito: %s", exc)

        _agi_thread = threading.Thread(
            target=_run, name="AGI-Team", daemon=True
        )
        _agi_thread.start()
        logger.info(
            "AGI Team avviato su http://%s:%d con modello DeepSeek V4 Flash Free",
            host,
            port,
        )
        return True

    except Exception as exc:
        logger.warning("AGI Team non avviato: %s", exc)
        return False


def stop_agi_team() -> None:
    """Arresta il team AGI (se in esecuzione)."""
    global _agi_thread, _server
    if _server is not None:
        _server.should_exit = True
        _server = None
    if _agi_thread is not None and _agi_thread.is_alive():
        logger.info("Arresto AGI Team...")
        _agi_thread = None
