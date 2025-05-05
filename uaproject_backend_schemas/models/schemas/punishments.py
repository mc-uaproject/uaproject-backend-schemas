from enum import StrEnum


class PunishmentType(StrEnum):
    WARN = "warn"
    MUTE = "mute"
    BAN = "ban"
    KICK = "kick"
    RESTRICTION = "restriction"


class PunishmentStatus(StrEnum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
