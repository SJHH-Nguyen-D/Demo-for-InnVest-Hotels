import pandas as pd
from uuid import uuid4
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeMeta, declarative_base, sessionmaker

DATABASE_URL = "mysql+pymysql://dennis:foobar@mysql/innvesthotels"

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


df = pd.read_csv("innvest_portfolio_hotels_data.csv")


# create accommodations
for idx, row in df:
    # _id = uuid4()
    hotel_id = i
    accommodationtype = random.choice(["suite", "room"])
    description = "lorem ipsum"
    squarefootage = random.randint(350, 700)
    maxoccupancy = random.randint(2, 9)
    numbeds = maxoccupancy // 2
    bedsize = random.choice(["twin", "double", "queen", "king"])
    