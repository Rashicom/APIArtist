from pydantic import BaseModel
from beanie import BeanieObjectId
from typing import Dict, List

class EndpointsBaseSchema(BaseModel):
    user: BeanieObjectId
    project: BeanieObjectId
    
    name: str
    endpoint: str

    is_dynamic_endpoint: bool
    static_data: Dict
    methods: List


class EndpointsRequestSchema(EndpointsBaseSchema):
    pass

class EndpointsResponseSchema(EndpointsBaseSchema):
    id: BeanieObjectId