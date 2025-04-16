from datetime import datetime
from enum import StrEnum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field, model_validator

from uaproject_backend_schemas.base import BaseResponseModel, IDMixin, TimestampsMixin


class NewsType(StrEnum):
    UPDATE = "update"
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"
    OTHER = "other"
    PERSONAL = "personal"
    CONGRATULATION = "congratulation"
    TECHNICAL = "technical"
    ANNOUNCEMENT = "announcement"
    EVENT = "event"
    QUEST = "quest"
    RECRUITMENT = "recruitment"
    HOLIDAY = "holiday"


class ImportanceType(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    URGENT = "urgent"
    EMERGENCY = "emergency"


class NewsImageBase(BaseModel):
    image_path: Optional[str] = None
    image_url: Optional[str] = None
    order: int = 0


class NewsBase(BaseResponseModel):
    title: str
    content: str
    type: NewsType
    importance: ImportanceType
    author: Optional[str] = None
    images: List[NewsImageBase] = []
    discord_message_id: Optional[str] = None
    telegram_message_id: Optional[str] = None
    is_weekly_update: bool = False
    parent_news_id: Optional[int] = None
    tags: List[str] = []
    format_type: str = "markdown"
    related_threads: List[str] = []
    event_time: Optional[datetime] = None
    is_pinned: bool = False
    is_archived: bool = False


class NewsCreate(NewsBase):
    pass


class NewsUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    type: Optional[NewsType] = None
    importance: Optional[ImportanceType] = None
    author: Optional[str] = None
    images: Optional[List[NewsImageBase]] = None
    discord_message_id: Optional[str] = None
    telegram_message_id: Optional[str] = None
    is_weekly_update: Optional[bool] = None
    parent_news_id: Optional[int] = None
    tags: Optional[List[str]] = None
    format_type: Optional[str] = None
    related_threads: Optional[List[str]] = None
    event_time: Optional[datetime] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None


class NewsResponse(NewsBase, IDMixin, TimestampsMixin):
    pass


class NewsComment(BaseModel):
    news_id: int
    author: str
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_edited: bool = False
    edited_at: Optional[datetime] = None
    parent_comment_id: Optional[int] = None
    reactions: Dict[str, int] = Field(default_factory=dict)


class NewsStats(BaseModel):
    news_id: int
    views_count: int = 0
    likes_count: int = 0
    comments_count: int = 0
    shares_count: int = 0
    last_viewed_at: Optional[datetime] = None


class NewsFilter(BaseModel):
    types: Optional[List[NewsType]] = None
    importance: Optional[List[ImportanceType]] = None
    tags: Optional[List[str]] = None
    author: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    is_pinned: Optional[bool] = None
    is_archived: Optional[bool] = None
    search_query: Optional[str] = None

    @model_validator(mode="before")
    def validate_dates(cls, values):
        start_date = values.get("start_date")
        end_date = values.get("end_date")
        if start_date and end_date and start_date > end_date:
            raise ValueError("start_date must be before end_date")
        return values


class NewsSort(StrEnum):
    CREATED_AT = "created_at"
    UPDATED_AT = "updated_at"
    TITLE = "title"
    TYPE = "type"
    IMPORTANCE = "importance"
    EVENT_TIME = "event_time"


class TechnicalNews(NewsBase):
    type: NewsType = Field(default=NewsType.TECHNICAL)
    affected_services: List[str] = []
    expected_downtime: Optional[str] = None
    status: str = "planned"


class RecruitmentNews(NewsBase):
    type: NewsType = Field(default=NewsType.RECRUITMENT)
    position: str
    requirements: List[str] = []
    deadline: Optional[datetime] = None
    application_link: Optional[str] = None


class EventNews(NewsBase):
    type: NewsType = Field(default=NewsType.EVENT)
    start_time: datetime
    end_time: Optional[datetime] = None
    location: Optional[str] = None
    rewards: List[str] = []
    participants_limit: Optional[int] = None


class HolidayNews(NewsBase):
    type: NewsType = Field(default=NewsType.HOLIDAY)
    holiday_name: str
    duration_days: int = 1
    special_features: List[str] = []
    rewards: List[str] = []


class QuestNews(NewsBase):
    type: NewsType = Field(default=NewsType.QUEST)
    quest_type: str
    difficulty: str
    rewards: List[str] = []
    requirements: List[str] = []
    completion_time: Optional[str] = None


class NewsPagination(BaseModel):
    page: int = 1
    per_page: int = 20
    total: Optional[int] = None
    total_pages: Optional[int] = None
