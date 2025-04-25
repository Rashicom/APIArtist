from project.models import Project
from project.repository import ProjectRepository
from beanie import BeanieObjectId
from fastapi import Request
from authx.models import User
from typing import Dict


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

    async def validate_end_point(self):
        """
        Validate endpoint : check the endpoint is exist in db or not
            - if yes set self.end_point_obj
            - else rise http exception
        """
        pass

    async def get_available_methods(self):
        """
        Get all avalable method for the self.end_point_obj
            - dependency >> validate_end_point must be called before this
        """
        pass

    async def get_endpoint_type(self):
        """
        Get endpoit type(static, dynamic)
            - dependency >> validate_end_point must be called before this
        """
        pass

    async def get_data(self):
        """
        Return data from endpoint
            - call self.__get
            - dependency >> validate_end_point must be called before this
        """
        pass

    async def set_data(self, method: str, data: Dict):
        """
        set data to an endpoint
            - call self.__<method>
            - dependency >> validate_end_point must be called before this
        """
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
