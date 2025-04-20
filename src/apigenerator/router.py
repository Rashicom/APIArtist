from fastapi import APIRouter, HTTPException, status
from authx.auth import CurrentUser
from .schema import EndpointsRequestSchema, EndpointsResponseSchema
from .repository import EndpointRepository
from project.repository import ProjectRepository

router = APIRouter()

@router.post(
    "/create",
    summary="Create endpoint",
    description="Create endpoint",
    response_model=EndpointsResponseSchema
)
async def create_endpoint(user:CurrentUser, data:EndpointsRequestSchema):
    project_obj = await ProjectRepository.retrieve_project(user, data.project)
    if not project_obj:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="project does not found")
    return await EndpointRepository.create(user=user, **data.model_dump())