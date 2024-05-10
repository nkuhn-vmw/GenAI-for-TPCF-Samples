# UAA performance metrics
Cloud Foundry User Accounts and Authentication (UAA) emits metrics constantly. These metrics help you to understand performance, troubleshoot problems, and assess the health of your installation in real time. These metrics are emitted through Loggregator.
This topic describes various metrics that UAA, virtual machines (VMs), and Java Virtual Machines (JVMs) emit.

## About UAA performance
The following tables explain different types of UAA and UAA-related metrics you can view. There are three different types of metrics discussed in these tables:

* [Global performance metrics](https://docs.cloudfoundry.org/uaa/uaa-metrics.html#global): Metric values that UAA emits

* [Virtual Machine vital statistics](https://docs.cloudfoundry.org/uaa/uaa-metrics.html#vm-vitals): Metric values that UAA reads from the VM

* [Java Virtual Machine vital statistics](https://docs.cloudfoundry.org/uaa/uaa-metrics.html#jvm-vitals): Metric values that UAA reads from the JVM
Each table contains:

* **Name:** The name of the metric.

* **Type:** How the metric is displayed. For example, counters, gauges, or timers.

* **Description:** An explanation of what values this metric displays.

* **Example:** A code sample of this metric’s output.

* **Indicator:** What changes in the metric’s value may indicate over time.

* **Status**: Whether a metric is active or static. Active metrics may change between metrics emissions. Static metrics are fixed and do not change.
If consuming UAA metrics through the Firehose, incremental metrics, or metrics that capture an
increment or decrement in a value because UAA’s last emission, are expressed as cumulative values.
For more information, see the [statsd-injector](https://github.com/cloudfoundry/statsd-injector) repository on GitHub.

### Global performance metrics
The following table describes metrics that UAA emits:
| Name | Type | Description | Example | Indicator | Status |
| --- | --- | --- | --- | --- | --- |
| `requests.global.completed.count` | Counter | Number of HTTP requests the server has processed since last metric emission. This metric includes all requests sent to the server, including health checks. | `uaa.requests.global.completed.count:1|c` | Use this metric to calculate request load and throughput. | Active |
| `requests.global.completed.time` | Gauge | Average time in milliseconds spent per HTTP request. This metric is calculated as an average across all completed requests, including health checks. | `uaa.requests.global.completed.time:60|g` | A rise may indicate problems with server or database. | Active |
| `server.inflight.count` | Gauge | Number of requests the server is currently processing, also called in-flight requests. | `uaa.server.inflight.count:1|g` | If this number climbs continuously, it can indicate that servers are getting saturated and are unable to handle the incoming load. | Active |
| `requests.global.unhealthy.count` | Counter in UAA v4.8 and earlier; gauge in UAA v4.9.0 and later | Number of completed requests that exceeded the tolerable response time since last metric emission. Each URL group can have a different tolerable completion time, which is preconfigured in each UAA release. These values are currently not configurable. | `uaa.requests.global.unhealthy.count:1|c` | If the number of requests not meeting tolerable completion time is growing, than either the tolerable request time must be configured to account for false negatives, or the server does not have enough capacity to handle the request load. The cause for this can be a need for an increase in server or database resources. In order to make a scaling decision, you need further metrics. | Active |
| `requests.global.unhealthy.time` | Gauge | Average time in milliseconds per completed HTTP request that did not finish within the set tolerable time since startup. | `uaa.requests.global.unhealthy.time:250|g` | It can be useful to compare this metric to `uaa.requests.global.completed.time`. | Active |
| `requests.global.status_4xx.count` | Counter | Number of HTTP requests that have returned `400` codes, or client errors, since UAA’s last metrics emission. These do not indicate server errors. A `400` code may indicate an invalid request to the server. | `uaa.requests.global.status_4xx.count:1|c` | This metric gives the client the ability to calculate error rates. It is often used to detect faulty apps that may be causing unnecessary processing on the server. | Active |
| `requests.global.status_5xx.count` | Counter | Number of HTTP requests that have returned `500` codes, or server errors, since UAA’s last metrics emission. | `uaa.requests.global.status_5xx.count:1|c` | This metric gives the client the ability calculate error rates and determine if further investigation is needed. | Active |
| `server.up.time` | Timer | Number of milliseconds that have elapsed since this server instance started. | `uaa.server.up.time:42346751|g` | This metric indicates the time since last startup. | Active |
| `server.idle.time` | Timer | Number of milliseconds that the server has spent in an idle state, when no requests were being processed. This allows a client to calculate the amount of actual, rather than cumulative, time the server has spent processing requests with `up.time-idle.time`. | `uaa.server.idle.time:2346751|g` | This metric allows the client to calculate when the server is receiving load time. | Active |
| `database.global.completed.count` | Counter | Number of database queries the server has processed since UAA’s last metrics emission. | `uaa.database.global.completed.count:1|c` | Use this metric to track the number of queries that have reached and been processed by the server over a period of time. | Active |
| `database.global.completed.time` | Gauge | Average amount of time in milliseconds per database query. | `uaa.database.global.completed.time:248|g` | Use this metric to track the time to complete a database query on average. | Active |
| `database.global.unhealthy.count` | Counter | Number of database queries that failed or did not meet the tolerated response time since UAA’s last metrics emission. The response time is not configurable during runtime. By default, it is set to three seconds. | `uaa.database.global.unhealthy.count:1|c` | Use this metric to monitor database query success and failure over time. | Active |
| `database.global.unhealthy.time` | Timer | Average amount of time in milliseconds per database query that was not within the tolerated response time. | `uaa.database.global.unhealthy.time:4678623|g` | Use this metric to monitor database response time. | Active |

## About UAA vital statistics
These sections describe metrics that the UAA VM and JVM emit.

### Virtual Machine vital statistics
The following table describes metrics that the UAA VM emits:
| Name | Type | Description | Example | Indicator | Status |
| --- | --- | --- | --- | --- | --- |
| `vitals.vm.cpu.count` | Gauge | How many CPUs are on this VM as reported by the JVM. This metric is useful when you want to read system load average. The number reported by load average must be correlated to the number of CPUs. | `uaa.vitals.vm.cpu.count:4|g` | This metric is required for a proper CPU load calculation. | Active |
| `vitals.vm.cpu.load` | Gauge | Average system CPU load as reported by the JVM. The value is reported as a whole number multiplied by .01. For example, a value of 163 is read as 1.63. | `uaa.vitals.vm.cpu.load:50|g` | If the value of `(cpu.load / 100.0 / cpu count) is more than 2.0, this indicates that the system may be overloaded and processing data slowly. | Active |
| `vitals.vm.memory.total` | Gauge | Total OS memory, in bytes, as reported by the JVM. | `uaa.vitals.vm.memory.total:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |
| `vitals.vm.memory.committed` | Gauge | OS memory, in bytes, committed to UAA processes, as reported by the JVM. | `uaa.vitals.vm.memory.committed:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |
| `vitals.vm.memory.free` | Gauge | Free OS memory, in bytes, as reported by the JVM. | `uaa.vitals.vm.memory.free:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |

### Java Virtual Machine vital statistics
The following table describes metrics that the UAA JVM emits:
| Name | Type | Description | Example | Indicator | Status |
| --- | --- | --- | --- | --- | --- |
| `vitals.jvm.cpu.load` | Gauge | UAA process CPU load average as reported by the JVM. This value is multiplied by 100 and reported as a whole number representing the CPU load on the VM incurred by the UAA process, excluding any other processes on the VM. | `uaa.vitals.jvm.cpu.load:25|g` | Health and scaling. If CPU load is showing as high, this metric can be used to confirm that it is indeed the UAA using up the CPU and not other jobs on the same VM. | Active |
| `vitals.jvm.thread.count` | Gauge | Number of threads running inside the UAA process, as reported by the JVM. | `uaa.vitals.jvm.thread.count:53|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |
| `vitals.jvm.heap.init` | Gauge | Minimum amount of OS memory, in bytes, requested by the UAA JVM process to be used as part of the Java heap memory, as reported by the JVM. | `uaa.vitals.jvm.heap.init:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Static |
| `vitals.jvm.heap.committed` | Gauge | Guaranteed amount of Java heap memory, in bytes, committed to the UAA JVM process, as reported by the JVM. | `uaa.vitals.jvm.heap.committed:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |
| `vitals.jvm.heap.used` | Gauge | Java heap memory, in bytes, currently in use by the UAA process as reported by the JVM. | `uaa.vitals.jvm.heap.used:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Static |
| `vitals.jvm.heap.max` | Gauge | Java heap memory, in bytes, that is the upper limit for the UAA processes, as reported by the JVM. | `uaa.vitals.jvm.heap.max:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Static |
| `vitals.jvm.non-heap.init` | Gauge | Minimum non-Java memory, in bytes, acquired by the UAA process, as reported by the JVM. | `uaa.vitals.jvm.non-heap.init:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |
| `vitals.jvm.non-heap.committed` | Gauge | Guaranteed non-Java memory, in bytes, committed by the UAA process, as reported by the JVM. | `uaa.vitals.jvm.non-heap.committed:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |
| `vitals.jvm.non-heap.used` | Gauge | Current non-Java memory, in bytes, that the UAA process can use, as reported by the JVM. | `uaa.vitals.jvm.non-heap.used:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |
| `vitals.jvm.non-heap.max` | Gauge | Upper limit of non-Java memory, in bytes, that the UAA process can use, as reported by the JVM. | `uaa.vitals.jvm.non-heap.max:1073741824|g` | Use this metric in conjunction with other performance metrics to assess system health. | Active |
For more information about JVM memory, see the [Oracle documentation](https://docs.oracle.com/javase/8/docs/api/index.html?java/lang/management/MemoryUsage.html).