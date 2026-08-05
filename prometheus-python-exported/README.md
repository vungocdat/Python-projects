# Python exporter for prometheus

Script gather resource information and expose it on port 9100 for prometheus / open telemetry

the flow

```
Program starts

↓

Create exporter
    ConsoleMetricExporter()

↓

Create reader
    "Run every 60 seconds"

↓

Create provider
    "Own all metrics"

↓

Register provider

↓

Create meter

↓

Register CPU gauge
    "When someone wants CPU,
     call cpu_callback"

↓

60 seconds pass

↓

Reader wakes up

↓

Reader asks gauge

↓

Gauge calls

cpu_callback(options)

↓

get_cpu_percentage()

↓

Observation(27.5)

↓

ConsoleMetricExporter prints it
```
