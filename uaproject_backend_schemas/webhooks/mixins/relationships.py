import logging
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel

from uaproject_backend_schemas.webhooks.mixins.base import WebhookBaseMixin
from uaproject_backend_schemas.webhooks.types import FieldChanges, Session

logger = logging.getLogger(__name__)


class RelationshipConfigModel(BaseModel):
    """Configuration for relationship fields"""

    fields: Optional[Union[List[str], BaseModel]] = None
    condition: Optional[str] = None
    condition_value: Optional[Any] = None
    condition_operator: str = "=="


class WebhookRelationshipsMixin(WebhookBaseMixin):
    """Mixin for handling relationships"""

    @classmethod
    def _process_relationships(
        cls, relationships: Optional[Dict[str, Any]]
    ) -> Optional[Dict[str, RelationshipConfigModel]]:
        """Process and return relationship configurations"""
        if not relationships:
            return None

        return {
            rel_name: RelationshipConfigModel(**rel_config.copy())
            for rel_name, rel_config in relationships.items()
        }

    def _is_condition_met(self, rel_config: RelationshipConfigModel) -> bool:
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

    def _extract_relationship_data(
        self, rel_object: Any, rel_config: RelationshipConfigModel
    ) -> FieldChanges:
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

    async def _add_relationship_data(
        self,
        session: Session,
        payload: Dict[str, Any],
        relationships: Dict[str, RelationshipConfigModel],
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
