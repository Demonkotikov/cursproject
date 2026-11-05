from fastapi import FastAPI
from app.api.v1 import (
    role_api_router, 
    profile_api_router, 
    olympiad_api_router,       # <-- Новый
    participation_api_router   # <-- Новый
)

app = FastAPI(title="Olympiad ARMA API")

app.include_router(role_api_router.router, prefix="/api/v1")
app.include_router(profile_api_router.router, prefix="/api/v1")
app.include_router(olympiad_api_router.router, prefix="/api/v1")        # <-- Новый
app.include_router(participation_api_router.router, prefix="/api/v1")   # <-- Новый

@app.get("/")
def root():
    return {"message": "API is running! Go to /docs to see all endpoints."}