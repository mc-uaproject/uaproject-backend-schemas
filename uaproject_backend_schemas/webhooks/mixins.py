import logging
from datetime import datetime
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    NamedTuple,
    Optional,
    Set,
    TypedDict,
    Union,
)

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from uaproject_backend_schemas.webhooks.schemas import WebhookStage

__all__ = [
    "WebhookScopeFields",
    "PayloadType",
    "WebhookPayloadMixin",
    "RelationshipConfig",
    "TemporalFieldConfig",
    "ChangeSet",
]


logger = logging.getLogger(__name__)


class RelationshipConfig(BaseModel):
    fields: Optional[List[str] | BaseModel] = None
    condition: Optional[str] = None
    condition_value: Optional[Any] = None
    condition_operator: str = "=="


class TemporalFieldConfig(BaseModel):
    """Configuration for fields with temporal state"""

    expires_at_field: str
    status_field: Optional[str] = None
    status_value: Optional[Any] = None
    scope_name: str


class WebhookScopeFields(BaseModel):
    trigger_fields: List[str]
    fields: Optional[List[str]] = None
    stage: WebhookStage = WebhookStage.AFTER
    relationships: Optional[Dict[str, RelationshipConfig]] = None
    temporal_fields: Optional[List[TemporalFieldConfig]] = None


PayloadType = Union[Dict[str, Any], Dict[Literal["before", "after"], Dict[str, Any]]]


class FieldChange(TypedDict):
    before: Any
    after: Any


class ChangeSet(NamedTuple):
    """Structure containing categorized field changes"""

    changed: Dict[str, FieldChange]
    untracked: Dict[str, FieldChange]
    unchanged: Dict[str, Any]


