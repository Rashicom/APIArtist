from project.models import Project
from project.repository import ProjectRepository
from beanie import BeanieObjectId
from fastapi import Request
from authx.models import User


async def get_project_by_id(user:User,project_id: BeanieObjectId):
    project_obj = ProjectRepository.retrieve_project(user,project_id)