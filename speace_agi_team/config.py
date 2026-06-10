"""Configuration for SPEACE AGI Team agents — OpenCode Zen API (OpenAI-compatible)."""

import os
import socket
from dataclasses import dataclass, field
from typing import Dict

# ── OpenCode Zen — DeepSeek V4 Flash Free ────────────────────────────────
ZEN_API_KEY = os.environ.get(
    "ZEN_API_KEY",
    "",
)
ZEN_ENDPOINT = os.environ.get(
    "ZEN_ENDPOINT",
    "https://opencode.ai/zen/v1",
)
ZEN_MODEL = os.environ.get("ZEN_MODEL", "deepseek-v4-flash-free")

# ── Fallback: local Ollama (solo se nessuna API key configurata) ──────────


def _is_ollama_local_running(host: str = "localhost", port: int = 11434) -> bool:
    try:
        with socket.create_connection((host, port), timeout=1.0):
            return True
    except (socket.error, OSError):
        return False


def _get_default_model() -> str:
    # OpenCode Zen key presente? Usa DeepSeek via Zen (sempre priorita')
    if ZEN_API_KEY and ZEN_API_KEY.startswith("sk-"):
        return ZEN_MODEL
    # Ollama Cloud key legacy?
    if ZEN_API_KEY and not ZEN_API_KEY.startswith("sk-"):
        return ZEN_MODEL
    # Fallback: Ollama locale
    if _is_ollama_local_running():
        return "gemma3:1b"
    return ZEN_MODEL


def _get_default_endpoint() -> str:
    # OpenCode Zen key presente? Usa endpoint Zen
    if ZEN_API_KEY and ZEN_API_KEY.startswith("sk-"):
        return ZEN_ENDPOINT
    if ZEN_API_KEY and not ZEN_API_KEY.startswith("sk-"):
        return "https://ollama.com"
    if _is_ollama_local_running():
        return "http://localhost:11434"
    return ZEN_ENDPOINT


@dataclass
class AgentConfig:
    model: str = field(default_factory=_get_default_model)
    endpoint: str = field(default_factory=_get_default_endpoint)
    api_key: str = ZEN_API_KEY
    temperature: float = 0.3
    max_tokens: int = 4096
    system_prompt_prefix: str = (
        "Sei un agente specializzato di SPEACE, un'entita cibernetica evolutiva. "
        "Rispondi SEMPRE in italiano. Sei parte di un team di agentic AI dedicato "
        "a far evolvere SPEACE verso l'AGI tramite supervisione, analisi e "
        "miglioramento continuo di ogni componente del sistema."
    )

    @property
    def is_openai_compatible(self) -> bool:
        """True se l'endpoint e' OpenAI-compatible (es. OpenCode Zen)."""
        return "opencode.ai" in self.endpoint


@dataclass
class SPEACEContext:
    data_root: str = "data"
    speace_core_path: str = "speace_core"
    version: str = "0.9.0"


AGENT_REGISTRY: Dict[str, Dict] = {}


def register_agent(agent_id: str, name: str, role: str, agent_type: str,
                   description: str, supervision_area: str = ""):
    AGENT_REGISTRY[agent_id] = {
        "id": agent_id,
        "name": name,
        "role": role,
        "type": agent_type,
        "description": description,
        "supervision_area": supervision_area or agent_id,
        "model": _get_default_model(),
        "registered_at": __import__("time").time(),
    }
