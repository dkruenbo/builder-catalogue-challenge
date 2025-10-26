from fastapi import HTTPException
from app.models.models import UserAnalysisResult, CollaborationResult, CollaborationOption, UserContribution
from app.functions.functions import (
    get_user_inventory, get_all_sets, get_set_requirements, can_build_set, 
    get_all_users, get_set_by_id, get_all_colors, calculate_user_contribution
)
from itertools import combinations


async def analyze_user_builds(username: str) -> UserAnalysisResult:
    """Analyze which sets a user can build with their collection"""
    try:
        # Get user's piece inventory
        inventory = await get_user_inventory(username)
        sets_response = await get_all_sets()
        sets = sets_response.Sets
        buildable = []
        unbuildable = []
        
        # Check each set against user's inventory
        for s in sets:
            set_id = s.id
            requirements, set_name = await get_set_requirements(set_id)
            set_data = {
                'id': set_id,
                'name': set_name,
                'pieces': s.totalPieces,
                'set_number': s.setNumber
            }
            
            # Categorize as buildable or not
            if can_build_set(inventory, requirements):
                buildable.append(set_data)
            else:
                unbuildable.append(set_data)
        
        # Compile results with statistics
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
    """Analyze detailed piece requirements for building a specific set"""
    try:
        # Get user inventory and set information
        inventory = await get_user_inventory(username)
        set_info = await get_set_by_id(set_id)
        requirements_dict, _ = await get_set_requirements(set_id)
        
        # Get color names for display
        colors_response = await get_all_colors()
        color_lookup = {str(color.code): color.name for color in colors_response.colours}
        
        # Build detailed requirements list with availability
        requirements = []
        can_build_all = True
        total_missing_pieces = 0
        missing_piece_types = 0
        
        for (piece_id, color_id), needed in requirements_dict.items():
            user_has = inventory.get((piece_id, color_id), 0)
            missing = max(0, needed - user_has)
            
            # Track missing pieces for statistics
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
        
        # Sort by availability (insufficient pieces first)
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


async def find_collaboration_partners(original_username: str, set_id: str, max_collaborators: int = 3) -> CollaborationResult:
    """Find other users who can collaborate to build a set together"""
    try:
        # Get original user's inventory and set requirements
        original_inventory = await get_user_inventory(original_username)
        set_info = await get_set_by_id(set_id)
        requirements_dict, _ = await get_set_requirements(set_id)
        
        # Calculate what pieces the original user is missing
        missing_pieces = {}
        total_missing_pieces = 0
        
        for (piece_id, color_id), needed in requirements_dict.items():
            user_has = original_inventory.get((piece_id, color_id), 0)
            if user_has < needed:
                missing = needed - user_has
                missing_pieces[(piece_id, color_id)] = missing
                total_missing_pieces += missing
        
        # If user can already build alone, no collaboration needed
        if not missing_pieces:
            return CollaborationResult(
                original_username=original_username,
                set_info=set_info.dict(),
                total_missing_pieces=0,
                missing_piece_types=0,
                collaboration_options=[],
                no_collaboration_found=False
            )
        
        # Get all potential collaborators (exclude original user)
        all_users = await get_all_users()
        potential_collaborators = [user for user in all_users.Users if user.username != original_username]
        
        collaboration_options = []
        
        # Try single collaborators first (most efficient)
        for user in potential_collaborators:
            try:
                user_inventory = await get_user_inventory(user.username)
                contribution = calculate_user_contribution(user, user_inventory, missing_pieces)
                
                if contribution['pieces_contributed'] > 0:
                    # Check if this single collaboration completes the set
                    remaining_missing = {}
                    for (piece_id, color_id), needed in missing_pieces.items():
                        user_provides = user_inventory.get((piece_id, color_id), 0)
                        still_missing = max(0, needed - user_provides)
                        if still_missing > 0:
                            remaining_missing[(piece_id, color_id)] = still_missing
                    
                    if len(remaining_missing) == 0:  # Complete collaboration found
                        collaboration_options.append(CollaborationOption(
                            collaborators=[UserContribution(**contribution)],
                            total_users=2,  # original + 1 collaborator
                            missing_pieces_filled=contribution['pieces_contributed'],
                            success_rate=100.0
                        ))
            except Exception:
                continue  # Skip users with API issues
        
        # Try pairs if no single collaborator works and we have few complete solutions
        if len([opt for opt in collaboration_options if opt.success_rate == 100.0]) < 3:
            # Get usernames already used in single collaborator solutions
            used_collaborators = set()
            for option in collaboration_options:
                if option.success_rate == 100.0:  # Only exclude from complete solutions
                    for collaborator in option.collaborators:
                        used_collaborators.add(collaborator.username)
            
            for user1, user2 in combinations(potential_collaborators[:20], 2):  # Limit to avoid too many API calls
                # Skip if either user is already in a complete single collaboration
                if user1.username in used_collaborators or user2.username in used_collaborators:
                    continue
                    
                try:
                    user1_inventory = await get_user_inventory(user1.username)
                    user2_inventory = await get_user_inventory(user2.username)
                    
                    contribution1 = calculate_user_contribution(user1, user1_inventory, missing_pieces)
                    contribution2 = calculate_user_contribution(user2, user2_inventory, missing_pieces)
                    
                    # Check if combined they can complete the set
                    remaining_missing = {}
                    for (piece_id, color_id), needed in missing_pieces.items():
                        combined_provides = (user1_inventory.get((piece_id, color_id), 0) + 
                                           user2_inventory.get((piece_id, color_id), 0))
                        still_missing = max(0, needed - combined_provides)
                        if still_missing > 0:
                            remaining_missing[(piece_id, color_id)] = still_missing
                    
                    if len(remaining_missing) == 0:  # Complete collaboration found
                        total_contributed = contribution1['pieces_contributed'] + contribution2['pieces_contributed']
                        collaboration_options.append(CollaborationOption(
                            collaborators=[
                                UserContribution(**contribution1),
                                UserContribution(**contribution2)
                            ],
                            total_users=3,  # original + 2 collaborators
                            missing_pieces_filled=total_contributed,
                            success_rate=100.0
                        ))
                except Exception:
                    continue
        
        # Sort by success rate (complete solutions first), then by fewer collaborators
        collaboration_options.sort(key=lambda x: (-x.success_rate, x.total_users))
        
        # Limit to top 10 options
        collaboration_options = collaboration_options[:10]
        
        return CollaborationResult(
            original_username=original_username,
            set_info=set_info.dict(),
            total_missing_pieces=total_missing_pieces,
            missing_piece_types=len(missing_pieces),
            collaboration_options=collaboration_options,
            no_collaboration_found=len(collaboration_options) == 0
        )
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error finding collaboration partners: {str(e)}")