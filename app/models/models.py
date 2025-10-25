from pydantic import BaseModel
from typing import List


# User-related models
class UserSummary(BaseModel):
    id: str
    username: str
    location: str
    brickCount: int


class PieceVariant(BaseModel):
    color: str
    count: int


class Piece(BaseModel):
    pieceId: str
    variants: List[PieceVariant]


class UserFull(BaseModel):
    id: str
    username: str
    location: str
    brickCount: int
    collection: List[Piece]


class UsersResponse(BaseModel):
    Users: List[UserSummary]


# Set-related models
class SetSummary(BaseModel):
    id: str
    name: str
    setNumber: str
    totalPieces: int


class SetPart(BaseModel):
    designID: str
    material: int
    partType: str


class SetPiece(BaseModel):
    part: SetPart
    quantity: int


class SetFull(BaseModel):
    id: str
    name: str
    setNumber: str
    totalPieces: int
    pieces: List[SetPiece]


class SetsResponse(BaseModel):
    Sets: List[SetSummary]


# Color-related models
class Color(BaseModel):
    name: str
    code: int


class ColorsResponse(BaseModel):
    colours: List[Color]
    disclaimer: str


# Analysis result models
class BuildableSet(BaseModel):
    id: str
    name: str
    pieces: int
    set_number: str


class UserAnalysisResult(BaseModel):
    username: str
    total_pieces: int
    unique_combinations: int
    total_sets: int
    buildable_sets: List[BuildableSet]
    buildable_count: int
    unbuildable_sets: List[BuildableSet]
    unbuildable_count: int