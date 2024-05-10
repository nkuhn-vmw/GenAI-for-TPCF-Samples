# Configuring load balancer health checks for Cloud Foundry routers
You can configure load balancer health checks for Cloud Foundry routers so requests go only to healthy
router instances.
In environments that require high availability, you must configure your redundant load balancer to forward traffic
directly to the Cloud Foundry (Cloud Foundry) routers. In environments that do not require high availability, you can skip the load balancer and configure DNS to resolve the Cloud Foundry domains directly to a single instance of a router.

## Add health check endpoints for routers
You can configure your load balancer to use either HTTP or HTTPS for checking the health of `gorouter`
and `tcp_router` processes.
To deactivate the HTTP health check endpoints, set the following properties to `false`:

- The `router.status.enable_nontls_health_checks` property on the `gorouter` job

- The `tcp_router.enable_nontls_health_checks` property on the `tcp_router` job

### Using HTTPS health check endpoints
To configure your load balancer to use HTTPS health check endpoints, add the IP addresses of all router instances,
along with their corresponding port and path:

* Gorouter (HTTP router): `https://GOROUTER_IP:8443/health`

* TCP router: `https://TCP_ROUTER_IP:443/health`

### Using HTTP health check endpoints
To configure your load balancer to use HTTP health check endpoints, add the IP addresses of all router instances,
along with their corresponding port and path:

* Gorouter (HTTP router): `http://GOROUTER_IP:8080/health`

* TCP router: `http://TCP_ROUTER_IP:80/health`
The preceding configuration assumes the default health check ports for the Cloud Foundry routers. To modify these
ports, see the following sections.

### Set the Gorouter Health Check Port
You can set the health check port for Gorouter in the `cf-deployment` manifest using the `router.status.port` property. The
value of this property
default setting is `8080`.

### Set the TCP Router Health Check Port
You can set the health check port for the TCP router in the `routing-release` manifest using the `tcp_router.health_check_port` property. The
value of this
property default setting is `80`.

## Set the healthy and unhealthy threshold properties for the Gorouter
To maintain high availability during upgrades to the Gorouter, each router is upgraded on a rolling basis. During upgrade of a
highly available environment with multiple routers, each router is shut down, upgraded, and restarted before the next router is
upgraded. This ensures that any pending HTTP requests passed to the Gorouter are handled correctly.
Cloud Foundry uses the following properties:
`router.drain_wait`: Specifies, in seconds, the `unhealthy` threshold that determines when the Gorouter stops accepting connections and
the process gracefully stops. During this period, the Gorouter continues to serve HTTP requests and the health check endpoint returns `503` errors.
`router.load\_balancer\_healthy\_threshold`: Specifies the amount of time, in seconds, that the load balancer waits until it declares the
Gorouter instance `started`. This enables the load balancer time to register the instance as `healthy`.
The following table describes the behavior of the load balancer health checks when a router shuts down and is restarted.
| Step | Description |
| --- | --- |
| 1 | A shutdown request is sent to the router. |
| 2 | The router receives shutdown request, which causes the following:

* The router begins sending Service Unavailable responses to the load balancer health checks.

* The load balancer continues sending HTTP request to the router
|
| 3 | The load balancer considers the router to be in an unhealthy state, which causes the load balancer to stop sending HTTP requests to the router.
The time between step 2 and 3 is defined by the values of the health check interval and threshold configured on the load balancer.
|
| 4 | The router shuts down.
The interval between step 2 and 4 is defined by the `router.drain_wait` property of the Gorouter. In general, the value of this property should be longer than the value of the interval and threshold values (interval x threshold) of the load balancer. This additional interval ensures that any remaining HTTP requests are handled before the router shuts down. |
| 5 | If the router shutdown is initiated by an upgrade, the Gorouter software is upgraded. |
| 6 | The router restarts. The router returns Service Unavailable responses for load balancer health checks for 20 seconds; during this time the routing table is preloaded.
The duration of the health check Service Unavailable response is configurable using the manifest property `router.requested\_route\_registration\_interval\_in\_seconds`, which defaults to 20 seconds.
|
| 7 | The routers begins returning Service Available responses to the load balancer health check. |
| 8 | The load balancer considers the router to be in a healthy state.
The time between step 7 and 8 is specified by the health check interval and threshold configured for your load balancer (health check threshold x health check interval). |
| 9 | Shut down and upgrade of the other router begins. |