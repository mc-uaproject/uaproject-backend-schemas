import base64
import secrets
from datetime import datetime, timezone
from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from pydantic import model_validator
from sqlalchemy import BigInteger
from sqlmodel import Column, ForeignKey, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.awesome.schemas import SchemaDefinition

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.user import User


def generate_session_token() -> str:
    """Generate a Discord-like session token."""
    random_bytes = secrets.token_bytes(32)

    token = base64.urlsafe_b64encode(random_bytes).decode("ascii").rstrip("=")

    return f"ua_{token}"


def generate_bot_token() -> str:
    """Generate a bot token with different prefix."""
    random_bytes = secrets.token_bytes(32)
    token = base64.urlsafe_b64encode(random_bytes).decode("ascii").rstrip("=")
    return f"bot_{token}"


class TokenType(StrEnum):
    """Token type enumeration."""

    SESSION = "session"
    BOT = "bot"


class SessionToken(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "session_tokens"
    __scope_prefix__ = "session"

    session_id: str = AwesomeField(
        default_factory=lambda: generate_session_token(), unique=True, nullable=False
    )
    user_id: int = AwesomeField(sa_column=Column(BigInteger, ForeignKey("users.id")))
    user: "User" = Relationship(back_populates="sessions")

    expires_at: datetime = AwesomeField(nullable=False)
    last_used_at: Optional[datetime] = AwesomeField()
    revoked: bool = AwesomeField(default=False)

    ip_address: Optional[str] = AwesomeField(default=None, max_length=64)
    user_agent: Optional[str] = AwesomeField(default=None, max_length=512)
    device_id: Optional[str] = AwesomeField(default=None, max_length=128)

    login_method: str = AwesomeField(default="discord")
    is_bot: bool = AwesomeField(default=False)
    token_type: TokenType = AwesomeField(default=TokenType.SESSION)

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, values: dict) -> dict:
        if isinstance(values, dict):
            if expires_at := values.get("expires_at"):
                if isinstance(expires_at, datetime) and expires_at <= datetime.now(timezone.utc):
                    is_bot = values.get("is_bot", False)
                    token_type = values.get("token_type", TokenType.SESSION)

                    if not is_bot and token_type == TokenType.SESSION:
                        raise ValueError("expires_at must be in the future")
        return values

    def is_expired(self) -> bool:
        """Check if the session token is expired."""
        if self.expires_at is None:
            return False
        return datetime.now(timezone.utc) > self.expires_at

    def is_active(self) -> bool:
        """Check if the session token is active (not revoked and not expired)."""
        return not self.revoked and not self.is_expired()

    def update_last_used(self) -> None:
        """Update the last_used_at timestamp to current time."""
        self.last_used_at = datetime.now(timezone.utc)

    def revoke(self) -> None:
        """Revoke the session token."""
        self.revoked = True

    def is_bot_token(self) -> bool:
        """Check if this is a bot token."""
        return self.is_bot or self.token_type == TokenType.BOT

    def is_permanent(self) -> bool:
        """Check if this token is permanent (bot or API token)."""
        return self.is_bot_token() and self.expires_at is None

    def get_token_prefix(self) -> str:
        """Get token prefix based on type."""
        if self.is_bot:
            return "bot_"
        else:
            return "session_"

    def get_public_id(self) -> str:
        """Get public identifier for API usage."""
        return self.session_id

    @classmethod
    def create_bot_token(cls, user_id: int, **kwargs) -> "SessionToken":
        """Create a bot token that never expires."""
        return cls(
            user_id=user_id,
            is_bot=True,
            token_type=TokenType.BOT,
            session_id=generate_bot_token(),
            expires_at=None,
            login_method="bot",
            **kwargs,
        )

    class Schemas(AwesomeModel.Schemas):
        class Create(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "last_used_at", "revoked"]
            optional = True
            permissions = [".write"]

        class CreateBot(SchemaDefinition):
            fields_exclude = [
                "id",
                "created_at",
                "updated_at",
                "last_used_at",
                "revoked",
                "expires_at",
            ]
            optional = True
            permissions = [".admin"]

        class Update(SchemaDefinition):
            fields_exclude = ["id", "created_at", "updated_at", "session_id", "user_id"]
            optional = True
            permissions = [".write"]

        class Response(SchemaDefinition):
            fields = [
                "id",
                "session_id",
                "user_id",
                "created_at",
                "expires_at",
                "last_used_at",
                "revoked",
                "ip_address",
                "user_agent",
                "device_id",
                "login_method",
            ]
            permissions = [".read.own"]

        class AdminResponse(SchemaDefinition):
            fields = [
                "id",
                "session_id",
                "user_id",
                "created_at",
                "expires_at",
                "last_used_at",
                "revoked",
                "ip_address",
                "user_agent",
                "device_id",
                "login_method",
            ]
            permissions = [".admin"]
