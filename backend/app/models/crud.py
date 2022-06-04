import json
import logging
import uuid
from datetime import datetime
from typing import List, Optional, Union

import boto3
import jsonlines
import jwt
import pandas as pd
from botocore.exceptions import ClientError
from fastapi import Depends, HTTPException
from jwt import PyJWTError
from sqlalchemy import and_, func, null, or_, select
from sqlalchemy.orm import Session

from ..api.v1.constants import FILE_EXTS
from ..api.v1.logger.exception_logger import logger
from ..core import config
from . import database, models, schemas
from .database import SessionLocal, get_db


# ==================================================
#                        HOTELS
# ==================================================

def get_hotel_by_id(hotel_id: str, db: Session) -> schemas.Hotels:
    hotel = (
        db.query(models.Hotels)
        .filter(models.Hotels.id == hotel_id)
        .first()
    )
    return hotel


# ==================================================
#                        ACCOMMODATIONS
# ==================================================


def get_accommodation_by_id(accommodation_id: str, db: Session) -> schemas.Accommodations:
    acc = (
        db.query(models.Accommodations)
        .filter(models.Accommodations.id == accommodation_id)
        .first()
    )
    return acc


# ==================================================
#                        TRANSACTIONS
# ==================================================


def get_transaction_by_id(transaction_id: str, db: Session) -> schemas.Transactions:
    trans = (
        db.query(models.Transactions)
        .filter(models.Transactions.id == transaction_id)
        .first()
    )
    return trans


# ==================================================
#                        REVIEWS
# ==================================================


def get_review_by_id(review_id: str, db: Session) -> schemas.Reviews:
    review = (
        db.query(models.Reviews)
        .filter(models.Reviews.id == review_id)
        .first()
    )
    return review 


def sql_commit(model, df: pd.DataFrame, db: Session):
    """
    This function commits data to the database.
    :param model: The database model needed for committing the data.
    :param df: The data to commit, must be a pandas dataframe.
    :param db: The session object for facilitating the commits.
    :return: None
    """
    for i in df.to_dict(orient="records"):
        c = model(**i)
        db.add(c)
        db.commit()
        db.refresh(c)
