# Import all models
from .application import Application
from .balance import Balance
from .claim import Claim
from .judging import Judging
from .punishment import Punishment
from .punishment_config import PunishmentConfig
from .role import Role
from .service import Service
from .transaction import Transaction
from .user import User
from .user_roles import UserRoles
from .user_token import Token
from .webhook import Webhook

# Update forward references for all models that use string relationships
Application.model_rebuild()
Balance.model_rebuild()
Claim.model_rebuild()
Judging.model_rebuild()
Punishment.model_rebuild()
PunishmentConfig.model_rebuild()
Role.model_rebuild()
Service.model_rebuild()
Transaction.model_rebuild()
UserRoles.model_rebuild()
Token.model_rebuild()
User.model_rebuild()
Webhook.model_rebuild()

__all__ = [
    "Application",
    "Balance",
    "Claim",
    "Judging",
    "Punishment",
    "PunishmentConfig",
    "Role",
    "ServiceTransaction",
    "UserRoles",
    "Token",
    "User",
    "Webhook",
]
