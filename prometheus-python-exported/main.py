import psutil


def get_cpu_percentage():
    """
    return a CPU usage in percentage
    """
    return psutil.cpu_percent()

def get_load_avg():
    """
    returns a tuple of load average for 1m, 5m and 15m
    """
    return psutil.getloadavg()

def get_memory_info():
    """
    return information about the memory - named tuple
    https://psutil.readthedocs.io/stable/#system-related-functions
    """
    return psutil.virtual_memory()

def disk_usage_info(mountpoint):
    """
    returns named tuple including total, used and free space (in bytes) and the percentage usage
    """
    return psutil.disk_usage(mountpoint)


if __name__ == "__main__":
    # initial check - create baseline
    psutil.cpu_percent()

    load = get_load_avg()
    load_1m = load[0]
    load_5m = load[1]
    load_15m = load[2]

    memory = get_memory_info()
    memory_percentage = memory.percent

    root_partition = disk_usage_info('/')
    root_percentage = root_partition.percent
