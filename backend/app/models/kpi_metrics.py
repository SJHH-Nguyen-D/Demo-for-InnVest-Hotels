from datetime import timedelta, datetime
import pandas as pd
from uuid import UUID
from typing import Union


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


def get_trr_pandas(df: pd.DataFrame, hotel: Union[UUID, str], start, stop):
    """
    Calculates total room revenue for a hotel during a particular period of time.
    """
    assert "price" in df.columns
    trr = df.\
            loc[
                (df.hotel == hotel) & 
                (df.datetime >= start & df.datetime <= stop), "price"
            ].sum()
    return trr


def get_trr_sql(hotel_id, engine=None, session=None):
    stmt = f"""
        SELECT SUM(price) as TRR
        FROM hotels h
        INNER JOIN transactions t
        ON h.id = t.hotel_id;
        WHERE h.id = {hotel_id}
    """
    if engine:
        with engine.begin() as conn:
            return conn.execute(stmt).fetchall()
    elif session:
        with session.connect() as conn:
            return session.execute(stmt).fetchall()


def revenue_per_available_room(trr: float = None, tra: int = None, tro: int = None):
    """
    RevPAR (revenue per available room) measures revenue generated over time,
    just through room bookings in a hotel.

    revpar = total_room_revenue / total rooms available    
    or
    revpar = ADR * occupancy %

    :trr (float): total room revenue in dollars, for a hotel in a period of time
    :tra (int): total rooms available for clients
    :returns RevPar (float): returns revenue per average available room

    """
    if trr and tra:
        return round(trr/tra, 2)
    elif tro and tra:
        return round(average_daily_rate(trr, tro) * (tro/tra), 2)
    else:
        raise("Unable to calculate RevPar")


def average_occupancy_rate(hotel_id, tra: int, tro: int, start: datetime, stop: datetime):
    """
    Average Occurancy Rate (OCC) per period of time (i.e., day, week, month, year)

    AOCC = tro/tra per period of time
    """

    inter = df.loc[
        (df["id"] == hotel_id) &
        (df["datetime"]>= start & df["datetime"] <= stop)
    ]

    inter.operationalrooms.apply(lambda x: x/)

    return None


def average_occupancy_rate_sql(hotel_id, tra: int, tro: int, start: datetime, stop: datetime, engine: None, db=None):
    """
    Average Occurancy Rate (OCC) per period of time (i.e., day, week, month, year)

    AOCC = tro/tra per period of time
    """

    stmt = f""""
        SELECT (SUM(a.occupied) / (
            SELECT operationalrooms
            FROM hotels
            WHERE id = {hotel_id}
        )) as OCC
        FROM hotels AS h
            INNER JOIN accommodations AS a
            ON h.id = a.hotel_id
            INNER JOIN transactions as t
            ON a.hotel_id = t.hotel_id
        WHERE h.id = {hotel_id}
            AND t.checkindate between {start} and {stop}
    """
    res = None
    if db:
        res = db.execute(stmt).fetchall()
        return res
    elif engine:
        with engine.begin() as conn:
            res = conn.execute(stmt).fetchall()
            return res
    else:
        raise


def average_length_of_stay_sql(hotel_id, engine, start: Union[str, datetime], stop: Union[str, datetime]):
    """
    The average length of stay of your guests measures the 
    profitability of your business. By dividing your total of 
    occupied room nights by the number of bookings, this metric 
    can give you a realistic estimate of your earnings.

    A longer LOS is considered better compared to a shorter 
    length, which means reduced profitability due to increased labour 
    costs arising from room turnovers between guests.

    average_LOS = (total occupied room nights/num bookings) per period
    """
    # TOOD: join hotel, transactions on hotel_id
    # TODO: filter by period and hotel id
    # TODO: for each transaction, find the difference between signin and checkout in days
    # TODO: count(*) as numBookings from transactions

    stmt = f"""

        WITH length_of_stay (cols, cols2) AS (
            SELECT x, d, COUNT(id) as num_bookings
            FROM transactions
            WHERE hotel_id = {hotel_id}
            AND checkindate between CONVERT({start})
            AND checkindate between CONVERT({stop})
        )

        WITH num_bookings (num_bookings) AS (
            SELECT SUM() as num_bookings
            FROM 
            WHERE 
        )
    
    """
    with engine.begin() as conn:
        res = conn.execute(stmt).fetchall()
    return res


def market_penetration_index(hotel_occupancy_rate: float, competitor_rate: float) -> float:
    """
    Market Penetration Index (MPI) as a metric compares your 
    hotel's occupancy rate to that of your competitors in 
    the market and provides an encompassing view of your 
    property's position therein.

    Dividing your hotel's occupancy rate by those offered 
    by your top competitors and multiplying by 100 would 
    give you your hotel's MPI. This metric gives you an 
    overview of your standing in the market and lets you 
    tweak your marketing efforts to entice prospects to 
    book with your property, instead of your rivals.

    MPI = (hotel_occupancy_rate / competitor_rate) * 100
    or
    MPI = ((Total rooms occupied/ total rooms available) / competitor_rate) * 100
    """
    return (hotel_occupancy_rate/competitor_rate) * 100


def gross_operating_profit_per_available_room(gop: float, tar: int):
    """
    Gross Operating Profit Per Avaiable Room (GOP PAR)

    GOP PAR can accurately indicate your hotel's success. It measures 
    performance across all revenue streams, not just rooms. 
    It identifies those parts of the hotel which are bringing in the 
    most revenue and also throws light on the operational costs incurred 
    in order to do so.

    Dividing Gross Operating Profit by rooms available can give you your 
    GOP PAR figure.

    :param gop (float): Gross operating profit in dollars of a hotel for a period of time
    :param tar (int): total number of available rooms for a hotel
    :returns gop_par(float): Gross Operating Profit per Available Room
    """
    gop_par = gop / tar
    return gop_par


def cost_per_occupied_room(hotel_id: Union[str, UUID], gop: float, tra: int):
    """
    Cost Per Occupied Room (CPOR)

    The Cost Per Occupied Room metric allows you to 
    determine the efficiency of your property, per room sold. 
    It helps in weighing your profitability, by taking into 
    consideration your property's both fixed and variable expenses.

    The figure derived by dividing the gross operating profit 
    by total rooms available is what CPOR is. You can get the 
    Gross Operating Profit by deducting the net sales from the 
    cost of goods sold and by further subtracting it from the 
    operating expenses which include administrative, selling or 
    general costs.

    CPOR = (gop / tra)

    GOP = NetSales - CostOfGoods - OperatingExpenses

    :param hotel_id (Union[str, UUID]): hotel identifier
    :param gop (float): gross operating profit in dollars for a period
    :param tra (int): total numberof rooms available
    :returns cpor: Cost Per Occupied Room in Dollars
    """
    # TODO: Filter by hotel_id
    return round(gop / tra, 2)


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