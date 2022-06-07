SELECT hotel_id, hotelfullyqualifiedname, YEAR(checkindate) as year, MONTH(checkindate) as month,  SUM(saleamount)
FROM transactions
LEFT JOIN hotels
ON transactions.hotel_id = hotels.id
GROUP BY YEAR(checkindate), MONTH(checkindate), hotel_id, HOTELFULLYQUALIFIEDNAME
ORDER BY  3, 4;
