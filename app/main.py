from fastapi import FastAPI
from . import models
from .database import engine
from . routers import post, user, auth, vote
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

'''

    Middleware is a function that runs before every request

'''

origins = ["*"]  # with * -> we allow every domain to talk with our API

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # we specify the origins that could talk with our API
    allow_credentials=True,
    allow_methods=["*"],  # we could specify some specific HTTP methods
    allow_headers=["*"],  # ->
    # we could allow only spcific headers for our public API
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get('/')
def root():
    return {'message': 'hello my first app'}
