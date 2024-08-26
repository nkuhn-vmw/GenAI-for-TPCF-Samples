# Container metrics
Here you can learn about the metrics that are emitted by all containers managed by Cloud Foundry (Cloud Foundry) and its scheduling
system, Diego.
Application metrics include the container metrics, and any custom application metrics that developers create.

## Diego container metrics
Diego containers emit resource usage metrics for the application instance. Diego averages and emits each metric every 15 seconds.
The following table describes all Diego container metrics:
| Metric | Description | Unit |
| --- | --- | --- |
| `cpu` | CPU time used by an app instance as a percentage of a single CPU core.
This is usually no greater than `100% * the number of vCPUs on the host Diego cell`, but it might be more due to discrepancies in measurement timing. | `float64` |
| `cpu_entitlement` | CPU time used by an app instance as a percentage of its CPU entitlement.
At minimum, the CPU time that a Diego Cell allocates to an app instance is
`min(app memory, 8 GB) * (Diego cell vCPUs/Diego cell memory) * 100%`. The operator of your Cloud Foundry deployment can
provide the `vCPUs/memory` ratio of the Diego Cell to developers.
If a Diego Cell is not already working at capacity, or if other workloads on the Diego Cell are idle, the Diego Cell can allocate more than the minimum
amount of CPU time to an app instance. | `float64` |
| `memory` | The amount of RAM memory in bytes that an app instance has used. | `uint64` |
| `memory_quota` | The amount of RAM memory in bytes that is available for an app instance to use. | `float64` |
| `disk` | The amount of disk space in bytes that an app instance has used. | `float64` |
| `disk_quota` | The amount of disk space in bytes that is available for an app instance to use. | `float64` |
| `container_age` | The age in nanoseconds of the Diego container. | `float64` |
| `log_rate` | The current log rate in bytes per second for an app instance. | `float64` |
| `log_rate_limit` | The log rate limit in bytes per second for an app instance. | `float64` |
| `rx_bytes` | Received network traffic in bytes for an app instance. | `uint64` |
| `tx_bytes` | Transmitted network traffic in bytes for an app instance. | `uint64` |
The operator of your Cloud Foundry deployment can [enable it to emit](https://bosh.io/jobs/rep?source=github.com/cloudfoundry/diego-release&version=2.93.0#p%3dloggregator.app_metric_exclusion_filter) the following additional, deprecated container metrics:
| Metric | Description | Unit |
| --- | --- | --- |
| `absolute_entitlement` | The amount of CPU time that a Diego Cell has allocated to an app instance, in nanoseconds.
At minimum, the CPU time that a Diego Cell allocates to an app instance is
`min(app memory, 8 GB) * (Diego cell vCPUs/Diego cell memory) * 100%`. The operator of your Cloud Foundry deployment can
provide the `vCPUs/memory` ratio of the Diego Cell to developers.
If a Diego Cell is not already working at capacity, or if other workloads on the Diego Cell are idle, the Diego Cell can allocate more than the minimum
amount of CPU time to an app instance. | `float64` |
| `absolute_usage` | The CPU time that an app instance has used, in nanoseconds.
`absolute_usage / absolute_entitlement` calculates a percentage of app instance usage per entitlement. | `float64` |
|
The way that Diego emits container metrics differs depending on the version of Loggregator used in your Cloud Foundry deployment:

* **Loggregator v1:** Diego emits most container metrics in a `ContainerMetric` envelope. Diego emits the `cpu_entitlement`,
`container_age`, `log_rate`, and `log_rate_limit` container metrics in `ValueMetric` envelopes.

* **Loggregator v2:** Diego emits all container metrics in gauge and counter envelopes. Diego emits the `cpu_entitlement`, `container_age`, `log_rate`, and `log_rate_limit` container metrics in separate gauge envelopes from other container metrics. The container metrics come in five envelopes:

+ One envelope containing `cpu`, `disk`, `disk_quota`, `memory`, and `memory_quota`

+ One envelope containing `cpu_entitlement`, and `container_age`

+ One envelope containing `log_rate` and `log_rate_limit`

+ One envelope containing `rx_bytes`

+ One envelope containing `tx_bytes`

## Retrieving container metrics from the cf CLI
You can retrieve container metrics using the Cloud Foundry Command Line Interface (cf CLI).

* To retrieve CPU, memory, and disk metrics for all instances of an application, see [Retrieve CPU, memory, and disk metrics](https://docs.cloudfoundry.org/loggregator/container-metrics.html#cpu-mem-disk).

* To retrieve network traffic metrics for all instances of an app, see [Retrieve network traffic metrics](https://docs.cloudfoundry.org/loggregator/container-metrics.html#cf-network-traffic).

### Retrieving CPU, Memory, and Disk metrics
To retrieve CPU, memory, and disk metrics for all instances of an application:

1. In a terminal window, run:
```
cf app APP-NAME
```
Where `APP-NAME` is the name of the app.
This command returns CPU, memory, and disk metrics for all instances of the app, similar to the following example:
```
Showing health and status for app dora-example in org o / space s as admin...
```
| Label in output | Metrics listed |
| --- | --- |
| `cpu` | `CpuPercentage` |
| `memory` | `MemoryBytes` of `MemoryBytesQuota` |
| `disk` | `DiskBytes` of `DiskBytesQuota` |
The listed metrics are described in [Diego container metrics](https://docs.cloudfoundry.org/loggregator/container-metrics.html#container-metrics).
```
type: web
sidecars:
instances: 1/1
memory usage: 1024M
state since cpu memory disk logging details

#0 running 2022-09-16T01:38:46Z 0.2% 36.3M of 1G 90.3M of 1G 0/s of unlimited
```
The preceding command shows what percentage of CPU the app is currently using relative to the total CPU on the host
machine.

### Retrieve network traffic metrics
To retrieve received- and transmitted bytes for all instances of an app:

1. Install the Log Cache CLI Plug-in from the [Log Cache cf CLI Plugin](https://github.com/cloudfoundry/log-cache-cli) repository on GitHub.

2. In a terminal window, run:
```
cf tail --name-filter="bytes" APP-NAME
```
Where `APP-NAME` is the name of the app.
This command returns `rx_bytes` and `tx_bytes` metrics for all instances of the app, similar to the following example:
```
2023-08-10T13:27:50.27+0000 [my-app/0] COUNTER rx_bytes:24842
2023-08-10T13:27:50.27+0000 [my-app/0] COUNTER tx_bytes:24306
2023-08-10T13:27:50.27+0000 [my-app/1] COUNTER rx_bytes:14832
2023-08-10T13:27:50.27+0000 [my-app/1] COUNTER tx_bytes:32312
```