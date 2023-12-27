SELECT c_city, s_city, d_year, sum(lo_revenue) AS revenue
FROM customer, lineorder, supplier, date
WHERE lo_custkey = c_custkey
AND lo_suppkey = s_suppkey
AND lo_orderdate = d_datekey
AND c_city in ('UNITED KI1', 'UNITED KI5') AND s_city in ('UNITED KI1', 'UNITED KI5')
AND lo_orderdate  >= 19971201 AND lo_orderdate <= 19971231
GROUP BY c_city, s_city, d_year
ORDER BY d_year ASC, revenue DESC;