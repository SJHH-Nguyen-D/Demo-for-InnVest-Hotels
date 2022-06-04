import asyncio

import uvicorn

from .fastapi_app import app
from .api.v1.logger.exception_logger import logger
from .models.database import Base, engine


@app.on_event("startup")
async def startup_event():
    logger.info("Startup")
    while True:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Created tables")
            break
        except Exception as e:
            logger.exception(f"Failed to create tables. Retrying in 3s: {e}")
            await asyncio.sleep(3)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
