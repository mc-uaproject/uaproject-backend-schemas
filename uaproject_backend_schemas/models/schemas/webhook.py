from enum import StrEnum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class WebhookStatus(StrEnum):
    ACTIVE = "active"
    PAUSED = "paused"
    ERROR = "error"
    DISABLED = "disabled"


class WebhookEvent(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    GET = "get"
    BULK_CREATE = "bulk_create"
    BULK_UPDATE = "bulk_update"
    BULK_DELETE = "bulk_delete"


class WebhookAuthType(StrEnum):
    """Authorization type for webhook"""

    BEARER = "bearer"
    BASIC = "basic"
    API_KEY = "api_key"
    HMAC = "hmac"
    OAUTH2 = "oauth2"
    CUSTOM = "custom"


class ConditionOperator(StrEnum):
    EQUALS = "eq"
    NOT_EQUALS = "neq"
    GREATER = "gt"
    LESS = "lt"
    GREATER_OR_EQUAL = "gte"
    LESS_OR_EQUAL = "lte"
    IN = "in"
    NOT_IN = "not_in"
    CONTAINS = "contains"
    NOT_CONTAINS = "not_contains"
    STARTS_WITH = "starts_with"
    ENDS_WITH = "ends_with"
    IS_NULL = "is_null"
    IS_NOT_NULL = "is_not_null"
    CHANGED = "changed"
    CHANGED_FROM = "changed_from"
    CHANGED_TO = "changed_to"
    REGEX = "regex"
    BETWEEN = "between"


class WebhookCondition(BaseModel):
    """Condition for triggering webhook"""

    field: str = Field(description="Path to field (supports nesting: 'user.profile.age')")
    operator: ConditionOperator = Field(description="Comparison operator")
    value: Optional[Any] = Field(default=None, description="Value for comparison")
    old_value: Optional[Any] = Field(default=None, description="Old value (for changed_from)")
    case_sensitive: bool = Field(default=True, description="Consider case for strings")
    value_type: Optional[Literal["int", "float", "date", "datetime"]] = Field(
        default=None, description="Value type for correct comparison: int, float, date, datetime"
    )


class WebhookConditionGroup(BaseModel):
    """Group of conditions with logical operator"""

    operator: Literal["AND", "OR", "NOT"] = Field(
        default="AND", description="Logical operator: AND, OR, NOT"
    )
    conditions: List[WebhookCondition] = Field(
        default_factory=list, description="List of conditions"
    )
    groups: Optional[List["WebhookConditionGroup"]] = Field(
        default=None, description="Nested groups of conditions"
    )


class WebhookFieldMapping(BaseModel):
    """Field mapping for sending"""

    source_path: str = Field(
        description="Path to field in model (supports nested: 'user.profile.name')"
    )
    target_field: str = Field(description="Name of field in webhook payload")
    include_old_value: bool = Field(default=False, description="Include old value for update")
    transform: Optional[str] = Field(default=None, description="Name of transformation function")
    default_value: Optional[Any] = Field(
        default=None, description="Default value if field not found"
    )
    aggregate: Optional[Literal["count", "sum", "avg", "min", "max", "list"]] = Field(
        default=None, description="Aggregation for collections: count, sum, avg, min, max, list"
    )
    flatten: bool = Field(default=False, description="Flatten nested objects")


class WebhookTrigger(BaseModel):
    """Config for trigger for model"""

    model_name: str = Field(description="Model name to watch")
    events: List[WebhookEvent] = Field(description="Events to trigger on")

    # Conditions for trigger
    conditions: Optional[WebhookConditionGroup] = Field(
        default=None, description="Conditions for trigger"
    )

    # Fields to send
    fields: List[WebhookFieldMapping] = Field(default_factory=list, description="Field mapping")
    include_all_fields: bool = Field(default=False, description="Include all fields")
    exclude_fields: Optional[List[str]] = Field(default=None, description="Exclude these fields")

    # Additional settings
    include_changes_diff: bool = Field(
        default=True, description="Include diff of changes for update"
    )
    include_metadata: bool = Field(default=True, description="Include metadata of event")

    # Rate limiting and optimization
    rate_limit: Optional[int] = Field(default=None, description="Max number of events per minute")
    batch_delay: Optional[int] = Field(default=None, description="Delay for batching events (ms)")
    batch_size: Optional[int] = Field(default=None, description="Max size of batch")
    debounce_ms: Optional[int] = Field(
        default=None, description="Debounce for frequent changes (ms)"
    )

    # Filters by permissions
    respect_permissions: bool = Field(default=True, description="Respect user permissions")
    filter_fields_by_permissions: bool = Field(
        default=True, description="Filter fields by permissions"
    )


class WebhookPayloadTemplate(BaseModel):
    """Template for payload to send"""

    format: Literal["json", "form-data", "xml", "custom"] = Field(
        default="json", description="Format: json, form-data, xml, custom"
    )
    template: Optional[Dict[str, Any]] = Field(
        default=None, description="Template for structure of data"
    )
    headers: Optional[Dict[str, str]] = Field(default=None, description="Additional headers")
    wrap_in_envelope: bool = Field(
        default=True, description="Wrap in standard envelope with metadata"
    )
    custom_envelope: Optional[Dict[str, Any]] = Field(
        default=None, description="Custom envelope template"
    )
    compression: Optional[Literal["gzip", "deflate"]] = Field(
        default=None, description="Compression: gzip, deflate"
    )
    encryption: Optional[Literal["aes256", "rsa"]] = Field(
        default=None, description="Encryption: aes256, rsa"
    )


class WebhookRetryPolicy(BaseModel):
    """Retry policy"""

    max_attempts: int = Field(default=3, description="Max number of retries", alias="max_retries")
    retry_delay: int = Field(default=60, description="Base delay between retries (seconds)")
    retry_multiplier: float = Field(default=2.0, description="Multiplier for exponential delay")
    max_retry_delay: int = Field(default=3600, description="Max delay between retries (seconds)")
    retry_on_status: List[int] = Field(
        default=[500, 502, 503, 504], description="HTTP statuses to retry on"
    )
    retry_on_timeout: bool = Field(default=True, description="Retry on timeout")


class WebhookLogStatus(StrEnum):
    """Execution status of a webhook log entry"""

    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"


# Fix circular import
WebhookConditionGroup.model_rebuild()
