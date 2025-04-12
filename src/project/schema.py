from pydantic import BaseModel, Field, UUID4, ConfigDict
from datetime import datetime
from typing import Optional
from beanie import BeanieObjectId

class ProjectBaseSchema(BaseModel):
    pass

class ProjectRequestSchema(ProjectBaseSchema):
    name: str

class ProjectResponseSchema(ProjectRequestSchema):
    id: BeanieObjectId
    project_id: UUID4
    base_url: str
    created_at: datetime
    updated_at: datetime