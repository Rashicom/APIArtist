from fastapi import APIRouter, Depends
from .service import get_project_by_id
from beanie import BeanieObjectId
from authx.auth import CurrentUser
from .service import get_project_by_id, EndpointManager
from fastapi import HTTPException, status

router = APIRouter()


"""
Request handlers
    All the request created by user handled by anyone of thie handler
    request consist project_id which indicate the user project and endpoint which is created by user in the project
"""


@router.get(
    "/{project_id}/{endpoint:path}",
    summary="Handle GET request",
    description="Handle GET request",
)
async def handle_get(user: CurrentUser, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(user, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    endpoint_manager = EndpointManager(user, project, endpoint)
    await endpoint_manager.validate_end_point()

    return {"test": "Test"}


@router.post(
    "/{project_id}/{endpoint:path}",
    summary="Handle POST request",
    description="Handle POST request",
)
async def handle_post(user: CurrentUser, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(user, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return {"test": "Test"}


@router.patch(
    "/{project_id}/{endpoint:path}",
    summary="Handle PATCH request",
    description="Handle PATCH request",
)
async def handle_patch(user: CurrentUser, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(user, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return {"test": "Test"}


@router.patch(
    "/{project_id}/{endpoint:path}",
    summary="Handle PATCH request",
    description="Handle PATCH request",
)
async def handle_patch(user: CurrentUser, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(user, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return {"test": "Test"}


@router.delete(
    "/{project_id}/{endpoint:path}",
    summary="Handle DELETE request",
    description="Handle DELETE request",
)
async def handle_delete(user: CurrentUser, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(user, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return {"test": "Test"}


@router.put(
    "/{project_id}/{endpoint:path}",
    summary="Handle PUT request",
    description="Handle PUT request",
)
async def handle_put(user: CurrentUser, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(user, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return {"test": "Test"}
