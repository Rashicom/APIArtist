from beanie import Document, before_event
from pydantic import Field, EmailStr
from datetime import datetime, timezone

class BaseMTimestampMixinodel:
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class User(Document, BaseMTimestampMixinodel):
    email: EmailStr
    name: str

    google_sub_id: str = Field(exclude=True)
    token: str = Field(exclude=True)
    refresh_token: str = Field(exclude=True)

    @before_event
    async def update_time(self):
        self.updated_at = datetime.now(timezone.utc)
    
    class Settings:
        collection = "users"

    class Config:
        exclude = {"token", "refresh_token", "google_sub_id"}