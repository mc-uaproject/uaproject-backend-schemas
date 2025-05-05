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
