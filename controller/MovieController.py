from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from db import get_db

from controller.UserController import get_user
from service.MovieService import MovieService
from model.Movie import Movie

router = APIRouter()

@router.get("/movies/{id}")
async def get_movie(id: int):
    return MovieService.get_movie(id)

@router.post("/movies")
async def create_movie(title: str, year:int, genre: str, view_count: int | None = None):
    return MovieService.create_movie(title, year, genre, view_count)

@router.put("/movies/{id}")
async def update_movie(id: int, title: str, year:int, genre: str, view_count: int | None = None):
    return MovieService.update_movie(id, title, year, genre, view_count)

@router.delete("/movies/{id}")
async def delete_movie(id: int):
    return MovieService.delete_movie(id)

@router.get("/movies")
async def get_movies():
    return MovieService.get_all_movies()

@router.delete("/movies")
async def delete_movies():
    return MovieService.delete_all_movies()

@router.post("/movies/{movie_id}/watch/{user_id}")
async def watch_movie(movie_id: int, user_id: int):
    return MovieService.watch_movie(movie_id, user_id)