from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime


Base = declarative_base()


class Movie(Base):
    __tablename__ = "movies"
    movie_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    release_year = Column(Integer, nullable=False)
    avg_rating = Column(Float, nullable=False, default=0.0)
    
    reviews = relationship("Review", back_populates="movie")
    
    
class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    movie_id = Column(UUID(as_uuid=True), ForeignKey("movies.movie_id"), nullable=False)
    review_content = Column(String, nullable=True)
    rate = Column(Integer, nullable=False)
    review_date = Column(DateTime, nullable=False, default=datetime.now)
    
    movie = relationship("Movie", back_populates="reviews")
