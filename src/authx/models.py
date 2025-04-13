from beanie import Document, before_event, Insert, Update
from pydantic import Field, EmailStr
from datetime import datetime, timezone
from utils.models import TimestampMixinodel


class User(Document, TimestampMixinodel):
    email: EmailStr
    name: str

    google_sub_id: str = Field(exclude=True)
    token: str = Field(exclude=True)
    refresh_token: str = Field(exclude=True)

    @before_event(Update)
    async def update_time(self):
        self.updated_at = datetime.now(timezone.utc)
    
    class Settings:
        collection = "users"

    class Config:
        exclude = {"token", "refresh_token", "google_sub_id"}