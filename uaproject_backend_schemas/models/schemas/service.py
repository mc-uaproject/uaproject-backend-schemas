from datetime import datetime
from enum import StrEnum
from typing import List, Optional

from uaproject_backend_schemas.awesome.base_model import AwesomeBaseModel


class ServiceCategory(StrEnum):
    DONATION = "donation"
    SERVICE = "service"


class ServiceType(StrEnum):
    ONE_TIME = "one_time"
    SUBSCRIPTION = "subscription"


class ServicePoint(AwesomeBaseModel):
    text: str
    tooltip: Optional[str] = None


class ServiceDiscount(AwesomeBaseModel):
    user_id: Optional[int] = None
    discount_percent: float
    start_date: datetime
    end_date: Optional[datetime] = None
    reason: Optional[str] = None


class ServerAvailabilityMode(StrEnum):
    """How service availability works across servers"""

    ALL = "all"  # Available on all servers simultaneously (e.g., toy)
    SPECIFIC = "specific"  # Only available on specific servers (e.g., survival graylist)
    SELECTABLE = "selectable"  # User selects which server to activate on (e.g., wealth)


class ServerAvailability(AwesomeBaseModel):
    """Configuration for service availability across servers"""

    mode: ServerAvailabilityMode
    servers: Optional[List[str]] = (
        None  # List of servers where available (null = current server only)
    )
