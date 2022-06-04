from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api_descriptions import main_description, tags_metadata
from .api.v1.api import api_router

app = FastAPI(
    title="Apogee",
    openapi_tags=tags_metadata,
    description=main_description,
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
