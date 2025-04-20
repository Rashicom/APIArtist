from fastapi import APIRouter, HTTPException, status
from authx.auth import CurrentUser
from .schema import EndpointsRequestSchema, EndpointsResponseSchema
from .repository import EndpointRepository
from project.repository import ProjectRepository
from beanie import BeanieObjectId

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



@router.get(
    "/list",
    summary="List all endpoint",
    description="List all endpoints"
)
async def list_endpoint(user:CurrentUser):
    pass


@router.get(
    "/{endpoint_id}/retrieve",
    summary="Get all endpoint",
    description="Get all endpoints"
)
async def get_endpoint(user:CurrentUser, id: BeanieObjectId):
    pass


@router.patch(
    "/{endpoint_id}/update",
    summary="Update endpoint",
    description="Update endpoint"
)
async def update_endpoint(user:CurrentUser, id: BeanieObjectId):
    pass


@router.delete(
    "/{endpoint_id}/delete",
    summary="Delete endpoint",
    description="Delete endpoint"
)
async def delete_endpoint(user:CurrentUser, id: BeanieObjectId):
    pass

