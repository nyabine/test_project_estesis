from fastapi import FastAPI

from public.movies import movies_router
from public.reviews import reviews_router

app = FastAPI()

app.include_router(movies_router)
app.include_router(reviews_router)