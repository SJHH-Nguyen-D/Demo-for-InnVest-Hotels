from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ....core import config
from ....models import auth, crud, schemas
from ....models.database import get_db

router = APIRouter()

resources_summary_switch = config.settings.RESOURCE_SUMMARY_SWITCH


@router.get(
    "/get-id/",
    status_code=status.HTTP_200_OK,
    tags=["read"],
    response_model=schemas.UserId,
)
def get_user_id(
    token=Depends(auth.oauth2_scheme),
    db: Session = Depends(get_db),
    settings: config.Settings = Depends(config.get_settings),
):
    user = crud.get_current_user(token, db, settings)
    if user:
        return {"id": user.id}
    else:
        raise HTTPException(404, detail="User not found.")
