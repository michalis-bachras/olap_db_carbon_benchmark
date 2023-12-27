import os.path

import pymonetdb
import subprocess



class MonetDBDatabase:

    def __init__(self, username, password, port, hostname, dbname, dbfarm):
        self.type = "monetdb"
        self.dbfarm = dbfarm
        if not os.path.exists(dbfarm):
            create_dbfarm_cmd = "monetdbd create " + dbfarm
            subprocess.run(create_dbfarm_cmd, shell=True)
        start_dbfarm_cmd = "monetdbd start " + dbfarm
        subprocess.run(start_dbfarm_cmd, shell=True)
        create_db_cmd = "monetdb create " + dbname
        subprocess.run(create_db_cmd, shell = True)
        start_db_cmd = "monetdb start " + dbname
        subprocess.run(start_db_cmd, shell=True)
        self.connection = pymonetdb.connect(username=username, password=password, port=port, hostname=hostname,
                                            database=dbname)
        # self.cursor = connection.cursor()

    def getType(self):
        return self.type

    def generate_load_queries(self, data_path, tables, ftype):
        sql_queries = []
        for table in tables:
            query = f"COPY INTO {table} FROM '{data_path}/{table}.{ftype}' USING DELIMITERS '|' NULL AS '';"
            sql_queries.append(query)
        return sql_queries,"sql"

    def execute(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        self.print_results(cursor)

    def print_results(self, cursor):
        if cursor.rowcount <= 0 or cursor.lastrowid == -1:
            print('The resultset is empty')
        else:
            # Fetch all rows of the resultset
            rows = cursor.fetchall()
            # Print the rows
            #for row in rows:
              #print(row)

    def close(self):
        self.connection.close()
        stop_dbfarm_cmd = "monetdbd stop " + self.dbfarm
        subprocess.run(stop_dbfarm_cmd, shell=True)