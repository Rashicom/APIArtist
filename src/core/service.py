from project.models import Project
from project.repository import ProjectRepository
from beanie import BeanieObjectId
from fastapi import Request, HTTPException, status
from authx.models import User
from typing import Dict
from core.repository import CoreRepository


async def get_project_by_id(project_id: BeanieObjectId):
    return await ProjectRepository.retrieve_project_by_id(project_id)


class EndpointManager:
    """
    user:user
    endpoint:endpoint string
    TODO: find endpoint obj using endpoint which is provided in url
        endpoint_obj = /api/user/{user_id}/change
        endpoint_str = /api/user/12/change
    """

    def __init__(self, user: User, project: Project, end_point: str):
        self.project = project
        self.end_point_string = end_point
        self.user = user
        self.end_point_obj = None

    async def validate_end_point(self):
        """
        Validate endpoint : check the endpoint is exist in db or not
            - if yes set self.end_point_obj
            - else rise http exception

        Validation logic
            Eg:
                endpoint : api/user/{user_id}/get
                target1  : api/user/4/get
                target2  : api/user/john/get
                result   : match
        1 - break into chunks
            Eg:
                api/user/4/get >> [api,user,4,get]
        2 - find records which have same number of chunks
        3 - iterate through endpoit records
            - iterage thorugh record endpoint chunks
            for each iter, all the below checks needs to be performed
            - if type(endpoint_chunk[n]) == {}:
                pass
            - elif endpoint_chunk[n] == target_chunk[n]:
                pass
            - else:
                break

            if not breaked
            self.endpoint_obj = obj
        """
        # get all endpoints in the project
        endpoints = await CoreRepository.get_endpoints_by_project_id(
            user_id=self.user.id, project_id=self.project.id
        )

        # stripe url, then split by slash
        # strie("/") remove prefix and suffix slashes
        target_endpoint_chunks = self.end_point_string.strip("/").split("/")

        # iterate through each endpoint
        for endpoint_obj in endpoints:

            # stripe("/") remove prefix and suffix slashes
            endpoint_chunks = endpoint_obj.endpoint.strip("/").split("/")

            # chunks len must be equal. else pass to next iteration
            if len(endpoint_chunks) != len(target_endpoint_chunks):
                continue

            # assuming this target_endpoint is matched
            # this status changed from the for loop if not matched
            is_match = True

            # iterate througn chunks
            for i in range(len(target_endpoint_chunks)):
                # continue to next chunk if var
                if endpoint_chunks[i][0] == "{":
                    continue
                # continue to next chunk if match
                elif endpoint_chunks[i] == target_endpoint_chunks[i]:
                    continue

                # terminate this iteration if not match any one the condition
                else:
                    is_match = False
                    break

            # if end_point_obj found, set in self and stop iteration
            if is_match:
                self.end_point_obj = endpoint_obj
                break
        if not self.end_point_obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="path not found"
            )
        return self.end_point_obj

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
