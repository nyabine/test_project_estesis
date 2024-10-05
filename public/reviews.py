from fastapi import APIRouter, Response
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.sql import func


from db import make_session
from models.common import ErrorModel, SuccessModel
from models.reviews import ReviewModel, ReviewCreateModel, ReviewPatchModel
from orm.entities import Movie, Review


from uuid import UUID
from datetime import datetime


reviews_router = APIRouter(tags=['review'], prefix='/api/movies')

      
@reviews_router.post('/{movie_id}/reviews')
async def create_review(review_model: ReviewCreateModel, movie_id = UUID) -> ReviewModel | ErrorModel:
    """
    Добавить отзыв
    """
    async with make_session() as session:
        review = Review(**review_model.model_dump())
        session.add(review)
        await session.flush()
        
        query = select(func.avg(Review.rate)).where(Review.movie_id == movie_id)
        avg_rating_result = await session.execute(query)
        avg_rating = avg_rating_result.scalar() or 0.0
        
        update_query = update(Movie).where(Movie.movie_id == movie_id).values(avg_rating=avg_rating)
        await session.execute(update_query)

        await session.commit()
        
        return ReviewModel(review_id = review.review_id,
                           movie_id = movie_id,
                           review_content = review.review_content,
                           rate = review.rate,
                           review_date = review.review_date)
    

@reviews_router.get('/{movie_id}/reviews')
async def get_all_film_reviews(movie_id: UUID) -> list[ReviewModel]:
    """
    Получить все отзывы на фильм в БД
    """
    async with make_session() as session:
        query = await session.execute(select(Review).where(Review.movie_id == movie_id).order_by(Review.review_id))
        out = []
        for review, in query:
            out.append(review)
            
    return out


@reviews_router.get('/{movie_id}/reviews/{review_id}')
async def get_review(movie_id: UUID, review_id: UUID, response: Response) -> ReviewModel | ErrorModel:
    """
    Получить отзыв по ID
    """ 
    async with make_session() as session:
        query = select(Review).where(Review.movie_id == movie_id, Review.review_id == review_id)
        selection = await session.execute(query)
        try:
            return selection.scalar_one()
        except NoResultFound:
            response.status_code = 404
            return ErrorModel(error="Review doesn't exist")


@reviews_router.delete('/{movie_id}/reviews/{review_id}')
async def delete_review(movie_id: UUID, review_id: UUID, response: Response) -> SuccessModel | ErrorModel:
    """
    Удаление отзыва
    """
    async with make_session() as session:
        try:
            delete_query = delete(Review).where(Review.review_id == review_id, Review.movie_id == movie_id)
            await session.execute(delete_query)

            avg_rating_query = select(func.avg(Review.rate)).where(Review.movie_id == movie_id)
            avg_rating_result = await session.execute(avg_rating_query)
            avg_rating = avg_rating_result.scalar() or 0.0

            update_query = update(Movie).where(Movie.movie_id == movie_id).values(avg_rating=avg_rating)
            await session.execute(update_query)

            await session.commit()
            return SuccessModel(success=True)
        except IntegrityError:
            response.status_code = 400
            return ErrorModel(error="Review can't be deleted")

@reviews_router.post('/{movie_id}/rate')
async def rate_film(movie_id: UUID, rate: int, response: Response) -> SuccessModel | ErrorModel:
    """
    Поставить оценку фильму (создает отзыв без содержания)
    """
    async with make_session() as session:
        try:
            review = Review(movie_id=movie_id, rate=rate, review_content = "", review_date=datetime.now())
            session.add(review)
            await session.flush()

            query = select(func.avg(Review.rate)).where(Review.movie_id == movie_id)
            avg_rating_result = await session.execute(query)
            avg_rating = avg_rating_result.scalar() or 0.0
            
            update_query = update(Movie).where(Movie.movie_id == movie_id).values(avg_rating=avg_rating)
            await session.execute(update_query)

            await session.commit()
            
            return SuccessModel(success=True)
        except IntegrityError:
            response.status_code = 400
            return ErrorModel(error="Unable to add rating")
            