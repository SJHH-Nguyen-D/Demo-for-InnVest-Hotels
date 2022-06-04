from fastapi import APIRouter

from ...core.config import settings
from .endpoints import (
    hotels,
    accommodations,
    transactions,
    reviews,
)

api_prefix = settings.API_V1_STR

api_router = APIRouter()
api_router.include_router(hotels.router, prefix=api_prefix, tags=[api_prefix, "health"])

api_router.include_router(accommodations.router, prefix=api_prefix, tags=[api_prefix, "health"])
api_router.include_router(transactions.router, prefix=api_prefix, tags=[api_prefix, "health"])
api_router.include_router(reviews.router, prefix=api_prefix, tags=[api_prefix, "health"])
