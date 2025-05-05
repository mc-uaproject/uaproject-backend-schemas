from enum import StrEnum


class ApplicationStatus(StrEnum):
    ACCEPTED = "accepted"
    DECLINED = "declined"
    REVIEW = "review"
    EDITING = "editing"
    NOT_SENT = "not_sent"
