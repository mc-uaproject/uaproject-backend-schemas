from typing import Any, Dict, Optional

from pydantic import BaseModel

__all__ = ["ActionConfigModel"]


class ActionConfigModel(BaseModel):
    """Configuration for webhook actions"""

    type: str
    condition: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    amount: Optional[str] = None
