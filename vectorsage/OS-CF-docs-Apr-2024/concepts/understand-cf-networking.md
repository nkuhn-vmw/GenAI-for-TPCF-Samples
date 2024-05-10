# Container-to-container networking
This topic provides you with an overview of how container-to-container networking works in Cloud Foundry.
Container-to-container networking is not available for apps hosted on Microsoft Windows.
The container-to-container networking feature enables app instances to communicate with each other directly.
For more information about how to enable and use container-to-container networking, see [Configuring Container-to-Container Networking](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html).When the container-to-container networking feature is disabled, all app-to-app traffic must go through the Gorouter.

## Architecture
Container-to-container networking integrates with [Garden-runC] in a Diego deployment. The CF Networking Release includes several core components, as well as swappable components. For more information about Garden-runC, see [Garden-runC](https://docs.cloudfoundry.org/concepts/architecture/garden.html#garden-runc) in *Garden*. For more information about Diego, see [Diego Components and Architecture](https://docs.cloudfoundry.org/concepts/diego/diego-architecture.html). For more information about the CF Networking release, see [CF Networking Release](https://github.com/cloudfoundry-incubator/cf-networking-release) on GitHub.
To understand the components and how they work, see the following diagram and tables.
The diagram highlights Cloud Foundry components in blue and green. The diagram also highlights swappable components in red.
![The c2c architecture diagram](https://docs.cloudfoundry.org/concepts/images/c2c-arch.png)

### Core components
The container-to-container networking BOSH release has the following core components:
| Part | Function |
| --- | --- |
| Policy Server | A central management node that:

* Maintains a database of policies for traffic between apps. The cf CLI calls an API to create or update a record in the policy database whenever you create or remove a policy.

* Exposes a JSON REST API used by the cf CLI. This API serves traffic using TLS.
|
| Garden External Networker |
A Garden-runC add-on deployed to every Diego Cell that:

* Runs the CNI plug-in component to set up the network for each app.

* Forwards ports to support incoming connections from the Gorouter, TCP Router, and Diego SSH Proxy. This keeps apps externally reachable.

* Installs outbound allow list rules to support Application Security Groups (ASGs).
|

### Swappable components
| Part | Function |
| --- | --- |
| Silk CNI plug-in | A plug-in that provides IP address management and network connectivity to app instances as follows:

* Uses a shared VXLAN overlay network to assign each container a unique IP address.

* Installs network interface in container using the Silk VXLAN back end. This is a shared, flat L3 network.
|
| VXLAN Policy Agent | Enforces network policy for traffic between apps as follows:

* Discovers network policies from the Policy Server Internal API.

* Updates iptables rules on the Diego Cell to allow approved inbound traffic.

* Tags outbound traffic with the unique identifier of the source app using the VXLAN Group-Based Policy (GBP) header.
|

## App instance communication
The following diagram illustrates how app instances communicate in a deployment with container-to-container networking enabled. In this example, the operator creates two policies to regulate the flow of traffic between **App A**, **App B**, and **App C**.

* Allow traffic from **App A** to **App B**

* Allow traffic from **App A** to **App C**
If traffic and its direction is not explicitly allowed, it is denied. For example, **App B** cannot send traffic to **App C**.
![Post Container-to-Container Networking](https://docs.cloudfoundry.org/concepts/images/post-c2c.png)

### Overlay network
Container-to-container networking uses an overlay network to manage communication between app instances.
Overlay networks are not externally routable, and traffic sent between containers does not exit the overlay. You can use the same overlay network range for different Cloud Foundry deployments in your environment.
The overlay network range defaults to `10.255.0.0/16`. You can modify the default to any [RFC 1918](https://tools.ietf.org/html/rfc1918) range that meets the following requirements:

* The range is not used by services that app containers access.

* The range is not used by the underlying Cloud Foundry infrastructure.
All Diego Cells in your Cloud Foundry deployment share this overlay network. By default, each Diego Cell is allocated a /24 range that supports 254 containers per Diego Cell, one container for each of the usable IP addresses, `.1` through `.254`. To modify the number of Diego Cells your overlay network supports, see [Overlay Network](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html#overlay) in *Configuring Container-to-Container Networking*.
Cloud Foundry container networking is currently supported only on Linux.

**Caution**
The overlay network IP address range must not conflict with any other IP addresses in the network. If a
conflict exists, Diego Cells cannot reach any endpoint that has a conflicting IP address.
Traffic to app containers from the Gorouter or from app containers to external services uses
Diego Cell IP addresses and NAT, not the overlay network.

### Policies
Enabling container-to-container networking for your deployment allows you to create policies for communication between app instances. The container-to-container networking feature also provides a unique IP address to each app container and provides direct IP reachability between app instances.
The policies you create specify a source app, destination app, protocol, and port so that app instances can communicate directly without going through the Gorouter, a load balancer, or a firewall. Container-to-container networking supports UDP and TCP, and you can configure policies for multiple ports. These policies apply immediately without having to restart the app.
Additionally, policies use and and track the GUIDs of the apps. The policies continue to work when apps redeploy, or if they crash and Diego places them in a new container. Pushing a brand new app requires a new policy, but not updates to an existing app because an app always retains its GUID.

## App service discovery
The Cloud Foundry platform supports DNS-based service discovery that lets apps find each other’s internal addresses. For example, a front end app instance can use the service discovery mechanism to establish communications with a back end app instance. To set up and use app service discovery, see [App service discovery](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html#discovery) in *Configuring container-to-container networking*.
Container-to-container app service discovery does not provide client-side load balancing or circuit-breaking, and it does not apply to `cf marketplace` services or require app binding. It just lets apps publish service endpoints to each other, unbrokered and unmediated.

## Alternative network stacks
The BOSH release that contains the container-to-container networking feature that is composed of a plug-in network stack. Advanced users or third party vendors can integrate a different network stack. For more information about third party plug-ins, see [3rd Party Plug-in Development for Container Networking](https://github.com/cloudfoundry-incubator/cf-networking-release/blob/develop/docs/3rd-party.md) in the CF Networking Release repository on GitHub.

## Container-to-container networking versus ASGs
Both app security groups (ASGs) and container-to-container networking policies affect traffic from app instances. The following table highlights differences between ASGs and container-to-container networking policies.
| | ASGs | Container-to-Container Networking Policies |
| --- | --- | --- |
| Policy granularity | From a space to an IP address range | From a source app to a destination app |
| Scope | For a space, org, or deployment | For app to app only |
| Traffic direction | Outbound control | Policies apply for incoming packets from other app instances |
| Source app | Is not known | Is identified because of direct addressability |
| Policies take affect | Immediately | Immediately |

## Securing container-to-container traffic
The platform provides a TLS encapsulation for container-to-container network traffic.
To utilize TLS capabilities, the client application can connect to port 61443 on the destination application over HTTPS. Traffic to application
container port 61443 is proxied to application port 8080 inside of the container. In this case:

* The platform provides certificates for each app.

* The platform makes sure that TLS ends within the destination container and passes cleartext traffic to the app.

* The destination app does not need special configuration.
Additionally, applications can implement TLS termination in their destination applications. Use this option if your application needs to use more TLS capabilities, like verifying client certificates and rejecting service for those that are not permitted, or if your application needs TLS termination on a different port than the default port, 8080.
Specific Cloud Foundry vendors might provide additional methods for securing container-to-container traffic.
For information about how the platform can encrypt public traffic to apps, see
[TLS to Apps and Other Back End Services](https://docs.cloudfoundry.org/concepts/http-routing.html#tls-to-back-end) in

*HTTP Routing*.