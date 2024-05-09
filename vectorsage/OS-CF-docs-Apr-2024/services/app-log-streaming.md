# App Log streaming
When you bind an application to an instance of an applicable service, Cloud Foundry streams logs for the
bound application to the service instance.

* Logs for all apps bound to a log consuming service instance are streamed to that instance.

* Logs for an app bound to multiple log consuming service instances are streamed to all instances.
To activate this capability, a service broker must implement the following:

1. In the [catalog](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#catalog-management) endpoint, the broker must include `requires: syslog_drain`. This minor security measure validates that a service returning a `syslog_drain_url` in response to the [bind](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#binding) operation has also declared that it expects log streaming.
If the broker does not include `requires: syslog_drain`, and the bind request returns a value for `syslog_drain_url`,
Cloud Foundry returns an error for the bind operation.

2. In response to a [bind](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#binding) request, the broker returns a value for `syslog_drain_url`. The syslog URL has a scheme of syslog, syslog-tls, or https and can include a port number. For example:
`"syslog_drain_url": "syslog://logs.example.com:1234"`

## How does it work?

1. Service broker returns a value for `syslog_drain_url` in response to bind.

2. Loggregator periodically polls an internal Cloud Controller endpoint for updates.

3. Upon discovering a new `syslog_drain_url`, Loggregator identifies the associated app.

4. Loggregator streams app logs for that app to the locations specified by the service instances’ `syslog_drain_url`s.
You can manually configure app logs to be streamed to a location of your choice
using user-provided service instances.
For details, see
[Using Third-Party Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html).