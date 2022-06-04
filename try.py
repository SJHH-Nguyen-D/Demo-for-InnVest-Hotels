import random
from datetime import datetime, timedelta


hrs = [i for i in range(24)]
chkothrs = [i for i in range(12)]
minssecs = [i for i in range(60)]
los = [i for i in range(1, 15)]  # length of hotel stayin days
mop = ("credit", "debit", "cash")


def pick(arr):
    return random.choice(arr)


def get_checkoutdate(
    start: datetime,
    allowable_los: list = [],
    allowable_hours: list = [],
    pickable_mins_secs: list = [],
) -> datetime:
    """
    Randomly pick checkout date based on checkindate.

    :param start (datetime):
    :param allowable_hours (list): list of allowable hours before 11am to checkout (all in UTC)
    :param pickable_mins_secs (list): list of pickable minutes and seconds
    :return checkoutdate (datetime): the checkout date formatted
    """
    assert allowable_hours, "cannot be none or empty"
    assert pickable_mins_secs, "cannot be none or empty"

    checkout_datetime = datetime.strptime(
        (start + timedelta(days=pick(allowable_los))).strftime(f"%Y-%m-%d {pick(allowable_hours)}:{pick(pickable_mins_secs)}:{pick(pickable_mins_secs)}"),
        f"%Y-%m-%d %H:%M:%S"
    )
    return checkout_datetime


start = datetime(2018, 1, 1, pick(hrs), pick(minssecs), pick(minssecs))
end = get_checkoutdate(
    start, 
    allowable_los=los, 
    allowable_hours=hrs, 
    pickable_mins_secs=minssecs
)

print(start)
print(end)
