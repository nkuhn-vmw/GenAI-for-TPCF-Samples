# Enabling W3C tracing in Cloud Foundry
You can use W3C tracing to troubleshoot failures or latency issues in your apps. You can trace requests and responses
across distributed systems. For more information, see [w3c.org](https://www.w3.org/TR/trace-context/).
To enable W3C tracing, add the following property to your BOSH deployment manifest file:
```
properties:
router:
tracing:
enable_w3c: true
```
Optionally, to specify the W3C tracing tenant ID name, add the following property:
```
properties:
router:
tracing:
enable_w3c: true
w3c_tenant_id: tenant-id
```
If specified, the tracestate identifier will be “tenant-id@gorouter” where “tenant-id” is the value specified. If not specified, the tracestate identifier will be `gorouter`.
For more information about how the Gorouter works with HTTP headers and W3C tracing, see [HTTP headers for W3C tracing](https://docs.cloudfoundry.org/concepts/http-routing.html#w3c-headers) in *HTTP Routing*.
To trace app requests and responses in Cloud Foundry, apps must also log W3C headers.
After adding W3C HTTP headers to app logs, developers can use `cf logs myapp` to correlate the trace and span IDs logged by the Gorouter with the trace IDs logged by their app. To correlate trace IDs for a request through multiple apps, each app must forward appropriate values for the headers with requests to other apps.