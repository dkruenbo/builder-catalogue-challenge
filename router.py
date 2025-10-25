from fastapi import APIRouter
from models import (
    UserAnalysisResult, UsersResponse, UserSummary, UserFull,
    SetsResponse, SetSummary, SetFull, ColorsResponse
)
from controller import analyze_user_builds
from functions import (
    get_all_users, get_user_by_username, get_user_by_id,
    get_all_sets, get_set_by_name, get_set_by_id, get_all_colors
)

router = APIRouter()

# =============================================================================
# Default API Endpoints - Direct mirror of external API
# =============================================================================

@router.get("/api/users", response_model=UsersResponse, tags=["default"])
async def api_all_users():
    """Get all available users"""
    return await get_all_users()


@router.get("/api/user/by-username/{username}", response_model=UserSummary, tags=["default"])
async def api_user_by_username(username: str):
    """Get user summary by username"""
    return await get_user_by_username(username)


@router.get("/api/user/by-id/{user_id}", response_model=UserFull, tags=["default"])
async def api_user_by_id(user_id: str):
    """Get full user data by ID"""
    return await get_user_by_id(user_id)


@router.get("/api/sets", response_model=SetsResponse, tags=["default"])
async def api_all_sets():
    """Get all available sets"""
    return await get_all_sets()


@router.get("/api/set/by-name/{name}", response_model=SetSummary, tags=["default"])
async def api_set_by_name(name: str):
    """Get set summary by name"""
    return await get_set_by_name(name)


@router.get("/api/set/by-id/{set_id}", response_model=SetFull, tags=["default"])
async def api_set_by_id(set_id: str):
    """Get full set data by ID"""
    return await get_set_by_id(set_id)


@router.get("/api/colours", response_model=ColorsResponse, tags=["default"])
async def api_all_colours():
    """Get all available colours"""
    return await get_all_colors()


# =============================================================================
# Brick Builder Catalogue Endpoints - Custom business logic
# =============================================================================

@router.get("/api/user/{username}/builds", response_model=UserAnalysisResult, tags=["brick-builder-catalogue"])
async def api_user_builds(username: str):
    """Analyze which sets a user can build with their collection"""
    return await analyze_user_builds(username)