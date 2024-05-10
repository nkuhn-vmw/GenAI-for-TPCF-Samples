# Configuring HTTP/2 support
You can configure your Cloud Foundry deployment to support HTTP/2 from ingress to egress.

## HTTP/2 support overview
For information about how HTTP/2 can benefit apps running on Cloud Foundry,
see [Routing HTTP/2 and gRPC Traffic to Apps](https://docs.cloudfoundry.org/devguide/http2-protocol.html).
Apps can benefit from HTTP/2 even if not all network segments use HTTP/2.
Headers are compressed and requests are multiplexed for HTTP/2 segments even if other network hops do not use HTTP/2.
However, some features like gRPC require all segments to use HTTP/2.
While browsers and other clients might indicate a request is being served over HTTP/2,
operators must ensure that all network hops use HTTP/2 to support gRPC.

## Prerequisites
Before you can configure your Cloud Foundry deployment to support HTTP/2, you must enable TLS.
Most implementations of HTTP/2 require TLS with Application-Layer Protocol Negotiation (ALPN).
For more information about ALPN, see [RFC 7301: Transport Layer Security (TLS) Application-Layer Protocol Negotiation Extension](https://datatracker.ietf.org/doc/html/rfc7301).

### Security considerations
If you use a firewall or other tools to monitor network traffic,
ensure that those tools support HTTP/2 connections.
If your network monitoring tools do not support HTTP/2 connections, configuring HTTP/2 can cause problems with protecting and analyzing traffic on your network.
Cloud Foundry recommends that you become familiar with common vulnerabilities in apps that support HTTP/2.
For example, HTTP/1.1 has vulnerabilities such as request smuggling and desync attacks, but these might be more prevalent in HTTP/2 environments.

## Enable end-to-end HTTP/2
This section describes how to enable HTTP/2 in your deployment from ingress to egress.
To enable end-to-end HTTP/2, you must configure the load balancers, the Cloud Foundry platform, and the app.

### Configure load balancers
To support HTTP/2, operators must configure platform load balancers to enable HTTP/2 ingress and egress.
Load balancers in front of Cloud Foundry can be either Layer 4 (TCP) or Layer 7 (Application).
Layer 4 load balancers tend to be simpler,
while Layer 7 load balancers offer more features by inspecting the contents of HTTP requests.
For example, a Layer 7 load balancer might send requests to different Cloud Foundry deployments based on the resources that are being requested.
You can configure many load balancers to function in either Layer 4 or Layer 7 mode.
For more information, see the following sections:

* [Configure Layer 4 TCP Load Balancers](https://docs.cloudfoundry.org/adminguide/supporting-http2.html#l4)

* [Configure Layer 7 Application Load Balancers](https://docs.cloudfoundry.org/adminguide/supporting-http2.html#l7)

#### Configure layer 4 TCP load balancers
Layer 4 load balancers do not terminate HTTP connections and support passing HTTP/2 traffic.
If you are terminating TLS traffic at a Layer 4 load balancer,
configure your load balancer to advertise support for HTTP/2 over ALPN.
ALPN ensures that a client making an HTTP request knows that the app server that is servicing the request can support HTTP/2.
If a load balancer terminates TLS without advertising HTTP/2 over ALPN, then clients must be configured to use HTTP/2 with prior knowledge.
For more information, see [Starting HTTP/2 with Prior Knowledge](https://datatracker.ietf.org/doc/html/rfc7540#section-3.4) in *RFC 7540: Hypertext Transfer Protocol Version 2 (HTTP/2)*.

#### Configure layer 7 application load balancers
Layer 7 load balancers terminate the incoming HTTP connection and initiate new HTTP connections to their back ends.
For end-to-end HTTP/2 support, Layer 7 load balancers must have HTTP/2 enabled for both ingress and egress HTTP connections.
The HAProxy BOSH release contains the canonical example of how to set up HTTP/2 load balancing for Cloud Foundry.
See the [BOSH release for HAProxy](https://github.com/cloudfoundry-incubator/haproxy-boshrelease) on GitHub.
When HTTP/2 is enabled, HAProxy advertises support for HTTP/2 over ALPN, accepts HTTP/2 ingress traffic for all connections, and negotiates using HTTP/2 over ALPN when connecting to the Gorouter.
Gorouter and many Layer 7 load balancers do not support WebSockets over HTTP/2.
For more information, see [RFC 8441](https://datatracker.ietf.org/doc/html/rfc8441).
Cloud Foundry uses WebSockets for streaming logs and metrics as well as apps that serve WebSocket traffic.
To continue supporting WebSockets in Cloud Foundry when you enable HTTP/2, you can do either of the following:

* Configure load balancers to forward WebSocket traffic over HTTP/1.1.

* Use a Layer 4 load balancer for WebSocket traffic.
For more information, see [Supporting WebSockets](https://docs.cloudfoundry.org/adminguide/supporting-websockets.html).

### Configure the Cloud Foundry platform
In routing-release v0.224.0 and later, HTTP/2 support is enabled by default.
To deactivate HTTP/2 support, set the `router.enable_http2` property to `false`.
When HTTP/2 is enabled, the Gorouter accepts HTTP/2 ingress traffic for all apps,
but does not connect to app instances over HTTP/2 unless configured on app routes.

### Configure Cloud Foundry apps
Before the Gorouter can send HTTP/2 traffic to apps,
the operator must configure HTTP/2 when mapping the route to the app.
This is because the Gorouter defaults to HTTP/1.1 for compatibility unless it knows that a given route and app combination supports HTTP/2.
After you map a route with HTTP/2 support enabled, the Gorouter sends all traffic to that app over HTTP/2, even traffic that ingresses to the Gorouter over HTTP/1.1.
To map a route to the app with HTTP/2 support:

1. Log in to the Cloud Foundry Command Line Interface (cf CLI) by running:
```
cf login -a API-URL -u USERNAME -p PASSWORD -o ORG -s SPACE
```
Where:

* `API-URL` is your API endpoint, [the URL of the Cloud Controller in your Cloud Foundry instance](http://docs.cloudfoundry.org/running/cf-api-endpoint.html).

* `USERNAME` is your username.

* `PASSWORD` is your password. Cloud Foundry discourages using the `-p` option, as it might record your password in your shell history.

* `ORG` is the org where your app is deployed.

* `SPACE` is the space in the org where your app is deployed.

2. Run the following command to map the route to your app:
```
cf map-route MY-APP EXAMPLE.COM --destination-protocol=http2
Creating route MY-APP.EXAMPLE.COM for org my-org / space my-space as admin...
OK
```
Where:

* `MY-APP` is the name of your app.

* `EXAMPLE.COM` is the route you want to map to your app.