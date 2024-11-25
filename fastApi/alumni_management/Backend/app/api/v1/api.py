from fastapi import APIRouter, Depends, HTTPException
from typing import List
from users.routes import router as users_router
from alumni.routes import router as alumni_router
from events.routes import router as events_router
from users.services import get_current_user
from users.schemas import User

api_router = APIRouter()

# Include main routers
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(alumni_router, prefix="/alumni", tags=["alumni"])
api_router.include_router(events_router, prefix="/events", tags=["events"])

# System endpoints
@api_router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "database": "up",
            "cache": "up",
            "storage": "up"
        }
    }

@api_router.get("/version")
async def get_version():
    return {
        "version": "1.0.0",
        "build": "123",
        "environment": "production"
    }

# Admin endpoints
@api_router.get("/admin/stats", tags=["admin"])
async def get_stats(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    
    return {
        "total_users": 100,
        "total_alumni": 80,
        "total_events": 25,
        "active_users": 75
    }

# Search endpoint
@api_router.get("/search", tags=["search"])
async def search(
    q: str,
    type: str = None,
    current_user: User = Depends(get_current_user)
):
    return {
        "results": [
            {"type": "alumni", "data": {}},
            {"type": "event", "data": {}}
        ],
        "total": 2
    }