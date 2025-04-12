from pydantic import BaseModel, Field, UUID4
from datetime import datetime
from typing import Optional

class ProjectBaseSchema(BaseModel):
    pass

class ProjectRequestSchema(ProjectBaseSchema):
    name: str

class ProjectResponseSchema(ProjectRequestSchema):
    project_id: UUID4
    base_url: str
    created_at: datetime
    updated_at: datetime