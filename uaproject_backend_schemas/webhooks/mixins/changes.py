import logging
from datetime import datetime
from typing import Any, Dict, List, NamedTuple, Optional, Set, TypedDict, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy import inspect
from sqlalchemy.orm import Mapper

from uaproject_backend_schemas.webhooks.mixins.base import WebhookBaseMixin, WebhookScopeFields
from uaproject_backend_schemas.webhooks.mixins.temporal import (
    WebhookTemporalMixin,
)

logger = logging.getLogger(__name__)

__all__ = ["FieldChange", "ChangeSet", "TriggeredScopeData", "WebhookChangesMixin"]

T = TypeVar("T")


class FieldChange(TypedDict):
    """Typed dictionary for storing field values before and after changes"""

    before: Optional[Any]
    after: Optional[Any]


class ChangeSet(NamedTuple):
    """Structure containing categorized field changes"""

    changed: Dict[str, FieldChange]
    untracked: Dict[str, FieldChange]
    unchanged: Dict[str, Any]


class TriggeredScopeData(TypedDict):
    """Typed dictionary for triggered scope data"""

    _untracked: Dict[str, FieldChange]
    _unchanged: Dict[str, Any]


class WebhookChangesMixin(WebhookBaseMixin, WebhookTemporalMixin):
    """Mixin for handling field changes"""

    @classmethod
    def _process_fields(cls, fields: Union[List[str], BaseModel, None]) -> Optional[Set[str]]:
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
        cls, fields_set: Optional[Set[str]], relationships: Optional[Dict[str, Any]]
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

    def get_changes(self, scope_name: str) -> ChangeSet:
        """Check if the webhook should be triggered for the specified scope and return changed fields with their states"""
        scopes = self.__class__.get_webhook_scopes()
        scope_config = scopes.get(scope_name)

        if not scope_config:
            return ChangeSet({}, {}, {})

        inspector = inspect(self)
        changed_fields: Dict[str, FieldChange] = {}
        unchanged_fields: Dict[str, Any] = {}
        untracked_fields: Dict[str, FieldChange] = {}

        if scope_config.temporal_fields:
            self._get_temporal_field_changes(
                scope_config.temporal_fields, inspector, changed_fields
            )

        self._get_regular_field_changes(
            scope_config, inspector, changed_fields, unchanged_fields, untracked_fields
        )

        return ChangeSet(changed_fields, untracked_fields, unchanged_fields)

    def _get_regular_field_changes(
        self,
        scope_config: WebhookScopeFields,
        inspector: Mapper,
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
                change: FieldChange = {
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
        triggered_scopes: Dict[str, Dict[str, Any]] = {}

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
        self, scopes: Dict[str, WebhookScopeFields], triggered_scopes: Dict[str, Dict[str, Any]]
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
