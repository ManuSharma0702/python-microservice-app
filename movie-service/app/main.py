from fastapi import FastAPI

from app.api.movies import movies
from app.api.db import metadata, engine, database
from fastapi.middleware.cors import CORSMiddleware

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/movies/openapi.json", docs_url="/api/v1/movies/docs")

allowed_origins = [
    "http://127.0.0.1:5500/",
    "http://localhost:5500"
    ,"*"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,  # Allow all origins for now, but this should be restricted in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(movies, prefix='/api/v1/movies', tags=['movies'])



