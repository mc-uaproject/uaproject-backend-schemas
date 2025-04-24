from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

__all__ = ["ActionConfigModel", "RelationshipConfigModel", "TemporalFieldConfig"]


class ActionConfigModel(BaseModel):
    """Configuration for webhook actions"""

    type: str
    condition: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None
    user_id: Optional[str] = None
    amount: Optional[str] = None


class RelationshipConfigModel(BaseModel):
    """Configuration for relationship fields"""

    fields: Optional[Union[List[str], BaseModel]] = None
    condition: Optional[str] = None
    condition_value: Optional[Any] = None
    condition_operator: str = "=="


class TemporalFieldConfig(BaseModel):
    """Configuration for fields with temporal state"""

    expires_at_field: str
    status_field: Optional[str] = None
    status_value: Optional[Any] = None
    scope_name: str
