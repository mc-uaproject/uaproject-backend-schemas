from typing import TYPE_CHECKING, List, Optional

from sqlmodel import BigInteger, Column, Enum, ForeignKey, Relationship

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.user import User

if TYPE_CHECKING:
    from uaproject_backend_schemas.models.claim import Claim


class JudgingVerdict(str, Enum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PARTIALLY_APPROVED = "partially_approved"


class Judging(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "judgings"
    __scope_prefix__ = "judging"
    model_config = {"arbitrary_types_allowed": True}

    judge_id: int = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("users.id"), nullable=False)
    )
    decision: str = AwesomeField(max_length=2000, nullable=False)
    verdict: JudgingVerdict = AwesomeField(
        sa_column=Column(Enum(JudgingVerdict, native_enum=False))
    )

    judge: Optional[User] = Relationship()
    claims: List["Claim"] = Relationship(back_populates="judging")
