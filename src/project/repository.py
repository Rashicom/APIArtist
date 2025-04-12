from .models import Project

class ProjectRepository:

    async def filter(*args, **kwargs):
        return await Project.find_all(kwargs).to_list()
    
    async def create(*args, **kwargs):
        project = Project(**kwargs)
        await project.insert()
        return project