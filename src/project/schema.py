from pydantic import BaseModel, Field, UUID4, ConfigDict
from datetime import datetime
from typing import Optional
from beanie import BeanieObjectId


class ProjectBaseSchema(BaseModel):
    pass


class ProjectRequestSchema(ProjectBaseSchema):
    name: str


class ProjectUpdateSchema(ProjectBaseSchema):
    name: Optional[str] = None


class ProjectResponseSchema(ProjectRequestSchema):
    id: BeanieObjectId
    base_url: str
    created_at: datetime
    updated_at: datetime
