from pydantic import BaseModel
from beanie import BeanieObjectId
from typing import Dict, List, Any, Optional
from .enums import EndpointTypes

class EndpointsBaseSchema(BaseModel):
    project: BeanieObjectId
    
    name: str
    endpoint: str

    methods: List
    endpoint_type: EndpointTypes
    static_data: Optional[Dict[str, Any]] = None
    dynamic_data: Optional[List[Dict[str, Any]]] = None


class EndpointsRequestSchema(EndpointsBaseSchema):
    pass

class EndpointsResponseSchema(EndpointsBaseSchema):
    id: BeanieObjectId