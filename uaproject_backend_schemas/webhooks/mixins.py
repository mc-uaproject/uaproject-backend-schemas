import logging
from typing import Any, Dict, List, Literal, Optional, Set, Tuple, Union

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession

from uaproject_backend_schemas.webhooks.schemas import WebhookStage

__all__ = ["WebhookScopeFields", "PayloadType", "WebhookPayloadMixin", "RelationshipConfig"]


logger = logging.getLogger(__name__)


class RelationshipConfig(BaseModel):
    fields: Optional[List[str] | BaseModel] = None
    condition: Optional[str] = None
    condition_value: Optional[Any] = None
    condition_operator: str = "=="


class WebhookScopeFields(BaseModel):
    trigger_fields: List[str]
    fields: Optional[List[str]] = None
    stage: WebhookStage = WebhookStage.AFTER
    relationships: Optional[Dict[str, RelationshipConfig]] = None


PayloadType = Union[Dict[str, Any], Dict[Literal["before", "after"], Dict[str, Any]]]


class WebhookPayloadMixin:
    """A mixin that adds webhook functionality to a model"""

    __scope_prefix__ = ""

    @classmethod
    def get_webhook_scopes(cls) -> Dict[str, WebhookScopeFields]:
        """Get webhook scopes for this specific class"""
        if not hasattr(cls, "_webhook_scopes_registry"):
            cls._webhook_scopes_registry = {}
        return cls._webhook_scopes_registry

    @classmethod
    def register_scope(
        cls,
        scope_name: str,
        trigger_fields: List[str] | Set[str],
        fields: List[str] | Set[str] | BaseModel | None = None,
        relationships: Dict[str, Dict[str, Any]] | None = None,
        stage: WebhookStage = WebhookStage.AFTER,
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
                   Example: {"service": {"fields": ["id", "name"], "condition": "service_id", "condition_value": 0, "condition_operator": ">"}}
            stage: WebhookStage indicating when the webhook should be triggered
                  and what data should be included in the payload
        """
        scope_name = f"{cls.__scope_prefix__}.{scope_name}"
        scopes = cls.get_webhook_scopes()

        if scope_name in scopes:
            raise ValueError(f"Scope '{scope_name}' is already registered for {cls.__name__}")

        trigger_fields_set = set(trigger_fields)

        if isinstance(fields, BaseModel):
            fields_set = set(fields.model_fields.keys())
        else:
            fields_set = set(fields) if fields is not None else None

        model_fields = set(cls.__table__.columns.keys())
        if invalid_triggers := trigger_fields_set - model_fields:
            raise ValueError(f"Invalid trigger fields for {cls.__name__}: {invalid_triggers}")

        if fields_set is not None:
            fields_to_check = fields_set.copy()
            relationship_names = set()

            if relationships:
                relationship_names = set(relationships.keys())
                fields_to_check = fields_set - relationship_names

            if invalid_fields := fields_to_check - model_fields:
                raise ValueError(f"Invalid payload fields for {cls.__name__}: {invalid_fields}")

        relationship_configs = None
        if relationships:
            relationship_configs = {
                rel_name: RelationshipConfig(**rel_config)
                for rel_name, rel_config in relationships.items()
            }
        scopes[scope_name] = WebhookScopeFields(
            trigger_fields=list(trigger_fields_set),
            fields=list(fields_set) if fields_set else None,
            relationships=relationship_configs,
            stage=stage,
        )

    def get_changes(
        self, scope_name: str
    ) -> Tuple[
        Dict[str, Dict[Literal["before", "after"], Any]],
        Dict[str, Dict[Literal["before", "after"], Any]],
        Dict[str, Any],
    ]:
        """Check if the webhook should be triggered for the specified scope and return changed fields with their states"""
        scopes = self.__class__.get_webhook_scopes()
        scope_config = scopes.get(scope_name)

        if not scope_config:
            return {}

        inspector = inspect(self)
        changed_fields = {}
        unchanged_fields = {}
        untracked_fields = {}

        model_relationships = set(self.__mapper__.relationships.keys())

        for field in scope_config.fields or [
            field for field in self.__table__.columns.keys() if field not in model_relationships
        ]:
            if hasattr(inspector.attrs, field):
                history = getattr(inspector.attrs, field).history
                if history.has_changes() and field in scope_config.trigger_fields:
                    changed_fields[field] = {
                        "before": history.deleted[0] if history.deleted else None,
                        "after": history.added[0] if history.added else getattr(self, field),
                    }
                elif history.has_changes() and field not in scope_config.trigger_fields:
                    untracked_fields[field] = {
                        "before": history.deleted[0] if history.deleted else None,
                        "after": history.added[0] if history.added else getattr(self, field),
                    }
                else:
                    unchanged_fields[field] = getattr(self, field)

        return changed_fields, untracked_fields, unchanged_fields

    def get_triggered_scopes(
        self,
    ) -> Dict[
        str,
        Dict[
            Literal["_untracked", "_unchanged"] | str, Dict[Literal["before", "after"] | str, Any]
        ],
    ]:
        """Get all scopes that should be triggered based on field changes and their states"""
        scopes = self.__class__.get_webhook_scopes()
        triggered_scopes: dict[str, dict] = {}

        for scope_name in scopes:
            changes, untracked, unchanged = self.get_changes(scope_name)
            if changes:
                triggered_scopes[scope_name] = changes
                triggered_scopes[scope_name]["_untracked"] = untracked
                triggered_scopes[scope_name]["_unchanged"] = unchanged

        return triggered_scopes

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
        model_relationships = set(self.__mapper__.relationships.keys())
        fields_to_include = {
            field
            for field in (scope_config.fields or self.__table__.columns.keys())
            if field not in model_relationships
        }

        relationships_to_load = scope_config.relationships or {}

        if scope_config.stage == WebhookStage.BOTH:
            return {
                "before": await self._get_payload_state(
                    session,
                    fields_to_include,
                    relationships_to_load,
                    scope_changes,
                    state="before",
                ),
                "after": await self._get_payload_state(
                    session, fields_to_include, relationships_to_load, scope_changes, state="after"
                ),
            }

        state = "before" if scope_config.stage == WebhookStage.BEFORE else "after"
        return await self._get_payload_state(
            session, fields_to_include, relationships_to_load, scope_changes, state
        )

    async def _get_payload_state(
        self,
        session: AsyncSession,
        fields: Set[str],
        relationships: Dict[str, RelationshipConfig],
        scope_changes: Dict[str, Dict[Literal["before", "after"], Any]],
        state: Literal["before", "after"],
    ) -> Dict[str, Any]:
        """Get payload for specified fields in the requested state including relationships"""
        payload = self._process_fields(scope_changes, fields, relationships, state)
        await self._process_relationships(session, payload, relationships)
        return payload

    def _process_fields(
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

    async def _process_relationships(
        self,
        session: AsyncSession,
        payload: Dict[str, Any],
        relationships: Dict[str, RelationshipConfig],
    ) -> None:
        """Process relationships and add them to the payload"""

        try:
            for rel_name in relationships:
                await session.refresh(self, attribute_names=[rel_name])

            for rel_name, rel_config in relationships.items():
                if not self._is_condition_met(rel_config):
                    continue

                rel_object = getattr(self, rel_name, None)
                if rel_object is not None:
                    payload[rel_name] = self._get_relationship_data(rel_object, rel_config)
        except Exception as e:
            logger.exception(f"Error processing relationships for {self.__class__.__name__}: {e}")

    def _is_condition_met(self, rel_config: RelationshipConfig) -> bool:
        """Check if the condition for a relationship is met"""
        if not rel_config.condition:
            return True

        condition_field = rel_config.condition
        condition_value = rel_config.condition_value
        condition_operator = rel_config.condition_operator
        field_value = getattr(self, condition_field)

        return self._evaluate_condition(field_value, condition_value, condition_operator)

    def _evaluate_condition(
        self, field_value: Any, condition_value: Any, condition_operator: str
    ) -> bool:
        """Evaluate the condition based on the operator"""
        try:
            if condition_operator == "==":
                return field_value == condition_value
            elif condition_operator == "!=":
                return field_value != condition_value
            elif condition_operator == ">":
                return field_value > condition_value
            elif condition_operator == "<":
                return field_value < condition_value
            elif condition_operator == ">=":
                return field_value >= condition_value
            elif condition_operator == "<=":
                return field_value <= condition_value
            elif condition_operator == "is not":
                return field_value is not condition_value
            elif condition_operator == "is":
                return field_value is condition_value
            else:
                return False
        except TypeError:
            logger.error(
                f"Condition check failed for field with value '{field_value}' "
                f"and condition value '{condition_value}'"
            )
            return False

    def _get_relationship_data(
        self, rel_object: Any, rel_config: RelationshipConfig
    ) -> Dict[str, Any]:
        """Get data for a relationship based on its configuration"""
        if rel_config.fields:
            if not isinstance(rel_config.fields, BaseModel):
                return {
                    rel_field: getattr(rel_object, rel_field)
                    for rel_field in rel_config.fields
                    if hasattr(rel_object, rel_field)
                }
            fields = set(rel_config.fields.model_fields.keys())
            return {
                rel_field: getattr(rel_object, rel_field)
                for rel_field in fields
                if hasattr(rel_object, rel_field)
            }
        if hasattr(rel_object, "to_dict"):
            return rel_object.to_dict()
        return {key: value for key, value in rel_object.__dict__.items() if not key.startswith("_")}
