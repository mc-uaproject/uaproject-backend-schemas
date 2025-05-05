from enum import StrEnum


class TransactionType(StrEnum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    PURCHASE = "purchase"
    DONATION = "donation"
    SYSTEM = "system"
    REFUND = "refund"
    ADJUSTMENT = "adjustment"
