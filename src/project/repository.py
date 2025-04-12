from .models import Project
from authx.models import User
from beanie import BeanieObjectId

class ProjectRepository:

    async def filter(*args, **kwargs):
        return await Project.find_all(kwargs).to_list()
    
    async def get_user_projects(user:User):
        return await Project.find(Project.user.id==user.id).to_list()

    async def delete_project(user:User, id:str):
        await Project.find(Project.user.id==user.id, Project.id==BeanieObjectId(id)).delete()

    async def create(*args, **kwargs):
        project = Project(**kwargs)
        await project.insert()
        return project