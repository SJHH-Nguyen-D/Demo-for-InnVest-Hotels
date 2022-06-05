select YEAR(checkindate) [YEAR], MONTH(checkindate) [MONTH], DATENAME(MONTH, checkindate) [Month Name], SUM(saleamount) [
                                            SALE AMT]
                                            FROM transactions
                                            GROUP BY YEAR(checkindate), MONTH(checkindate), DATENAME(MONTH, checkindate)
                                            ORDER BY 1, 2
                                            LIMIT 5;
