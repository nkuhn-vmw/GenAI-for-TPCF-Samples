# Enabling Zipkin tracing in Cloud Foundry
You can use Zipkin tracing to troubleshoot failures or latency issues in your apps. You can trace requests and responses
across distributed systems. For more information, see [Zipkin.io](http://zipkin.io/).
To enable Zipkin tracing, add the following property to your BOSH deployment manifest file:
```
properties:
router:
tracing:
enable_zipkin: true
```
For more information about how the Gorouter works with HTTP headers and Zipkin tracing, see the [HTTP Headers](https://docs.cloudfoundry.org/concepts/http-routing.html#http-headers) section of the *HTTP Routing* topic.
To trace app requests and responses in Cloud Foundry, apps must also log Zipkin headers.
After adding Zipkin HTTP headers to app logs, developers can use `cf logs myapp` to correlate the trace and span IDs logged by the Gorouter with the trace IDs logged by their app. To correlate trace IDs for a request through multiple apps, each app must forward appropriate values for the headers with requests to other apps.