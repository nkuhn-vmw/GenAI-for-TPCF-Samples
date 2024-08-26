# Enabling and configuring TCP routing in Cloud Foundry
You can enable TCP routing in Cloud Foundry. Learn about TCP routing and go through the steps of enabling and configuring it.

## TCP routing overview
You can use TCP routing to run apps that serve requests on non-HTTP TCP protocols.
You can use TCP routing to comply with regulatory requirements to stop TLS as close
to apps as possible so that packets are not decrypted before reaching the app level.

## TCP routing architecture
The following diagram shows the layers of network address translation that occur in Cloud Foundry
in support of TCP routing.
![Route Ports](https://docs.cloudfoundry.org/adminguide/images/route_ports.png)
The following example workflow ships with route ports, back end ports, and app ports:

1. You create a TCP route for your app based on a TCP domain and a route port, and
map this route to one or more apps. See [Create a Route](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#create-route) in *Configuring Routes and Domains*.

2. Clients make requests to the route. DNS resolves the domain name to the load balancer.

3. The load balancer listens on the port and forwards requests for the domain to the TCP
routers. The load balancer must listen on a range of ports to support multiple TCP route
creation. Additionally, Cloud Foundry must be configured with this range,
so that the platform knows which ports can be reserved when you create TCP routes.

4. The TCP router can be dynamically configured to listen on the port when the route is mapped
to an app. The domain the request was originally sent to is no longer relevant to the routing
of the request to the app. The TCP router keeps a dynamically updated record of the back
ends for each route port. The back ends represent instances of an app mapped to the route.
The TCP router chooses a back end using a round-robin load balancing algorithm for each new
TCP connection from a client. Because the TCP router is protocol-agnostic, it does not recognize
individual requests, only TCP connections. All client requests transit the same connection
to the selected back end until the client or back end closes the connection. Each subsequent
connection initiates the selection of a back end.

5. Because containers each have their own private network, the TCP router does not have direct
access to app containers. When a container is created for an app instance, a port on the Diego
Cell VM is randomly chosen and iptables are configured to forward requests for this port to
the internal interface on the app container. The TCP router then receives a mapping of the
route port to the Diego Cell IP and port.

6. By default, the Diego Cell only routes requests to port `8080`, the app port, on the app
container internal interface. The app port is the port on which apps must listen. Developers
can use the Cloud Controller API to update the ports an app can receive requests on.
For more
information, see [Configuring Apps to Listen on Custom Ports (Beta)](https://docs.cloudfoundry.org/devguide/custom-ports.html).

## Prerequisites for activating TCP routing

**Note** If you have mutual TLS app identity verification enabled, app containers accept incoming communication only from the Gorouter. This disables TCP routing. For more information, see [TLS to Apps and Other Back End Services](https://docs.cloudfoundry.org/concepts/http-routing.html#tls-to-back-end) in *HTTP Routing*.
Before you activate TCP routing, you must set up networking requirements.
To set up networking
requirements:

1. Choose a domain from which you can create TCP routes for your apps. For
example, create a domain which is similar to your app domain but prefixed by the TCP subdomain,
such as `tcp.APP-DOMAIN.com`, where `APP-DOMAIN` is the name of your app domain.

2. Configure DNS to resolve this domain name to the IP address of a highly available load
balancer that can forward traffic for the domain to the TCP routers. For more information,
see [Domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#domains) in *Configuring Routes
and Domains*. If you are operating an environment that does not require high availability,
configure DNS to resolve the TCP domain name you have chosen directly to a single instance
of the TCP router.

3. (Optional) Choose IP addresses for the TCP routers and configure your load balancer to
forward requests for the domain you chose in the first step above to these addresses. Skip
this step if you have configured DNS to resolve the TCP domain name to an instance of the
TCP router. Configure these IPs as your static IPs in your deployment manifest.

4. (Optional) Decide how many TCP routes you want to support. For each TCP route, you must
reserve a port. Configure your load balancer to forward the range of ports to the TCP routers.
Skip this step if you have configured DNS to resolve the TCP domain name to an instance of
the TCP router. For more information about configuring port reservations, see [Modify TCP
Port Reservations](https://docs.cloudfoundry.org/adminguide/enabling-tcp-routing.html#modify-ports).

5. (Optional) Configure the `routing_api.router_groups` manifest property with the same range
of ports that you configured your load balancer with in the previous step:
```
routing_api.router_groups:
− name: default-tcp
reservable_ports: CONFIGURED-PORTS
type: tcp
```
Where `CONFIGURED-PORTS` is the range of ports that you configured your load balancer
with in the previous step.
For more information, see the [Routing Release](https://github.com/cloudfoundry-incubator/routing-release)
repository in GitHub.
To modify the ports after you have deployed, see [Modify TCP Port Reservations](https://docs.cloudfoundry.org/adminguide/enabling-tcp-routing.html#modify-ports).

## Configure TCP routing after deploying Cloud Foundry
After you activate TCP routing and deploy Cloud Foundry, you must add the TCP
shared domain and configure org quotas that allow you to create TCP routes. To do this,
you must use the Cloud Foundry Command Line Interface (cf CLI) and have an admin user account.
For more information about the cf CLI, see [Using the Cloud Foundry Command Line Interface
(cf CLI)](https://docs.cloudfoundry.org/cf-cli/).

### Configure Cloud Foundry with your TCP Domain
After you deploy Cloud Foundry, you must configure Cloud Foundry
with the domain that you configured in [Prerequisites for Enabling TCP Routing](https://docs.cloudfoundry.org/adminguide/enabling-tcp-routing.html#prerequisites).
This is the domain from which developers create TCP routes.
To configure Cloud Foundry with your TCP domain:

1. To list your router groups, run:
```
cf router-groups
```
You must see `default-tcp` as a response.

2. Create a shared domain and associate it with the `default-tcp` router group by running:
```
cf create-shared-domain tcp.APP-DOMAIN.com --router-group default-tcp
```
Where `APP-DOMAIN` is the name of your app domain.

3. Verify that `TCP` appears under `type` next to your TCP domain by running:
```
cf domains
```

### Configure a quota for TCP routes
Because TCP route ports are a limited resource in some environments, quotas are configured
to allow creation of zero TCP routes by default. After you deploy Cloud Foundry,
you can increase the maximum number of TCP routes for all orgs or for particular orgs and
spaces. Because you reserve a route port for each TCP route, you manage the quota for route
ports using the `--reserved-route-ports` cf CLI command option.
For more information, see
[Creating and Modifying Quota Plans](https://docs.cloudfoundry.org/adminguide/quota-plans.html).
You can configure quotas for TCP routes in the following ways:

* If you have a default quota that applies to all orgs, you can update it to configure the
number of route ports that can be reserved by each org by running:
```
cf update-org-quota QUOTA --reserved-route-ports NUMBER-OF-ROUTE-PORTS
```
Where:

+ `QUOTA` is the maximum number of TCP routes you want to allocate to all orgs.

+ `NUMBER-OF-ROUTE-PORTS` is the number of route ports you want to allow each org to reserve.

* To create a new quota that governs the number of route ports that can be created in a
particular org:

1. Target the org for which you want to create the quota by running:
```
cf target -o ORG-NAME
```
Where `ORG-NAME` is the name of the org for which you want to create the quota.

2. Run:
```
create-org-quota QUOTA --reserved-route-ports NUMBER-OF-ROUTE-PORTS
```
Where:

+ `QUOTA` is the maximum number of TCP routes you want to allocate to particular orgs.

+ `NUMBER-OF-ROUTE-PORTS` is the number of route ports you want to allow each org to
reserve.

* To create a new quota that governs the number of route ports that can be created in a
particular space:

1. Target the space to create the quota by running:
```
cf target -s SPACE-NAME
```
Where `SPACE-NAME` is the name of the space for which you want to create the quota.

2. Run:
```
cf create-space-quota QUOTA --reserved-route-ports NUMBER-OF-ROUTE-PORTS
```
Where:

+ `QUOTA` is the maximum number of TCP routes you want to allocate to a particular space.

+ `NUMBER-OF-ROUTE-PORTS` is the number of route ports you want to allow the space to reserve.

## Create a TCP route
For information about creating a TCP route, see [Create a TCP Route with a Port](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#create-route-with-port) in *Configuring Routes
and Domains*.

## Modify TCP port reservations
After deploying Cloud Foundry, you can modify the range of ports available
for TCP routes using `cf curl` commands, as demonstrated with the following commands. The
commands require you to have an admin user account with the `routing.router_groups.read`
and `routing.router_groups.write` scopes.

1. In a terminal window, view the `reservable_ports` by running:
```
cf curl /routing/v1/router_groups
```
Record the `guid` from the output.

2. To configure a new port, run:
```
cf curl /routing/v1/router_groups/GUID
```
Where `GUID` is the GUID you recorded in the previous step.
To configure multiple ports, enter a comma-separated list of ports or port ranges by
running:
```
cf curl \

-X PUT -d '{"reservable_ports":"PORTS-OR-PORT-RANGES"}' \
/routing/v1/router_groups/f7392031-a488-4890-8835-c4a038a3bded
```
Where `PORTS-OR-PORT-RANGES` is a comma-separated list of ports or port ranges. For
example, `"reservable_ports":"1024-1199,1234-1248,1312"`.

**Important**
Do not enter `reservable_ports` that conflict
with other TCP router instances or ephemeral port ranges. Cloud Foundry recommends
using port ranges within `1024-2047` and `18000-32767` on default
installations. Check which ports are available on the TCP router VMs to verify that no
additional ports are in use. For more information, see [TCP router fails to configure routes when there is a port conflict with a local process](https://github.com/cloudfoundry/routing-release/issues/184) in the Routing Release repository on GitHub.