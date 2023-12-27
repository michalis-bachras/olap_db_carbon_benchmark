import csv
import json
import os
import time
from collections import namedtuple

import psutil
import pyRAPL
import requests
import ipinfo

from core.tracker import Tracker

carbon_intensity = 0

LinuxDiskIOStats = namedtuple('DiskIOStats',
                              ['read_count', 'write_count', 'read_bytes', 'write_bytes', 'read_time', 'write_time',
                               'read_merged_count', 'write_merged_count', 'busy_time'])


def print_tracker_results(job, tracker_results):
    print("Results for " + job + ":")
    if tracker_results['dram_total_energy'] != 0:
        print("Total energy consumed by RAM is:" + str(tracker_results['dram_total_energy']) + " μJ")
        print("Average energy consumed by RAM is:" + str(tracker_results['avg_dram_energy']) + " μJ/μsec")
        print("Total carbon emitted by RAM is:" + str(
            calculate_kwh(tracker_results['avg_dram_energy']) * carbon_intensity) + " gCO₂eq")
    for i in range(len(tracker_results['cpu_total_energy'])):
        print(
            "Total energy consumed by package " + str(i) + " is " + str(tracker_results['cpu_total_energy'][i]) + " μJ")
        print("Average energy consumed by package " + str(i) + " is " + str(
            tracker_results['avg_cpu_energy'][i]) + " μJ/μsec")
        print("Total carbon emitted by package " + str(i) + " is " + str(
            calculate_kwh(tracker_results['cpu_total_energy'][i]) * carbon_intensity) + " gCO₂eq")
    print("Total execution time is: " + str(tracker_results['total_duration']) + " μsec")


# def get_ip():
#   ip = requests.get('https://checkip.amazonaws.com').text.strip()
#    return ip

def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]


def get_location():
    ip_address = get_ip()
    access_token = '23d3ea0900771d'
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip_address)
    location_data = {
        "ip": ip_address,
        "city": details.city,
        # "region": response.get("region"),
        "country": details.country,
        "latitude": details.latitude,
        "longitude": details.longitude
    }
    # response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    # location_data = {
    #    "ip": ip_address,
    #    "city": response.get("city"),
    #    "region": response.get("region"),
    #    "country": response.get("country_name"),
    #    "latitude": response.get("latitude"),
    #    "longitude": response.get("longitude")
    # }
    return location_data


def get_latest_carbon_intensity():
    location = get_location()
    print(location)
    latitude = location.get("latitude")
    longitude = location.get("longitude")
    url = "https://api-access.electricitymaps.com/free-tier/carbon-intensity/latest?lat=" + str(
        latitude) + "&lon=" + str(longitude)
    headers = {
        "auth-token": "9oKv71Ozq9kcZSOw9UrFK8UZL9ahMNXM"
    }
    response = requests.get(url, headers=headers)
    print(response.text)
    data = json.loads(response.text)
    global carbon_intensity
    carbon_intensity = data.get("carbonIntensity")
    # return data


def calculate_kwh(energy_uJ):
    power_kwh = energy_uJ / (3.6 * 10 ** 12)  # From μJoules to kWh
    return power_kwh


def initializeOutput(benchmark, database):
    csv_header = ['Label', 'dram_avgE(μJ/μsec)', 'dram_totalE(μJ)', 'dram_carbon']
    with open(benchmark.path + "results/" + benchmark.type + "_" + benchmark.sf + "_" + database + ".csv", 'w', encoding='UTF8') as f:
        for i in range(len(pyRAPL._sensor._socket_ids)):
            csv_header.append('cpu_' + str(i) + '_avgE(μJ/μsec)')
            csv_header.append('cpu_' + str(i) + '_totalE(μJ)')
            csv_header.append('cpu_' + str(i) + '_carbon')
        csv_header.append('Latency(sec)')
        # IO headers
        csv_header.append('Device')
        csv_header.append('Read Count')
        csv_header.append('Write Count')
        csv_header.append('Read Bytes')
        csv_header.append('Write Bytes')
        csv_header.append('Read Time(ms)')
        csv_header.append('Write Time(ms)')
        csv_header.append('Busy Time(ms)')

        writer = csv.writer(f)
        # write the header
        writer.writerow(csv_header)


def export_query_stats(benchmark, database, label, results, latency, io_counters):
    data = [label]
    with open(benchmark.path + "results/" + benchmark.type + "_" + benchmark.sf + "_" + database + ".csv", 'a', encoding ='UTF8') as f:
        writer = csv.writer(f)
        data.append(results['avg_dram_energy'])
        data.append(results['dram_total_energy'])
        data.append(calculate_kwh(results['dram_total_energy']) * carbon_intensity)
        cpu_counter = 0
        while cpu_counter < len(pyRAPL._sensor._socket_ids):
            data.append(results['avg_cpu_energy'][cpu_counter])
            data.append(results['cpu_total_energy'][cpu_counter])
            data.append(calculate_kwh(results['cpu_total_energy'][cpu_counter]) * carbon_intensity)
            cpu_counter = cpu_counter + 1
        data.append(latency)
        for device, io_counter in io_counters.items():
            if 'loop' in device:
                continue
            data.append(device)
            data.append(io_counter.read_count)
            data.append(io_counter.write_count)
            data.append(io_counter.read_bytes)
            data.append(io_counter.write_bytes)
            data.append(io_counter.read_time)
            data.append(io_counter.write_time)
            data.append(io_counter.busy_time)
            break
        writer.writerow(data)


