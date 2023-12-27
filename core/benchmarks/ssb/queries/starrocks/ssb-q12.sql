SELECT year(lo_orderdate) AS year,
    s_nation, p_category, sum(lo_revenue - lo_supplycost) AS profit
FROM date, customer, supplier, part, lineorder
WHERE lo_custkey = c_custkey
AND lo_suppkey = s_suppkey
AND lo_partkey = p_partkey
AND lo_orderdate = d_datekey
AND c_region = 'AMERICA' AND s_region = 'AMERICA'
AND lo_orderdate >= 19970101 and lo_orderdate <= 19981231
AND p_mfgr in ( 'MFGR#1' , 'MFGR#2')
GROUP BY year, s_nation, p_category
ORDER BY year ASC, s_nation ASC, p_category ASC;