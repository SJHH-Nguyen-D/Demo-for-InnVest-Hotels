import uuid

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy import Text as sqlalchemyText
from sqlalchemy.dialects.mysql import BINARY
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Column
from sqlalchemy.sql.sqltypes import Float
from sqlalchemy.types import TypeDecorator, SmallInteger, Float

from .database import Base

UUID_LEN = 64
ID_LEN = 10
EXT_LEN = 4

SHORT_STR = 128
MED_STR = 512
LONG_STR = 2048


class BinaryUUID(TypeDecorator):
    """
    Optimize UUID keys. Store as 16 bit binary, retrieve as uuid.
    """

    impl = BINARY(16)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        try:
            return value.bytes
        except AttributeError:
            try:
                return uuid.UUID(value).bytes
            except TypeError:
                return value

    def process_result_value(self, value, dialect):
        return uuid.UUID(bytes=value)


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(BinaryUUID, primary_key=True, index=True, default=uuid.uuid4)
    hotelbrandname = Column(String(MED_STR), nullable=False)
    hotelfullyqualifiedname = Column(String(MED_STR), nullable=False)
    hotelcountry = Column(String(MED_STR), nullable=False)
    hotelprovince = Column(String(2), nullable=False)
    hotelcity = Column(String(MED_STR), nullable=False)
    hotelstreenumber = Column(Integer, nullable=False)
    hotelstreetname = Column(String(MED_STR), nullable=False)
    hotelpostalcode = Column(String(MED_STR), nullable=False)
    website = Column(String(MED_STR), nullable=True)
    phonenum = Column(Integer, nullable=False)
    description = Column(String(LONG_STR), nullable=True)
    servicelevel = Column(String(MED_STR), nullable=True)
    bar_lounge = Column(Boolean, nullable=False, default=False)
    breakfast_included = Column(Boolean, nullable=False, default=False)
    business_center = Column(Boolean, nullable=False, default=False)
    cold_weather_hook_up = Column(Boolean, nullable=False, default=False)
    dry_cleaning_service = Column(Boolean, nullable=False, default=False)
    electric_vehicle_charging = Column(Boolean, nullable=False, default=False)
    executive_lounge = Column(Boolean, nullable=False, default=False)
    gift_shop = Column(Boolean, nullable=False, default=False)
    kids_club = Column(Boolean, nullable=False, default=False)
    laundry_self = Column(Boolean, nullable=False, default=False)
    meeting_event_space = Column(Boolean, nullable=False, default=False)
    outdoor_patio = Column(Boolean, nullable=False, default=False)
    parking_self = Column(Boolean, nullable=False, default=False)
    parking_valet = Column(Boolean, nullable=False, default=False)
    pets_allowed = Column(Boolean, nullable=False, default=False)
    pool = Column(Boolean, nullable=False, default=False)
    restaurant = Column(Boolean, nullable=False, default=False)
    room_service = Column(Boolean, nullable=False, default=False)
    spa = Column(Boolean, nullable=False, default=False)
    swimming_pool_indoor = Column(Boolean, nullable=False, default=False)
    swimming_pool_outdoor = Column(Boolean, nullable=False, default=False)
    wheelchair_accessible = Column(Boolean, nullable=False, default=False)
    kitchen = Column(Boolean, nullable=False, default=False)
    microwave_and_refridgerator = Column(Boolean, nullable=False, default=False)
    outdoor_recreation = Column(Boolean, nullable=False, default=False)
    maxoccupancy = Column(Integer, nullable=False)
    operationalrooms = Column(Integer, nullable=False)

    accommodations = relationship("Accomodations", back_populates="hotel", cascade="all, delete")
    reviews = relationship("Reviews", back_populates="hotel", cascade="all, delete")
    transactions = relationship("Transactions", back_populates="hotel", cascade="all, delete")


class Accommodations(Base):
    __tablename__ = "accommodations"

    id = Column(BinaryUUID, primary_key=True, index=True, default=uuid.uuid4)
    hotel_id = Column(BinaryUUID, ForeignKey("hotels.id"))
    hotel_id = Column(BinaryUUID, ForeignKey("hotels.id"))
    accommodationtype = Column(String(5), nullable=False)
    description = Column(sqlalchemyText(2**32 - 1), nullable=True)
    squarefootage = Column(Integer, nullable=True)
    maxoccupancy = Column(SmallInteger, nullable=True)
    numbeds = Column(SmallInteger, nullable=True)
    bedsize = Column(String(SHORT_STR), nullable=True)
    roomnumber = Column(SmallInteger, nullable=True)
    roomfloor = Column(SmallInteger, nullable=True)
    amenities = Column(sqlalchemyText(2**32 - 1), nullable=True)
    occupied = Column(Boolean, nullable=False, default=False)
    rate = Column(Float, nullable=True)

    hotel = relationship("Hotels", back_populates="accommodations", passive_deletes=True)
    transactions = relationship("Accommodations", back_populates="accommodation", passive_deletes=True)


class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(BinaryUUID, primary_key=True, index=True, default=uuid.uuid4)
    hotel_id = Column(BinaryUUID, ForeignKey("hotels.id"))
    accommodation_id = Column(BinaryUUID, ForeignKey("accommodations.id"))
    checkindate = Column(DateTime, nullable=True)
    checkoutdate = Column(DateTime, nullable=True)
    methodofpayment = Column(String(SHORT_STR), nullable=True)
    saleamount = Column(Float(2), nullable=True)

    hotel = relationship(
        "Hotels", back_populates="transactions", cascade="all, delete"
    )
    accomodation = relationship(
        "Accommodations", back_populates="", cascade="all, delete"
    )


class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(BinaryUUID, primary_key=True, index=True, default=uuid.uuid4)
    hotel_id = Column(BinaryUUID, ForeignKey("hotels.id"))
    reviewdate = Column(DateTime, nullable=True)
    reviewedby = Column(String(MED_STR), nullable=True)
    travelledfrom = Column(String(MED_STR), nullable=True)
    travelcompanions = Column(String(MED_STR), nullable=True)
    typeoftrip = Column(String(MED_STR), nullable=True)
    title = Column(String(100), nullable=True)
    feedback = Column(String(255), nullable=True)
    roomcomfort = Column(SmallInteger, nullable=True)
    roomcleanliness = Column(SmallInteger, nullable=True)
    staffservice = Column(SmallInteger, nullable=True)
    facilities = Column(SmallInteger, nullable=True)
    value = Column(SmallInteger, nullable=True)
    wifi = Column(SmallInteger, nullable=True)
    appropriate = Column(Boolean, nullable=True, default=True)

    site = relationship("Sites", back_populates="resource", passive_deletes=True)
    hotel = relationship(
        "Hotels", back_populates="reviews", cascade="all, delete"
    )
