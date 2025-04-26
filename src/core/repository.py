from project.models import Project
from apigenerator.models import Endpoints
from authx.models import User


class CoreRepository:
    async def get_endpoints_by_project_id(self):
        """
        return all endpoints of a project
        """
        pass

    async def get_endpoint_by_id(self):
        """
        return endpoint of a endpoint_id
        """
        pass
