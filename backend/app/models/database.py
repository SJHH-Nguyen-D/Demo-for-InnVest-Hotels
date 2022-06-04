from app.core.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

settings = get_settings()

DATABASE_URL = settings.DB_URL if settings.DB_URL else "mysql+pymysql://dennis:foobar@mysql/innvesthotels"

engine = create_engine(
    DATABASE_URL,
    echo=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base: DeclarativeMeta = declarative_base()

# dependency to be injected
def get_db():
    db = SessionLocal()
    try:
        # use only one yield statement and always use yield instead of return, as per fastAPI hints
        yield db
    finally:
        db.close()
