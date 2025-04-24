from fastapi import APIRouter, HTTPException, Response, status
from .models import Project
from authx.auth import CurrentUser
from .repository import ProjectRepository
from .schema import ProjectRequestSchema, ProjectResponseSchema, ProjectUpdateSchema
from typing import List
from beanie import BeanieObjectId

router = APIRouter()


@router.post(
    "/create",
    summary="Create a project",
    description="Create a project to get a base url",
    response_model=ProjectResponseSchema,
)
async def create_project(user: CurrentUser, project_data: ProjectRequestSchema):
    """
    Generate Base Url
    User can generate base url to create multiple endpoints under it
    """
    try:
        return await ProjectRepository.create(**project_data.model_dump(), user=user)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Cound not create project",
        )


@router.get(
    "/list",
    summary="List projects",
    description="List all projects created by the user",
    response_model=List[ProjectResponseSchema],
)
async def list_projects(user: CurrentUser):
    return await ProjectRepository.get_user_projects(user)


@router.get(
    "/retrieve/{id}",
    summary="Get a specific project",
    description="Get a specific project which is the user owned",
    response_model=ProjectResponseSchema,
)
async def retrieve_project(user: CurrentUser, id: BeanieObjectId):
    project_obj = await ProjectRepository.retrieve_project(user, id)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="project not found"
        )
    return project_obj


@router.delete(
    "/delete/{id}",
    summary="Delete project",
    description="Delete project",
)
async def delete_project(user: CurrentUser, id: BeanieObjectId):
    await ProjectRepository.delete_project(user, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/update/{id}",
    summary="Update project",
    description="Update project",
    response_model=ProjectResponseSchema,
)
async def update_project(
    user: CurrentUser, project_data: ProjectUpdateSchema, id: BeanieObjectId
):
    print(project_data)
    return await ProjectRepository.update_project(user, id, project_data)
