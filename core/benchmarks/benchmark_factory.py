from core.benchmarks.ssb import SSBBenchmark
from core.benchmarks.tpcds import TPCDSBenchmark
from core.benchmarks.tpch import TPCHBenchmark


class BenchmarkFactory:
    def create_benchmark(self, benchmark_type):
        if benchmark_type == 'tpch':
            print('tpch')
            return TPCHBenchmark()
        elif benchmark_type == 'tpcds':
            return TPCDSBenchmark()
        elif benchmark_type == 'ssb':
            return SSBBenchmark()
