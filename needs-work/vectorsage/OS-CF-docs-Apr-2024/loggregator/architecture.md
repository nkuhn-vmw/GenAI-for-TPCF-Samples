# Logging and metrics architecture
Logging and metrics architecture includes components that transport logs and metrics from your Cloud Foundry deployment to destinations such as the Cloud Foundry Command-Line Interface (cf CLI), monitoring tools, or internal system components.
Depending on the configuration of your Cloud Foundry deployment, your Cloud Foundry deployment uses either a Loggregator Firehose architecture or a shared-nothing architecture.
In addition to the components in these architectures, you can also use a System Metrics Agents architecture on a Loggregator deployment to collect metrics from system components and expose them on Prometheus scrapable endpoints.

## Architecture reference diagrams
This section provides architecture diagrams that show the components that collect, store, and forward logs and metrics in your Cloud Foundry deployment.
You can use these diagrams to:

* Understand the components that transport logs and metrics on your Cloud Foundry deployment.

* Diagnose performance issues related to logging and metrics.

* Make decisions about how to best scale the components or consumers described in the architecture.
This section includes the following diagrams:

* Loggregator Firehose architecture. For more information, see [Loggregator Firehose Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html#firehose-architecture).

* Shared-nothing architecture. For more information, see [Shared-nothing Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html#shared-nothing-architecture).

* System Metrics Agents architecture. For more information, see [System Metrics Agents Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html#system-metrics-agents).

### Loggregator Firehose architecture
The following diagram shows how logs and metrics are transported from components and apps on your deployment to Loggregator Firehose consumers, such as nozzles, monitoring tools, or third-party software.
![How logs and metrics are transported.](https://docs.cloudfoundry.org/loggregator/images/architecture/firehose-reference.png)
[View a larger version of this image.](https://docs.cloudfoundry.org/loggregator/images/architecture/firehose-reference.png)
The following components are included in the Loggregator Firehose architecture, as shown in the previous diagram:

* **Prom Scraper:** Prom Scrapers run on both component VMs and Diego Cell VMs. They aggregate metrics from components located on those VMs through Prometheus exposition. Prom Scrapers then forward the metrics to Forwarder Agents.

* **Statsd Injector:** Statsd Injectors run on component VMs. They receive metrics from components over the Statsd protocol. Statsd Injectors then forward the metrics to Forwarder Agents.

* **Forwarder Agent:** Forwarder Agents run on both component VMs and Diego Cell VMs. They receive logs and metrics from the apps and components located on those VMs. Forwarder Agents then forward the logs and metrics to Loggregator Agents and other agents.

* **Loggregator Agent:** Loggregator Agents run on both component VMs and Diego Cell VMs. They receive logs and metrics from the Forwarder Agents, then forward the logs and metrics from multiple Dopplers.

* **Doppler:** Dopplers receive logs and metrics from Loggregator Agents, store them in temporary buffers, and forward them to Traffic Controllers and Reverse Log Proxies.

* **Traffic Controller:** Traffic Controllers poll Doppler servers for logs and metrics, then translate these messages from the Doppler servers as necessary for external and legacy APIs. It services the Firehose Endpoint, also known as the V1 Firehose. The Firehose cf CLI plug-in allows you to view the output of the Firehose. For more information about the Firehose plug-in, see [Installing the Loggregator Firehose plug-in for cf CLI](https://docs.cloudfoundry.org/loggregator/cli-plugin.html).

* **Reverse Log Proxy (V2 Firehose):** Reverse Log Proxies (RLPs) collect logs and metrics from Dopplers and forward them to Log Cache and other consumers over gRPC. Operators can scale up the number of RLPs based on overall log volume.

* **Reverse Log Proxy Gateway (V2 Firehose):** Reverse Log Proxies Gateways (RLP Gateways) collect logs and metrics from Reverse Log Proxies and forward them to consumers over HTTP. Collecting logs and metrics through the RLP Gateway has lower throughput compared to consuming from the Traffic Controller or Reverse Log Proxy.

* **Log Cache:** Log Cache allows viewing of logs and metrics over a specified period of time. The Log Cache includes API endpoints and a CLI plug-in to query and filter logs and metrics. To download the Log Cache CLI plug-in, see [Cloud Foundry Plug-ins](https://plugins.cloudfoundry.org/). The Log Cache API endpoints are available by default. For more information about using the Log Cache API, see [Log Cache](https://github.com/cloudfoundry/log-cache-release/tree/main/src#apis) on GitHub.

* **Log Cache Syslog Server:** The Log Cache Syslog Server receives logs and metrics from Syslog Agents and sends them to Log Cache.

### Shared-nothing architecture
This section describes the components in the shared-nothing architecture that collect, store, and transport logs and metrics on your deployment.
Similar to the Loggregator Firehose Architecture, the shared-nothing architecture allows you to forward logs and metrics from your deployment to external and internal consumers.
In contrast to the Loggregator Firehose architecture, logs and metrics pass through fewer components in the shared-nothing architecture.
![In shared-nothing architecture, the logs and metrics egress directly from deployment VMs, eliminating the need for VMs running doppler and traffic controller components.](https://docs.cloudfoundry.org/loggregator/images/architecture/shared-nothing-reference.png)
[View a larger version of this image.](https://docs.cloudfoundry.org/loggregator/images/architecture/shared-nothing-reference.png)
The following components are included in the shared-nothing architecture, as shown in the previous diagram:

* **Prom Scraper:** Prom Scrapers run on both Cloud Foundry component VMs and Diego Cell VMs. They aggregate metrics from Cloud Foundry components located on those VMs through Prometheus exposition. Prom Scrapers then forward those metrics to Forwarder Agents.

* **Statsd Injector:** Statsd Injectors run on Cloud Foundry component VMs. They receive metrics from Cloud Foundry components over the Statsd protocol. Statsd Injectors then forward those metrics to Forwarder Agents.

* **Forwarder Agent:** Forwarder Agents run on both Cloud Foundry component VMs and Diego Cell VMs. They receive logs and metrics from the apps and Cloud Foundry components located on those VMs. Forwarder Agents then forward the logs and metrics to Loggregator Agents and other agents.

* **Syslog Agent:** Syslog Agents run on Cloud Foundry VMs to collect and forward logs to configured syslog drains. You can specify the destination for logs when defining the individual syslog drain bound to an application or in the Cloud Foundry configuration for all apps in your foundation as an aggregate drain. You can also set the drain scope. Any VM running a syslog agent may connect to configured syslog drains: including Diego Cells, Routers, and Cloud Controllers.

* **Syslog Binding Cache** (not pictured): Syslog Agents can overwhelm CAPI when querying for existing bindings. To address this, the Syslog Binding Cache is a caching proxy between the Syslog Agents and CAPI.

* **Metrics Agents:** Metrics Agents receive metrics from Forwarder Agents and make them available to Metric Scrapers through Prometheus Exposition.

* **Metrics Discovery Registrars:** Metrics Discovery Registrars register each scrapeable endpoint with NATS for discovery by Metrics Scrapers.

* **Log Cache:** Log Cache allows viewing of logs and metrics over a specified period of time. The Log Cache includes API endpoints and a CLI plug-in to query and filter logs and metrics. To download the Log Cache CLI plug-in, see [Cloud Foundry Plug-ins](https://plugins.cloudfoundry.org/). The Log Cache API endpoints are available by default. For more information about using the Log Cache API, see [Log Cache](https://github.com/cloudfoundry/log-cache-release/tree/main/src#apis) on GitHub.

* **Log Cache Syslog Server:** The Log Cache Syslog Server receives logs and metrics from Syslog Agents and sends them to Log Cache.

* **OTel Collector (experimental):** [OpenTelemetry Collectors](https://opentelemetry.io/docs/collector/) are configured to receive metrics from Forwarder Agents and send them to external drains using a variety of available formats.

### System Metrics Agents architecture
The following diagram shows the architecture of a deployment that uses System Metrics Agents to collect VM and system-level metrics.
![NSX-T Overview](https://docs.cloudfoundry.org/loggregator/images/architecture/system-metrics-agents.png)
[View a larger version of this image.](https://docs.cloudfoundry.org/loggregator/images/architecture/system-metrics-agents.png)
The following describes the components of a Loggregator deployment that uses System Metrics Agents, as shown in the previous diagram:

* **System Metrics Agent:** A standalone agent to provide VM system metrics using a Prometheus-scrapeable endpoint.

* **System Metrics Scraper:** The System Metrics Scraper forwards metrics from System Metrics Agents to Loggregator Agents over mTLS.

## How components transport logs and metrics
This section provides detailed descriptions of how the components in the Loggregator Firehose architecture and in the shared-nothing architecture transport logs and metrics on your deployment.
It describes the transport of logs and metrics during the following phases:

* How components in the logging and metrics architectures collect and forward metrics from VMs on your deployment. For more information, see [How logs and metrics egress from VMs](https://docs.cloudfoundry.org/loggregator/architecture.html#vms-egress).

* How components in a Loggregator Firehose architecture collect and forward logs and metrics. For more information, see [How Loggregator Firehose forwards logs and Mmtrics](https://docs.cloudfoundry.org/loggregator/architecture.html#firehose).

* How the logging and metrics architectures expose logs and metrics to consumers. For more information, see [How consumers receive logs and metrics](https://docs.cloudfoundry.org/loggregator/architecture.html#consumers).

### How logs and metrics egress from VMs
The following describes the transport of logs and metrics from VMs through system components to a destination:

1. Apps and component VMs on your deployment emit logs and metrics.

2. Logs and metrics pass through two forwarders:

* rsyslog: This sends logs from the component VMs in Syslog RFC 5424 format.

* Forwarder Agent: This sends metrics and app logs to the Syslog Agent, the Metrics Agent, and the Loggregator Agent.

3. From the Forwarder Agent, logs and metrics then pass through each of the following agents:

* Syslog Agent: This sends app logs in Syslog RFC 5424 format to aggregate and app log destinations.

* Metrics Agent: This exposes metrics for Prometheus-style scraping.

* Loggregator Agent: This sends metrics and app logs to the Loggregator Firehose.

* OTel Collector (experimental): This sends app and component metrics in a variety of formats to aggregate metric destinations.
For more information about how logs and metrics flow through the Loggregator Firehose, see [How Loggregator Firehose forwards logs and metrics](https://docs.cloudfoundry.org/loggregator/architecture.html#firehose).
The following diagram shows the transport of logs and metrics from VMs on your deployment:
![Transport of logs and metrics from VMs on your deployment.](https://docs.cloudfoundry.org/loggregator/images/architecture/vms.png)

### How Loggregator Firehose forwards logs and metrics
For deployments that use a Loggregator Firehose architecture, the Loggregator Agent forwards logs and metrics emitted by apps and component VMs on your deployment to the Loggregator Firehose.
The following information describes how the Loggregator Firehose sends logs and metrics through the V1 and V2 Firehose APIs:

1. The Loggregator Agent sends each log and metric to one Doppler. It distributes the logs and metrics among a random group of five Dopplers.

2. Dopplers make a copy of each log and metric for each consumer. The Dopplers then send the logs and metrics to Traffic Controllers and Reverse Log Proxies for distribution.

3. Traffic Controllers and Reverse Log Proxies distribute logs and metrics in the following ways:

* Traffic Controllers receive WebSocket connections from V1 Firehose Consumers, and send logs and metrics as V1 Envelopes. If any of these consumers start to fall behind, Traffic Controllers log a slow consumer alert and disconnect that particular consumer.

* Reverse Log Proxies receive gRPC connections from V2 Firehose Consumers and send logs and metrics as V2 Envelopes. If a consumer falls behind, the envelopes are dropped.

* Reverse Log Proxy Gateways (RLP Gateways) receive HTTP connections from V2 Firehose consumers, and send logs and metrics as JSON-encoded V2 Envelopes. Reverse Log Proxy Gateways connect to Reverse Log Proxies, rather than directly to Dopplers.
The following diagram shows the flow of logs and metrics through the Loggregator Firehose as previously described:
![A Loggregator Agent appears inside the VMs block. Loggregator Agents send to Dopplers, located on Doppler VMs. Dopplers, in turn, send to both Traffic Controllers and Reverse Log Proxies.](https://docs.cloudfoundry.org/loggregator/images/architecture/firehose.png)

### How consumers receive logs and metrics
Consumers of logs and metrics include the Cloud Foundry Command Line Interface (cf CLI), Cloud Foundry web UIs such as Stratos, and any observability or monitoring product integrations.
The cf CLI and any Cloud Foundry web UIs can access logs and metrics through Log Cache. Log Cache receives logs and metrics from either the Firehose or directly from VMs through syslog. Log Cache provides short-term storage for logs and metrics where the cf CLI and web UIs can access them.
Integrations with observability or monitoring products receive logs and metrics through one of the following methods, depending on the logging and metrics architecture that your deployment uses:

* Connect to the Loggregator Firehose for access to both logs and metrics.

* Receive logs in syslog RFC 5424 format and metrics in OTel Collector-supported formats.
The following diagram shows how consumers of logs and metrics receive logs and metrics from your deployment:
![A Forwarder Agent is one of the VMs in the VMs block. Apps are shown sending to the Forwarder Agent, and Components are shown sending metrics to the the Forwarder Agent. Components also send logs to syslog.](https://docs.cloudfoundry.org/loggregator/images/architecture/consumers.png)

## Related BOSH components
This section describes the components that forward BOSH reported VM metrics to Loggregator. BOSH-reported VM metrics measure the health of BOSH-deployed VMs on which apps and components are deployed. Loggregator streams BOSH-reported VM metrics through the Firehose.
The following components send BOSH reported VM metrics to Loggregator:

* **BOSH Agent:** BOSH Agents are located on component VMs and Diego Cell VMs. They collect metrics, such as Diego Cell capacity remaining, from the VM and forward them to the BOSH Health Monitor.

* **BOSH Health Monitor:** The BOSH Health Monitor receives metrics from the BOSH Agents. It then forwards the metrics to a third-party service or to the BOSH System Metrics Forwarder.

* **BOSH System Metrics Plugin:** This plug-in reads health events. For example, VM heartbeats and alerts from the BOSH Health Monitor, and streams them to the System Metrics Agent.

* **BOSH System Metrics Forwarder:** The BOSH System Metrics Forwarder is located on the Loggregator Traffic Controller. It forwards heartbeat events from the System Metrics Agent as envelopes to Loggregator through a Loggregator Agent.