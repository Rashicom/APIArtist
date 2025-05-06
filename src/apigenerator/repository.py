from .models import Endpoints, DynamicData
from authx.models import User
from beanie import BeanieObjectId
from typing import Dict, List
from fastapi import HTTPException, status
from .schema import EndpointsUpdateSchema


class EndpointRepository:
    async def create(*args, **kwargs):
        try:
            endpoint_obj = Endpoints(**kwargs)
            await endpoint_obj.insert()
            return endpoint_obj
        except Exception as e:
            print("cannot create endpoint : ", e)
            return None

    async def list(user: User):
        return await Endpoints.find(Endpoints.user.id == user.id).to_list()

    async def filter_by_project(user: User, project: BeanieObjectId):
        return await Endpoints.find(
            Endpoints.user.id == user.id, Endpoints.project.id == project
        ).to_list()

    async def get_by_id(user: User, id: BeanieObjectId):
        return await Endpoints.find_one(Endpoints.id == id)

    async def update(user: User, id: BeanieObjectId, data: EndpointsUpdateSchema):
        endpoint_obj = await Endpoints.find_one(
            Endpoints.user.id == user.id, Endpoints.id == id
        )
        if not endpoint_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="endpoint does not exist",
            )
        await endpoint_obj.set(data.model_dump(exclude_none=True))
        return endpoint_obj

    async def delete(user: User, id: BeanieObjectId):
        endpoint_obj = await Endpoints.find_one(
            Endpoints.user.id == user.id, Endpoints.id == id
        )
        if not endpoint_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="endpoint does not exist",
            )
        await endpoint_obj.delete()


class DynamicDataRepository:
    async def create(*args, **kwargs):
        try:
            dynamic_data_obj = DynamicData(**kwargs)
            await dynamic_data_obj.insert()
            return dynamic_data_obj
        except Exception as e:
            print(e)
            print("Exception while create dynamic data")
            return None
            # TODO: logging

    async def bulk_create(data_list: List[Dict]):
        try:
            dynamic_data_objs = [DynamicData(**data) for data in data_list]
            await DynamicData.insert_many(dynamic_data_objs)
            return dynamic_data_objs
        except Exception as e:
            print("Exception while bulk create dynamic data")
            return None
            # TODO: logging

    async def list(endpoint_id: BeanieObjectId):
        return await DynamicData.find(DynamicData.endpoint.id == endpoint_id).to_list()

    async def update(endpoint_id: BeanieObjectId, path_params_filter: dict, data: dict):
        """
        make query for get all dynamic data object
        fiter using endpoint id
        filter usig path params filter
        then update the resultend record using data
        """
        query = {
            "endpoint.$id": endpoint_id,
            **{f"data.{k}": v for k, v in path_params_filter.items()},
        }
        matching_docs = await DynamicData.find(query).to_list()

        # rise exception if no records found
        if len(matching_docs) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
            )
        for record in matching_docs:
            record.data.update(data)
            await record.save()  # TODO: optimize
        return matching_docs

    async def delete(endpoint_id: BeanieObjectId, path_params_filter: dict):
        """
        - find recors using endpoint id and pathe params filter
        - if not mathicng record rise exception
        - else delete all record
        """
        query = {
            "endpoint.$id": endpoint_id,
            **{f"data.{k}": v for k, v in path_params_filter.items()},
        }
        matching_docs = await DynamicData.find(query)

        # rise exception if no records found
        if len(matching_docs) == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
            )
        await matching_docs.delete()
