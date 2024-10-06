from fastapi import APIRouter, Response
from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from fastapi_filter import FilterDepends


from db import make_session
from models.common import ErrorModel, SuccessModel
from models.movies import MovieModel, MovieCreateModel, MovieFilter
from orm.entities import Movie


from uuid import UUID


movies_router = APIRouter(tags=['movie'], prefix='/api/movies')


@movies_router.post('/')
async def create_movie(movie_model: MovieCreateModel, response: Response) -> MovieModel | ErrorModel:
    """
    Добавить фильм
    """
    async with make_session() as session:
        if not movie_model.title:
            response.status_code = 400
            return ErrorModel(error="Movie title cannot be empty")
        
        check_exists = await session.execute(select(Movie).where(Movie.title == movie_model.title))
        if check_exists.scalars().first():
            response.status_code = 400
            return ErrorModel(error="Movie with this title already exists")
        
        movie = Movie(**movie_model.model_dump())
        session.add(movie)
        await session.commit()
        
        return MovieModel(movie_id=movie.movie_id,
                          title=movie.title,
                          description=movie.description,
                          release_year=movie.release_year,
                          avg_rating=movie.avg_rating)
        

@movies_router.get('/')
async def get_all_movies(movie_filter: MovieFilter = FilterDepends(MovieFilter)) -> list[MovieModel]:
    """
    Получить все фильмы в БД с возможностью фильтрации (по названию, описанию, году релиза и/или рейтингу)
    
    """
    async with make_session() as session:
        query = select(Movie).order_by(Movie.movie_id)
        filtered_query = movie_filter.filter(query)
        result = await session.execute(filtered_query)
        out = []
        for movie, in result:
            out.append(movie)
            
    return out


@movies_router.get('/{movie_id}')
async def get_movie(movie_id: UUID, response: Response) -> MovieModel | ErrorModel:
    """
    Получить фильм по ID
    """ 
    async with make_session() as session:
        query = select(Movie).where(Movie.movie_id == movie_id)
        selection = await session.execute(query)
        try:
            return selection.scalar_one()
        except NoResultFound:
            response.status_code = 404
            return ErrorModel(error="Movie doesn't exist")


@movies_router.put('/{movie_id}')
async def update_movie(movie_id: UUID, movie_body: MovieCreateModel, response: Response) -> MovieModel | ErrorModel:
    """
    Замена информации о фильме
    """
    async with make_session() as session:
        query = update(Movie).where(Movie.movie_id == movie_id)\
            .values(**movie_body.model_dump())
        await session.execute(query)
        await session.commit()
    return await get_movie(movie_id, response)


@movies_router.delete('/{movie_id}')
async def delete_movie(movie_id: UUID, response: Response) -> SuccessModel | ErrorModel:
    """
    Удаление фильма
    """
    async with make_session() as session:
        try:
            query = delete(Movie).where(Movie.movie_id == movie_id)
            result = await session.execute(query)
            
            if result.rowcount == 0:
                response.status_code = 404
                return ErrorModel(error="Movie doesn't exist")
            
            await session.commit()
            return SuccessModel(success=True)
        except IntegrityError:
            response.status_code = 400
            return ErrorModel(error="Movie can't be deleted")
