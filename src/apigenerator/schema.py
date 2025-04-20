from pydantic import BaseModel, field_serializer, field_validator, model_validator
from pydantic_core import PydanticCustomError
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
    static_data: Optional[StaticData] = None
    dynamic_data: Optional[List[Dict[str, Any]]] = None

    @field_validator("endpoint", mode="before")
    @classmethod
    def validate_endpoint(cls,endpoint):
        # validate for url restricted chars
        if any(char in endpoint for char in {' '}):
            raise PydanticCustomError(
                "Invalied endpoint",
                "endpoint should not contain any restricted chars"
            )
        # append prefix if not there
        return endpoint if endpoint.startswith("/") else f"/{endpoint}"

    @model_validator(mode="before")
    @classmethod
    def validate_endpoint_type(cls, data):
        # check the static data and dynamic data provided according to the endpoint type
        if data.get("endpoint_type") == EndpointTypes.STATIC:
            if not data.get("static_data"):
                raise PydanticCustomError(
                    "static_data",
                    "static_data must be provided for static endpoint"
                )
        elif data.get("endpoint_type") == EndpointTypes.DYNAMIC:
            if not data.get("dynamic_data"):
                raise PydanticCustomError(
                    "dynamic_data",
                    "dynamic_data must be provided for dynamic endpoint"
                )
        return data

class EndpointsRequestSchema(EndpointsBaseSchema):
    pass


class EndpointsResponseSchema(EndpointsBaseSchema):
    id: BeanieObjectId
    project: Link[Project]