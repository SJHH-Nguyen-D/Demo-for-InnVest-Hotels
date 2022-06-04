import os
from typing import List, Union

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....api.v1.payload_examples.examples import (
    annotate_recommendations_payload_example,
    example_topic_modelling,
)
from ....core.config import settings
from ....models import auth, crud, schemas
from ....models.database import get_db
from ...v1.recommendation.predict import predict
from ...v1.recommendation.recommender import Recommender
from ...v1.recommendation.train import train
from ...v1.topic_modelling.topic_model import generate_BERT_topics
from ..logger.exception_logger import logger

router = APIRouter()
rec_eng = Recommender()

S3_BUCKET = settings.RECOMMENDATION_DATASET_BUCKET

CREDS = {
    "key": os.getenv("AWS_ACCESS_KEY_ID"),
    "secret": os.getenv("AWS_SECRET_ACCESS_KEY"),
}


@router.post(
    "/annotate-recommendations/",
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.UserRatings],
)
def annotate_recommendations(
    updates=Body(..., example=annotate_recommendations_payload_example),
    db: Session = Depends(get_db),
):
    """
    Route annotates user resource recommendations as well as trains the recommender

    Expected payload structure:

    {   "data": {
            "chat_query": "I want to know if I can xyz",
            "items": [
                {
                    "id": 1234, # this is the resource/page id
                    "labels": ["label1", "label2"],
                    "rating": 0.0,
                    "url": "https://www.resource.com/resource.pdf",
                    "type": None, # inferred after
                },
            ],
            "ml_stage": "training"
        }
    }

    """
    data = updates.get("data", None)

    if not data:
        return HTTPException(status_code=400, detail="No data submitted.")
    else:
        try:
            ratings = crud.update_user_ratings(data, db)
            return ratings
        except Exception as e:
            logger.error(e)
            print(e)
            return HTTPException(
                status_code=400, detail="Unable to update user ratings"
            )


@router.get(
    "/random/",
    status_code=status.HTTP_200_OK,
    response_model=Union[List[schemas.RandomRecommendationOut], schemas.ErrorMessage],
)
def random_recommendations(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(crud.get_current_active_user),
    token: str = Depends(auth.oauth2_scheme),
):
    # TODO:
    n_recs = 5

    if not n_recs:
        return HTTPException(status_code=404, detail="No data submitted.")
    else:
        try:
            recs = crud.get_random_recs(n_recs, current_user, db)
            return recs
        except Exception as e:
            logger.error(e)
            return {"status_code": 500, "detail": e}


@router.post("/warm/", status_code=status.HTTP_201_CREATED)
def warm_recommendations(
    data=Body(..., example={"n_recs": 5}),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(crud.get_current_active_user),
    token: str = Depends(auth.oauth2_scheme),
):
    """
    Get initial recommendations using topic modelling with word2vec model
    """
    # TODO:
    n_recs = data.get("n_recs", 5)

    if not n_recs:
        return HTTPException(status_code=404, detail="No data submitted.")
    else:
        try:
            ratings = crud.get_warm_recs(n_recs, current_user, db)
        except Exception as e:
            logger.error(e)

    return ratings


@router.put("/train-recommender/", status_code=status.HTTP_200_OK)
def train_recommendations(
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    """
    Trains the recommendation engine with the current data in the dataset.
    """

    try:
        train(db)
        return {"status": 200, "message": "Successfully trained recommender"}
    except Exception as e:
        logger.error(e)
        return HTTPException(400, detail=f"Failed to train recommender with error: {e}")


@router.post(
    "/recommendations/",
    status_code=status.HTTP_201_CREATED,
    response_model=Union[List[schemas.RecommendationOut], schemas.ErrorMessage],
)
def rec_recommendations(
    payload=Body(
        ..., example={"query": "I want to know more about how to start a business."}
    ),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(crud.get_current_active_user),
    token: str = Depends(auth.oauth2_scheme),
):
    """
    recommendations using the trained recommendation engine.
    """
    chat = payload.get("query", None)

    if chat:
        try:
            preds = predict(chat)
            return preds

        except Exception as e:
            logger.error(e)
            return {"status_code": 500, "detail": e}
    else:
        return HTTPException(
            status_code=400, detail="Key Error: missing key 'chat_query' in payload."
        )
