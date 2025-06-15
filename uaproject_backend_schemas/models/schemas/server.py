from enum import StrEnum


class ServerType(StrEnum):
    """Types of game servers available."""

    SURVIVAL = "survival"
    EVERVAULT = "evervault"


class ServerAccessStatus(StrEnum):
    """Status of user's access to a specific server."""

    NOT_APPLIED = "not_applied"
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"
