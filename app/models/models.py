from pydantic import BaseModel
from typing import List


# =============================================================================
# User-related models
# =============================================================================

class UserSummary(BaseModel):  # Basic user info without collection
    id: str
    username: str
    location: str
    brickCount: int


class PieceVariant(BaseModel):  # Color variant of a piece type
    color: str
    count: int


class Piece(BaseModel):  # Piece type with all color variants
    pieceId: str
    variants: List[PieceVariant]


class UserFull(BaseModel):  # Complete user info with full collection
    id: str
    username: str
    location: str
    brickCount: int
    collection: List[Piece]


class UsersResponse(BaseModel): # Response model for all users
    Users: List[UserSummary]


# Set-related models
class SetSummary(BaseModel): # Basic set info
    id: str
    name: str
    setNumber: str
    totalPieces: int


class SetPart(BaseModel): # A part in a set
    designID: str
    material: int
    partType: str


class SetPiece(BaseModel): # A piece with quantity in a set
    part: SetPart
    quantity: int


class SetFull(BaseModel): # Full set info including pieces
    id: str
    name: str
    setNumber: str
    totalPieces: int
    pieces: List[SetPiece]


class SetsResponse(BaseModel): # Response model for all sets
    Sets: List[SetSummary]


# Color-related models
class Color(BaseModel): # A color entry
    name: str
    code: int


class ColorsResponse(BaseModel): # Response model for all colors
    colours: List[Color]
    disclaimer: str


# Analysis result models
class BuildableSet(BaseModel): # A set that can be built
    id: str
    name: str
    pieces: int
    set_number: str


class UserAnalysisResult(BaseModel): # Analysis result for a user's buildable sets
    username: str
    total_pieces: int
    unique_combinations: int
    total_sets: int
    buildable_sets: List[BuildableSet]
    buildable_count: int
    unbuildable_sets: List[BuildableSet]
    unbuildable_count: int


# Collaboration models
class UserContribution(BaseModel): # A user's contribution to filling missing pieces
    username: str
    user_id: str
    location: str
    total_pieces: int
    pieces_contributed: int
    missing_pieces_filled: List[dict]


class CollaborationOption(BaseModel): # An option for collaboration
    collaborators: List[UserContribution]
    total_users: int
    missing_pieces_filled: int
    success_rate: float 


class CollaborationResult(BaseModel): # Result of collaboration analysis
    original_username: str
    set_info: dict
    total_missing_pieces: int
    missing_piece_types: int
    original_user_pieces_provided: List[dict]
    original_user_total_contribution: int
    collaboration_options: List[CollaborationOption]
    no_collaboration_found: bool