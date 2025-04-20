from pydantic import BaseModel, field_serializer
from beanie import BeanieObjectId
from typing import Dict, List, Any, Optional
from .enums import EndpointTypes, HttpMethods
from beanie import Link
from project.models import Project


class StaticData(BaseModel):
    get: Optional[Dict] = {}
    post: Optional[Dict] = {}
    patch: Optional[Dict] = {}
    put: Optional[Dict] = {}
    delete: Optional[Dict] = {}

class EndpointsBaseSchema(BaseModel):
    project: BeanieObjectId
    
    name: str
    endpoint: str

    methods: List[HttpMethods]
    endpoint_type: EndpointTypes
    static_data: StaticData
    dynamic_data: Optional[List[Dict[str, Any]]] = None


class EndpointsRequestSchema(EndpointsBaseSchema):
    pass


class EndpointsResponseSchema(EndpointsBaseSchema):
    id: BeanieObjectId
    project: Link[Project]