import pandas as pd
from uuid import uuid4
import random
from sqlalchemy import create_engine
from datetime import datetime

df = pd.read_csv("innvest_portfolio_hotels_data.csv")
hotels = pd.read_csv("innvest_portfolio_hotels_data.csv")

def determine_room_floor(df, id):
    if df.loc[df["id"] == id, "hotelbrandname"].tolist()[0] == "Comfort Inn":
        return random.choice([i for i in range(1, 3+1)])
    else:
        return random.choice([i for i in range(1, 50)])


def determine_saleamount(df, id):
    if df.loc[df["id"] == id, "hotelbrandname"].tolist()[0] == "Comfort Inn":
        return round(random.uniform(125, 350), 2)
    else:
        return round(random.uniform(250, 600), 2)

# create accommodations
rooms = []
for idx, row in df.iterrows():
    # number of operational rooms
    for i in range(row[-2]):
        maxoccupancy = random.randint(2, 9)
        d = {
                "id" : uuid4(),
                "hotel_id" : row[-1],
                "accommodationtype" : random.choice(["suite", "room"]),
                "description" : "lorem ipsum",
                "squarefootage" : random.randint(350, 700),
                "maxoccupancy" : maxoccupancy,
                "numbeds" : maxoccupancy // 2,
                "bedsize" : random.choice(["twin", "double", "queen", "king"]),
                "roomnumber": random.choice([i for i in range(10)]),
                "roomfloor": determine_room_floor(df, row[-1]),
                "amenities": "",
                "occupied": random.choice([True, False]),
                "saleamount": determine_saleamount(df, row[-1])
        }
        rooms.append(d)

acc_df = pd.DataFrame(rooms)
acc_df.to_csv("innvest_hotels_portfolio_accommodations.csv", index=False)
