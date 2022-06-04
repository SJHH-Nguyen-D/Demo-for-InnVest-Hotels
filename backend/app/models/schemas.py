import datetime
import pathlib
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, Json


class ErrorMessage(BaseModel):
    status_code: int
    detail: str


# ==================================================
#                 REVIEWS 
# ==================================================

class Reviews(BaseModel):
    id: UUID
    hotel_id: Union[UUID, str]
    reviewdate: Optional[datetime.datetime] = None
    reviewedby: Optional[str] = None
    travelledfrom: Optional[str] = None
    travelcompanions: Optional[str] = None
    typeoftrip: Optional[str] = None
    title: str
    feedback: Optional[str] = None
    roomcomfort: int
    roomcleanliness: int
    staffservice: int
    facilities: int
    value: int
    wifi: int
    appropriate: bool

    class Config:
        orm_mode = True


# ==================================================
#                 TRANSACTIONS 
# ==================================================

class Transactions(BaseModel):
    id: UUID
    hotel_id: Optional[Union[UUID, str]] = None
    accommodation_id: Optional[Union[UUID, str]] = None
    checkindate: Optional[datetime.datetime] = None
    checkoutdate: Optional[datetime.datetime] = None
    methodofpayment: str
    saleamount: float

    class Config:
        orm_mode = True


# ==================================================
#                 ACCOMMODATIONS 
# ==================================================

class Accommodations(BaseModel):
    id: UUID
    hotel_id: Union[UUID, str]
    accommodationtype: str
    description: Optional[str] = None
    squarefootage: int
    maxoccupancy: int
    numbeds: int
    bedsize: str
    roomnumber: int
    roomfloor: int
    amenities: str
    occupied: bool
    rate: float
    transactions: Optional[List[Transactions]]= []

    class Config:
        orm_mode = True


# ==================================================
#                 HOTELS 
# ==================================================

class Hotels(BaseModel):
    id: UUID
    hotelbrandname: str
    hotelfullyqualifiedname: str
    hotelcountry: str
    hotelprovince: str
    hotelcity: str
    hotelstreetnumber: int
    hotelstreename: str
    hotelpostalcode: str
    website: str
    phonenum: int
    description: str,
    servicelevel: str
    maxoccupancy: int
    operationalrooms: int
    bar_lounge: bool = False
    breakfast_included: bool = False
    business_center: bool = False
    cold_weather_hook_up: bool = False
    dry_claning_service: bool = False
    electric_vehicle_charging: bool = False
    executive_lounge: bool = False
    kids_club: bool = False
    laundry_stuff: bool = False
    meeting_event_space: bool = False
    outdoor_patio: bool = False
    parking_self: bool = False
    parking_valet: bool = False
    pets_allowed: bool = False
    pool: bool = False
    restaurant: bool = False
    room_service: bool = False
    spa: bool = False
    swimming_pool_indoor: bool = False
    swimming_pool_outdoor: bool = False
    wheelchair_accessible: bool = False
    kitchen: bool = False
    microwave_and_refridgerator: bool = False
    outdoor_recreation: bool = False

    accommodations: Optional[List[Accommodations]]= []
    reviews: Optional[List[Reviews]] = []

    class Config:
        orm_mode = True
