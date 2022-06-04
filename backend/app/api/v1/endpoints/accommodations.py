import uuid
from typing import List

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ....core import config
from ....models import crud, models, schemas
from ....models.database import get_db
from ..logger.exception_decor import exception
from ..logger.exception_logger import logger

router = APIRouter()

@router.get(
    "/accommodations/{accommodation_id}",
    status_code=status.HTTP_200_OK,
    tags=["read"],
    response_model=schemas.Accommodations,
)
def get_accommodation_by_id(
    accommodation_id: str,
    db: Session = Depends(get_db),
):
    """
    :param accommodation_id: The UUID value that denotes the domain of the website. This also populates the routing path.
    :param db: The database object. Depends on the currently active db session.
    :return: Corresponding accommodation record from the db.
    """
    acc = crud.get_acc_by_id(accommodation_id, db)
    if acc:
        return acc 
    else:
        raise HTTPException(404, detail=f"Accommodiation with id: <{accommodation_id}> not found.")

