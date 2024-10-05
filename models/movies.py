from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID


class MovieCreateModel(BaseModel):
    title: str
    description: str
    release_year: int
    avg_rating: float
    
    
class MovieModel(MovieCreateModel):
    movie_id: UUID
    
    
class MoviePatchModel(BaseModel):
    title: str = Field(...)
    description: Optional[str] = Field(None)
    release_year: int = Field(...)
    avg_rating: float = Field(...)