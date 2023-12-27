from tableauhyperapi import HyperProcess, Telemetry, Connection, CreateMode


class HyperDatabase:

    def __init__(self, dbname, db_path):
        self.type = "hyper"
        self.hyper = HyperProcess(telemetry=Telemetry.DO_NOT_SEND_USAGE_DATA_TO_TABLEAU)
        # self.hyper
        self.connection = Connection(endpoint=self.hyper.endpoint, database=db_path + dbname + ".hyper",create_mode= CreateMode.CREATE_IF_NOT_EXISTS)
        self.connection.catalog.create_database_if_not_exists(dbname)
        #self.connection.catalog.attach_database(dbname)
        # results = self.connection.execute_query("CREATE DATABASE IF NOT EXISTS " + dbname)
        # results.close()
        self.connection.catalog.create_schema_if_not_exists(dbname)
        # results = self.connection.execute_query("CREATE SCHEMA IF NOT EXISTS " + dbname)
        # results.close()
        # results = self.connection.execute_query("SET SCHEMA " +dbname)
        # results.close()

    def getType(self):
        return self.type

    def generate_load_queries(self, data_path, tables, ftype):
        sql_queries = []
        # ftype = 'csv'
        for table in tables:
            query = f"COPY {table} FROM '{data_path}/{table}.{ftype}' WITH ( FORMAT => 'csv', DELIMITER => '|' , header => false);"
            sql_queries.append(query)

        return sql_queries, "sql"

    def execute(self, query):
        for statement in filter(None, map(str.strip, query.split(';'))):
            results = self.connection.execute_query(statement)
            for row in results:
                print(row)
            results.close()

    def close(self):
        self.connection.close()
        self.hyper.close()
