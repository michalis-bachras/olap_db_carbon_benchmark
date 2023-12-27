import duckdb

from core.databases.db import Database


class DuckDBDatabase:

    def __init__(self, dbname, db_path):
        self.type = "duckdb"
        self.connection = duckdb.connect(db_path + dbname + ".db")

    def getType(self):
        return self.type

    def generate_load_queries(self, data_path, tables, ftype):
        sql_queries = []
        for table in tables:
            query = f"COPY {table} FROM '{data_path}/{table}.{ftype}' WITH DELIMITER '|';"
            sql_queries.append(query)

        return sql_queries, "sql"

    def create_schema(self, schema):
        duckdb.sql(schema)

    def create_schema_TPCH(self):
        duckdb.sql(
            "CREATE TABLE customer(c_custkey INTEGER NOT NULL, c_name VARCHAR(25) NOT NULL, c_address VARCHAR(40) NOT NULL, "
            "c_nationkey INTEGER NOT NULL, c_phone CHAR(15) NOT NULL, c_acctbal DECIMAL(15,2) NOT NULL, c_mktsegment CHAR(10) NOT NULL, "
            "c_comment VARCHAR(117) NOT NULL);")
        duckdb.sql(
            "CREATE TABLE lineitem(l_orderkey INTEGER NOT NULL, l_partkey INTEGER NOT NULL, l_suppkey INTEGER NOT NULL, "
            "l_linenumber INTEGER NOT NULL, l_quantity DECIMAL(15,2) NOT NULL, l_extendedprice DECIMAL(15,2) NOT NULL, "
            "l_discount DECIMAL(15,2) NOT NULL, l_tax DECIMAL(15,2) NOT NULL, l_returnflag CHAR(1) NOT NULL, l_linestatus CHAR(1) NOT NULL, "
            "l_shipdate DATE NOT NULL, l_commitdate DATE NOT NULL, l_receiptdate DATE NOT NULL, l_shipinstruct CHAR(25) "
            "NOT NULL, "
            "l_shipmode CHAR(10) NOT NULL, l_comment VARCHAR(44) NOT NULL);")
        duckdb.sql(
            "CREATE TABLE nation(n_nationkey INTEGER NOT NULL, n_name CHAR(25) NOT NULL, n_regionkey INTEGER NOT NULL,"
            " n_comment VARCHAR(152) NOT NULL);")
        duckdb.sql(
            "CREATE TABLE orders(o_orderkey INTEGER NOT NULL, o_custkey INTEGER NOT NULL, o_orderstatus CHAR(1) NOT NULL, "
            "o_totalprice DECIMAL(15,2) NOT NULL, o_orderdate DATE NOT NULL, o_orderpriority CHAR(15) NOT NULL, "
            "o_clerk CHAR(15) NOT NULL, o_shippriority INTEGER NOT NULL, o_comment VARCHAR(79) NOT NULL);")
        duckdb.sql(
            "CREATE TABLE part(p_partkey INTEGER NOT NULL, p_name VARCHAR(55) NOT NULL, p_mfgr CHAR(25) NOT NULL, "
            "p_brand CHAR(10) NOT NULL, p_type VARCHAR(25) NOT NULL, p_size INTEGER NOT NULL, p_container CHAR(10) NOT NULL, "
            "p_retailprice DECIMAL(15,2) NOT NULL, p_comment VARCHAR(23) NOT NULL);")
        duckdb.sql(
            "CREATE TABLE partsupp(ps_partkey INTEGER NOT NULL, ps_suppkey INTEGER NOT NULL, ps_availqty INTEGER NOT NULL,"
            " ps_supplycost DECIMAL(15,2) NOT NULL, ps_comment VARCHAR(199) NOT NULL);")
        duckdb.sql(
            "CREATE TABLE region(r_regionkey INTEGER NOT NULL, r_name CHAR(25) NOT NULL, r_comment VARCHAR(152) NOT NULL);")
        duckdb.sql(
            "CREATE TABLE supplier(s_suppkey INTEGER NOT NULL, s_name CHAR(25) NOT NULL, s_address VARCHAR(40) NOT NULL, "
            "s_nationkey INTEGER NOT NULL, s_phone CHAR(15) NOT NULL, s_acctbal DECIMAL(15,2) NOT NULL, "
            "s_comment VARCHAR(101) NOT NULL);")

    def load_data(self, path):
        duckdb.sql(
            "COPY customer FROM '/home/michalis/Documents/UofT/MSRG/CloudDB discussion/TPCH/TPC-H V3.0.1/dbgen/data_100mb/customer.tbl' WITH "
            "DELIMITER '|';")
        duckdb.sql(
            "COPY lineitem FROM '/home/michalis/Documents/UofT/MSRG/CloudDB discussion/TPCH/TPC-H V3.0.1/dbgen/data_100mb/lineitem.tbl' ( DELIMITER "
            "'|' );")
        duckdb.sql(
            "COPY nation FROM '/home/michalis/Documents/UofT/MSRG/CloudDB discussion/TPCH/TPC-H V3.0.1/dbgen/data_100mb/nation.tbl' WITH DELIMITER '|';")
        duckdb.sql(
            "COPY orders FROM '/home/michalis/Documents/UofT/MSRG/CloudDB discussion/TPCH/TPC-H V3.0.1/dbgen/data_100mb/orders.tbl' ( DELIMITER '|' );")
        duckdb.sql(
            "COPY part FROM '/home/michalis/Documents/UofT/MSRG/CloudDB discussion/TPCH/TPC-H V3.0.1/dbgen/data_100mb/part.tbl' WITH DELIMITER '|';")
        duckdb.sql(
            "COPY partsupp FROM '/home/michalis/Documents/UofT/MSRG/CloudDB discussion/TPCH/TPC-H V3.0.1/dbgen/data_100mb/partsupp.tbl' WITH DELIMITER '|';")
        duckdb.sql(
            "COPY region FROM '/home/michalis/Documents/UofT/MSRG/CloudDB discussion/TPCH/TPC-H V3.0.1/dbgen/data_100mb/region.tbl' WITH DELIMITER '|';")
        duckdb.sql(
            "COPY supplier FROM '/home/michalis/Documents/UofT/MSRG/CloudDB discussion/TPCH/TPC-H V3.0.1/dbgen/data_100mb/supplier.tbl' WITH DELIMITER '|';")

    def execute(self, query):
        # result = duckdb.sql(query)
        result = self.connection.sql(query)
        if result is not None:
            result.show()

    def close(self):
        self.connection.close()