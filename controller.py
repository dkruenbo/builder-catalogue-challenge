from fastapi import HTTPException
from models import UserAnalysisResult
from functions import get_user_inventory, get_all_sets, get_set_requirements, can_build_set, get_all_users


async def analyze_user_builds(username: str) -> UserAnalysisResult:
    """Analyze which sets a user can build"""
    try:
        inventory = await get_user_inventory(username)
        sets_response = await get_all_sets()
        sets = sets_response.Sets
        buildable = []
        
        for s in sets:
            set_id = s.id
            requirements, set_name = await get_set_requirements(set_id)
            if can_build_set(inventory, requirements):
                buildable.append({
                    'name': set_name,
                    'pieces': s.totalPieces,
                    'set_number': s.setNumber
                })
        
        result_data = {
            'username': username,
            'total_pieces': sum(inventory.values()),
            'unique_combinations': len(inventory),
            'total_sets': len(sets),
            'buildable_sets': sorted(buildable, key=lambda x: x['pieces']),
            'buildable_count': len(buildable)
        }
        
        return UserAnalysisResult(**result_data)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found or API error: {str(e)}")


async def get_users_list():
    """Get list of all users"""
    users_response = await get_all_users()
    return users_response.Users


async def get_sets_list():
    """Get list of all sets"""
    sets_response = await get_all_sets()
    return sets_response.Sets