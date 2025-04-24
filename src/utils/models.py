from pydantic import Field
from datetime import datetime


class TimestampMixinodel:
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
