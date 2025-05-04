from fastapi import APIRouter
from app.news.admin.views import router as admin_router
from app.news.likes.views import router as likes_router


router = APIRouter(tags=["News"])

router.include_router(admin_router, prefix="/admin")
router.include_router(likes_router, prefix="/likes")
