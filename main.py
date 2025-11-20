from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controller import UserController, MovieController, UserRatingController
from db import engine, Base
import model
from repository.exceptions import (UsernameExistsException, EmailExistsException, UserNotFoundException,
                                   MovieTitleExistsException, MovieNotFoundException, UserRatingNotFoundException,
                                   UserRatingExistsException)
from fastapi.responses import JSONResponse

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Дозволяє всі методи (GET, POST, PUT, DELETE)
    allow_headers=["*"],  # Дозволяє всі заголовки
)


app.include_router(UserController.router)
app.include_router(MovieController.router)
app.include_router(UserRatingController.router)
Base.metadata.create_all(bind=engine)

@app.exception_handler(UsernameExistsException)
async def username_exists_handler(_, exc: UsernameExistsException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(EmailExistsException)
async def email_exists_handler(_, exc: EmailExistsException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(_, exc: UserNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(MovieTitleExistsException)
async def movie_title_exists_handler(_, exc: MovieTitleExistsException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(MovieNotFoundException)
async def movie_not_found_handler(_, exc: MovieNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(UserRatingNotFoundException)
async def user_rating_not_found_handler(_, exc: UserRatingNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

@app.exception_handler(UserRatingExistsException)
async def user_rating_exists_handler(_, exc: UserRatingExistsException):
    return JSONResponse(status_code=409, content={"detail": str(exc)})