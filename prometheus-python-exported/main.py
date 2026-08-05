import psutil
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import ConsoleMetricExporter, PeriodicExportingMetricReader
import time

# ===

# psutil metric functions

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

# initial check - create baseline
psutil.cpu_percent()

# ===

# OTEL setup

# object that knows how to export
exporter = ConsoleMetricExporter()

# every 60s collect metric and send it to exporter called "exporter"
# readoer does not know how to print. Exporter does
# it is a timer to trigger the exporter
reader = PeriodicExportingMetricReader(exporter, export_interval_millis=60000)

# object that own all metric - know "reader" and even "exporter"
provider = MeterProvider(metric_readers=[reader])

# register the provider above (globally)
# before: OTEL -> nothing
# now: OTEL -> provider
metrics.set_meter_provider(provider)

# create something a like direcotry that contains the metrics
meter = metrics.get_meter('os_stats_collector')

# ===

# callbacks wrapper: matches the shape OTel requires
def cpu_callback(options):
    yield metrics.Observation(get_cpu_percentage())

# ===

# the shape of the metric (meter is a varaible created above)

meter.create_observable_gauge(
    name = 'system.cpu.usage',
    callbacks = [cpu_callback],
    description = 'current cpu usage in %',
    unit = '%'
)


if __name__ == "__main__":
    # infinite loop to keep the script alive
    while True:
        time.sleep(3600)
