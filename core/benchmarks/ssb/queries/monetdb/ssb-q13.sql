SELECT d_year, s_city, p_brand,
    sum(lo_revenue - lo_supplycost) AS profit
FROM date, customer, supplier, part, lineorder
WHERE lo_custkey = c_custkey
AND lo_suppkey = s_suppkey
AND lo_partkey = p_partkey
AND lo_orderdate = d_datekey
AND s_nation = 'UNITED STATES'
AND lo_orderdate >= 19970101 and lo_orderdate <= 19981231
AND p_category = 'MFGR#14'
GROUP BY d_year, s_city, p_brand
ORDER BY d_year ASC, s_city ASC, p_brand ASC;