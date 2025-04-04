from authx.router import router as authx_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(authx_router, prefix="/authx", tags=["AuthX"])