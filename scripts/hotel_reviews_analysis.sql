SELECT r.hotel_id, h.hotelfullyqualifiedname, avg(r.roomcomfort), avg(r.roomcleanliness), avg(r.staffservice), avg(r.facilities)
FROM reviews r
LEFT JOIN hotels h
ON r.hotel_id = h.id
GROUP BY r.hotel_id, h.hotelfullyqualifiedname;
