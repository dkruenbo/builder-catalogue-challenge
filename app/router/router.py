from fastapi import APIRouter, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models.models import (
    UserAnalysisResult, UsersResponse, UserSummary, UserFull,
    SetsResponse, SetSummary, SetFull, ColorsResponse
)
from app.controllers.controller import analyze_user_builds, analyze_set_build
from app.functions.functions import (
    get_all_users, get_user_by_username, get_user_by_id,
    get_all_sets, get_set_by_name, get_set_by_id, get_all_colors
)

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# =============================================================================
# Frontend Routes
# =============================================================================

@router.get("/", response_class=HTMLResponse, tags=["frontend"])
async def home(request: Request):
    """Home page with user search form"""
    try:
        users_response = await get_all_users()
        users = users_response.Users
        return templates.TemplateResponse("index.html", {
            "request": request,
            "users": users
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "users": [],
            "error": f"Could not load users: {str(e)}"
        })


@router.post("/analyze", response_class=HTMLResponse, tags=["frontend"])
async def analyze_user(request: Request, username: str = Form(...)):
    """Analyze user's buildable sets and show results"""
    try:
        results = await analyze_user_builds(username.strip())
        return templates.TemplateResponse("results.html", {
            "request": request,
            "results": results
        })
    except HTTPException as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": e.detail,
            "username": username
        })


@router.get("/set/{set_id}/build/{username}", response_class=HTMLResponse, tags=["frontend"])
async def view_set_build(request: Request, set_id: str, username: str):
    """View detailed build requirements for a specific set"""
    try:
        build_data = await analyze_set_build(set_id, username)
        return templates.TemplateResponse("set-build.html", {
            "request": request,
            **build_data
        })
    except HTTPException as e:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": e.detail,
            "username": username
        })


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
    """Analyze which sets a user can build with their inventory"""
    return await analyze_user_builds(username)