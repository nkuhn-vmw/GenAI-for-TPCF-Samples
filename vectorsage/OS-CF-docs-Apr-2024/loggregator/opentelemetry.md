# Configuring the OpenTelemetry Collector
You can deploy an [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/) for Cloud Foundry
to egress metrics.
When the OpenTelemetry (OTel) Collector is deployed, the Loggregator Forwarder Agent forwards platform and application metrics
to the OTel Collector, which then egresses metrics using one or more metric exporters that you configure.

**Caution**
OpenTelemetry Collector is currently an experimental feature and should not be used in production systems.

## Metric Exporter configuration
The OTel Collector has a standard YAML-based file format for configuration. When deploying Cloud Foundry
with Otel Collector support, provide only the exporter configuration.

**Important**
Specify only the configuration under the `exporters` section of the OpenTelemetry Collector configuration. It
is not currently possible to configure Receivers or Processors.
For example, to configure the OpenTelemetry Collector to egress metrics using OTLP over gRPC, you can provide the following
minimal configuration. This will use the defaults for gRPC and TLS configuration.
```
otlp:
endpoint: 203.0.113.10:4317
```
As the OTel Collector is typically deployed on all VMs, you must ensure that all VMs in your deployment are
allowed to connect to the OTLP server endpoint.

### mTLS
To configure the exporter to use an mTLS connection to the remote OTLP endpoint, you can specify [additional TLS
configuration](https://github.com/open-telemetry/opentelemetry-collector/blob/main/config/configtls/README.md).
```
otlp:
endpoint: 203.0.113.10:4317
tls:
cert_pem: |
PEM_ENCODED_CERTIFICATE
key_pem: |
PEM_ENCODED_PRIVATE_KEY
ca_pem: |
PEM_ENCODED_CERTIFICATE
```

### gRPC compression
You can configure the type of compression used for OTLP gRPC exporters. The OTLP gRPC exporter uses `gzip` compression
by default. To reduce CPU usage of the OTel Collector (increasing the size of the payload) you can optionally configure
the OTLP gRPC exporter to use `snappy` compression. Validate that the server you are sending metrics to
support `snappy` compression before making this change.
```
otlp:
endpoint: 203.0.113.10:4317
compression: snappy
```

### Multiple exporters
The OTel Collector supports defining multiple exporters, each with its own configuration. For example, you can define
two OTLP gRPC exporters that egress metrics to different destinations.
```
otlp:
endpoint: 203.0.113.10:4317
otlp/another:
endpoint: 203.0.113.11:4317
```

### Authentication
The Cloud Foundry distribution of the OpenTelemetry Collector does not support configuration of
authenticator extensions for exporters at this time.

### Reviewing the available exporters
The Cloud Foundry distribution of the OpenTelemetry Collector ships with a number of exporters. To see
the exporters that are available for use, run the following command on a VM that has otel-collector deployed.
```
/var/vcap/packages/otel-collector/otel-collector components
```

## Deploying the OpenTelemetry Collector
CF Deployment provides [experimental operations files](https://github.com/cloudfoundry/cf-deployment/tree/main/operations/experimental)
that you can use to deploy the OTel Collector:

* [on Linux](https://github.com/cloudfoundry/cf-deployment/blob/main/operations/experimental/add-otel-collector.yml)

* [on Windows](https://github.com/cloudfoundry/cf-deployment/blob/main/operations/experimental/add-otel-collector-windows.yml)
For example, to deploy a fresh CF Deployment with OTel Collector enabled, run:
```
bosh deploy cf-deployment.yml \

--ops-file=operations/experimental/add-otel-collector.yml \

--var-file=otel_collector_metric_exporters=YOUR_METRIC_EXPORTER_CONFIG_FILE_PATH.yml \

--var=system_domain=YOUR_SYSTEM_DOMAIN
```