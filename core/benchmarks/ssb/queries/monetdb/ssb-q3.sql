SELECT sum(lo_extendedprice * lo_discount) AS revenue
FROM lineorder, date
WHERE lo_orderdate = d_datekey
AND d_weeknuminyear = 6
AND lo_orderdate >= 19940101 and lo_orderdate <= 19941231
AND lo_discount BETWEEN 5 AND 7 AND lo_quantity BETWEEN 26 AND 35;