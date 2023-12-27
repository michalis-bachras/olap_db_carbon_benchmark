COPY INTO customer FROM '/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpch/data/data_100mb/customer.tbl' USING DELIMITERS '|';
COPY INTO lineitem FROM '/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpch/data/data_100mb/lineitem.tbl' USING DELIMITERS '|';
COPY INTO nation FROM '/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpch/data/data_100mb/nation.tbl' USING DELIMITERS '|';
COPY INTO orders FROM '/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpch/data/data_100mb/orders.tbl' USING DELIMITERS '|';
COPY INTO part FROM '/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpch/data/data_100mb/part.tbl' USING DELIMITERS '|';
COPY INTO partsupp FROM '/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpch/data/data_100mb/partsupp.tbl' USING DELIMITERS '|';
COPY INTO region FROM '/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpch/data/data_100mb/region.tbl' USING DELIMITERS '|';
COPY INTO supplier FROM '/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpch/data/data_100mb/supplier.tbl' USING DELIMITERS '|';
