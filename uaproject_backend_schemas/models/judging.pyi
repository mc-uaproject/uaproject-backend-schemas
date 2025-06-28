# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.claim import Claim
from uaproject_backend_schemas.models.schemas.judging import JudgingVerdict
from uaproject_backend_schemas.models.user import User

class Judging(AwesomeModel):
    """Base judging model."""

    claims: list[Claim]
    created_at: datetime
    decision: str
    id: int
    judge: Optional[User]
    judge_id: int
    updated_at: datetime
    verdict: JudgingVerdict
    schemas: JudgingSchemas
    filter: type[JudgingFilter]
    sort: type[JudgingSort]

class JudgingSchemas:
    """Schemas for the Judging model."""

    create: JudgingSchemaCreate
    redis: JudgingSchemaRedis
    response: JudgingSchemaResponse
    update: JudgingSchemaUpdate

class JudgingSchemaCreate(AwesomeBaseModel):
    """create schema for Judging model"""

    decision: str
    verdict: JudgingVerdict
    judge_id: int

class JudgingSchemaRedis(AwesomeBaseModel):
    """redis schema for Judging model"""

    verdict: Optional[JudgingVerdict]
    judge: Optional[User]
    decision: Optional[str]
    judge_id: Optional[int]
    claims: Optional[list[Claim]]
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    id: Optional[int]

class JudgingSchemaResponse(AwesomeBaseModel):
    """response schema for Judging model"""

    verdict: JudgingVerdict
    decision: str
    judge_id: int
    updated_at: Optional[datetime]
    created_at: Optional[datetime]
    id: Optional[int]

class JudgingSchemaUpdate(AwesomeBaseModel):
    """update schema for Judging model"""

    id: Optional[int]
    decision: Optional[str]
    verdict: Optional[JudgingVerdict]

class JudgingFilter(BaseModel):
    """Pydantic-class for filtering the Judging model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    judge_id: Optional[int] = None
    min_judge_id: Optional[Any] = None
    max_judge_id: Optional[Any] = None
    decision: Optional[str] = None
    verdict: Optional[JudgingVerdict] = None
    claims_id: Optional[Any] = None

class JudgingSort(StrEnum):
    """Enum for sorting the Judging model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
