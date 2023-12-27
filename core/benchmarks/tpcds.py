from core.benchmarks.benchmark import Benchmark
from core.databases.duckdb import DuckDBDatabase
from core.databases.postgresql import PostgreSQLDatabase
import psutil

import time
from core.tracker import Tracker
import utils
import subprocess
import os


class TPCDSBenchmark(Benchmark):

    def __init__(self):
        with open('core/benchmarks/tpcds/tpcds-schema.sql', 'r') as file:
            self.schema = file.read()
        self.tables = [
            "call_center",
            "catalog_returns",
            "customer_address",
            "customer_demographics",
            "household_demographics",
            "inventory",
            "promotion",
            "ship_mode",
            "store_returns",
            "time_dim",
            "web_page",
            "web_sales",
            "catalog_page",
            "catalog_sales",
            "customer",
            "date_dim",
            "income_band",
            "item",
            "reason",
            "store",
            "store_sales",
            "warehouse",
            "web_returns",
            "web_site"
        ]
        self.path = "core/benchmarks/tpcds/"
        self.type = "tpcds"

    def createSchema(self, db):
        print("Creating TPCDS schema in " + str(type(db)))
        with open('core/benchmarks/tpcds/' + db.type + '_schema.sql', 'r') as file:
            schema = file.read()
        db.execute(schema)

    def loadData(self, db,data_path):
        #data_path = "/home/michalis/Documents/UofT/MSRG/Carbon/benchmarks/tpcds/data/data_1gb/starrocks_data/"
        print("Loading TPCDS data in " + str(type(db)))
        load_tuple = db.generate_load_queries(data_path, self.tables, "csv")
        tracker = Tracker(10000, "tpcds", "tpcds-load data")
        io_counters_start = psutil.disk_io_counters(perdisk=True)
        tracker.start()
        start_time = time.time()
        if load_tuple[1] == "sql":
            for query in load_tuple[0]:
                db.execute(query)
        elif load_tuple[1] == "shell":
            for command in load_tuple[0]:
                subprocess.run(command, shell=True)
        elif load_tuple[1] == "custom":
            db.load_data(data_path, self.tables, "csv")
        end_time = time.time()
        tracker.stop()
        io_counters_end = psutil.disk_io_counters(perdisk=True)
        elapsed_time = end_time - start_time
        # Calculate and export all measured metrics
        utils.calculate_run_stats(self, db.type, "load data", tracker.results, io_counters_start, io_counters_end,
                                  elapsed_time)
        #utils.print_tracker_results("load data", tracker.results)

    def run(self, db):
        queries = []
        qpath = self.path + "queries/" + db.getType()
        for j in range(1, 100):
            queryName = "tpcds_q" + str(j) + ".sql"
            with open(os.path.join(qpath, queryName), "r") as file:
                query = file.read()
                queries.append(query)
        total_stream_time = 0
        counter = 1
        for query in queries:
            tracker = Tracker(10000, "tpcds", "tpcds-q" + str(j))
            io_counters_start = psutil.disk_io_counters(perdisk=True)
            tracker.start()
            start_time = time.time()
            db.execute(query)
            end_time = time.time()
            tracker.stop()
            io_counters_end = psutil.disk_io_counters(perdisk=True)
            elapsed_time = end_time - start_time
            # Calculate and export all measured metrics
            utils.calculate_run_stats(self, db.type, "tpcds-q" + str(counter), tracker.results, io_counters_start,
                                      io_counters_end,
                                      elapsed_time)
            total_stream_time = total_stream_time + elapsed_time
            counter = counter + 1

        # Number of queries in the stream
        num_queries = len(queries)
        # Calculate and print throughput
        throughput = num_queries / total_stream_time
        utils.export_throughput(self, db.type, throughput)
        if db.type == 'hyper':
            db.close()
