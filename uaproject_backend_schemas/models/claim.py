from typing import List, Optional

from sqlmodel import BigInteger, Column, Enum, ForeignKey, Relationship, Table

from uaproject_backend_schemas.awesome.fields import AwesomeField
from uaproject_backend_schemas.awesome.mixins import IDMixin, TimestampsMixin
from uaproject_backend_schemas.awesome.model import AwesomeModel
from uaproject_backend_schemas.models.judging import Judging
from uaproject_backend_schemas.models.user import User


class ClaimStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    REJECTED = "rejected"


claim_claimant_link = Table(
    "claim_claimant_link",
    AwesomeModel.metadata,
    Column("claim_id", BigInteger, ForeignKey("claims.id"), primary_key=True),
    Column("user_id", BigInteger, ForeignKey("users.id"), primary_key=True),
)

claim_defendant_link = Table(
    "claim_defendant_link",
    AwesomeModel.metadata,
    Column("claim_id", BigInteger, ForeignKey("claims.id"), primary_key=True),
    Column("user_id", BigInteger, ForeignKey("users.id"), primary_key=True),
)


class Claim(AwesomeModel, IDMixin, TimestampsMixin, table=True):
    __tablename__ = "claims"
    __scope_prefix__ = "claim"
    model_config = {"arbitrary_types_allowed": True}

    title: str = AwesomeField(max_length=255, nullable=False)
    description: Optional[str] = AwesomeField(max_length=2000, nullable=True)
    status: ClaimStatus = AwesomeField(
        sa_column=Column(
            Enum(ClaimStatus, native_enum=False),
            default=ClaimStatus.OPEN,
            server_default=ClaimStatus.OPEN,
        )
    )
    judging_id: Optional[int] = AwesomeField(
        sa_column=Column(BigInteger, ForeignKey("judgings.id"), nullable=True)
    )

    claimants: List[User] = Relationship(
        sa_relationship=claim_claimant_link,
        back_populates="claims_as_claimant",
        sa_relationship_kwargs={"secondary": claim_claimant_link},
    )
    defendants: List[User] = Relationship(
        sa_relationship=claim_defendant_link,
        back_populates="claims_as_defendant",
        sa_relationship_kwargs={"secondary": claim_defendant_link},
    )
    judging: Optional[Judging] = Relationship(back_populates="claims")
