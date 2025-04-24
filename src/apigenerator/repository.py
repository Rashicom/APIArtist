from .models import Endpoints
from authx.models import User
from beanie import BeanieObjectId
from typing import Dict
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
        endpoint_obj = Endpoints.find_one(
            Endpoints.user.id == user.id, Endpoints.id == id
        )
        if not endpoint_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="endpoint does not exist",
            )
        await endpoint_obj.delete()
