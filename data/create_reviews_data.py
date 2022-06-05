import pandas as pd
import os
from uuid import uuid4
import random
from typing import Union, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from timeit import default_timer
from faker import Faker


fake = Faker()
Faker.seed(57)


def get_fk_table(hotel_csv_data_path: "str") -> pd.DataFrame:
    """
    :param hotel_csv_data_path (str): path-like string to local hotel csv data
    :returns hotel_fk_dataframe (pd.DataFrame): a dataframe with only the required UUIDs for hotels.
    """
    try:
        return pd.read_csv(hotel_csv_data_path).rename({"id": "hotel_id"}, axis=1)[
            "hotel_id"
        ]
    except Exception as e:
        print(e)
        return


def write_dataframe(dataframe: pd.DataFrame, out_path="") -> None:
    if not os.path.exists(out_path):
        dataframe.to_csv(out_path, index=False)
        print(f"Wrote data to: {out_path}")


class ReviewDataGenerator:
    def __init__(
        self,
        fks: pd.DataFrame = None,
    ):
        """
        Class to generate customer review data for each hotel.
        Starts from Jan 1, 2017 to Dec 31, 2022.
        """
        self.fks = pd.DataFrame(fks)
        self.data = []

    @staticmethod
    def pick(arr):
        return random.choice(arr)

    @staticmethod
    def get_title():
        return fake.sentence(nb_words=10, variable_nb_words=True)

    @staticmethod
    def get_reviewdate():
        return fake.date_between(
            start_date=datetime(2017, 1, 1), end_date=datetime(2022, 12, 31)
        )

    @staticmethod
    def get_travelcompanions():
        return np.random.choice(
            [
                "Family",
                "Friends",
                "Partner",
                "Significant Other",
                "Other",
                "None",
                "n/a",
            ]
        )

    @staticmethod
    def get_rating():
        return np.random.choice(
            [i for i in range(1, 6)], p=[0.1, 0.05, 0.05, 0.2, 0.6]
        )

    @staticmethod
    def get_typeoftrip():
        return np.random.choice(["Business", "Leisure", "Vacation", "Other"])

    @staticmethod
    def get_feedback():
        return fake.sentence()

    @staticmethod
    def get_appropriateness():
        return np.random.choice([True, False], p=[0.95, 0.05], replace=False)

    def generate_reviews_dataset(self):
        """
        :returns dataset (pd.DataFrame): Generates a DataFrame of Reviews
        """
        start_time = default_timer()

        for idx, row in self.fks.iterrows():
            for _ in range(1000):
                d = row.to_dict()
                d["id"] = str(uuid4())
                d["reviewdate"] = self.get_reviewdate()
                d["reviewedby"] = f"{fake.first_name()} {fake.last_name()}"
                d["travelledfrom"] = fake.country()
                d["travelcompanions"] = self.get_travelcompanions()
                d["typeoftrip"] = self.get_typeoftrip()
                d["title"] = self.get_title()
                d["feedback"] = self.get_feedback()
                d["roomcomfort"] = self.get_rating()
                d["roomcleanliness"] = self.get_rating()
                d["staffservice"] = self.get_rating()
                d["facilities"] = self.get_rating()
                d["value"] = self.get_rating()
                d["appropriate"] = self.get_appropriateness()
                self.data.append(d)
                inter = default_timer()
                print(f"{(inter-start_time):.3f}s has elapsed.")

        stop_time = default_timer()
        print(f"Elapsed time for creating reviews: {(start_time-stop_time):.3f}s")
        print(f"{len(self.data)} reviews created.")
        return pd.DataFrame(self.data)


if __name__ == "__main__":
    fks = get_fk_table("innvest_portfolio_hotels_data.csv")
    r = ReviewDataGenerator(fks=fks)
    rv_df = r.generate_reviews_dataset()
    write_dataframe(rv_df, out_path="innvest_hotels_portfolio_reviews.csv")
