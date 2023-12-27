SELECT d_year, c_nation, sum(lo_revenue - lo_supplycost) AS profit
FROM date, customer, supplier, part, lineorder
WHERE  lo_custkey = c_custkey
AND lo_suppkey = s_suppkey
AND lo_partkey = p_partkey
AND lo_orderdate = d_datekey
AND c_region = 'AMERICA' AND s_region = 'AMERICA' AND p_mfgr in ('MFGR#1', 'MFGR#2')
GROUP BY d_year, c_nation
ORDER BY d_year ASC, c_nation ASC;