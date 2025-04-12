from authx.router import router as authx_router
from project.router import router as project_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(authx_router, prefix="/authx", tags=["AuthX APIs"])
router.include_router(project_router, prefix="/project", tags=["Project APIs"])