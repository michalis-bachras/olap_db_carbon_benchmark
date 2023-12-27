# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import argparse
import os
import time

import psutil
import pyRAPL.outputs

import utils
from core.benchmarks.benchmark_factory import BenchmarkFactory
from core.databases.dbfactory import DatabaseFactory
from core.databases.hyper import HyperDatabase
from core.tracker import Tracker

import requests

if __name__ == '__main__':
    pyRAPL.setup()
    # print(utils.get_location())
    # carbon_intensity = utils.get_latest_carbon_intensity()
    # print(carbon_intensity)
    # utils.get_latest_carbon_intensity()
    # print(psutil.disk_partitions())
    parser = argparse.ArgumentParser(description="Run five different benchmarks.")
    parser.add_argument("--benchmark", type=str, default=1, choices=["tpch", "tpcds", "ssb"],
                        help="Choose between tpch,tpcds,ssb", required=True)
    parser.add_argument("--database", type=str, default=1, choices=["duckdb", "psql", "monetdb", "starrocks", "hyper"],
                        help="Choose between duckdb,psql,monetdb,starrocks,hyper", required=True)
    parser.add_argument("--data", type=str, help="the path where benchmark data are stored", required=True)
    if "duckdb" in parser.parse_known_args()[0].database:
        parser.add_argument("--db_path", type=str, help="path of persistent storage")
    if "hyper" in parser.parse_known_args()[0].database:
        parser.add_argument("--db_path", type=str, help="path of persistent storage")
    if "monetdb" in parser.parse_known_args()[0].database:
        parser.add_argument("--username", type=str, default="monetdb", help="username of the database")
        parser.add_argument("--password", type=str, default="monetdb", help="password of the database")
        parser.add_argument("--port", type=int, default=50000, help="port of the database")
        parser.add_argument("--hostname", type=str, default="localhost", help="hostname of the database")
        parser.add_argument("--dbname", type=str, help="name of the database")
        parser.add_argument("--dbfarm", type=str, help="dbfarm of the database")
    if "starrocks" in parser.parse_known_args()[0].database:
        parser.add_argument("--ip", type=str, help="ip address of starrocks' fe")
        parser.add_argument("--name", type=str, help="name of the database")
    if "psql" in parser.parse_known_args()[0].database:
        parser.add_argument("--username", type=str, default="postgres", help="username of the database")
        parser.add_argument("--password", type=str, default="postgres", help="password of the database")
        parser.add_argument("--port", type=int, default=5432, help="port of the database")
        parser.add_argument("--hostname", type=str, default="localhost", help="hostname of the database")
        parser.add_argument("--dbname", type=str, help="name of the database")
    parser.add_argument("--iterations", type=int, default=1000, help="Number of iterations for each benchmark.")
    args = parser.parse_args()
    # print(args.benchmark)

    # Prepare for benchmark execution
    benchmark_factory = BenchmarkFactory()
    benchmark = benchmark_factory.create_benchmark(args.benchmark)
    # Set the scale factor for the current execution of the benchmark
    benchmark.sf = utils.extract_sf_from_path(args.data)
    db_factory = DatabaseFactory()
    db = db_factory.create_database(args)
    utils.initializeOutput(benchmark, args.database)
    benchmark.createSchema(db)


    # Calculate the energy consumption in idle state
    utils.calculate_average_energy(16, benchmark, db.type)

    benchmark.loadData(db, args.data)
    # calculate_average_energy(16)
    benchmark.run(db)
    db.close()
