from beanie import Document, Link
from typing import Optional, List, Dict, Any
from authx.models import User
from project.models import Project
from pydantic import BaseModel, Field
from .enums import EndpointTypes, HttpMethods
from .schema import StaticData


class Endpoints(Document):
    """
    api suffix pattern
        BASER_URL/uuid/api/<query>
    """

    user: Link[User]
    project: Link[Project]

    name: str = None
    endpoint: str

    methods: List[HttpMethods]

    """
    End point type
    - static:
        user can define the response data which is not effected by any other methods such as patch, delete, put
    - dynamic (real api)
        user can define the response data and the data which is effected by other requests such as put, patch and delete
        this endpoints bahaves like a real api
    """
    endpoint_type: EndpointTypes

    # if static endpoint, static data can be served
    """
    Example
        static_data = {
            "get":{data},
            "post":{},
            "patch":{}
        }
    """
    static_data: Optional[StaticData] = None


class DynamicData(Document):
    """
    This table store the data of dynamic api
    endpoints can filter and change the data(put,patch, delete)

    records limit:
        - an endpoints can have n number of records accordint to which package they purchased

    data : -
        - data is considred as a row in table
        - each data post create a object in this collection

    WARNING : as data grows this collection size can grow to critical
    SOLUTION TODO:
        - make data as a List[Dict] and restrict size of list to a appropreate len wich size less than mondodb max value size
        - one the max limit of one object reached save other data in a new record
        - while retrieving/operation data, aggrage all data then perform

    """

    endpoint: Link[Endpoints]
    data: dict = Field(default_factory=dict)
