from typing import Any, Callable, Dict, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")

# Basic types
FieldValue = Any
FieldChanges = Dict[str, FieldValue]
FieldChange = Dict[str, Optional[FieldValue]]
ChangesDict = Dict[str, FieldChange]

# Callback types
ActionHandler = Callable[[Any, Dict[str, Any]], None]
TemporalCallback = Callable[[int, str, ChangesDict], None]

# Configuration types
ActionConfig = Dict[str, Any]
TemporalConfig = Dict[str, Any]
RelationshipConfig = Dict[str, Any]

# Session type
Session = AsyncSession
