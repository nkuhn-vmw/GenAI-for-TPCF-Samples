# Logging and metrics in Cloud Foundry
You can use logging and metrics in Cloud Foundry
(Cloud Foundry). Learn about logs and metrics sources, and
transport systems. It also lists products for viewing logs and metrics.

## Accessing metrics
You must use a Cloud Foundry Command-Line Interface (cf CLI) plug-in to access and view metrics
directly from the command line. You can use either the Firehose plug-in or the Log Cache plug-in.

### Accessing metrics using the Log Cache CLI plug-in
To access metrics with the Log Cache plug-in:

1. Log in to the cf CLI by running:
```
cf login -a API-URL -u USERNAME -p PASSWORD
```
Where:

* `API-URL` is your API endpoint.

* `USERNAME` is your username.

* `PASSWORD` is your password.

2. Install the Log Cache CLI plug-in by running:
```
cf install-plug-in -r CF-Community "log-cache"
```
For more information, see [log-cache](https://plugins.cloudfoundry.org/#log-cache) in *cf
CLI plug-ins* on the Cloud Foundry website.

3. Run:
```
cf query 'METRIC-NAME{source_id="SOURCE-ID"}'
```
Where:

* `METRIC-NAME` is the name of the metric you want to view.

* `SOURCE-ID` is the source ID of the component for which you want to view metrics.
To find the source ID and metric name of the metric you want to view, see [CF Component Metrics](https://docs.cloudfoundry.org/running/all_metrics.html) and [UAA Performance Metrics](https://docs.cloudfoundry.org/uaa/uaa-metrics.html).

### Accessing metrics using the Firehose plug-in
To access metrics using the Firehose plug-in:

1. Log in to the cf CLI by running:
```
cf login -a API-URL -u USERNAME -p PASSWORD
```
Where:

* `API-URL` is your API endpoint.

* `USERNAME` is your username.

* `PASSWORD` is your password.

2. Install the Firehose cf CLI plug-in by running:
```
cf install-plugin -r CF-Community "Firehose Plugin"
```
For more information, see [Firehose plug-ins](https://plugins.cloudfoundry.org/#Firehose%20Plugin)
in *cf CLI Plug-ins* on the Cloud Foundry website.

3. Run:
```
cf nozzle -no-filter | grep SOURCE-ID | grep -i METRIC-NAME
```
Where:

* `METRIC-NAME` is the name of the metric you want to view.

* `SOURCE-ID` is the source ID of the component for which you want to view metrics.
For example:
```
cf nozzle -no-filter | grep bbs | grep -i ConvergenceLRPDuration
```
Because metrics are scraped at different intervals, it might take up to fifteen minutes for
the Firehose to receive all metrics for the component. Run `cf nozzle` again until you have
received a complete set of metrics for a component. For more information, see [Firehose
Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html#firehose-architecture) in *Loggregator Architecture*.
To find the source ID and metric name of the metric you want to view, see [CF Component Metrics](https://docs.cloudfoundry.org/running/all_metrics.html) and [UAA Performance Metrics](https://docs.cloudfoundry.org/uaa/uaa-metrics.html).
For more information about nozzles, see [Scaling Nozzles](https://docs.cloudfoundry.org/loggregator/log-ops-guide.html#scaling-nozzles) in *Loggregator Guide for CF Operators*..

## Sources for logs and metrics
The following sources are for Cloud Foundry logs and metrics:

* Cloud Foundry platform components, such as a Diego Cell, MySQL Server, or
Cloud Controller

* Apps and app containers deployed on Cloud Foundry
The following table describes the data included in logs and metrics from each source:
| Source | Logs data | Metrics data |
| --- | --- | --- |
| Platform components | Logs from Cloud Foundry components | * Health metrics from BOSH-deployed VMs1

* Platform metrics from Cloud Foundry components. For example, Diego
Cell capacity remaining and Gorouter throughput.

* Metrics for any service tile that self-publishes to the Loggregator Firehose. For
example, Redis and MySQL.
|
| Apps and app containers | Logs from apps2 | * Container metrics3
|
1For more information about using the BOSH Health Monitor to collect health metrics
on VMs, see [Selecting and configuring a monitoring system](https://docs.vmware.com/en/VMware-Tanzu-Application-Service/4-0/tas-for-vms/monitoring-metrics.html).
2For more information about app logging, see [App Logging in TAS for VMs](https://docs.vmware.com/en/VMware-Tanzu-Application-Service/4-0/tas-for-vms/deploy-apps-streaming-logs.html).
3For more information about container metrics, see [Container Metrics](https://docs.cloudfoundry.org/loggregator/container-metrics.html).

## Transport Systems for logs and metrics
The following transport systems deliver logs and metrics from their source to an observability
product for viewing:

* **Loggregator:** Loggregator is the transport system for both logs and metrics on apps deployed
on Cloud Foundry, as well as metrics on Cloud Foundry platform
components.
For more information about the Loggregator system, including Loggregator architecture
and components, see [Loggregator Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html) and for the types
of envelopes being transported in Loggregator, see [Envelope Types](https://github.com/cloudfoundry/loggregator-api#v2-envelope-types).

* **rsyslogd on Cloud Foundry component VMs:** rsyslogd is the transport system
for Cloud Foundry component logs. Users can configure rsyslogd to transport
component logs to a third-party syslog server.
The following table lists the transport system for logs and metrics on Cloud Foundry
platform components and apps:
| Source | Logs transport system | Metrics transport system |
| --- | --- | --- |
| Platform components | rsyslogd on Cloud Foundry component VMs | Loggregator |
| Apps | Loggregator | Loggregator |

## Viewing logs and metrics
The following table lists the products and tools for viewing Cloud Foundry logs
and metrics:
| Source | Products and tools for viewing logs | Products and tools for viewing metrics |
| --- | --- | --- |
| Platform components | To view system logs from Cloud Foundry components, configure
rsyslogd to transport logs to a third-party product. |
You can use the following products or tools to view platform component and VM metrics:

* Loggregator Firehose CLI Plug in. See [Installing the Loggregator
Firehose plug-in for CLI](https://docs.cloudfoundry.org/loggregator/cli-plugin.html).

* Loggregator Log Cache CLI plug-in. See [Cloud Foundry Community cf CLI plug-ins](https://plugins.cloudfoundry.org/).
|
| Apps |
You can use the following products or tools to view app logs:

* cf CLI cf logs command. See [Cloud Foundry CLI Reference Guide.](https://cli.cloudfoundry.org/en-US/cf/logs.html)

* Syslog forwarding. See [Streaming App Logs to Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html).

* Loggregator Firehose CLI plug-in. See [Installing the Loggregator
Firehose plug-in for CLI](https://docs.cloudfoundry.org/loggregator/cli-plugin.html).

* Loggregator Log Cache CLI plug-in. See [Cloud Foundry Community cf CLI plug-ins](https://plugins.cloudfoundry.org/).
|
You can use the following products or tools to view app metrics:

* Loggregator Firehose CLI plug-in. See [Installing the Loggregator
Firehose plug-in for CLI](https://docs.cloudfoundry.org/loggregator/cli-plugin.html).

* Loggregator Log Cache CLI plug-in. See [Cloud Foundry Community cf CLI plug-ins](https://plugins.cloudfoundry.org/).
|