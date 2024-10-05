from pydantic import BaseModel, Field
from uuid import UUID
import datetime


class ReviewCreateModel(BaseModel):
    movie_id: UUID
    review_content: str
    rate: int
    review_date: datetime.datetime
    
    
class ReviewModel(ReviewCreateModel):
    review_id: UUID
    
    
class ReviewPatchModel(BaseModel):
    movie_id: UUID = Field(...)
    review_content: str = Field(...)
    rate: int = Field(...)
    review_date: datetime.datetime = Field(...)
