from project.models import Project
from apigenerator.models import Endpoints
from authx.models import User
from beanie import BeanieObjectId


class CoreRepository:
    async def get_endpoints_by_project_id(
        self, user_id: BeanieObjectId, project_id: BeanieObjectId
    ):
        """
        return all endpoints of a project
        """
        return await Endpoints.find(
            Endpoints.user.id == user_id, Endpoints.project.id == project_id
        ).to_list()

    async def get_endpoint_by_id(self):
        """
        return endpoint of a endpoint_id
        """
        pass
