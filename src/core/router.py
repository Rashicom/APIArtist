from fastapi import APIRouter, Depends, Request, Body
from .service import get_project_by_id
from beanie import BeanieObjectId
from authx.auth import CurrentUser
from .service import get_project_by_id, EndpointManager
from fastapi import HTTPException, status
from pydantic import UUID4
from apigenerator.enums import EndpointTypes

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
async def handle_get(request: Request, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    user = project.user
    endpoint_manager = EndpointManager(user, project, endpoint)

    # rise 404 http exception if not found
    end_point_obj = await endpoint_manager.resolve_end_point()

    # automatically raise method not found(405) if method is not there
    method = await endpoint_manager.resolve_methods(request.method)

    data = await endpoint_manager.get()
    return data


@router.post(
    "/{project_id}/{endpoint:path}",
    summary="Handle POST request",
    description="Handle POST request",
)
async def handle_post(
    request: Request, project_id: BeanieObjectId, endpoint: str, body: dict = Body(None)
):
    project = await get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    user = project.user
    endpoint_manager = EndpointManager(user, project, endpoint)

    # rise 404 http exception if not found
    end_point_obj = await endpoint_manager.resolve_end_point()

    # automatically raise method not found(405) if method is not there
    method = await endpoint_manager.resolve_methods(request.method)

    # retrun data according to endpoint type
    if end_point_obj.endpoint_type == EndpointTypes.DYNAMIC:
        # body to endpoint type validation
        if not body:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dynamic api must includ a body",
            )

        # post data
        # TODO: feat : body validation
        data = await endpoint_manager.post(data=body)
    else:
        data = await endpoint_manager.post()
    return data


@router.patch(
    "/{project_id}/{endpoint:path}",
    summary="Handle PATCH request",
    description="Handle PATCH request",
)
async def handle_patch(request: Request, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    user = project.user
    endpoint_manager = EndpointManager(user, project, endpoint)

    # rise 404 http exception if not found
    end_point_obj = await endpoint_manager.resolve_end_point()

    # automatically raise method not found(405) if method is not there
    method = await endpoint_manager.resolve_methods(request.method)

    data = await endpoint_manager.get_data()
    return data


@router.patch(
    "/{project_id}/{endpoint:path}",
    summary="Handle PATCH request",
    description="Handle PATCH request",
)
async def handle_patch(request: Request, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    user = project.user
    endpoint_manager = EndpointManager(user, project, endpoint)

    # rise 404 http exception if not found
    end_point_obj = await endpoint_manager.resolve_end_point()

    # automatically raise method not found(405) if method is not there
    method = await endpoint_manager.resolve_methods(request.method)

    data = await endpoint_manager.get_data()
    return data


@router.delete(
    "/{project_id}/{endpoint:path}",
    summary="Handle DELETE request",
    description="Handle DELETE request",
)
async def handle_delete(request: Request, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    user = project.user
    endpoint_manager = EndpointManager(user, project, endpoint)

    # rise 404 http exception if not found
    end_point_obj = await endpoint_manager.resolve_end_point()

    # automatically raise method not found(405) if method is not there
    method = await endpoint_manager.resolve_methods(request.method)

    data = await endpoint_manager.get_data()
    return data


@router.put(
    "/{project_id}/{endpoint:path}",
    summary="Handle PUT request",
    description="Handle PUT request",
)
async def handle_put(request: Request, project_id: BeanieObjectId, endpoint: str):
    project = await get_project_by_id(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    user = project.user
    endpoint_manager = EndpointManager(user, project, endpoint)

    # rise 404 http exception if not found
    end_point_obj = await endpoint_manager.resolve_end_point()

    # automatically raise method not found(405) if method is not there
    method = await endpoint_manager.resolve_methods(request.method)

    data = await endpoint_manager.get_data()
    return data
