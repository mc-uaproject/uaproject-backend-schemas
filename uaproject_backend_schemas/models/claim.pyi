# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from pydantic import BaseModel

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.judging import Judging
from uaproject_backend_schemas.models.schemas.claim import ClaimStatus
from uaproject_backend_schemas.models.user import User

class Claim(AwesomeModel):
    """Base claim model."""

    updated_at: datetime
    id: int
    title: str
    description: str
    status: ClaimStatus
    judging_id: Optional[int]
    claimants: Optional[List[User]]
    defendants: Optional[List[User]]
    judging: Optional[Judging]
    schemas: ClaimSchemas
    scopes: ClaimScopes
    filters: ClaimFilters
    sorts: ClaimSorts
    filter: type[ClaimFilter]
    sort: type[ClaimSort]

class ClaimSchemas:
    """Schemas for the Claim model."""

    create: ClaimSchemaCreate
    response: ClaimSchemaResponse
    update: ClaimSchemaUpdate

class ClaimSchemaCreate(AwesomeBaseModel):
    """create schema for Claim model"""

    title: str
    description: str
    claimants: Optional[List[User]]
    defendants: Optional[List[User]]

class ClaimSchemaResponse(AwesomeBaseModel):
    """response schema for Claim model"""

    updated_at: datetime
    id: int
    title: str
    description: str
    status: ClaimStatus
    judging_id: Optional[int]
    claimants: Optional[List[User]]
    defendants: Optional[List[User]]
    judging: Optional[Judging]

class ClaimSchemaUpdate(AwesomeBaseModel):
    """update schema for Claim model"""

    title: str
    description: str
    status: ClaimStatus

class ClaimScopes:
    """Scopes for the Claim model."""

class ClaimFilters:
    """Declarative filters for the Claim model."""

class ClaimFilter(BaseModel):
    """Pydantic-class for filtering the Claim model."""

class ClaimSorts:
    """Declarative sorts for the Claim model."""

class ClaimSort(StrEnum):
    """Enum for sorting the Claim model."""
