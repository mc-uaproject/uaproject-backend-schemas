# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.judging import Judging
from uaproject_backend_schemas.models.schemas.claim import ClaimStatus
from uaproject_backend_schemas.models.user import User

class Claim(AwesomeModel):
    """Base claim model."""

    claimants: list[User]
    created_at: datetime
    defendants: list[User]
    description: str
    id: int
    judging: Optional[Judging]
    judging_id: Optional[int]
    status: ClaimStatus
    title: str
    updated_at: datetime
    schemas: ClaimSchemas
    filter: type[ClaimFilter]
    sort: type[ClaimSort]

class ClaimSchemas:
    """Schemas for the Claim model."""

    create: ClaimSchemaCreate
    redis: ClaimSchemaRedis
    response: ClaimSchemaResponse
    update: ClaimSchemaUpdate

class ClaimSchemaCreate(AwesomeBaseModel):
    """create schema for Claim model"""

    title: str
    description: str
    claimants: Optional[list[User]]
    defendants: Optional[list[User]]

class ClaimSchemaRedis(AwesomeBaseModel):
    """redis schema for Claim model"""

    judging: Optional[Judging]
    status: Optional[ClaimStatus]
    judging_id: Optional[int]
    claimants: Optional[list[User]]
    updated_at: Optional[datetime]
    defendants: Optional[list[User]]
    title: Optional[str]
    description: Optional[str]
    id: Optional[int]
    created_at: Optional[datetime]

class ClaimSchemaResponse(AwesomeBaseModel):
    """response schema for Claim model"""

    status: ClaimStatus
    judging_id: Optional[int]
    updated_at: Optional[datetime]
    title: str
    description: str
    id: Optional[int]
    created_at: Optional[datetime]

class ClaimSchemaUpdate(AwesomeBaseModel):
    """update schema for Claim model"""

    id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    status: Optional[ClaimStatus]

class ClaimFilter(BaseModel):
    """Pydantic-class for filtering the Claim model."""

    updated_at: Optional[datetime] = None
    min_updated_at: Optional[Any] = None
    max_updated_at: Optional[Any] = None
    id: Optional[int] = None
    min_id: Optional[Any] = None
    max_id: Optional[Any] = None
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[ClaimStatus] = None
    judging_id: Optional[int] = None
    min_judging_id: Optional[Any] = None
    max_judging_id: Optional[Any] = None
    claimants_id: Optional[Any] = None
    defendants_id: Optional[Any] = None

class ClaimSort(StrEnum):
    """Enum for sorting the Claim model."""

    ID = "id"
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
