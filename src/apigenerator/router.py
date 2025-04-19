from fastapi import APIRouter
from authx.auth import CurrentUser
from .schema import EndpointsRequestSchema, EndpointsResponseSchema
from .repository import EndpointRepository

router = APIRouter()

@router.post(
    "/create",
    summary="Create endpoint",
    description="Create endpoint",
    response_model=EndpointsResponseSchema
)
async def create_endpoint(user:CurrentUser, data:EndpointsRequestSchema):
    return await EndpointRepository.create(user=user, **data.model_dump())