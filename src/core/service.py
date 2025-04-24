from project.models import Project
from project.repository import ProjectRepository
from beanie import BeanieObjectId
from fastapi import Request
from authx.models import User


async def get_project_by_id(user:User,project_id: BeanieObjectId):
    project_obj = ProjectRepository.retrieve_project(user,project_id)



class EndpointManager:
    """
    user:user
    endpoint:endpoint string
    TODO: find endpoint obj using endpoint which is provided in url
        endpoint_obj = /api/user/{user_id}/change
        endpoint_str = /api/user/12/change
    """
    def __init__(self, project:Project, end_point:str):
        self.project = project
        self.end_point_string = end_point
        self.end_point_obj = None

    async def get_end_point(self):
        pass

    async def get_available_methods(self):
        pass