class WebhookPayloadMixin:
    """A mixin that adds webhook functionality to a model"""

    __scope_prefix__ = ""
    _temporal_expiration_callbacks = {}

    @classmethod
    def get_webhook_scopes(cls) -> Dict[str, WebhookScopeFields]:
        """Get webhook scopes for this specific class"""
        if not hasattr(cls, "_webhook_scopes_registry"):
            cls._webhook_scopes_registry = {}
        return cls._webhook_scopes_registry

    @classmethod
    def register_temporal_expiration_callback(
        cls, callback: Callable[[int, str, Dict[str, FieldChange]], None]
    ) -> None:
        """
        Register a callback function that will be called when a temporal field expires

        Args:
            callback: A function that takes (instance_id, scope_name, changes) as parameters
        """
        cls._temporal_expiration_callbacks[cls.__name__] = callback

    @classmethod
    def register_scope(
        cls,
        scope_name: str,
        trigger_fields: List[str] | Set[str],
        fields: List[str] | Set[str] | BaseModel | None = None,
        relationships: Dict[str, Dict[str, Any]] | None = None,
        stage: WebhookStage = WebhookStage.AFTER,
        temporal_fields: List[Dict[str, Any]] | None = None,
    ) -> None:
        """
        Register a new scope for the model with specified
        trigger fields, optional payload fields and relationships.

        Args:
            scope_name: Unique identifier for the scope
            trigger_fields: Fields that will trigger the webhook when modified
            fields: Optional specific fields to include in the payload.
                   If None, all fields will be included. Can also be a Pydantic BaseModel.
            relationships: Optional dictionary mapping relationship names to their configurations
            stage: WebhookStage indicating when the webhook should be triggered
            temporal_fields: Optional list of temporal field configurations
        """
        scope_name = f"{cls.__scope_prefix__}.{scope_name}"
        scopes = cls.get_webhook_scopes()

        if scope_name in scopes:
            raise ValueError(f"Scope '{scope_name}' is already registered for {cls.__name__}")

        trigger_fields_set = set(trigger_fields)
        fields_set = cls._process_fields(fields)

        cls._validate_trigger_fields(trigger_fields_set)
        cls._validate_payload_fields(fields_set, relationships)

        relationship_configs = cls._process_relationships(relationships)
        temporal_field_configs = cls._process_temporal_fields(temporal_fields)

        scopes[scope_name] = WebhookScopeFields(
            trigger_fields=list(trigger_fields_set),
            fields=list(fields_set) if fields_set else None,
            relationships=relationship_configs,
            stage=stage,
            temporal_fields=temporal_field_configs,
        )

    @classmethod
    def _process_fields(cls, fields) -> Optional[Set[str]]:
        """Process and return fields as a set."""
        if isinstance(fields, BaseModel):
            return set(fields.model_fields.keys())
        return set(fields) if fields is not None else None

    @classmethod
    def _validate_trigger_fields(cls, trigger_fields_set: Set[str]) -> None:
        """Validate trigger fields against model fields."""
        model_fields = set(cls.__table__.columns.keys())
        if invalid_triggers := trigger_fields_set - model_fields:
            raise ValueError(f"Invalid trigger fields for {cls.__name__}: {invalid_triggers}")

    @classmethod
    def _validate_payload_fields(
        cls, fields_set: Optional[Set[str]], relationships: Optional[Dict]
    ) -> None:
        """Validate payload fields and relationships."""
        if fields_set is not None:
            fields_to_check = fields_set.copy()
            relationship_names = set()

            if relationships:
                relationship_names = set(relationships.keys())
                fields_to_check = fields_set - relationship_names

            model_fields = set(cls.__table__.columns.keys())
            if invalid_fields := fields_to_check - model_fields:
                raise ValueError(f"Invalid payload fields for {cls.__name__}: {invalid_fields}")

    @classmethod
    def _process_relationships(
        cls, relationships: Optional[Dict]
    ) -> Optional[Dict[str, RelationshipConfig]]:
        """Process and return relationship configurations."""
        if not relationships:
            return None

        return {
            rel_name: RelationshipConfig(**rel_config.copy())
            for rel_name, rel_config in relationships.items()
        }

    @classmethod
    def _process_temporal_fields(
        cls, temporal_fields: Optional[List[Dict]]
    ) -> Optional[List[TemporalFieldConfig]]:
        """Process and validate temporal field configurations."""
        if not temporal_fields:
            return None

        model_fields = set(cls.__table__.columns.keys())
        temporal_field_configs = [TemporalFieldConfig(**config) for config in temporal_fields]

        for config in temporal_field_configs:
            if config.expires_at_field not in model_fields:
                raise ValueError(
                    f"Expires at field '{config.expires_at_field}' doesn't exist in {cls.__name__}"
                )
            if config.status_field and config.status_field not in model_fields:
                raise ValueError(
                    f"Status field '{config.status_field}' doesn't exist in {cls.__name__}"
                )

        return temporal_field_configs

    def get_changes(self, scope_name: str) -> ChangeSet:
        """Check if the webhook should be triggered for the specified scope and return changed fields with their states"""
        scopes = self.__class__.get_webhook_scopes()
        scope_config = scopes.get(scope_name)

        if not scope_config:
            return ChangeSet({}, {}, {})

        inspector = inspect(self)
        changed_fields, unchanged_fields, untracked_fields = {}, {}, {}

        if scope_config.temporal_fields:
            self._get_temporal_field_changes(
                scope_config.temporal_fields, inspector, changed_fields
            )

        self._get_regular_field_changes(
            scope_config, inspector, changed_fields, unchanged_fields, untracked_fields
        )

        return ChangeSet(changed_fields, untracked_fields, unchanged_fields)

    def _get_temporal_field_changes(
        self,
        temporal_configs: List[TemporalFieldConfig],
        inspector,
        changed_fields: Dict[str, FieldChange],
    ) -> None:
        """Extract changes from temporal fields"""
        for temp_config in temporal_configs:
            expires_field = temp_config.expires_at_field

            if not hasattr(inspector.attrs, expires_field):
                continue

            history = getattr(inspector.attrs, expires_field).history
            if not history.has_changes():
                continue

            old_value = history.deleted[0] if history.deleted else None
            new_value = history.added[0] if history.added else None
            now = datetime.now()

            if self._is_field_expired(old_value, new_value, now):
                changed_fields[expires_field] = {
                    "before": old_value,
                    "after": new_value,
                }

                if temp_config.status_field:
                    self._handle_status_field_change(temp_config, changed_fields)

                self._trigger_expiration_callback(temp_config, expires_field, old_value)

    def _is_field_expired(self, old_value: Any, new_value: Any, now: datetime) -> bool:
        """Check if a temporal field has expired"""
        return (
            old_value
            and isinstance(old_value, datetime)
            and old_value > now
            and (new_value is None or (isinstance(new_value, datetime) and new_value <= now))
        )

    def _handle_status_field_change(
        self, temp_config: TemporalFieldConfig, changed_fields: Dict[str, FieldChange]
    ) -> None:
        """Update status field values in changes"""
        status_field = temp_config.status_field
        if not hasattr(self, status_field):
            return

        status_value = getattr(self, status_field)
        if status_value != temp_config.status_value:
            changed_fields[status_field] = {
                "before": status_value,
                "after": temp_config.status_value,
            }

    def _trigger_expiration_callback(
        self, temp_config: TemporalFieldConfig, expires_field: str, old_value: Any
    ) -> None:
        """Call registered callback function when temporal field expires"""
        class_name = self.__class__.__name__

        if class_name not in self._temporal_expiration_callbacks or not hasattr(self, "id"):
            return

        callback = self._temporal_expiration_callbacks[class_name]
        try:
            callback(
                self.id,
                temp_config.scope_name,
                {expires_field: {"before": old_value, "after": None}},
            )
        except Exception as e:
            logger.error(f"Error in temporal expiration callback: {e}", exc_info=True)

    def _get_regular_field_changes(
        self,
        scope_config: WebhookScopeFields,
        inspector,
        changed_fields: Dict[str, FieldChange],
        unchanged_fields: Dict[str, Any],
        untracked_fields: Dict[str, FieldChange],
    ) -> None:
        """Process regular (non-temporal) fields and categorize changes"""
        model_relationships = set(self.__mapper__.relationships.keys())

        fields_to_check = scope_config.fields or [
            field for field in self.__table__.columns.keys() if field not in model_relationships
        ]

        for field in fields_to_check:
            if not hasattr(inspector.attrs, field):
                continue

            if field == "id":
                unchanged_fields[field] = getattr(self, field)
                continue

            history = getattr(inspector.attrs, field).history

            if history.has_changes():
                change = {
                    "before": history.deleted[0] if history.deleted else None,
                    "after": history.added[0] if history.added else getattr(self, field),
                }

                if field in scope_config.trigger_fields and field not in changed_fields:
                    changed_fields[field] = change
                elif field not in scope_config.trigger_fields:
                    untracked_fields[field] = change
            else:
                unchanged_fields[field] = getattr(self, field)

    def get_triggered_scopes(self) -> Dict[str, Dict[str, Any]]:
        """Get all scopes that should be triggered based on field changes and their states"""
        scopes = self.__class__.get_webhook_scopes()
        triggered_scopes = {}

        for scope_name, scope_config in scopes.items():
            change_set = self.get_changes(scope_name)
            if change_set.changed:
                triggered_scopes[scope_name] = {
                    **change_set.changed,
                    "_untracked": change_set.untracked,
                    "_unchanged": change_set.unchanged,
                }
        self._check_temporal_expirations(scopes, triggered_scopes)

        return triggered_scopes

    def _check_temporal_expirations(
        self, scopes: Dict[str, WebhookScopeFields], triggered_scopes: Dict[str, Dict]
    ) -> None:
        """Check for temporal fields that have expired and add to triggered scopes"""
        now = datetime.now()

        for scope_name, scope_config in scopes.items():
            if not scope_config.temporal_fields or scope_name in triggered_scopes:
                continue

            for temp_config in scope_config.temporal_fields:
                if temp_config.scope_name in triggered_scopes or not hasattr(
                    self, temp_config.expires_at_field
                ):
                    continue

                expires_at = getattr(self, temp_config.expires_at_field)
                is_expired = expires_at is None or (
                    isinstance(expires_at, datetime) and expires_at <= now
                )

                if is_expired:
                    triggered_scopes[temp_config.scope_name] = {
                        "_untracked": {},
                        "_unchanged": {},
                        temp_config.expires_at_field: {"before": expires_at, "after": None},
                    }

                    if temp_config.status_field and hasattr(self, temp_config.status_field):
                        current_value = getattr(self, temp_config.status_field)
                        triggered_scopes[temp_config.scope_name][temp_config.status_field] = {
                            "before": current_value,
                            "after": temp_config.status_value,
                        }

    async def get_payload_for_scope(
        self,
        session: AsyncSession,
        scope_name: str,
        scope_changes: Dict[str, Dict[Literal["before", "after"], Any]],
    ) -> PayloadType:
        """
        Get the payload for the specified scope based on its stage configuration.

        Returns:
            - For BOTH stage: Dict with 'before' and 'after' states
            - For BEFORE/AFTER stage: Dict with current state
        """
        scopes = self.__class__.get_webhook_scopes()
        if scope_name not in scopes:
            raise ValueError(f"Unknown scope: {scope_name}")

        scope_config = scopes[scope_name]

        fields_to_include = self._get_fields_to_include(scope_config)
        relationships_to_load = scope_config.relationships or {}

        if scope_config.stage == WebhookStage.BOTH:
            return {
                "before": await self._get_payload_state(
                    session, fields_to_include, relationships_to_load, scope_changes, "before"
                ),
                "after": await self._get_payload_state(
                    session, fields_to_include, relationships_to_load, scope_changes, "after"
                ),
            }

        state = "before" if scope_config.stage == WebhookStage.BEFORE else "after"
        return await self._get_payload_state(
            session, fields_to_include, relationships_to_load, scope_changes, state
        )

    def _get_fields_to_include(self, scope_config: WebhookScopeFields) -> Set[str]:
        """Get the set of fields to include in payload, excluding relationships"""
        model_relationships = set(self.__mapper__.relationships.keys())

        if scope_config.fields:
            fields = set(scope_config.fields)
        else:
            fields = set(self.__table__.columns.keys())

        return {field for field in fields if field not in model_relationships}

    async def _get_payload_state(
        self,
        session: AsyncSession,
        fields: Set[str],
        relationships: Dict[str, RelationshipConfig],
        scope_changes: Dict[str, Dict[Literal["before", "after"], Any]],
        state: Literal["before", "after"],
    ) -> Dict[str, Any]:
        """Get payload for specified fields in the requested state including relationships"""
        payload = self._process_field_values(scope_changes, fields, relationships, state)

        await self._add_relationship_data(session, payload, relationships)

        return payload

    def _process_field_values(
        self,
        scope_changes: Dict[str, Dict[Literal["before", "after"], Any]],
        fields: Set[str],
        relationships: Dict[str, RelationshipConfig],
        state: Literal["before", "after"],
    ) -> Dict[str, Any]:
        """Process fields and add them to the payload using scope changes"""
        payload = {}

        for field in fields:
            if field in relationships:
                continue

            if field in scope_changes:
                value = scope_changes[field].get(state, None)
            elif field in scope_changes.get("_untracked", {}):
                value = scope_changes["_untracked"][field].get(state, None)
            else:
                value = getattr(self, field, None)

            payload[field] = value

        return payload

    async def _add_relationship_data(
        self,
        session: AsyncSession,
        payload: Dict[str, Any],
        relationships: Dict[str, RelationshipConfig],
    ) -> None:
        """Process relationships and add them to the payload"""
        if not relationships:
            return

        try:
            if rel_attrs := list(relationships.keys()):
                await session.refresh(self, attribute_names=rel_attrs)

            for rel_name, rel_config in relationships.items():
                if not self._is_condition_met(rel_config):
                    continue

                rel_object = getattr(self, rel_name, None)
                if rel_object is not None:
                    payload[rel_name] = self._extract_relationship_data(rel_object, rel_config)

        except Exception as e:
            logger.exception(f"Error processing relationships for {self.__class__.__name__}: {e}")

    def _is_condition_met(self, rel_config: RelationshipConfig) -> bool:
        """Check if the condition for a relationship is met"""
        if not rel_config.condition:
            return True

        condition_field = rel_config.condition
        condition_value = rel_config.condition_value
        condition_operator = rel_config.condition_operator

        if not hasattr(self, condition_field):
            logger.warning(
                f"Condition field '{condition_field}' not found in {self.__class__.__name__}"
            )
            return False

        field_value = getattr(self, condition_field)
        return self._evaluate_condition(field_value, condition_value, condition_operator)

    def _evaluate_condition(
        self, field_value: Any, condition_value: Any, condition_operator: str
    ) -> bool:
        """Evaluate the condition based on the operator"""
        operators = {
            "==": lambda a, b: a == b,
            "!=": lambda a, b: a != b,
            ">": lambda a, b: a > b,
            "<": lambda a, b: a < b,
            ">=": lambda a, b: a >= b,
            "<=": lambda a, b: a <= b,
            "is": lambda a, b: a is b,
            "is not": lambda a, b: a is not b,
        }

        try:
            operator_func = operators.get(condition_operator)
            if not operator_func:
                logger.warning(f"Unknown condition operator: {condition_operator}")
                return False

            return operator_func(field_value, condition_value)

        except TypeError as e:
            logger.error(
                f"Condition check failed for field with value '{field_value}' "
                f"and condition value '{condition_value}': {e}"
            )
            return False

    def _extract_relationship_data(
        self, rel_object: Any, rel_config: RelationshipConfig
    ) -> Dict[str, Any]:
        """Extract data for a relationship based on its configuration"""
        if rel_config.fields:
            if isinstance(rel_config.fields, BaseModel):
                fields = list(rel_config.fields.model_fields.keys())
            else:
                fields = rel_config.fields

            return {
                rel_field: getattr(rel_object, rel_field)
                for rel_field in fields
                if hasattr(rel_object, rel_field)
            }

        if hasattr(rel_object, "to_dict"):
            return rel_object.to_dict()

        return {key: value for key, value in rel_object.__dict__.items() if not key.startswith("_")}
