from fastapi import APIRouter, Depends

from dependencies.auth import user_basic_auth_required_for_unsafe_methods
from rest.short_urls.create_views import router as create_views_router
from rest.short_urls.list_views import router as list_views_router

router = APIRouter(
    tags=["Short URLs rest"],
    prefix="/short-urls",
    dependencies=[Depends(user_basic_auth_required_for_unsafe_methods)],
)
router.include_router(list_views_router)
router.include_router(create_views_router)
