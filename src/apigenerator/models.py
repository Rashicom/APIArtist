from beanie import Document, Link
from typing import Optional, List, Dict, Any
from authx.models import User
from project.models import Project
from pydantic import BaseModel

class HttpMethods(BaseModel):
    method: str

class Endpoints(Document):
    """
    api suffix pattern
        BASER_URL/uuid/api/<query>
    """
    user: Link[User]
    project: Link[Project]

    name: str = None
    endpoint: str
    
    # dynamic endpoint
    is_dynamic_endpoint: bool = False

    # if not dynamic endpoint, static data can be served
    """
    Example
        static_data = {
            "get":{data},
            "post":{},
            "patch":{}
        }
    """
    static_data: Dict[str, Any]

    methods: List[HttpMethods]

    meta = {
        'indexes': [
            {'field':('project', 'endpoint'), 'unique':True}
        ]
    }


class ResponseData(Document):
    endpoint = Link[Endpoints]
    data: Dict[str, Any]

