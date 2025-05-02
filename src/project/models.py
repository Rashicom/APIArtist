from utils.models import TimestampMixinodel
from beanie import Document, before_event, after_event, Insert, Link, Replace
from pydantic import Field, EmailStr, UUID4
import uuid
from config import get_settings
from authx.models import User
from typing import Optional

settings = get_settings()


class Project(Document, TimestampMixinodel):
    """
    Generate Base Url
    User can generate base url to create multiple endpoints under it
    """

    project_id: UUID4 = Field(default_factory=uuid.uuid4)
    user: Link[User]
    name: str
    base_url: Optional[str] = None

    @after_event(Insert)
    async def generate_base_url(self):
        if not self.base_url:
            self.base_url = f"{settings.BASE_URL}/{self.id}/api"
            await self.save()
