import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from uaproject_backend_schemas.webhooks.mixins.base import WebhookBaseMixin
from uaproject_backend_schemas.webhooks.mixins.config import TemporalFieldConfig
from uaproject_backend_schemas.webhooks.types import ChangesDict, TemporalCallback, TemporalConfig

logger = logging.getLogger(__name__)

__all__ = ["WebhookTemporalMixin"]


class WebhookTemporalMixin(WebhookBaseMixin):
    """Mixin for handling temporal fields"""

    _temporal_expiration_callbacks: Dict[str, TemporalCallback] = {}

    @classmethod
    def register_temporal_expiration_callback(cls, callback: TemporalCallback) -> None:
        """
        Register a callback function that will be called when a temporal field expires

        Args:
            callback: A function that takes (instance_id, scope_name, changes) as parameters
        """
        cls._temporal_expiration_callbacks[cls.__name__] = callback

    @classmethod
    def _process_temporal_fields(
        cls, temporal_fields: Optional[List[TemporalConfig]]
    ) -> Optional[List[TemporalFieldConfig]]:
        """Process and validate temporal field configurations"""
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

    def _get_temporal_field_changes(
        self,
        temporal_configs: List[TemporalFieldConfig],
        inspector: Any,
        changed_fields: ChangesDict,
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
        self, temp_config: TemporalFieldConfig, changed_fields: ChangesDict
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
