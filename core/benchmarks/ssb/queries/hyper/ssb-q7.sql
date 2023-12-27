SELECT
    c_nation,
    s_nation,
    d_year,
    sum(lo_revenue) AS revenue FROM customer, lineorder, supplier, date
WHERE lo_custkey = c_custkey
AND lo_suppkey = s_suppkey
AND lo_orderdate = d_datekey
AND c_region = 'ASIA' AND s_region = 'ASIA' AND lo_orderdate >= 19920101
AND lo_orderdate <= 19971231
GROUP BY c_nation, s_nation, d_year
ORDER BY  d_year ASC, revenue DESC;