from pydantic import (
    BaseModel,
    field_serializer,
    field_validator,
    model_validator,
    Field,
)
from pydantic_core import PydanticCustomError
from beanie import BeanieObjectId
from typing import Dict, List, Any, Optional, Union
from .enums import EndpointTypes, HttpMethods
from beanie import Link
from project.models import Project


class StaticData(BaseModel):
    get: Optional[
        Union[Dict, List[Dict]]
    ] = {}  # get data can be a dict or list of dicts
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

    @field_validator("endpoint", mode="before")
    @classmethod
    def validate_endpoint(cls, endpoint):
        # validate for url restricted chars
        if any(char in endpoint for char in {" "}):
            raise PydanticCustomError(
                "Invalied endpoint", "endpoint should not contain any restricted chars"
            )
        # append prefix if not there
        return endpoint if endpoint.startswith("/") else f"/{endpoint}"

    @model_validator(mode="before")
    @classmethod
    def validate_endpoint_type(cls, data: Dict):
        # check the static data and dynamic data provided according to the endpoint type
        if data.get("endpoint_type") == EndpointTypes.STATIC:
            if not data.get("static_data"):
                raise PydanticCustomError(
                    "static_data", "static_data must be provided for static endpoint"
                )
        elif data.get("endpoint_type") == EndpointTypes.DYNAMIC:
            if not data.get("dynamic_data"):
                raise PydanticCustomError(
                    "dynamic_data", "dynamic_data must be provided for dynamic endpoint"
                )
        return data

    @field_validator("static_data", mode="after")
    @classmethod
    def validate_static_data(cls, data):

        # validation only performed if data is not null
        if not data:
            return data

        # restrict get lenght if get data a list
        if isinstance(data.get, list):
            if len(data.get) > 5:
                raise PydanticCustomError(
                    "static_data", "get data should not exceede 5 objects"
                )
        return data


class EndpointsRequestSchema(EndpointsBaseSchema):
    dynamic_data: List[Dict] = Field(default_factory=list)


class EndpointsUpdateSchema(BaseModel):
    """
    only name, endpoint and methods can be changed
    project and endpoint type cant be changed once it defined
    """

    name: Optional[str] = None
    endpoint: Optional[str] = None

    methods: Optional[List[HttpMethods]] = None


class EndpointsResponseSchema(EndpointsBaseSchema):
    id: BeanieObjectId
    project: Link[Project]
