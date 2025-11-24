from fastapi import APIRouter
from src.routes.users import user_config
from src.routes.users import users

router = APIRouter()

router.include_router(user_config.router)
router.include_router(users.router)