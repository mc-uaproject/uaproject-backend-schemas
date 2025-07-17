from enum import StrEnum


class ClaimStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"
    REJECTED = "rejected"
