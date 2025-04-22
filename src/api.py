from authx.router import router as authx_router
from project.router import router as project_router
from apigenerator.router import router as apigenerator_router
from core.router import router as core_router

from fastapi import APIRouter

router = APIRouter()

router.include_router(authx_router, prefix="/authx", tags=["AuthX APIs"])
router.include_router(project_router, prefix="/project", tags=["Project APIs"])
router.include_router(apigenerator_router, prefix="/api-generator", tags=["API Generator"])
router.include_router(core_router,prefix="/", tags=["Core APIs"])