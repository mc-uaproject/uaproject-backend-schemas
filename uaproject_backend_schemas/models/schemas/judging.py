from enum import StrEnum


class JudgingVerdict(StrEnum):
    APPROVED = "approved"
    REJECTED = "rejected"
    PARTIALLY_APPROVED = "partially_approved"
