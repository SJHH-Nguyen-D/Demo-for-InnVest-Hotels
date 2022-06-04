import shutil
import uuid
from tempfile import NamedTemporaryFile
from typing import List

import boto3
from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ....core import config
from ....models import crud, models, schemas
from ....models.database import get_db
from ..logger.exception_decor import exception
from ..logger.exception_logger import logger

router = APIRouter()

@router.get(
    "/hotels/{hotel_id}",
    status_code=status.HTTP_200_OK,
    tags=["read"],
    response_model=schemas.Hotels,
)
def get_hotel_by_id(
    hotel_id: str,
    db: Session = Depends(get_db),
):
    """
    :param hotel_id: The UUID value .
    :param db: The database object. Depends on the currently active db session.
    :return: Corresponding hotel record from the db.
    """
    hotel = crud.get_hotel_by_id(hotel_id, db)
    if hotel:
        return hotel 
    else:
        raise HTTPException(404, detail=f"Hotel with id: <{hotel_id}> not found.")
