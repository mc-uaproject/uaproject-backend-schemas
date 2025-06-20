from .application import Application
from .application_section import ApplicationSection
from .balance import Balance
from .claim import Claim
from .file import File
from .judging import Judging
from .news import News
from .punishment import Punishment
from .punishment_config import PunishmentConfig
from .role import Role
from .service import Service
from .ticket import Ticket
from .ticket_message import TicketMessage
from .transaction import Transaction
from .user import User
from .user_roles import UserRoles
from .user_token import Token
from .webhook import Webhook

Application.model_rebuild()
ApplicationSection.model_rebuild()
Balance.model_rebuild()
Claim.model_rebuild()
File.model_rebuild()
Judging.model_rebuild()
News.model_rebuild()
Punishment.model_rebuild()
PunishmentConfig.model_rebuild()
Role.model_rebuild()
Service.model_rebuild()
Ticket.model_rebuild()
TicketMessage.model_rebuild()
Transaction.model_rebuild()
UserRoles.model_rebuild()
Token.model_rebuild()
User.model_rebuild()
Webhook.model_rebuild()

__all__ = [
    "Application",
    "ApplicationSection",
    "Balance",
    "Claim",
    "File",
    "Judging",
    "News",
    "Punishment",
    "PunishmentConfig",
    "Role",
    "Service",
    "Ticket",
    "TicketMessage",
    "Transaction",
    "UserRoles",
    "Token",
    "User",
    "Webhook",
]
