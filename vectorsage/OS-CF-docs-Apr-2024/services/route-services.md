# Offering route services
You can offer a service to a Cloud Foundry (Cloud Foundry) services
Marketplace.
For information about consuming these services, see
[Manage App Requests with Route Services](https://docs.cloudfoundry.org/devguide/services/route-binding.html).
Route services require Diego. Your deployment must use the Diego architecture or you must enable Diego for your app.
Cloud Foundry app developers might want to apply
transformation or processing to requests before they reach an
app. Common examples of use cases include authentication, rate
limiting, and caching services.
Route services are a kind of
Marketplace service that you can use to apply various
transformations to app requests by binding an app’s route to a service
instance. Through integrations with service brokers and, optionally,
with the Cloud Foundry routing tier, providers can
offer these services with a familiar, automated,
self-service, and on-demand user experience.

## Architecture
Cloud Foundry supports the following models for
route services:

* [Fully-brokered services](https://docs.cloudfoundry.org/services/route-services.html#fully-brokered).

* [Static, brokered services](https://docs.cloudfoundry.org/services/route-services.html#static-brokered).

* [User-provided services](https://docs.cloudfoundry.org/services/route-services.html#user-provided).
In each model, you configure a route service to process traffic
addressed to an app.

### Fully-brokered service
In the fully-brokered service model, the Cloud Foundry
router receives all traffic to apps in the deployment before any
processing by the route service. You can bind a route service
to any app, and if an app is bound to a route service, the Cloud Foundry router sends
the traffic to the
service. After the route service processes requests, it sends it
back to the load balancer in front of the Cloud Foundry
router. The second time through, the Cloud Foundry
router recognizes that the route service has already handled them, and
forwards them directly to app instances.
![Fully brokered service model](https://docs.cloudfoundry.org/services/images/route-services-fully-brokered.png)
The route service can run inside or outside of Cloud Foundry, as long as it
fulfills the [Service Instance
responsibilities](https://docs.cloudfoundry.org/services/route-services.html#service-instance-responsibilities) to integrate it
with the Cloud Foundry router.
A service broker
publishes the route service to the Cloud Foundry
marketplace, and makes it available to developers.
You can then
create an instance of the service and bind it to your apps with the
following commands:
```
cf create-service BROKER-SERVICE-PLAN SERVICE-INSTANCE
```
```
cf bind-route-service YOUR-APP-DOMAIN SERVICE-INSTANCE [--hostname HOSTNAME] [--path PATH]
```
You can configure the service either through the service provider web interface or by passing
[arbitrary parameters](https://docs.cloudfoundry.org/devguide/services/managing-services.html#arbitrary-params-create)
to their `cf create-service` call through the `-c` flag.

**Advantages:**

* You can can use a Service Broker to dynamically configure how the
route service processes traffic to specific apps.

* Adding route services requires no manual infrastructure
configuration.

* Traffic to apps that do not use the service makes fewer network hops because requests for those apps do not pass through the route service.

**Disadvantages:**

* Traffic to apps that use the route service makes additional network
hops, as compared to the static model.

### Static, brokered service
In the static brokered service model, an operator installs a static
routing service, which might be a piece of hardware, in front of the
load balancer. The routing service runs outside of Cloud Foundry and receives traffic
to all apps running in
the Cloud Foundry deployment. The service provider
creates a service broker to publish the service to the Cloud Foundry marketplace.
As with a fully-brokered
service, you can use the service by instantiating it with `cf
create-service` and binding it to an app with `cf bind-route-service`.
![Static brokered service model.](https://docs.cloudfoundry.org/services/images/route-services-static-brokered.png)
In this model, you configure route services on an app-by-app
basis. When you bind a service to an app, the service broker directs
the routing service to process that app’s traffic rather than pass the
requests through unchanged.

**Advantages:**

* You can use a service broker to dynamically configure how the
route service processes traffic to specific apps.

* Traffic to apps that use the route service takes fewer network hops.

**Disadvantages:**

* Adding route services requires manual infrastructure configuration.

* Traffic to apps that do not use the route service make unnecessary
network hops. Requests for all apps hosted by the deployment pass
through the route service component.

### User-provided service
If a route service is not listed in the Cloud Foundry
marketplace by a broker, you can still bind it to your app as
a user provided service. The service can run anywhere, either inside
or outside of Cloud Foundry, but it must fulfill the
integration requirements described in [Service Instance
responsibilities](https://docs.cloudfoundry.org/services/route-services.html#service-instance-responsibilities). The service
also needs to be reachable by an outbound connection from the Cloud Foundry router.
![Bound to your app as user provided service.](https://docs.cloudfoundry.org/services/images/route-services-user-provided.png)
This model is identical to the fully brokered service model, except
without the broker. You can configure the service manually, outside
of Cloud Foundry.
You can then create a user provided
service instance and bind it to your app with the following commands,that supply the URL of their route
service:
```
cf create-user-provided-service SERVICE-INSTANCE -r ROUTE-SERVICE-URL
```
```
cf bind-route-service DOMAIN SERVICE-INSTANCE [--hostname HOSTNAME]
```

**Advantages:**

* Adding route services requires no manual infrastructure configuration.

* Traffic to apps that do not use the service makes fewer network hops
because requests for those apps do not pass through the route
service.

**Disadvantages:**

* You must manually provision and configure route services out
of the context of Cloud Foundry because no service
broker automates these operations.

* Traffic to apps that use the route service makes additional network
hops, as compared to the static model.

### Architecture comparison
The previous models require the broker and service instance
responsibilities summarized in the following table:
| Route Services Architecture | Fulfills Cloud Foundry [Service Instance Responsibilities](https://docs.cloudfoundry.org/services/route-services.html#service-instance-responsibilities) | Fulfills Cloud Foundry [Broker Responsibilities](https://docs.cloudfoundry.org/services/route-services.html#broker-responsibilities) |
| --- | --- | --- |
| Fully-Brokered | Yes | Yes |
| Static Brokered | No | Yes |
| User-Provided | Yes | No |

## Service instance
The following information applies only when a broker returns `route_service_url`
in a bind response.
Binding a service instance to a route associates the
`route_service_url` with the route in the Cloud Foundry
router. All requests for the route are proxied to the URL specified by
`route_service_url`.
The Cloud Foundry router includes the `X-CF-Forwarded-Url` header
containing the originally requested URL, as
well as the `X-CF-Proxy-Signature` and `X-CF-Proxy-Metadata` headers used
by the router to validate that the route-service sent the
request. These headers are described in the [Headers](https://docs.cloudfoundry.org/services/route-services.html#headers) section.

### Service instance responsibilities
The route service must handle requests by either:

* Accepting the request, making a new request to the original
requested URL, or to another location, and then responding to the
original requestor.

* Rejecting the request by responding with a non `2xx` HTTP status code.
When forwarding a request to the originally requested URL, the route
service must forward the `X-CF-Forwarded-Url`, `X-CF-Proxy-Signature` and
`X-CF-Proxy-Metadata` headers on the request or it is rejected.
When forwarding a request to a location other than the originally
requested URL, the route service strips these headers.

### Headers
The following HTTP headers are added by the Gorouter to requests
forwarded to route services.

#### X-CF-Forwarded-Url
The `X-CF-Forwarded-Url` header contains the originally requested
URL. The route service might choose to forward the request to this URL
or to another.

#### X-CF-Proxy-Signature
When the Gorouter receives a request with this header, it accepts
and forwards the request to the app only if the URL of the request
matches the one associated with the token, if the request was
received on time. Otherwise, the request is rejected.
`X-CF-Proxy-Signature` also signals to the Gorouter that a request has
transited a route service. If this header is present, the Gorouter
does not forward the request to a route service. The route-service
needs to forward these headers in subsequent requests to the orignal
requested URL, so that it knows not to send the request back to the
route service but to the app. The headers must NOT be sent in the
HTTP response to the GoRouter, only in the new HTTP request to the
GoRouter.
The `X-CF-Proxy-Signature` header is
an **access token**. Anyone possessing your `X-CF-Proxy-Signature`
token can bypass the route service. Do not share your your `X-CF-Proxy-Signature`
token with anyone.
CF-hosted Route Services cannot be chained: If the route service
forwards the request to a URL to resolve a route for a
different app on Cloud Foundry, the route must not have
a bound route service. Otherwise, the request is rejected as the
requested URL does not match the one in the forwarded
`X-CF-Proxy-Signature` header.

##### X-CF-Proxy-Metadata
The `X-CF-Proxy-Metadata` header aids in the encryption and
description of `X-CF-Proxy-Signature`.

### SSL certificates
When Cloud Foundry is deployed in a development
environment, certificates hosted by the load balancer are self-signed,
and not signed by a trusted Certificate Authority. When the route
service finishes processing an inbound request and makes a call to the
value of `X-CF-Forwarded-Url`, be prepared to accept the self-signed
certificate when integrating with a non-production deployment of Cloud Foundry.

### Timeouts
Route services must forward the
request to the app route within the number of seconds configured by
the `router.route_service_timeout` property. The
`router.route_service_timeout` property defaults to 60 seconds.
In addition, all requests must respond in the number of seconds
configured by the `request_timeout_in_seconds` property. The
`request_timeout_in_seconds` property default to 900 seconds.
Timeouts are configurable for the router using the cf-release BOSH
deployment manifest. For more information, see the [spec](https://github.com/cloudfoundry-incubator/routing-release/blob/master/jobs/gorouter/spec).

## Broker responsibilities

### Catalog endpoint
Brokers must include `requires: ["route_forwarding"]` for a service in
the catalog endpoint. If this is not present, Cloud Foundry does not permit users to bind an instance of
the service to a route.

### Binding endpoint
When you bind a route to a service instance, Cloud Foundry sends a bind request to the broker, including
the route address with `bind_resource.route`. A route is an address
used by clients to reach apps mapped to the route. The broker might
return `route_service_url`, containing a URL where Cloud Foundry proxy requests for the route. This URL
must have an `https` scheme, or the Cloud Controller rejects the
binding. `route_service_url` is optional, and not returning this field
allows a broker to dynamically configure a network component already
in the request path for the route, requiring no change in the Cloud Foundry router.
For more information about bind requests, see the
[Binding](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#binding) section of the *Open Service Broker API
(v2.13)* spec on GitHub.

## Route services examples

* [Logging Route
Service](https://github.com/cloudfoundry-samples/logging-route-service):
This route service can be pushed as an app to Cloud Foundry. It fulfills the service instance
responsibilities and logs requests received and sent. It can
be used to see the route service integration in action by tailing
its logs.

* [Rate Limiting Route
Service](https://github.com/cloudfoundry-samples/ratelimit-service):
This example route service is a simple Cloud Foundry
app that provides rate limiting to control the rate of traffic to an
app.

* [Spring Boot examples](https://github.com/in28minutes/spring-boot-examples).

## Tutorial
The following instructions show how to use the Logging Route
Service described in [Route Services examples](https://docs.cloudfoundry.org/services/route-services.html#examples) to verify that when a
route service is bound to a route, requests for that route are proxied
to the route service.
For a video of this tutorial, see [Route Services in Pivotal Cloud
Foundry 1.7](https://youtu.be/VaaZJE2E4jI) on YouTube.
These commands require the Cloud Foundry Command Line Interface (cf
CLI) v6.16 or later.
To use the logging route service:

1. Push the logging route service as an app by running:
```
cf push logger
```

2. Create a user provided service instance, and include the route of
the logging route service you pushed as `route_service_url`. Make sure
to use `https` for the scheme.
Run:
```
cf create-user-provided-service mylogger -r https://logger.cf.example.com
```

1. Push a sample app such as [Spring
Music](https://github.com/cloudfoundry-samples/spring-music). By
default, this creates a route `spring-music.cf.example.com`.
Run:
```
cf push spring-music
```

1. Bind the user provided service instance to the route of your sample
app. The `bind-route-service` command takes a route and a service
instance.
The route is specified in the following example by domain
`cf.example.com` and hostname `spring-music`.
Run:
```
cf bind-route-service cf.example.com mylogger --hostname spring-music
```

1. Tail the logs for your route service by running:
```
cf logs logger
```

2. Send a request to the sample app and view in the route service logs
that the request is forwarded to it by running:
```
curl spring-music.cf.example.com
```

## Security considerations
The contract between route services and the Gorouter, applicable for
fully brokered and user-provided models, activates a Cloud Foundry operator to suggest
whether or not requests
forwarded from the route service to a load balancer are encrypted. The
Cloud Foundry operator makes this suggestion by setting
the `router.route_services_recommend_https` manifest property.
This suggestion does not allow the platform to guarantee that a route
service obeys the scheme of the `X-Forwarded-Url` header. If a route
service ignores the scheme and downgrades the request to plain text, the requester can intercept, and use or edit the data
within it.
For increased security, follow these recommendations:

* A load balancer stops TLS and can sanitize and reset
`X-Forwarded-Proto` based on whether the request it received was
encrypted or not. Set the `router.sanitize_forwarded_proto: false`
manifest property for the Gorouter.

* A load balancer configured for TCP passthrough can sanitize and
reset the header based on whether the request it received was
encrypted or not. Set the `router.sanitize_forwarded_proto: true`
manifest property for the Gorouter.
For more information about
securing traffic into Cloud Foundry, see [Securing
Traffic into Cloud Foundry](https://docs.cloudfoundry.org/adminguide/securing-traffic.html).
When a route service is mapped
to a route, the Gorouter sanitizes the `X-Forwarded-Proto`
header once, even though requests pass through the Gorouter more than
once.

## Recommendations for securing route services
To best secure communications through route services, Cloud Foundry operators :

1. Set the `router.route_services_recommend_https: true` manifest
property.

2. Set the `router.disable_http: true` manifest property. Setting this
property deactivates the HTTP listener, and forces all communication to the
Gorouter to be HTTPS. This assumes all route services communicate
over HTTPS with the Gorouter. This causes requests from other clients
made to port 80 to be rejected. You must confirm that clients of all
apps make requests over TLS.

3. Confirm that route services do not change the value of the
`X-Forwarded-Proto` header.