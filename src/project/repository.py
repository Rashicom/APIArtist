from .models import Project
from authx.models import User
from beanie import BeanieObjectId
from .schema import ProjectUpdateSchema
from fastapi import HTTPException, status

class ProjectRepository:

    async def filter(*args, **kwargs):
        return await Project.find_all(kwargs).to_list()
    
    async def get_user_projects(user:User):
        return await Project.find(Project.user.id==user.id).to_list()
    
    async def retrieve_project(user:User, id:BeanieObjectId):
        return await Project.find_one(Project.user.id == user.id, Project.id == id)

    async def delete_project(user:User, id:str):
        proj_obj = await Project.find_one(Project.user.id==user.id, Project.id==BeanieObjectId(id))
        if not proj_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
        return proj_obj
    
    async def update_project(user:User, id:BeanieObjectId, data:ProjectUpdateSchema):
        project_obj = await Project.find_one(Project.user.id==user.id, Project.id==BeanieObjectId(id))
        if not project_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="project not found")
        await project_obj.set(data.model_dump())
        return project_obj

    async def create(*args, **kwargs):
        project = Project(**kwargs)
        await project.insert()
        return project