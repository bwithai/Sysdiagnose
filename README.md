# What is Sysdiagnose?
Sysdiagnose is a utility on most Apple devices that can be used to gather system-wide diagnostic
information. It includes logging from different services and reports on the state of systems. What
is contained in a sysdiagnose will vary depending on what type of device and which version of the
macOS, iOS, iPadOS, tvOS, watchOS and visionOS.

[How to Trigger a Sysdiagnose Manually](https://hcsonline.com/images/PDFs/Sysdiagnose.pdf)

###### This is the backend server of  [KasperskyLab](https://github.com/KasperskyLab/iShutdown)

## Prerequisites

The scripts relies on the following Python dependencies respectively:
- Server
    >fastapi==0.110.0 
  > 
    >uvicorn==0.27.1
  > 
  >python-multipart==0.0.9
- Sysdiagnose Detection
    >datetime, os, re, sys, tarfile
- Parse shutdown logs
    >argparse, csv, datetime, hashlib, os, re, shutil, tarfile
- Stats
  >argparse, collections, datetime, re 


## Installation
```bash
git clone https://github.com/bwithai/Sysdiagnose.git
cd Sysdiagnose
# create your python virtual environment variable (venv)
pip install -r requirements.txt
uvicorn main:app
```
## Usage
we have three endpoints:
> upload_file
  - Upload your sysdiagnose_2024.03.01_13-30-50+0400_iPhone-OS_iPhone_00H000.tar.gz file
  - [How to Trigger a Sysdiagnose Manually](https://hcsonline.com/images/PDFs/Sysdiagnose.pdf)
> log-parsing
  - Analysts and users want to share their log files and parse them for different purposes.
> log-stats
  - Understanding how often or when a user has rebooted the phone.


## What do you get?

Among the tools which have been run, and whose output has been collected for you may consist of
the following:
- **ps** which lists information about all processes running at present, and its thread-aware variant
- **fs_usage** which reports system calls and page faults related to filesystem activity
- **spindump** which profiles your entire system for a period of time
- **vm_stat** which shows Mach virtual memory statistics
- **top** which displays sorted information about all processes running at present
- **powermetrics** which shows CPU usage statistics
- **lsof** which lists details of all open files
- **footprint** which gives memory information about processes
- **vmmap** and heap on process(es) using large amounts of memory, showing their virtual
memory and heap allocations
- **diskutil** checking mounted drives
- **gpt** detailing GUID partition tables
- **hdiutil** checking mounted disk images
- **BootCacheControl** checking caches used during startup
- **df** checking disk free space
- **mount** checking mounted file systems
- **netstat** giving detailed network status
- **ifconfig** detailing network interfaces
- **ipconfig** detailing IP configuration
- **scutil** checking system configuration
- **dig** checking name service (DNS) lookup
- **pmset** detailing power management settings
- **system_profiler** which compiles a full system profile just as the System Profiler app does
- **ioreg** gives details of all input and output devices registered with I/O Kit.

Decompressed, its reports will typically occupy over 200 MB with more than 1500 files and folders.