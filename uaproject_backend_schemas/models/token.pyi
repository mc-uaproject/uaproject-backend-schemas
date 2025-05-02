# AUTO-GENERATED FILE. DO NOT EDIT MANUALLY.

from datetime import datetime
from typing import Literal
from uuid import UUID

from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.utils import AwesomeBaseModel
from uaproject_backend_schemas.models.user_token import Token

class Token(AwesomeModel):
    """Base user model."""

    schemas: TokenSchemas
    scopes: TokenScopes

class TokenSchemas:
    """Schemas for the user model."""

class TokenScopes:
    """Visibility scopes for the user model."""

    full: TokenScopeFull

class TokenScopeFull(AwesomeBaseModel):
    """full visibility scope for Token model"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int

class TokenScopeFullWithPermissions(AwesomeBaseModel):
    """full visibility scope for Token model with permissions"""

    id: int
    updated_at: datetime
    token: UUID
    user_id: int

class TokenScopeFullWithPermissionsTokenWrite(AwesomeBaseModel):
    """full visibility scope for Token model with permissions token.write"""

    token: UUID

class TokenScopeFullWithPermissionsTokenRead(AwesomeBaseModel):
    """full visibility scope for Token model with permissions token.read"""

    token: UUID

    def with_permissions(
        self, permissions: list[Literal["token.write", "token.read"]]
    ) -> (
        TokenScopeFullWithPermissionsTokenWrite
        | TokenScopeFullWithPermissionsTokenRead
        | TokenScopeFullWithPermissions
    ): ...
