from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from repository.MovieRepository import MovieRepository
from service.MovieService import MovieService
from model.DTOs.MovieDTO import MovieOut, MovieCreate, MovieUpdate

router = APIRouter(tags=["Movie methods"])

@router.get("/movies/{id}", response_model=MovieOut)
async def get_movie(id: int, db: Session = Depends(get_db)):
    return MovieService(MovieRepository(db)).get_movie(id)

@router.post("/movies", response_model=MovieOut)
async def create_movie(dto: MovieCreate, db: Session = Depends(get_db)):
    return MovieService(MovieRepository(db)).create_movie(dto)

@router.put("/movies/{id}", response_model=MovieOut)
async def update_movie(id: int, dto: MovieUpdate, db: Session = Depends(get_db)):
    return MovieService(MovieRepository(db)).update_movie(id, dto)

@router.delete("/movies/{id}")
async def delete_movie(id: int, db: Session = Depends(get_db)):
    MovieService(MovieRepository(db)).delete_movie(id)

@router.get("/movies", response_model=List[MovieOut])
async def get_movies(db: Session = Depends(get_db)):
    return MovieService(MovieRepository(db)).get_all_movies()

@router.delete("/movies")
async def delete_movies(db: Session = Depends(get_db)):
    return  MovieService(MovieRepository(db)).delete_all_movies()
# @router.post("/movies/{movie_id}/watch/{user_id}")
# async def watch_movie(movie_id: int, user_id: int):
#     return MovieService.watch_movie(movie_id, user_id)