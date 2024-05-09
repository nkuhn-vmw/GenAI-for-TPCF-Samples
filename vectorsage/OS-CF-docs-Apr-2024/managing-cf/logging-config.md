# Configuring system logging
This topic explains how to configure the Cloud Foundry logging and metrics system.
For more information, see [Logging and metrics architecture](https://docs.cloudfoundry.org/loggregator/architecture.html).

## Choose an architecture
The configuration available depends on the logging and metrics architecture that you have selected.

* [Loggregator firehose architecture](https://docs.cloudfoundry.org/loggregator/architecture.html#firehose-architecture). This is the original logging and metrics architecture. In this architecture, the [Loggregator agent](https://docs.cloudfoundry.org/loggregator/architecture.html#-how-logs-and-metrics-egress-from-vms) running on each VM collects and sends this data out to Doppler components, which temporarily buffer the data before periodically forwarding it to the Traffic Controller or Reverse Log Proxy (RLP).

* [Shared nothing architecture](https://docs.cloudfoundry.org/loggregator/architecture.html#shared-nothing-architecture). Logs are shipped directly from VMs using syslog instead of passing through the Loggregator Firehose components. The metrics agent provides Prometheus endpoints to expose metrics.
It is also possible to combine elements of both architectures in the same deployment. For example, you can retain existing Loggregator Firehose integrations but use syslog agent to send logs to syslog drains.

## Scale loggregator
Cloud Foundry system components and apps constantly generate log and metrics data. If your deployment is configured to use the Loggregator Firehose Architecture and the log and metrics data input to a Doppler exceeds its buffer size for a given interval, data can be lost.
See the indicators described in the [loggregator-release](https://github.com/cloudfoundry/loggregator-release/blob/main/jobs/doppler/templates/indicators.yml.erb) on GitHub. For example, see the log loss rate and suggested actions. Typical actions include scaling Doppler, Traffic Controller, or RLP instances.

## Scale shared nothing
See [loggregator-agent-release](https://github.com/cloudfoundry/loggregator-agent-release/blob/main/jobs/loggr-syslog-agent/templates/indicators.yml.erb) on GitHub for the indicators for the syslog agent.

## Scale Log Cache
See [log-cache-release](https://github.com/cloudfoundry/log-cache-release/blob/main/jobs/log-cache/templates/indicators.yml.erb) on GitHub for the indicators for Log Cache.

## Customize Logging and metric components
Review the [cf-deployment operations files](https://github.com/cloudfoundry/cf-deployment/tree/main/operations) on GitHub that provide for common customizations.
You can further customize each component by changing its properties in the deployment manifest. The BOSH job specs in each BOSH release
are the best reference for the set of configurable properties for logging and metric components.
For more information, see the [BOSH documentation](https://bosh.io/docs/jobs/#spec).

### loggregator-release

* [doppler](https://github.com/cloudfoundry/loggregator-release/blob/main/jobs/doppler/spec)

* [loggregator\_trafficcontroller](https://github.com/cloudfoundry/loggregator-release/blob/main/jobs/loggregator_trafficcontroller/spec)

* [reverse\_log\_proxy](https://github.com/cloudfoundry/loggregator-release/blob/main/jobs/reverse_log_proxy/spec)

* [reverse\_log\_proxy\_gateway](https://github.com/cloudfoundry/loggregator-release/blob/main/jobs/reverse_log_proxy_gateway/spec)

### loggregator-agent-release

* [loggr-forwarder-agent](https://github.com/cloudfoundry/loggregator-agent-release/blob/main/jobs/loggr-forwarder-agent/spec)

* [loggregator\_agent](https://github.com/cloudfoundry/loggregator-agent-release/blob/main/jobs/loggregator_agent/spec)

* [loggr-syslog-agent](https://github.com/cloudfoundry/loggregator-agent-release/blob/main/jobs/loggr-syslog-agent/spec)

* [loggr-syslog-binding-cache](https://github.com/cloudfoundry/loggregator-agent-release/blob/main/jobs/loggr-syslog-binding-cache/spec)

* [prom\_scraper](https://github.com/cloudfoundry/loggregator-agent-release/blob/main/jobs/prom_scraper/spec)

### metrics-discovery-release

* [metrics-agent](https://github.com/cloudfoundry/metrics-discovery-release/blob/main/jobs/metrics-agent/spec)