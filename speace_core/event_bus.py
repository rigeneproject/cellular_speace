import asyncio
from typing import Callable, Dict, List

import structlog

from speace_core.cellular_brain.base.digital_signal import DigitalSignal

logger = structlog.get_logger(__name__)


class EventBus:
    def __init__(self):
        self._subscribers: Dict[str, List[Callable[[DigitalSignal], None]]] = {}

    def subscribe(self, channel: str, handler: Callable[[DigitalSignal], None]) -> None:
        self._subscribers.setdefault(channel, []).append(handler)

    def unsubscribe(self, channel: str, handler: Callable[[DigitalSignal], None]) -> None:
        if channel in self._subscribers:
            try:
                self._subscribers[channel].remove(handler)
            except ValueError:
                pass

    async def publish(self, channel: str, signal: DigitalSignal) -> None:
        handlers = self._subscribers.get(channel, [])
        if handlers:
            await asyncio.gather(
                *(self._safe_dispatch(h, signal) for h in handlers),
                return_exceptions=True,
            )

    async def _safe_dispatch(
        self, handler: Callable[[DigitalSignal], None], signal: DigitalSignal
    ) -> None:
        try:
            result = handler(signal)
            if asyncio.isawaitable(result):
                await result
        except Exception:
            logger.exception("event_bus_dispatch_failed", handler=handler.__name__)
