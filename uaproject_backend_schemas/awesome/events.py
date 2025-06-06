from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, List, Type, TypeVar

if TYPE_CHECKING:
    from .model import AwesomeModel

TModel = TypeVar("TModel", bound="AwesomeModel")


class AwesomeEvents(Generic[TModel]):
    """Model event system that allows registering and triggering handlers for events (insert/update)."""

    def __init__(self, model_cls: Type[TModel]):
        self.model_cls = model_cls
        self._listeners: Dict[str, List[Callable[[TModel], Any]]] = {
            "after_insert": [],
            "after_update": [],
        }

    def register(self, event: str, handler: Callable[[TModel], Any]):
        """Register a handler for an event (after_insert, after_update, etc.).
        :param event: event name (string)
        :param handler: function or coroutine to be called when the event occurs
        """
        if event not in self._listeners:
            self._listeners[event] = []
        self._listeners[event].append(handler)

    def list_events(self) -> List[str]:
        """Return a list of all registered event names."""
        return list(self._listeners.keys())

    def get_event_handlers(self, event: str) -> List[Callable]:
        """Get all handlers for a specific event."""
        return self._listeners.get(event, [])

    def has_event(self, event: str) -> bool:
        """Check if event has any handlers."""
        return event in self._listeners and len(self._listeners[event]) > 0

    def get_events_info(self) -> Dict[str, int]:
        """Return information about all events and their handler counts."""
        return {event: len(handlers) for event, handlers in self._listeners.items()}

    def __len__(self) -> int:
        """Return total number of event handlers across all events."""
        return sum(len(handlers) for handlers in self._listeners.values())

    def __contains__(self, event: str) -> bool:
        """Check if event exists (supports 'in' operator)."""
        return event in self._listeners

    def __repr__(self) -> str:
        """String representation of events manager."""
        total_handlers = len(self)
        return f"<AwesomeEvents for {self.model_cls.__name__}: {len(self._listeners)} events, {total_handlers} handlers>"

    async def trigger(self, event: str, instance: TModel):
        """Trigger (asynchronously) the specified event for the given model instance.
        Sequentially runs all Actions subscribed to the event, and then other handlers."""
        if hasattr(self.model_cls, "actions"):
            await self.model_cls.actions._run_event(event, instance)
        if event in self._listeners:
            for handler in list(self._listeners[event]):
                if inspect.iscoroutinefunction(handler):
                    await handler(instance)
                else:
                    handler(instance)
