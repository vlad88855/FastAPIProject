from fastapi import FastAPI

from controller import UserController, MovieController, UserRatingController

app = FastAPI()
app.include_router(UserController.router)
app.include_router(MovieController.router)
app.include_router(UserRatingController.router)
