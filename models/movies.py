from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
from fastapi_filter.contrib.sqlalchemy import Filter
from orm.entities import Movie


class MovieCreateModel(BaseModel):
    title: str
    description: str
    release_year: int   
    
    
class MovieModel(MovieCreateModel):
    movie_id: UUID
    avg_rating: float
    
    
class MoviePatchModel(BaseModel):
    title: str = Field(...)
    description: Optional[str] = Field(None)
    release_year: int = Field(...)
    avg_rating: float = Field(...)
    
    
class MovieFilter(Filter):
    title__in: Optional[list[str]] = Field(default=None, alias="title")
    description__in: Optional[list[str]] = Field(default=None, alias="description")
    release_year__gte: Optional[int] = Field(default=None, alias="release_year")
    avg_rating__lt: Optional[float] = Field(default=None, alias="avg_rating")
    
    class Constants(Filter.Constants):
        model = Movie
    
    class Config:
        populate_by_name = True
        