# © 2023 AO Kaspersky Lab. All Rights Reserved.
# Checks Sysdiagnose archives for traces of possible iOS infections using malware such as Pegasus

import os
import sys
import re
import tarfile
from datetime import datetime

# from termcolor import colored


result = ""


def count_occurrences(content, target_phrase):
    return content.count(target_phrase)


def find_anomalies_before_sigterm(content, anomaly_phrase, threshold=3):
    sigterm_pattern = re.compile(r'SIGTERM: \[(\d+)\]')
    content_lines = content.splitlines()

    anomalies_timestamps = []
    anomaly_count = 0

    for line in content_lines:
        if anomaly_phrase in line:
            anomaly_count += 1
        elif sigterm_match := sigterm_pattern.search(line):
            if anomaly_count >= threshold:
                unix_timestamp = int(sigterm_match.group(1))
                anomalies_timestamps.append(datetime.utcfromtimestamp(unix_timestamp))
            anomaly_count = 0

    return anomalies_timestamps


def process_hits(content, hit_phrase):
    count = 0
    decoded_dates = []
    values = []
    sigterm_pattern = re.compile(r'SIGTERM: \[(\d+)\]')
    found_hit = False
    last_decoded_date = None

    for line in content.splitlines():
        if hit_phrase in line:
            count += 1
            found_hit = True
            value = line.split(hit_phrase, 1)[1].strip()
            values.append(value)
        match = sigterm_pattern.search(line)
        if match:
            unix_timestamp = int(match.group(1))
            date = datetime.utcfromtimestamp(unix_timestamp)
            if found_hit:
                decoded_dates.append(date.strftime('%Y-%m-%d %H:%M:%S UTC'))
            found_hit = False
            last_decoded_date = date.strftime('%Y-%m-%d %H:%M:%S UTC')

    return count, decoded_dates, values, last_decoded_date


def extract_target_file_contents(tar_file_path, target_file_name):
    with tarfile.open(tar_file_path, 'r:gz') as tar:
        for member in tar.getmembers():
            if member.name.endswith(target_file_name):
                with tar.extractfile(member) as target_file:
                    return target_file.read().decode('utf-8')


def detect_sys_diagnose(tar_file_path):
    response_message = {}
    response_message["green"] = []
    response_message["red"] = []
    response_message["yellow"] = []
    response_message["black"] = []
    target_file_name = "shutdown.log"

    if os.path.isfile(tar_file_path):
        target_file_contents = extract_target_file_contents(
            tar_file_path, target_file_name
        )
        if target_file_contents:
            occurrences = count_occurrences(target_file_contents, "SIGTERM")
            response_message["green"].append(f"Detected {occurrences} reboot(s). Good practice to follow.")

            # Find delay anomalies before SIGTERM reboot
            anomaly_phrase = "these clients are still here"
            anomalies_timestamps = find_anomalies_before_sigterm(target_file_contents, anomaly_phrase)

            if anomalies_timestamps:
                response_message["red"].append(
                    f"Detected {len(anomalies_timestamps)} reboot(s) with 3 or more delays before a reboot.")
                response_message["yellow"].append(
                    timestamp.strftime('%Y-%m-%d %H:%M:%S UTC') for timestamp in anomalies_timestamps)
            else:
                response_message["green"].append("No anomalies detected with the specified conditions.")

            # Find entries in common malware path
            # List of paths to check
            paths_to_check = ["/private/var/db/", "/private/var/tmp/"]

            # Loop through each path and process hits
            for path in paths_to_check:
                hit_count, decoded_dates, values, last_decoded_date = process_hits(target_file_contents, path)

                if hit_count > 0:
                    response_message['red'].append(
                        f"Suspicious processes in '{path}' occurred {hit_count} time(s). Further investigation needed!")
                    response_message['red'].append("The suspicious processes are:\n" + '\n'.join(values))
                    response_message['yellow'].append("Detected during reboot(s) on:\n" + '\n'.join(decoded_dates))
                elif last_decoded_date:
                    response_message['green'].append(
                        f"No suspicious processes detected in '{path}'. Last reboot was on: {last_decoded_date}")

            return response_message
        else:
            response_message["black"].append(f"Target file '{target_file_name}' not found in the archive.")
            return ""
    else:
        return ""
