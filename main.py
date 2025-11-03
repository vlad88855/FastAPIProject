from fastapi import FastAPI
from controller import UserController, MovieController, UserRatingController
from db import engine, Base
import model


app = FastAPI()
app.include_router(UserController.router)
app.include_router(MovieController.router)
app.include_router(UserRatingController.router)
Base.metadata.create_all(bind=engine)

