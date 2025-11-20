from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db import get_db
from repository.MovieRepository import MovieRepository
from service.MovieService import MovieService
from model.DTOs.MovieDTO import MovieOut, MovieCreate, MovieUpdate, MovieGenre
from dependencies import get_movie_service


router = APIRouter(tags=["Movie methods"])

@router.get("/movies/{id}", response_model=MovieOut)
async def get_movie(id: int, service: MovieService = Depends(get_movie_service)):
    return service.get_movie(id)


@router.post("/movies", response_model=MovieOut)
async def create_movie(dto: MovieCreate, service: MovieService = Depends(get_movie_service)):
    return service.create_movie(dto)


@router.put("/movies/{id}", response_model=MovieOut)
async def update_movie(id: int, dto: MovieUpdate, service: MovieService = Depends(get_movie_service)):
    return service.update_movie(id, dto)


@router.delete("/movies/{id}")
async def delete_movie(id: int, service: MovieService = Depends(get_movie_service)):
    service.delete_movie(id)


@router.get("/movies", response_model=List[MovieOut])
async def get_movies(
    skip: int = 0,
    limit: Optional[int] = None,
    genre: Optional[MovieGenre] = None,
    service: MovieService = Depends(get_movie_service)
):
    return service.get_all_movies(skip, limit, genre)


@router.delete("/movies")
async def delete_movies(service: MovieService = Depends(get_movie_service)):
    return  service.delete_all_movies()

# @router.post("/movies/{movie_id}/watch/{user_id}")
# async def watch_movie(movie_id: int, user_id: int):
#     return MovieService.watch_movie(movie_id, user_id)