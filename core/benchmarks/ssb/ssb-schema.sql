CREATE TABLE lineorder (
    lo_orderkey     INTEGER NOT NULL,
    lo_linenumber   INTEGER NOT NULL,
    lo_custkey      INTEGER NOT NULL,
    lo_suppkey      INTEGER NOT NULL,
    lo_partkey      INTEGER NOT NULL,
    lo_orderdate    INTEGER NOT NULL,
    lo_shippriority INTEGER NOT NULL,
    lo_quantity     INTEGER NOT NULL,
    lo_extendedprice DECIMAL(15,2) NOT NULL,
    lo_ordertotalprice DECIMAL(15,2) NOT NULL,
    lo_discount     DECIMAL(15,2) NOT NULL,
    lo_revenue      DECIMAL(15,2) NOT NULL,
    lo_supplycost   DECIMAL(15,2) NOT NULL,
    lo_tax          DECIMAL(15,2) NOT NULL,
    lo_commitdate   INTEGER NOT NULL,
    lo_shipmode      CHAR(10) NOT NULL
);

CREATE TABLE customer (
    c_custkey       INTEGER NOT NULL,
    c_name          CHAR(25) NOT NULL,
    c_address       VARCHAR(40) NOT NULL,
    c_city          CHAR(10) NOT NULL,
    c_nation        CHAR(15) NOT NULL,
    c_region        CHAR(12) NOT NULL,
    c_phone         CHAR(15) NOT NULL,
    c_mktsegment    CHAR(10) NOT NULL
);

CREATE TABLE supplier (
    s_suppkey       INTEGER NOT NULL,
    s_name          CHAR(25) NOT NULL,
    s_address       VARCHAR(40) NOT NULL,
    s_city          CHAR(10) NOT NULL,
    s_nation        CHAR(15) NOT NULL,
    s_region        CHAR(12) NOT NULL,
    s_phone         CHAR(15) NOT NULL
);

CREATE TABLE part (
    p_partkey       INTEGER NOT NULL,
    p_name          VARCHAR(22) NOT NULL,
    p_mfgr          CHAR(6) NOT NULL,
    p_category      CHAR(7) NOT NULL,
    p_brand1        CHAR(9) NOT NULL,
    p_color         CHAR(11) NOT NULL,
    p_type          VARCHAR(25) NOT NULL,
    p_size          INTEGER NOT NULL
);

CREATE TABLE dates (
    d_datekey       INTEGER NOT NULL,
    d_date          CHAR(18) NOT NULL,
    d_dayofweek     CHAR(10) NOT NULL,
    d_month         CHAR(10) NOT NULL,
    d_year          INTEGER NOT NULL,
    d_yearmonthnum  INTEGER NOT NULL,
    d_yearmonth     CHAR(7) NOT NULL,
    d_daynuminweek  INTEGER NOT NULL,
    d_daynuminmonth INTEGER NOT NULL,
    d_daynuminyear  INTEGER NOT NULL,
    d_monthnuminyear INTEGER NOT NULL,
    d_lastdayinweekfl INTEGER NOT NULL,
    d_lastdayinmonthfl INTEGER NOT NULL,
    d_holidayfl     INTEGER NOT NULL,
    d_weekdayfl     INTEGER NOT NULL
);
