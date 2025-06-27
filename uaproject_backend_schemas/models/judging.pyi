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
    decision: str
    id: int
    judge: Optional[User]
    judge_id: int
    updated_at: datetime
    verdict: JudgingVerdict
    schemas: JudgingSchemas
    scopes: JudgingScopes
    filter: type[JudgingFilter]
    sort: type[JudgingSort]

class JudgingSchemas:
    """Schemas for the Judging model."""

    create: JudgingSchemaCreate
    response: JudgingSchemaResponse
    update: JudgingSchemaUpdate

class JudgingSchemaCreate(AwesomeBaseModel):
    """create schema for Judging model"""

    decision: str
    verdict: JudgingVerdict
    judge_id: int

class JudgingSchemaResponse(AwesomeBaseModel):
    """response schema for Judging model"""

    updated_at: datetime
    id: int
    judge_id: int
    decision: str
    verdict: JudgingVerdict
    judge: Optional[User]
    claims: list[Claim]

class JudgingSchemaUpdate(AwesomeBaseModel):
    """update schema for Judging model"""

    decision: Optional[str]
    verdict: Optional[JudgingVerdict]

class JudgingScopes:
    """Scopes for the Judging model."""

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
