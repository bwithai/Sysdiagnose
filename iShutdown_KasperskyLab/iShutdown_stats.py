# © 2023 AO Kaspersky Lab. All Rights Reserved.
# Creates reboot statistics from Shutdown.log forensic artifact

import re
import collections
import argparse
from datetime import datetime


def get_log_stats(logfile):
    # Initialize counters and storage
    sigterm_count = 0
    first_sigterm_time = None
    last_sigterm_time = None
    sigterm_per_month = collections.defaultdict(int)

    # Process the log file
    with open(logfile, 'r') as file:
        for line in file:
            match = re.search(r'SIGTERM: \[(\d+)\]', line)
            if match:
                sigterm_count += 1
                timestamp = int(match.group(1))
                timestamp = datetime.fromtimestamp(timestamp)

                if first_sigterm_time is None or timestamp < first_sigterm_time:
                    first_sigterm_time = timestamp
                if last_sigterm_time is None or timestamp > last_sigterm_time:
                    last_sigterm_time = timestamp

                month_key = '{year}-{month:02}'.format(
                    year=timestamp.year, month=timestamp.month
                )
                sigterm_per_month[month_key] += 1

    # Output the results
    result = {}
    result['reboots_summary'] = []
    result['reboots_per_month'] = []

    result['reboots_summary'].append(f"Number of reboots in the log: {sigterm_count}")
    if first_sigterm_time:
        result['reboots_summary'].append(f"First reboot detected in the log: {first_sigterm_time}")
    if last_sigterm_time:
        result['reboots_summary'].append(f"Last reboot detected in the log: {last_sigterm_time}")
    print("Reboots counts per month:")

    for month, count in sorted(sigterm_per_month.items()):
        result['reboots_per_month'].append(f"{month}: {count}")

    return result
