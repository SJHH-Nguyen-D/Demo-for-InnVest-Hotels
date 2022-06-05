from datetime import timedelta, datetime
import pandas as pd

# load data
df = pd.read_csv("../data/innvest_portfolio_hotels_data.csv")

def total_available_rooms(nra: int, dip: int) -> int:
    """
    Total Available Rooms (TAR)

    A measure of inventory.

    You can calculate the capacity in the system of hotels by 
    multiplying the number of rooms available with the number of 
    days in a particular period. 

    TAR = TNA x Days-in-Period

    For example, a 100 room hotel property which has only 
    90 rooms operating, would need to take 90 as the 
    base for applying a RevPAR formula.

    :param nra (int): number of available rooms
    :param dip (int): number of days within a period

    :returns: total available rooms (int)
    """
    return nra * dip

# total available rooms in 
total_available_rooms_sql = """
        CREATE OR REPLACE VIEW AS TOTALAVAILABLEROOMS AS

    """

def average_daily_rate(trr: float, tro: int) -> float:
    """
    Calculates ADR for a hotel

    Identify performance over time by drawing a comparison 
    between the current and previous periods or seasons. 
    Keeping an eye on your competitors and juxtaposing their performance against 
    yourself as an ADR hotel can also be done with the help of this metric.

    Dividing the total room revenue by total rooms occupied can give 
    you a figure for your hotel's ADR, though the ADR formula does 
    not account for unsold or empty rooms. This means that it 
    may not provide a holistic picture of your property's performance, 
    but as an ongoing performance metric, it works well in isolation.

    :param trr (float): total room revenue
    :param tro (int): total rooms occupied

    :returns: average daily rate (float)
    """
    return round(trr / tro, 2)


def get_number_of_days_in_period(p_start: datetime, p_end: datetime) -> int:
    """
    Used in calculating Total Available Rooms

    :param p_start (datetime): the start of the period
    :param p_end (datetime): the end of the period

    :returns: the total number of days between the start and stop of a period, stop inclusive.
    """
    if (isinstance(p_start, datetime)) and (isinstance(p_end, datetime)):
        try:
            return abs((p_end-p_start).days)
        except Exception as e:
            raise(e)
    elif (isinstance(p_start, str)) and (isinstance(p_end, str)):
        try:
            date_format = "%d-%m-%Y"
            start = datetime.strptime(p_start, date_format)
            stop = datetime.strptime(p_end, date_format)
            return abs((stop-start).days)
        except Exception as e:
            raise(e)
    else:
        raise("p_start and p_end need to both be datetime formatted or string formatted")


def get_TAR_by_id(df: pd.DataFrame, id: int, p_start: datetime, p_end: datetime) -> :
    """
    Gets Total Available Rooms by Hotel ID
    """
    try:
        days = get_number_of_days_in_period(p_start, p_end)
    except Exception as e:
        raise(f"Unable to calculate num days in period with error: {e}")

    try:
        return total_available_rooms(df.at[df["id"]==id, "operationalrooms"], days)
    except Exception as e:
        raise(f"Unable to calculate total available rooms with error: {e}")


def sql_total_available_rooms(id: int, p_start, p_end):
    TAR_SQL = f"""
        SELECT (DATEDIFF(days,  {p_start}, {p_end}) * operationalrooms) as totalAvailableRooms
        FROM hotels
        WHERE id = {id}
    """
    return TAR_SQL


p_start = datetime(2020, 3, 17)
p_end = datetime(2024, 3, 17)

get_TAR_by_id(df, 2, p_start, p_end)