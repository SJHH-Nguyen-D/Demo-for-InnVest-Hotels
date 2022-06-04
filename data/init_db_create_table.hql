create database if not exists salesPortfolio;
use salesPortfolio;
create external table if not exists hotels
(`HID` BIGINT,
  hotelbrandname STRING,
  hotelfullyqualifiedname STRING,
  hotelcountry STRING,
  hotelprovince STRING,
  hotelcity STRING,
  hotelstreetnumber SMALLINT,
  hotelstreetname STRING,
  hotelpostalcode STRING,
  website STRING,
  phonenum INT,
  servicelevel STRING,
  maxoccupancy INT,
  operationalrooms INT,
  bar_lounge BOOLEAN,
  breakfast_included BOOLEAN,
  business_center BOOLEAN,
  cold_weather_hook_up BOOLEAN,
  dry_cleaning_service BOOLEAN,
  electric_vehicle_charging BOOLEAN,
  executive_lounge BOOLEAN,
  kids_club BOOLEAN,
  laundry_self BOOLEAN,
  meeting_event_space BOOLEAN,
  outdoor_patio BOOLEAN,
  parking_self BOOLEAN,
  parking_valet BOOLEAN,
  pets_allowed BOOLEAN,
  pool BOOLEAN,
  restaurant BOOLEAN,
  room_service BOOLEAN,
  spa BOOLEAN,
  swimming_pool_indoor BOOLEAN,
  swimming_pool_outdoor BOOLEAN,
  wheelchair_accessible BOOLEAN,
  kitchen BOOLEAN,
  microwave_and_refridgerator BOOLEAN,
  outdoor_recreation BOOLEAN,
  primary key (HID) -- disable novalidate
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/salesPortfolio.db/hotels';

create external table if not exists accomodations (
  `AID` BIGINT,
  accomodationtype CHAR(15),
  description CHAR(255),
  squarefootage INT,
  maxoccupancy INT,
  numbeds INT,
  bedsize CHAR(20),
  refundable BOOLEAN,
  roomnumber INT,
  roomfloor INT,
  roomrate DOUBLE,
  amenities STRING,
  primary key (AID) disable novalidate,
  hid BIGINT,
  constraint fk_hotel_room
    foreign key (hid)
      references hotels(HID),
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/salesPortfolio.db/accomodations';

-- create external table if not exists patron (
--   pid uuid,
--   firstname STRING,
--   lastname STRING,
--   vip BOOLEAN,
--   premium BOOLEAN,
--   homestreetnumber int,
--   homestreetname STRING,
--   homepostalcode STRING,
--   homecountry STRING,
--   homecity STRING,
--   email STRING,
--   firsttransaction date,
--   phonenumber varCHAR(15),
--   altnumber varCHAR(15), 
--   primary key(pid),
--   hid uuid,
--   constraint fk_hotel_patron
--     foreign key(hid)
--       references hotels(hid)
--       on delete set cascade
-- )
-- row format delimited
-- fields terminated by ','
-- lines terminated by '\n'
-- stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/salesPortfolio.db/patrons';

create external table if not exists transactions (
  `TID` BIGINT,
  hid BIGINT,
  aid BIGINT,
  checkindate DATE,
  checkoutdate DATE,
  methodofpayment STRING,
  price DOUBLE,
  primary key(tid),
  constraint fk_hotel_sales
    foreign key(hid)
      references hotels(HID)
      ON DELETE CASCADE
  constraint fk_accomodation_sales
    foreign key(hid)
      references accomodations(AID)
      ON DELETE CASCADE
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/salesPortfolio.db/transactions';

create external table if not exists reviews (
  `REVID` BIGINT,
  hid BIGINT,
  reviewdatetime DATE,
  reviewedby STRING,
  travelledfrom CHAR(100),
  revieweragebracket STRING,
  travelcompanions CHAR(25),
  typeoftrip CHAR(25),
  title CHAR(100),
  feedback CHAR(255),
  roomcomfort TINYINT,
  roomcleanliness TINYINT,
  staffservice TINYINT,
  facilities TINYINT,
  value TINYINT,
  wifi TINYINT,
  appropriate BOOLEAN,
  primary key(REVID),
  constraint fk_hotel_reviews
    foreign key(hid)
      references hotels(HID)
      on delete cascade
)
row format delimited
fields terminated by ','
lines terminated by '\n'
stored as textfile location 'hdfs://namenode:8020/user/hive/warehouse/salesPortfolio.db/reviews';