def export_throughput(benchmark, database, throughput):
    csv_header = ['Throughput(queries/sec)']
    with open(benchmark.path + "results/" + benchmark.type + "_" + benchmark.sf + "_" + database + ".csv", 'a', encoding='UTF8') as f:
        writer = csv.writer(f)
        # write the header
        writer.writerow(csv_header)
        data = [throughput]
        writer.writerow(data)


def measure_io_operations(initial_io_counters, final_io_counters):
    # Calculate the difference in IO counters
    io_counters_diff = {}
    for device, final_counter in final_io_counters.items():
        initial_counter = initial_io_counters.get(device)
        diff_counter = LinuxDiskIOStats(
            read_count=final_counter.read_count - initial_counter.read_count,
            write_count=final_counter.write_count - initial_counter.write_count,
            read_bytes=final_counter.read_bytes - initial_counter.read_bytes,
            write_bytes=final_counter.write_bytes - initial_counter.write_bytes,
            read_time=final_counter.read_time - initial_counter.read_time,
            write_time=final_counter.write_time - initial_counter.write_time,
            read_merged_count=final_counter.read_merged_count - initial_counter.read_merged_count,
            write_merged_count=final_counter.write_merged_count - initial_counter.write_merged_count,
            busy_time=final_counter.busy_time - initial_counter.busy_time
        )
        io_counters_diff[device] = diff_counter

    return io_counters_diff


def filter_non_zero_counters(io_counters_diff):
    # Filter out devices with no IO operations
    non_zero_counters = {device: counter for device, counter in io_counters_diff.items() if any(counter)}
    return non_zero_counters


def calculate_run_stats(benchmark, database, job, tracker_results, io_counters_start, io_counters_end, latency):
    # Measure IO operations
    io_operations_result = measure_io_operations(io_counters_start, io_counters_end)

    # Filter out disk devices with no IO operations
    non_zero_counters = filter_non_zero_counters(io_operations_result)

    # Print the results
    # for device, io_counter in non_zero_counters.items():
    #   if 'loop' in device:
    #        continue
    #    print(f"Device: {device}")
    #   print(f"Read Count: {io_counter.read_count}")
    #   print(f"Write Count: {io_counter.write_count}")
    #    print(f"Read Bytes: {io_counter.read_bytes}")
    #   print(f"Write Bytes: {io_counter.write_bytes}")
    #   print(f"Read Time(ms): {io_counter.read_time}")
    #    print(f"Write Time(ms): {io_counter.write_time}")
    #    print(f"Busy Time(ms): {io_counter.busy_time}")
    #    print("")
    #   break

    print_tracker_results(job, tracker_results)
    export_query_stats(benchmark, database, job, tracker_results, latency, non_zero_counters)


# Extract scale factor from data path
def extract_sf_from_path(path):
    # Get the base name of the path
    base_name = os.path.basename(path)
    # Extract scale factor
    parts = base_name.split('_')
    return parts[1]


# Calculates the average energy consumption before executing anything
def calculate_average_energy(duration,benchmark,db_type):
    print("Measuring the energy consumption of the system in idle state for " + str(duration) + " seconds\n")
    tracker = Tracker(1, "machine", "avgEnergy")
    start_time = time.time()
    tracker.start()
    io_counters_start = psutil.disk_io_counters(perdisk=True)
    while time.time() - start_time < duration:
        # Do nothing
        pass
    tracker.stop()
    io_counters_end = psutil.disk_io_counters(perdisk=True)
    print_tracker_results("idle state", tracker.results)
    data = ["idle state"]
    with open(benchmark.path + "results/" + benchmark.type + "_" + benchmark.sf + "_" + db_type + ".csv", 'a',
              encoding='UTF8') as f:
        writer = csv.writer(f)
        data.append(tracker.results['avg_dram_energy'])
        data.append(tracker.results['dram_total_energy'])
        data.append(calculate_kwh(tracker.results['dram_total_energy']) * carbon_intensity)
        cpu_counter = 0
        while cpu_counter < len(pyRAPL._sensor._socket_ids):
            data.append(tracker.results['avg_cpu_energy'][cpu_counter])
            data.append(tracker.results['cpu_total_energy'][cpu_counter])
            data.append(calculate_kwh(tracker.results['cpu_total_energy'][cpu_counter]) * carbon_intensity)
            cpu_counter = cpu_counter + 1
        data.append(duration)
        writer.writerow(data)
