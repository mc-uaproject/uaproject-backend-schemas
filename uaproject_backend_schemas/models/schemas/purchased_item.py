from enum import StrEnum


class PurchasedItemStatus(StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    CANCELLED = "cancelled"
    REPLACED = "replaced"  # For upgraded services
