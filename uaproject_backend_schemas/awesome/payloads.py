from typing import Any, Literal

from pydantic import BaseModel


class PayloadBaseModel(BaseModel):
    action: str
    scope: str
    payload: dict[str, Any]


class BothPayloadBaseModel(BaseModel):
    payload: dict[Literal["before", "after"], dict[str, Any]]


PayloadModels = PayloadBaseModel | BothPayloadBaseModel
