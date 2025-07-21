# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Optional

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

    judge: Optional[User]
    id: Optional[int]
    updated_at: Optional[datetime]
    decision: Optional[str]
    claims: Optional[list[Claim]]
    judge_id: Optional[int]
    verdict: Optional[JudgingVerdict]
    created_at: datetime

class JudgingSchemaResponse(AwesomeBaseModel):
    """response schema for Judging model"""

    id: Optional[int]
    updated_at: Optional[datetime]
    decision: str
    judge_id: int
    verdict: JudgingVerdict
    created_at: datetime

class JudgingSchemaUpdate(AwesomeBaseModel):
    """update schema for Judging model"""

    id: Optional[int]
    decision: Optional[str]
    verdict: Optional[JudgingVerdict]
    created_at: datetime

class JudgingFilter(BaseModel):
    """Pydantic-class for filtering the Judging model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[datetime] = None
    max_updated_at: Optional[datetime] = None
    id: Optional[int] = None
    min_id: Optional[int] = None
    max_id: Optional[int] = None
    judge_id: Optional[int] = None
    min_judge_id: Optional[int] = None
    max_judge_id: Optional[int] = None
    decision: Optional[str] = None
    verdict: Optional[JudgingVerdict] = None
    claims_id: Optional[int] = None

class JudgingSort(StrEnum):
    """Enum for sorting the Judging model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
