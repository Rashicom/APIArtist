from fastapi import APIRouter, HTTPException, status, Response
from authx.auth import CurrentUser
from .schema import (
    EndpointsRequestSchema,
    EndpointsResponseSchema,
    EndpointsUpdateSchema,
)
from .repository import EndpointRepository, DynamicDataRepository
from project.repository import ProjectRepository
from beanie import BeanieObjectId
from typing import List
from .enums import EndpointTypes

router = APIRouter()


@router.post(
    "/create",
    summary="Create endpoint",
    description="Create endpoint",
    response_model=EndpointsResponseSchema,
)
async def create_endpoint(user: CurrentUser, data: EndpointsRequestSchema):
    project_obj = await ProjectRepository.retrieve_project(user, data.project)
    if not project_obj:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="project does not found",
        )
    endpoint_obj = await EndpointRepository.create(user=user, **data.model_dump())

    # update dynamic data collection if endpoint type is dynamic
    if endpoint_obj.endpoint_type == EndpointTypes.DYNAMIC:
        dynamic_data_obj = await DynamicDataRepository.create(
            endpoint=endpoint_obj, data=data.dynamic_data
        )
    return endpoint_obj


@router.get(
    "/list",
    summary="List all endpoint",
    description="List all endpoints",
    response_model=List[EndpointsResponseSchema],
)
async def list_endpoint(user: CurrentUser, project_id: BeanieObjectId = None):
    if project_id:
        return await EndpointRepository.filter_by_project(user=user, project=project_id)
    return await EndpointRepository.list(user=user)


@router.get(
    "/{endpoint_id}/retrieve",
    summary="Get all endpoint",
    description="Get all endpoints",
    response_model=EndpointsResponseSchema,
)
async def get_endpoint(user: CurrentUser, id: BeanieObjectId):
    return await EndpointRepository.get_by_id(user=user, id=id)


@router.patch(
    "/{endpoint_id}/update",
    summary="Update endpoint",
    description="Update endpoint",
    response_model=EndpointsResponseSchema,
)
async def update_endpoint(
    user: CurrentUser, id: BeanieObjectId, data: EndpointsUpdateSchema
):
    return await EndpointRepository.update(user=user, id=id, data=data)


@router.delete(
    "/{endpoint_id}/delete", summary="Delete endpoint", description="Delete endpoint"
)
async def delete_endpoint(user: CurrentUser, id: BeanieObjectId):
    await EndpointRepository.delete(user=user, id=id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
