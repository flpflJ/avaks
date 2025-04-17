from fastapi import APIRouter

from .rtable.views import router as rrouter

router = APIRouter()
router.include_router(router=rrouter, prefix="/reference_books")
