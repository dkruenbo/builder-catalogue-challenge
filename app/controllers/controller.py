from fastapi import HTTPException
from app.models.models import UserAnalysisResult
from app.functions.functions import get_user_inventory, get_all_sets, get_set_requirements, can_build_set, get_all_users, get_set_by_id, get_all_colors


async def analyze_user_builds(username: str) -> UserAnalysisResult:
    """Analyze which sets a user can build"""
    try:
        inventory = await get_user_inventory(username)
        sets_response = await get_all_sets()
        sets = sets_response.Sets
        buildable = []
        unbuildable = []
        
        for s in sets:
            set_id = s.id
            requirements, set_name = await get_set_requirements(set_id)
            set_data = {
                'id': set_id,
                'name': set_name,
                'pieces': s.totalPieces,
                'set_number': s.setNumber
            }
            
            if can_build_set(inventory, requirements):
                buildable.append(set_data)
            else:
                unbuildable.append(set_data)
        
        result_data = {
            'username': username,
            'total_pieces': sum(inventory.values()),
            'unique_combinations': len(inventory),
            'total_sets': len(sets),
            'buildable_sets': sorted(buildable, key=lambda x: x['pieces']),
            'buildable_count': len(buildable),
            'unbuildable_sets': sorted(unbuildable, key=lambda x: x['pieces']),
            'unbuildable_count': len(unbuildable)
        }
        
        return UserAnalysisResult(**result_data)
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found or API error: {str(e)}")


async def analyze_set_build(set_id: str, username: str):
    """Analyze what pieces are needed to build a specific set"""
    try:
        # Get user inventory
        inventory = await get_user_inventory(username)
        
        # Get set information
        set_info = await get_set_by_id(set_id)
        
        # Get set requirements
        requirements_dict, _ = await get_set_requirements(set_id)
        
        # Get colors for better display
        colors_response = await get_all_colors()
        color_lookup = {str(color.code): color.name for color in colors_response.colours}
        
        # Build requirements list with user inventory comparison
        requirements = []
        can_build_all = True
        total_missing_pieces = 0
        missing_piece_types = 0
        
        for (piece_id, color_id), needed in requirements_dict.items():
            user_has = inventory.get((piece_id, color_id), 0)
            missing = max(0, needed - user_has)
            
            if user_has < needed:
                can_build_all = False
                missing_piece_types += 1
                total_missing_pieces += missing
            
            requirements.append({
                'piece_id': piece_id,
                'color_id': color_id,
                'color_name': color_lookup.get(color_id, None),
                'needed': needed,
                'user_has': user_has,
                'missing': missing
            })
        
        # Sort by whether user has enough pieces (insufficient first)
        requirements.sort(key=lambda x: (x['user_has'] >= x['needed'], x['piece_id']))
        
        return {
            'set_info': set_info,
            'requirements': requirements,
            'can_build': can_build_all,
            'username': username,
            'missing_piece_types': missing_piece_types,
            'total_missing_pieces': total_missing_pieces
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error analyzing set build: {str(e)}")


async def get_users_list():
    """Get list of all users"""
    users_response = await get_all_users()
    return users_response.Users


async def get_sets_list():
    """Get list of all sets"""
    sets_response = await get_all_sets()
    return sets_response.Sets