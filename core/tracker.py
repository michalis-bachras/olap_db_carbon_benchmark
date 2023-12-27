import time

import pyRAPL
import pyRAPL.outputs
from pyRAPL import Measurement

from periodic import PeriodicMeter


class Tracker(object):
    def __init__(self, interval, benchmark, measurement):
        self.interval = interval
        self.benchmark = benchmark
        self.meter = pyRAPL.Measurement(measurement)

        self.last_measured_time: float = 0
        self.cpu_total_energy = []
        self.avgCPUEnergy = []
        for i in range(len(pyRAPL._sensor._socket_ids)):
            self.cpu_total_energy.append(0)
            self.avgCPUEnergy.append(0)
        self.dram_total_energy = 0
        self.total_duration = 0
        self.avgRAMEnergy = 0

        self._scheduler = PeriodicMeter(
            function=self.measureEnergy,
            interval=self.interval
        )

        self.results = {}

    def start(self):
        self.meter.begin()
        self.last_measured_time = time.time()
        self._scheduler.start()

    def stop(self):
        self.meter.end()
        self._scheduler.stop()
        result = self.meter.result
        #Store results
        self.total_duration = self.total_duration + result.duration
        if result.dram is not None:
            self.dram_total_energy = self.dram_total_energy + float(result.dram) #/ float(result.duration)
            self.avgRAMEnergy = self.dram_total_energy/self.total_duration
           # print("Energy consumed by RAM is:" + str(float(result.dram) / float(result.duration)) + " μJ/μsec")
        for i in range(len(pyRAPL._sensor._socket_ids)):
            self.cpu_total_energy[i] = self.cpu_total_energy[i] + float(result.pkg[i]) #/ float(result.duration)
            self.avgCPUEnergy[i] = self.cpu_total_energy[i]/self.total_duration
            #print("Energy consumed by package " + str(i) + " is " + str(
             #   float(result.pkg[i]) / float(result.duration)) + " μJ/μsec")
        self.results['avg_cpu_energy'] = self.avgCPUEnergy
        self.results['avg_dram_energy'] = self.avgRAMEnergy
        self.results['cpu_total_energy'] = self.cpu_total_energy
        self.results['dram_total_energy'] = self.dram_total_energy
        self.results['total_duration'] = self.total_duration

    def measureEnergy(self):
        self.meter.end()
        result = self.meter.result
        if result.dram is not None and float(result.dram) > 0:
            self.dram_total_energy = self.dram_total_energy + float(result.dram) / float(result.duration)
            #print("Energy consumed by RAM is:" + str(float(result.dram) / float(result.duration)) + " μJ/μsec")
        for i in range(len(pyRAPL._sensor._socket_ids)):
            if float(result.pkg[i]) > 0:
                self.cpu_total_energy[i] = self.cpu_total_energy[i] + float(result.pkg[i]) / float(result.duration)
            #print("Energy consumed by package " + str(i) + " is " + str(
             #   float(result.pkg[i]) / float(result.duration)) + " μJ/μsec")
        self.total_duration = self.total_duration + result.duration
        # Start a measurement for the next interval
        self.meter.begin()
