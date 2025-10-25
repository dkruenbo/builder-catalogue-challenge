from collections import defaultdict
from typing import Dict, Tuple
import httpx
from models import (
    UsersResponse, UserSummary, UserFull,
    SetsResponse, SetSummary, SetFull,
    ColorsResponse
)

API_BASE = "https://d30r5p5favh3z8.cloudfront.net"


async def get_json(url: str) -> dict:
    """Async HTTP client for API calls"""
    headers = {
        'User-Agent': 'Brick-Builder-Catalogue/1.0',
        'Accept': 'application/json'
    }
    async with httpx.AsyncClient(headers=headers, timeout=30.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()


# User-related functions
async def get_all_users() -> UsersResponse:
    """Get all available users"""
    response_data = await get_json(f"{API_BASE}/api/users")
    return UsersResponse(**response_data)


async def get_user_by_username(username: str) -> UserSummary:
    """Get user summary by username"""
    response_data = await get_json(f"{API_BASE}/api/user/by-username/{username}")
    return UserSummary(**response_data)


async def get_user_by_id(user_id: str) -> UserFull:
    """Get full user data by ID"""
    response_data = await get_json(f"{API_BASE}/api/user/by-id/{user_id}")
    return UserFull(**response_data)


# Set-related functions
async def get_all_sets() -> SetsResponse:
    """Get all available brick sets"""
    response_data = await get_json(f"{API_BASE}/api/sets")
    return SetsResponse(**response_data)


async def get_set_by_name(name: str) -> SetSummary:
    """Get set summary by name"""
    response_data = await get_json(f"{API_BASE}/api/set/by-name/{name}")
    return SetSummary(**response_data)


async def get_set_by_id(set_id: str) -> SetFull:
    """Get full set data by ID"""
    response_data = await get_json(f"{API_BASE}/api/set/by-id/{set_id}")
    return SetFull(**response_data)


# Color-related functions
async def get_all_colors() -> ColorsResponse:
    """Get all available colors"""
    response_data = await get_json(f"{API_BASE}/api/colours")
    return ColorsResponse(**response_data)


# Utility functions for analysis
async def get_user_inventory(username: str) -> Dict[Tuple[str, str], int]:
    """Get user's brick piece inventory"""
    user_summary = await get_user_by_username(username)
    user_data = await get_user_by_id(user_summary.id)
    
    inventory = defaultdict(int)
    for piece in user_data.collection:
        piece_id = piece.pieceId
        for variant in piece.variants:
            color_id = variant.color
            count = variant.count
            key = (piece_id, color_id)
            inventory[key] += count
    return inventory


async def get_set_requirements(set_id: str) -> Tuple[Dict[Tuple[str, str], int], str]:
    """Get piece requirements for a specific set"""
    set_data = await get_set_by_id(set_id)
    
    requirements = defaultdict(int)
    for item in set_data.pieces:
        piece_id = item.part.designID
        color_id = str(item.part.material)
        quantity = item.quantity
        key = (piece_id, color_id)
        requirements[key] += quantity
    return requirements, set_data.name


def can_build_set(inventory: Dict[Tuple[str, str], int], requirements: Dict[Tuple[str, str], int]) -> bool:
    """Check if user has enough pieces to build a set"""
    for key, needed in requirements.items():
        if inventory.get(key, 0) < needed:
            return False
    return True