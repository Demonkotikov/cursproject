from fastapi import FastAPI
from app.api.v1 import (
    role_api_router, profile_api_router,
    olympiad_api_router, participation_api_router,
    auth_api_router  # <-- Новый роутер
)

app = FastAPI(title="АРМ для олимпиад")

app.include_router(auth_api_router.router, prefix="/api/v1")
app.include_router(role_api_router.router, prefix="/api/v1")
app.include_router(profile_api_router.router, prefix="/api/v1")
app.include_router(olympiad_api_router.router, prefix="/api/v1")
app.include_router(participation_api_router.router, prefix="/api/v1")

