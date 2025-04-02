from beanie import Document, before_event
from pydantic import Field, EmailStr
from datetime import datetime, timezone

class BaseMTimestampMixinodel:
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc))

class User(Document, BaseMTimestampMixinodel):
    email: EmailStr
    name: str
    google_sub_id: str

    @before_event
    async def update_time(self):
        self.updated_at = datetime.now(timezone.utc)
    
    class Settings:
        collection = "users"