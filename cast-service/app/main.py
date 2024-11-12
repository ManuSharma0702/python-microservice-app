from fastapi import FastAPI
from app.api.casts import casts
from app.api.db import metadata, database, engine
from fastapi.middleware.cors import CORSMiddleware
metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/casts/openapi.json", docs_url="/api/v1/casts/docs")


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

app.include_router(casts, prefix='/api/v1/casts', tags=['casts'])