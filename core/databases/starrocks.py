from sqlalchemy import create_engine
from sqlalchemy.schema import Table, MetaData
from sqlalchemy.sql.expression import select, text
import pymysql
import mysql.connector


class StarrocksDatabase:

    def __init__(self,ip,dbname):
        self.type = "starrocks"
        try:
            self.connection = mysql.connector.connect(host=ip, user='root', port='9030')
            self.ip = ip
            self.dbname = dbname
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to Starrocks ", db_Info)
                createdb_query = "CREATE DATABASE IF NOT EXISTS " + dbname + ";"
                self.execute(createdb_query)
                usedb_query = "USE " + dbname + ";"
                self.execute(usedb_query)

        except mysql.connector.Error as e:
            print("Error while connecting to Starrocks", e)


    def getType(self):
        return self.type

    def generate_load_queries(self, data_path, tables, ftype):
        commands = []
        for table in tables:
            #tableName = table + "_changed"
            tableName = table
            command = ("curl --location-trusted -u root: -T '" + data_path + "/" + tableName + "." + ftype + "' -H 'format: CSV' -H 'column_separator:|' -XPUT "
                       "http://" + self.ip + ":8030/api/" + self.dbname +"/" + table + "/_stream_load")
            commands.append(command)
        return commands, "shell"

    def execute(self, query):
        if self.connection.is_connected():
            db_Info = self.connection.get_server_info()
            print("Connected to Starrocks ", db_Info)
        cursor = self.connection.cursor()
        for statement in filter(None, map(str.strip, query.split(';'))):
            cursor.execute(statement)
            self.print_results(cursor)
        #cursor.execute(query)
        #self.print_results(cursor)

    def print_results(self, cursor):
        # Fetch the results
        records = cursor.fetchall()
        for row in records:
            print(row)

    def close(self):
        self.connection.close()