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

    methods: List[HttpMethods]

    meta = {
        'indexes': [
            {'field':('project', 'endpoint'), 'unique':True}
        ]
    }


class ResponseData(Document):
    endpoint = Link[Endpoints]
    data: Dict[str, Any]

