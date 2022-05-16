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
        specs['gpu_model'].append(gpu.VideoProcessor)
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

    # get network from psutil
    specs['network'] = {}
    specs['network']['interfaces'] = []
    for x in psutil.net_if_addrs().keys():
        specs['network']['interfaces'].append(x)
        specs['network'][x] = {}
        specs['network'][x]['ip'] = psutil.net_if_addrs()[x][0].address
        specs['network'][x]['netmask'] = psutil.net_if_addrs()[x][0].netmask
        specs['network'][x]['broadcast'] = psutil.net_if_addrs()[x][0].broadcast
        specs['network'][x]['mac'] = psutil.net_if_addrs()[x][1].address
        specs['network'][x]['up'] = psutil.net_if_stats()[x].isup
        specs['network'][x]['speed'] = str(psutil.net_if_stats()[x].speed)
        specs['network'][x]['bytes_sent'] = str(psutil.net_io_counters(pernic=True)[x].bytes_sent)
        specs['network'][x]['bytes_send_formatted'] = str(get_size(psutil.net_io_counters(pernic=True)[x].bytes_sent, "B"))
        specs['network'][x]['bytes_recv'] = str(psutil.net_io_counters(pernic=True)[x].bytes_recv)
        specs['network'][x]['bytes_recv_formatted'] = str(get_size(psutil.net_io_counters(pernic=True)[x].bytes_recv, "B"))
        specs['network'][x]['packets_sent'] = str(psutil.net_io_counters(pernic=True)[x].packets_sent)
        specs['network'][x]['packets_recv'] = str(psutil.net_io_counters(pernic=True)[x].packets_recv)
        specs['network'][x]['errin'] = str(psutil.net_io_counters(pernic=True)[x].errin)
        specs['network'][x]['errout'] = str(psutil.net_io_counters(pernic=True)[x].errout)
        specs['network'][x]['dropin'] = str(psutil.net_io_counters(pernic=True)[x].dropin)
        specs['network'][x]['dropout'] = str(psutil.net_io_counters(pernic=True)[x].dropout)
    specs['network']['bytes_sent'] = str(psutil.net_io_counters().bytes_sent)
    specs['network']['bytes_send_formatted'] = str(get_size(psutil.net_io_counters().bytes_sent, "B"))
    specs['network']['bytes_recv'] = str(psutil.net_io_counters().bytes_recv)
    specs['network']['bytes_recv_formatted'] = str(get_size(psutil.net_io_counters().bytes_recv, "B"))
    specs['network']['packets_sent'] = str(psutil.net_io_counters().packets_sent)
    specs['network']['packets_recv'] = str(psutil.net_io_counters().packets_recv)
    specs['network']['errin'] = str(psutil.net_io_counters().errin)
    specs['network']['errout'] = str(psutil.net_io_counters().errout)
    specs['network']['dropin'] = str(psutil.net_io_counters().dropin)
    specs['network']['dropout'] = str(psutil.net_io_counters().dropout)

    # get load from psutil
    specs['load'] = {}
    specs['load']['1min'] = str(psutil.getloadavg()[0])
    specs['load']['5min'] = str(psutil.getloadavg()[1])
    specs['load']['15min'] = str(psutil.getloadavg()[2])

    # get all processes from psutil
    specs['processes'] = {}
    specs['processes']['total'] = str(len(psutil.pids()))
    # get all running processes from psutil

    temprunning = []
    tempsleeping = []
    tempstopped = []
    tempzombie = []
    tempall = []

    for x in psutil.pids():
        try:
            a = psutil.Process(x)
            if a.status() == 'running':
                temprunning.append(a)
            elif a.status() == 'sleeping':
                tempsleeping.append(a)
            elif a.status() == 'stopped':
                tempstopped.append(a)
            elif a.status() == 'zombie':
                tempzombie.append(a)
            tempall.append(a)
        except psutil.NoSuchProcess:
            pass

    specs['processes']['running'] = str(len(temprunning))
    specs['processes']['sleeping'] = str(len(tempsleeping))
    specs['processes']['stopped'] = str(len(tempstopped))
    specs['processes']['zombie'] = str(len(tempzombie))
    specs['processes']['total'] = str(len(tempall))

    return specs

def get_uuid():
    try:
        return str(uuid.uuid4())
    except:
        return 'unknown'