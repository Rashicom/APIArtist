from project.models import Project
from project.repository import ProjectRepository
from beanie import BeanieObjectId
from fastapi import Request
from authx.models import User


async def get_project_by_id(user:User,project_id: BeanieObjectId):
    project_obj = ProjectRepository.retrieve_project(user,project_id)


async def get_endpoint():
    """
    user:user
    endpoint:endpoint string
    TODO: find endpoint obj using endpoint which is provided in url
        endpoint_obj = /api/user/{user_id}/change
        endpoint_str = /api/user/12/change
    """

    pass