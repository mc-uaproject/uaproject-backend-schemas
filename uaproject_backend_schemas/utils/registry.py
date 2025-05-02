from typing import Any, Dict, Type

from uaproject_backend_schemas.awesome.utils import AwesomeActions, AwesomeModel
from uaproject_backend_schemas.models.user import User


class AwesomeRegistry:
    models: Dict[str, Type[AwesomeModel]] = {}

    @classmethod
    def register(cls, model_cls: Type[AwesomeModel]):
        cls.models[model_cls.__name__] = model_cls

    @classmethod
    def get_payload(cls, model_cls: Type[AwesomeModel], scope_name: str):
        return model_cls.schemas.__getattr__(scope_name)

    @classmethod
    async def call_action(cls, event: str, instance: Any):
        await AwesomeActions.call(event, instance)


AwesomeRegistry.register(User)
