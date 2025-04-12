from fastapi import APIRouter, HTTPException, status
from .models import Project
from authx.auth import CurrentUser
from .repository import ProjectRepository
from .schema import ProjectRequestSchema, ProjectResponseSchema
from typing import List

router = APIRouter()

@router.post(
    "/create",
    summary="Create a project",
    description="Create a project to get a base url",
    response_model=ProjectResponseSchema
)
async def create_project(user:CurrentUser, project_data:ProjectRequestSchema):
    """
    Generate Base Url
    User can generate base url to create multiple endpoints under it
    """
    try:
        return await ProjectRepository.create(**project_data.model_dump(),user=user)    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Cound not create project")
    
@router.get(
    "/list",
    summary="List projects",
    description="List all projects created by the user",
    response_model=List[ProjectResponseSchema]
)
async def list_projects(user:CurrentUser):
    return await ProjectRepository.filter(user=user)
