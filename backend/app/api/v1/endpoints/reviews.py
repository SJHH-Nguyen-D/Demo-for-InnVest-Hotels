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
    "/transactions/{transaction_id}",
    status_code=status.HTTP_200_OK,
    tags=["read"],
    response_model=schemas.Transactions,
)
def get_transaction_by_id(
    transaction_id: str,
    db: Session = Depends(get_db),
):
    """
    :param transaction_id: The UUID value that denotes the domain of the website. This also populates the routing path.
    :param db: The database object. Depends on the currently active db session.
    :return: Corresponding accommodation record from the db.
    """
    transax = crud.get_transaction_by_id(transaction_id, db)
    if transax:
        return transax 
    else:
        raise HTTPException(404, detail=f"Transaction with id: <{transaction_id}> not found.")

