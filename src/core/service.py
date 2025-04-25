from project.models import Project
from project.repository import ProjectRepository
from beanie import BeanieObjectId
from fastapi import Request
from authx.models import User


async def get_project_by_id(user: User, project_id: BeanieObjectId):
    project_obj = ProjectRepository.retrieve_project(user, project_id)


class EndpointManager:
    """
    user:user
    endpoint:endpoint string
    TODO: find endpoint obj using endpoint which is provided in url
        endpoint_obj = /api/user/{user_id}/change
        endpoint_str = /api/user/12/change
    """

    def __init__(self, project: Project, end_point: str):
        self.project = project
        self.end_point_string = end_point
        self.end_point_obj = None

    async def get_end_point(self):
        "get end point"
        pass

    async def get_available_methods(self):
        pass

    async def get_endpoint_type(self):
        pass

    async def get_data(self):
        """
        Return data from endpoint
        """
        pass

    async def set_data(self):
        pass

    async def __post(self):
        """
        handle post
        """
        pass

    async def __get(self):
        """
        handle get
        """
        pass

    async def __patch(self):
        """
        handle patch
        """
        pass

    async def __put(self):
        """
        handle put
        """
        pass

    async def __delete(self):
        """
        handle delete
        """
        pass
