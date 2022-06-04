import pandas as pd
import os
from uuid import uuid4
import random
from typing import Union, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from timeit import default_timer


def get_fk_table(hotel_df: pd.DataFrame = None, acc_df: pd.DataFrame = None):
    """
    :param hotel_df (pd.DataFrame): dataframe containing hotel_ids
    :param acc_df (pd.DataFrame): dataframe containing accommodation_ids
    :returns merged (pd.DataFrame): a dataframe with only the required brand column and foreign keys
    """
    hotel_df.merge(acc_df, how="inner", on="hotel_id")
    merged = hotel_df.merge(acc_df, how="inner", left_on="id", right_on="hotel_id")[
        ["id_x", "id_y", "hotelbrandname"]
    ].rename({"id_x": "hotel_id", "id_y": "accommodation_id"}, axis=1)
    return merged


def write_dataframe(dataframe:pd.DataFrame, out_path=""):
    if not os.path.exists(out_path):
        dataframe.to_csv(out_path, index=False)
        print(f"Wrote data to: {out_path}")


class TransactionDataGenerator:
    def __init__(
        self, 
        fks: pd.DataFrame = None,
    ):
        """
        Class to generate transaction data for each accommodation
        for each hotel. Starts from Jan 1, 2017 to Dec 31, 2022.
        """
        self.fks = fks
        self.data = []
        self.hrs = [i for i in range(24)]
        self.chkothrs = [i for i in range(12)]
        self.minssecs = [i for i in range(60)]
        self.los = [i for i in range(1, 15)]  # length of hotel stayin days
        self.mop = ("credit", "debit", "cash")
        self.random_days_between_los = [i for i in range(1)]
        self.last_checkindate = datetime(2022, 12, 31)
        self.vfcd = datetime(
            2017, 1, 1, 
            self.pick(self.hrs), 
            self.pick(self.minssecs), 
            self.pick(self.minssecs)
        )

    def pick(arr):
        return random.choice(arr)

    def get_checkindate(self, current_acc_id: str):
        """
        :param current_acc_id (str): accommodation uuid
        :param vfcd (datetime): very first checkin date
        :param tx_dict_list (list): list of dicts of data points created for our final dataframe
        :returns checkindate (datetime): pick the next checkin date
        """
        # if list empty
        # or if last accommodation unit has finished
        if (len(self.data) < 1) or (self.data[-1]["accommodation_id"] != current_acc_id):
            return self.vfcd
        else:
            checkindate = self.data[-1]["checkoutdate"] + timedelta(days=self.pick(self.random_days_between_los))
            return checkindate

    def get_checkoutdate(
        self,
        start: datetime
    ) -> datetime:
        """
        Randomly pick checkout date based on checkindate.

        :param start (datetime):
        :return checkoutdate (datetime): the checkout date formatted
        """

        checkout_datetime = datetime.strptime(
            (start + timedelta(days=self.pick(self.los))).strftime(f"%Y-%m-%d {self.pick(self.hrs)}:{self.pick(self.minssecs)}:{self.pick(self.minssecs)}"),
            f"%Y-%m-%d %H:%M:%S"
        )
        return checkout_datetime

    def generate_saleamount(acc_id: str, data: pd.DataFrame = None):
        """
        Generate the saleamount of a transaction based on the brand of hotel
        The accommodation ID belongs to.
        """
        hotname = data.loc[data["hotel_id"] == acc_id, "hotelbrandname"].unique()[0]
        if hotname in ("Comfort Inn", "Holiday Inn", "Holiday Inn Express"):
            base = round(np.random.uniform(165, 400), 2)
            return base + (round(base * np.random.uniform(0.0, 0.15), 2))
        else:
            base = round(np.random.uniform(250, 650), 2)
            return base + (round(base * np.random.uniform(0.0, 0.15), 2))

    def generate_transaction_dataset(self) -> pd.DataFrame:
        """
        :returns dataset (pd.DataFrame): Generates a DataFrame of Transactions
        """

        start_time = default_timer()

        for idx, row in self.fks.iterrows():
            most_recent_chrono_startdate = self.vfcd
            while most_recent_chrono_startdate < self.last_checkindate:
                d = row.to_dict()
                checkindate = self.get_checkindate(
                    d["accommodation_id"], 
                    self.vfcd, 
                    self.data
                )
                d["checkindate"] = checkindate
                d["checkoutdate"] = self.get_checkoutdate(checkindate)
                d["methodofpayment"] = self.pick(self.mop)
                d["saleamount"] = self.generate_saleamount(d["hotel_id"], data=fks)
                most_recent_chrono_startdate = d["checkoutdate"]
                self.data.append(d)
        stop_time = default_timer()
        print(f"Elapsed time for creating transactions: {(start_time-stop_time):.3f}s")
        print(f"{len(self.data)} transactions created.")
        return pd.DataFrame(self.data)


if __name__ == "__main__":
    acc_data = pd.read_csv("innvest_hotels_portfolio_accommodations.csv")
    hot_data = pd.read_csv("innvest_portfolio_hotels_data.csv")
    fks = get_fk_table(hotel_df=hot_data, acc_df=acc_data)
    t = TransactionDataGenerator(fks=fks)
    tx_df = t.generate_transaction_dataset()
    write_dataframe(tx_df, out_path="innvest_hotels_portfolio_transactions.csv")
