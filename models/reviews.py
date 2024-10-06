from typing import Optional
from pydantic import BaseModel, Field
from uuid import UUID
import datetime


class ReviewCreateModel(BaseModel):
    movie_id: UUID
    review_content: str
    rate: int 
    
    
class ReviewModel(ReviewCreateModel):
    review_id: UUID
    review_date: Optional[datetime.datetime] = datetime.datetime.now()
    
    
class ReviewPatchModel(BaseModel):
    movie_id: UUID = Field(...)
    review_content: str = Field(...)
    rate: int = Field(...)
    review_date: Optional[datetime.datetime] = None
