from project.models import Project
from project.repository import ProjectRepository
from beanie import BeanieObjectId
from fastapi import Request, HTTPException, status
from authx.models import User
from typing import Dict
from core.repository import CoreRepository
from apigenerator.enums import HttpMethods, EndpointTypes
from apigenerator.repository import DynamicDataRepository


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
        self.user = user
        self.project = project
        self.end_point_string = end_point
        self.end_point_obj = None
        self.method = None

        self.path_parameters = dict()
        self.query_parameters = dict()

    async def resolve_end_point(self):
        """
        resolve endpoint : check the endpoint is exist in db or not
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

    async def resolve_methods(self, target_method):
        """
        check the target_method is available in this endpoint
        - if yes set in self.method
        - this method is used to call appropriate action(__get, __post, __patch, __delete)
        dependency >> validate_end_point must be called before this
        """
        if HttpMethods(target_method) in self.end_point_obj.methods:
            self.method = target_method
            return self.method
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail="Method not allowed"
        )

    async def load_path_parameters(self):
        """
        Retrieve path parameters from url
        store in class var as a dict named as self.path_parameters
            [
                {"field_name":"value passed in url"},
            ]
        """
        url_path_chunks = self.end_point_string.strip("/").split(
            "/"
        )  # path retrieved from url
        endpoint_chunks = self.end_point_obj.endpoint.strip("/").split(
            "/"
        )  # endpoint object matched with the url
        for i in range(len(endpoint_chunks)):
            if endpoint_chunks[i][0] == "{":
                # append parameter into self.path_parameters
                self.path_parameters.update(
                    {endpoint_chunks[i].strip("{}"): url_path_chunks[i]}
                )

    async def load_query_parameters(self):
        """
        Retrieve query parameters from url
        store in class var as a dict named as self.query_parameters
            [
                {"field_name":"value passed in url"},
            ]
        """
        url_path_chunks = self.end_point_string.strip("/").split(
            "?"
        )  # path retrieved from url
        for chunk in url_path_chunks:
            # this chunk is a query param if and only if it contais a "="
            if "=" in chunk:
                key, val = chunk.split("=")
                self.query_parameters.update({key: val})

    async def get_endpoint_type(self):
        """
        Get endpoit type(static, dynamic)
            - dependency >> validate_end_point must be called before this
        """
        return self.end_point_obj.endpoint_type

    async def get_data(self):
        """
        Return data from endpoint
            - call self.__get
            - dependency >> validate_end_point must be called before this
        """
        end_point_type = await self.get_endpoint_type()
        if end_point_type == EndpointTypes.STATIC:
            print("static buisiness logic")
            return await self.get()
        else:
            pass
            # TODO: impliment dynamic logic

    async def set_data(self, method: str, data: Dict):
        """
        set data to an endpoint
            - call self.__<method>
            - dependency >> validate_end_point must be called before this
        """
        pass

    async def post(self, data: Dict = None):
        """
        handle post
        """
        if await self.get_endpoint_type() == EndpointTypes.STATIC:
            return getattr(self.end_point_obj.static_data, self.method.lower())

        dynamic_data_obj = await DynamicDataRepository.create(
            endpoint=self.end_point_obj, data=data
        )
        return dynamic_data_obj.data

    async def get(self):
        """
        handle get
        """
        if await self.get_endpoint_type() == EndpointTypes.STATIC:
            return getattr(self.end_point_obj.static_data, self.method.lower())

        dynamic_data_obj = await DynamicDataRepository.list(self.end_point_obj.id)

        # returning datas from dynamic_data objs
        return [dt.data for dt in dynamic_data_obj]

    async def patch(self):
        """
        handle patch
        """
        if await self.get_endpoint_type() == EndpointTypes.STATIC:
            return getattr(self.end_point_obj.static_data, self.method.lower())
        # TODO: chage perticular dynamic data collection
        pass

    async def put(self):
        """
        handle put
        """
        if await self.get_endpoint_type() == EndpointTypes.STATIC:
            return getattr(self.end_point_obj.static_data, self.method.lower())
        # TODO: change dynamic data collection
        pass

    async def delete(self):
        """
        handle delete
        """
        if await self.get_endpoint_type() == EndpointTypes.STATIC:
            return getattr(self.end_point_obj.static_data, self.method.lower())
        # TODO: delete a perticular dynamic data collection
        pass
