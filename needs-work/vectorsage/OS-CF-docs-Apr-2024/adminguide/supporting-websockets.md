# Supporting WebSockets in Cloud Foundry
In this topic, learn how Cloud Foundry uses WebSockets, why use WebSockets in your apps, and how to configure your
load balancer to support WebSockets.
You can use a load balancer to distribute incoming traffic across Cloud Foundry router instances and configure your load balancer for WebSockets. Otherwise, the Loggregator system cannot stream app logs to developers, or app event data and component metrics to third-party aggregation services. Additionally, developers cannot use WebSockets in their apps.

## WebSocket overview
The WebSocket protocol provides full duplex communication over a single TCP connection. Apps use WebSockets to perform real time data exchange between a client and a server more efficiently than HTTP.
Cloud Foundry uses WebSockets for the following metrics and logging purposes:

1. To stream all app event data and component metrics from the Doppler server instances to the Traffic Controller.

2. To stream app logs from the Traffic Controller to developers using the Cloud Foundry Command Line Interface (cf CLI) .

3. To stream all app event data and component metrics from the Traffic Controller over the Firehose endpoint to external apps or services.
For more information about these Loggregator components, see [Loggregator Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html).

## Configuring your load balancer for WebSockets
To form a WebSocket connection, the client sends an HTTP request that contains an `Upgrade` header and other headers required to complete the WebSocket handshake. You must configure your load balancer to not upgrade the HTTP request, but rather to pass the `Upgrade` header through to the Cloud Foundry router. The procedures required to configure your load balancer depends on your IaaS and load balancer. The following list includes several possible approaches:

* Some load balancers can recognize the `Upgrade` header and pass these requests through to the Cloud Foundry router without returning the WebSocket handshake response. This might or might not be default behavior, and might require additional configuration.

* Some load balancers do not support passing WebSocket handshake requests containing the `Upgrade` header to the Cloud Foundry router. For instance, the Amazon Web Services (AWS) Elastic Load Balancer (ELB) does not support this behavior. In this scenario, you must configure your load balancer to forward TCP traffic to your Cloud Foundry router to support WebSockets. If your load balancer does not support TCP pass-through of WebSocket requests on the same port as other HTTP requests, you can do one of the following:

+ Configure your load balancer to listen on a non-standard port (the built-in Cloud Foundry load balancer listens on 8443 by default for this purpose), and forward requests for this port in TCP mode. App clients must make WebSockets upgrade requests to this port. If you choose this strategy, you must follow the steps in [Set Your Loggregator Port](https://docs.cloudfoundry.org/adminguide/supporting-websockets.html#modify).

+ If a non-standard port is not acceptable, add a load balancer that handles WebSocket traffic (or another IP on an existing load balancer) and configure it to listen on standard ports 80 and 443 in TCP mode. Configure DNS with a new hostname, such as `ws.cf.example.com`, to be used for WebSockets. This hostname should resolve to the new load balancer interface.
Regardless of your IaaS and configuration, you must configure your load balancer to send the X-Forwarded-For and X-Forwarded-Proto headers for non-WebSocket HTTP requests on ports 80 and 443. For more information, see [Securing Traffic into TAS for VMs](https://docs.vmware.com/en/VMware-Tanzu-Application-Service/3.0/tas-for-vms/securing-traffic.html).
Gorouter rejects WebSockets requests for routes that are bound to route services.
These requests return a 503 error and a `X-Cf-Routererror
route_service_unsupported` header.

**Note**
Gorouter does not support WebSockets over HTTP/2.
For more information, see [RFC 8441](https://datatracker.ietf.org/doc/html/rfc8441).
Configure your load balancer to always send WebSocket requests to Gorouter over HTTP/1.1.
For more information, see [Configuring HTTP/2 Support](https://docs.cloudfoundry.org/adminguide/supporting-http2.html#load-balancer).

## Setting your Loggregator port
By default, the Cloud Foundry release manifest assigns port 4443 for TCP/WebSocket communications. If you have configured your load balancer to use a port other than 4443 for TCP/WebSocket traffic, you must edit your Cloud Foundry manifest to set the value of `properties.logger_endpoint.port` to the correct port. Locate the following section of your Cloud Foundry manifest and replace `YOUR-WEBSOCKET-PORT` with the appropriate value:
```
properties:
logger_endpoint:
port: YOUR-WEBSOCKET-PORT
```