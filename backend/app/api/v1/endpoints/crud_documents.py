import shutil
import uuid
from tempfile import NamedTemporaryFile
from typing import List

import boto3
from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from ....core import config
from ....init_dummy import create_dummy
from ....models import auth, crud, models, schemas
from ....models.database import get_db
from ....models.utils import parse_document_metadata
from ..logger.exception_decor import exception
from ..logger.exception_logger import logger

router = APIRouter()

resources_summary_switch = config.settings.RESOURCE_SUMMARY_SWITCH

s3 = boto3.resource("s3")
pdf_bucket = s3.Bucket(config.settings.PDF_BUCKET)


@router.get(
    "/site/{site_id}",
    status_code=status.HTTP_200_OK,
    tags=["read"],
    response_model=schemas.Sites,
)
def view_uploaded_site(
    site_id: str,
    current_user: schemas.User = Depends(crud.get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    :param current_user: Current API user.
    :param site_id: The UUID value that denotes the domain of the website. This also populates the routing path.
    :param db: The database object. Depends on the currently active db session.
    :return: Corresponding site record from the db.
    """
    site = crud.get_site_by_id(site_id, db, current_user)
    if site:
        return site
    else:
        raise HTTPException(404, detail=f"Site with id: <{site_id}> not found.")


@router.get(
    "/doc/{document_id}",
    status_code=status.HTTP_200_OK,
    tags=["read"],
    response_model=schemas.DocumentFile,
)
def view_uploaded_doc(
    document_id: str,
    current_user: schemas.User = Depends(crud.get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    :param current_user: Current API user
    :param document_id: document id to be viewed.
    :param db: The database object. Depends on the currently active db session.
    :return: Corresponding site record from the db.
    """
    doc = (
        db.query(models.DocumentFile)
        .filter(models.DocumentFile.id == uuid.UUID(document_id).bytes)
        .first()
    )
    # if doc:
    #     return doc.__dict__
    doc = crud.get_doc_by_id(document_id, db, current_user)
    if doc:
        return doc
    else:
        raise HTTPException(404, detail=f"Document with id: <{document_id}> not found.")


@router.post(
    "/doc/{document_id}/summarize/", status_code=status.HTTP_201_CREATED, tags=["read"]
)
def choose_to_summarize_documents(document_id: str):
    return summarize_document(document_id)


@router.put(
    "/doc/{document_id}/summarize/",
    status_code=status.HTTP_201_CREATED,
    tags=["read"],
    response_model=schemas.Resources,
)
def summarize_document(
    document_id: str,
    current_user: schemas.User = Depends(crud.get_current_active_user),
    db: Session = Depends(get_db),
):
    return crud.update_resource_summary(document_id, current_user, db)


@router.post(
    "/upload/",
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.DocumentFile],
)
def create_and_upload_user_doc(
    files: List[UploadFile] = File(...),
    current_user: schemas.User = Depends(crud.get_current_active_user),
    db: Session = Depends(get_db),
):

    # TODO: find method to include both files json body with summarization switch
    # TODO: because using both files and body is funky rn
    return upload_files(files, current_user, db)


@exception(logger)
def upload_files(files, user, db):
    """
    The master upload function, which does the uploading tasks.
    # :param summ_flag: The boolean flags to choose summarization of all or certain documents.
    :param files: The list of files to be uploaded to storage.
    :param user: The user logged into the session.
    :param db: The database or session object.
    :return: A list of DocumentFile model objects.
    """
    global pdf_bucket, resources_summary_switch
    try:
        create_dummy(db)
    except Exception as e:
        raise Exception(
            f"The dummy table rows could not be inserted, this will produce problems with pdf uploads: {e}"
        )
    docs = []
    for file in files:
        filename = file.filename
        with NamedTemporaryFile() as temp_file:
            shutil.copyfileobj(file.file, temp_file)
            if config.settings.S3_SWITCH:
                key = f"{user.organization_id}/{filename}"
                pdf_bucket.put_object(Key=key)
            else:
                key = ""
            # parse metadata to write to tables
            # TODO: celery task
            data = parse_document_metadata(temp_file.name)
            data["filepath"] = key
            data["filename"] = filename
            data["title"] = filename.split(".")[0]
            data["extension"] = filename.split(".")[-1]
            crud.upload_doc_to_db(
                db,
                site_id=uuid.UUID(int=0),
                doc_path=temp_file.name,
                title=data["title"],
                extension=data["extension"],
                key=key,
                resource_summ_switch=resources_summary_switch,
            )

        doc = crud.create_user_document(data=data, db=db, user=user)
        docs.append(doc)

    return docs


@router.post(
    "/upload-emails/",
    status_code=status.HTTP_201_CREATED,
    response_model=List[schemas.DocumentFile],
)
async def upload_from_email(
    email: str,
    x_authorization: str = Header(None),
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
    settings: config.Settings = Depends(config.get_settings),
):
    if x_authorization:
        token = x_authorization
    else:
        token = auth.get_token_from_request(x_authorization)

    authorized = await auth.validate_token_has_scope(token, "zenith-email-aws-ses")
    if not authorized:
        raise HTTPException(403, detail="Invalid access token")

    user = crud.get_user(db, email)
    if not user:
        raise HTTPException(404, detail=f"User with email {email} not found")

    return upload_files(user, db, files, settings)
