from __future__ import annotations

import asyncio
import inspect
from typing import TYPE_CHECKING, Any, Callable, Dict, Generic, List, Optional, Type, TypeVar

if TYPE_CHECKING:
    from uaproject_backend_schemas.awesome.model import AwesomeModel

TModel = TypeVar("TModel", bound="AwesomeModel")


class AwesomeActions(Generic[TModel]):
    """Model actions manager: registration and execution of Actions."""

    def __init__(self, model_cls: Type[TModel]):
        self.model_cls = model_cls
        self._actions: Dict[str, Callable] = {}
        self._actions_meta: Dict[str, Dict[str, Any]] = {}

    def register(self, name: str, func: Callable[[TModel], Any], events: Optional[List[str]] = None):
        """Register a new action under the specified name.
        :param name: unique action name
        :param func: function or coroutine implementing the action (takes a model instance)
        :param events: optional list of events that trigger the action automatically
        """
        self._actions[name] = func
        self._actions_meta[name] = {
            "func": func,
            "doc": func.__doc__ or "",
            "events": events if events is not None else [],
        }

    def get_action(self, name: str) -> Optional[Callable]:
        """Get action function by name."""
        return self._actions.get(name)

    def list_actions(self) -> List[str]:
        """Return a list of names of all registered actions."""
        return list(self._actions.keys())

    async def run(self, instance: TModel):
        """Asynchronously execute all registered actions for the given model instance."""
        tasks = []
        for name, func in self._actions.items():
            if inspect.iscoroutinefunction(func):
                tasks.append(asyncio.create_task(func(instance)))
            else:
                result = func(instance)
                if result is False:
                    raise Exception(f"Action '{name}' returned False (execution error)")
        if tasks:
            results = await asyncio.gather(*tasks)
            for name, res in zip(self._actions.keys(), results):
                if res is False:
                    raise Exception(f"Action '{name}' returned False (execution error)")

    async def _run_event(self, event: str, instance: TModel):
        """(Internal method) Execute all actions subscribed to the specified event."""
        tasks = []
        for name, meta in self._actions_meta.items():
            if event in meta.get("events", []):
                func = meta["func"]
                if inspect.iscoroutinefunction(func):
                    tasks.append(asyncio.create_task(func(instance)))
                else:
                    result = func(instance)
                    if result is False:
                        raise Exception(f"Action '{name}' failed to execute (returned False) on event {event}")
        if tasks:
            results = await asyncio.gather(*tasks)
            for name, res in zip([n for n, m in self._actions_meta.items() if event in m.get("events", [])], results):
                if res is False:
                    raise Exception(f"Action '{name}' failed to execute (returned False) on event {event}")

    def __iter__(self):
        """Iterate over all registered actions (for convenience, e.g., list(Model.actions))."""
        return iter(self._actions.items())
