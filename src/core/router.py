from fastapi import APIRouter


router = APIRouter()


"""
Request handlers
    All the request created by user handled by anyone of thie handler
    request consist project_id which indicate the user project and endpoint which is created by user in the project
"""

@router.get(
    "/{project_id}/{endpoint:path}",
    summary="Handle GET request",
    description="Handle GET request"
)
async def handle_get(project_id, endpoint:str):
    print(">>>>",endpoint)
    return {"test":"Test"}


@router.post(
    "/{project_id}/{endpoint:path}",
    summary="Handle POST request",
    description="Handle POST request"
)
async def handle_post(project_id, endpoint:str):
    print(">>>>",endpoint)
    return {"test":"Test"}


@router.patch(
    "/{project_id}/{endpoint:path}",
    summary="Handle PATCH request",
    description="Handle PATCH request"
)
async def handle_patch(project_id, endpoint:str):
    print(">>>>",endpoint)
    return {"test":"Test"}


@router.patch(
    "/{project_id}/{endpoint:path}",
    summary="Handle PATCH request",
    description="Handle PATCH request"
)
async def handle_patch(project_id, endpoint:str):
    print(">>>>",endpoint)
    return {"test":"Test"}


@router.delete(
    "/{project_id}/{endpoint:path}",
    summary="Handle DELETE request",
    description="Handle DELETE request"
)
async def handle_delete(project_id, endpoint:str):
    print(">>>>",endpoint)
    return {"test":"Test"}


@router.put(
    "/{project_id}/{endpoint:path}",
    summary="Handle PUT request",
    description="Handle PUT request"
)
async def handle_put(project_id, endpoint:str):
    print(">>>>",endpoint)
    return {"test":"Test"}