# get specs of this computer
import os
import platform
import subprocess
import sys
import time
import uuid
import psutil
import cpuinfo
import wmi
import datetime
import win32api

def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# get specs of this computer
def get_specs():
    specs = {}

    data = wmi.WMI().Win32_ComputerSystem()[0]

    # get hostname
    specs['manufacturer'] = data.Manufacturer
    specs['hostname'] = data.Name
    specs['model'] = data.Model

    bt = datetime.datetime.fromtimestamp(psutil.boot_time())
    specs['boot_time'] = bt.strftime("%Y-%m-%d %H:%M:%S")

    specs['os'] = platform.system()
    specs['os_release'] = platform.release()
    specs['os_version'] = platform.version()
    specs['os_machine'] = platform.machine()

    # get cpu name using cpuinfo
    specs['cpu'] = cpuinfo.get_cpu_info()

    # get gpu info
    c = wmi.WMI()
    specs['gpu'] = []
    specs['gpu_driver'] = []
    specs['gpu_model'] = []
    specs['gpu_vendor'] = []
    specs['gpu_ram'] = []
    for gpu in c.Win32_VideoController():
        specs['gpu'].append(gpu.Name)
        specs['gpu_driver'].append(gpu.DriverVersion)
        specs['gpu_model'].append(gpu.AdapterRAM)
        specs['gpu_vendor'].append(gpu.AdapterCompatibility)
        specs['gpu_ram'].append(gpu.AdapterRAM)

    # get ram from psutil
    specs['ram'] = {}
    specs['ram']['total'] = str(get_size(psutil.virtual_memory().total, "B"))
    specs['ram']['available'] = str(get_size(psutil.virtual_memory().available, "B"))
    specs['ram']['available_bytes'] = str(psutil.virtual_memory().available)
    specs['ram']['used'] = str(get_size(psutil.virtual_memory().used, "B"))
    specs['ram']['used_bytes'] = str(psutil.virtual_memory().used)
    specs['ram']['percent'] = str(psutil.virtual_memory().percent)
    specs['ram']['swap'] = str(get_size(psutil.swap_memory().used, "B"))
    specs['ram']['swap_bytes'] = str(psutil.swap_memory().used)
    specs['ram']['swap_free'] = str(get_size(psutil.swap_memory().free, "B"))
    specs['ram']['swap_free_bytes'] = str(psutil.swap_memory().free)
    specs['ram']['swap_total'] = str(get_size(psutil.swap_memory().total, "B"))
    specs['ram']['swap_percent'] = str(psutil.swap_memory().percent)

    # get disk from psutil
    specs['disk'] = {}
    drives = win32api.GetLogicalDriveStrings()
    drives = drives.split('\000')[:-1]
    for x in drives:
        x = x.replace('\\\\', '\\')
        try:
            specs['disk'][x] = {}
            specs['disk'][x]['total'] = str(psutil.disk_usage(x + '/').total)
            specs['disk'][x]['total_formated'] = str(get_size(psutil.disk_usage(x + '/').total, "B"))
            specs['disk'][x]['used'] = str(psutil.disk_usage(x + '/').used)
            specs['disk'][x]['used_formated'] = str(get_size(psutil.disk_usage(x + '/').used, "B"))
            specs['disk'][x]['free'] = str(psutil.disk_usage(x + '/').free)
            specs['disk'][x]['free_formated'] = str(get_size(psutil.disk_usage(x + '/').free, "B"))
            specs['disk'][x]['percent'] = str(psutil.disk_usage(x + '/').percent)
        except Exception as e:
            drives.remove(x)
    specs['disk']['drives'] = drives

    return specs

def get_uuid():
    try:
        return str(uuid.uuid4())
    except:
        return 'unknown'