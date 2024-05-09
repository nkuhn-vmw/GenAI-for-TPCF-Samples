# Configuring container-to-container networking
The container-to-container networking feature, also known as CF Networking, allows direct network traffic between apps. For an overview of how container-to-container networking works, see [Container-to-container networking](https://docs.cloudfoundry.org/concepts/understand-cf-networking.html).

**Important**
Container-to-container networking is not available for apps hosted on Microsoft Windows.

## Activate container-to-container networking
Container networking is installed by default when you install Cloud Foundry using `cf-deployment`.
For instructions for using `cf-deployment`, see the [Cloud Foundry documentation](https://docs.cloudfoundry.org/deploying/cf-deployment/index.html).
Container networking has properties you can configure to change the default behavior.
The following table has a list of properties and instructions for editing them.
For more information about container networking configuration, see [Configuration Information for Operators](https://github.com/cloudfoundry/cf-networking-release/blob/develop/docs/configuration.md).
| Container-to-container networking opsfiles | Description |
| --- | --- |
|
```

- type: replace
path: /instance_groups/name=diego-cell/jobs/name=vxlan_policy_agent/properties/iptables_logging?
value: true
```
|
The default value for `iptables_logging` is `false`.
(Optional) Change the value to `true` to activate logging for Container-to-Container policy iptables rules.
|
|
```

- type: replace
path: /instance_groups/name=diego-cell/jobs/name=cni/properties/iptables_logging?
value: true
```
|
The default value for `iptables_logging` is `false`.
(Optional) Change the value to `true` to activate
logging for Application Security Group (ASG) iptables rules.
|
|
```

- type: replace
path: /instance_groups/name=diego-api/jobs/name=silk-controller/properties/network?
value: REPLACE-WITH-OVERLAY-NETWORK-CIDR
```
|
(Optional) Enter an IP range for the overlay network. The CIDR must specify an RFC 1918 range. If you do not set a custom range, the deployment uses `10.255.0.0/16`.
See [App Instance Communication](https://docs.cloudfoundry.org/concepts/understand-cf-networking.html#app-comm) for more information.
|
|
```

- type: replace
path: /instance_groups/name=diego-cell/jobs/name=cni/properties/mtu?
value: REPLACE-WITH-MTU
```
(Optional) You can manually configure the Maximum Transmission Unit (MTU) value to support additional encapsulation overhead.
| |
To see how container networking works with and without service discovery, see [Cats and Dogs with Service Discovery](https://github.com/cloudfoundry/cf-networking-examples/blob/master/docs/c2c-with-service-discovery.md) in GitHub. In this tutorial, you deploy two apps and create a Container-to-Container Networking policy that allows them to communicate directly with each other.

## Configure the overlay network
Container-to-container networking uses an overlay network to manage communication between app instances.
By default, each Diego Cell in the overlay network is allocated a /24 range that supports 254 containers per cell, one container for each of the usable IP addresses, `.1` through `.254`.
For more information about the overlay network, see [Overlay network](https://docs.cloudfoundry.org/concepts/understand-cf-networking.html#overlay-network) in *Container-to-container networking*.

### Configure the number of Diego Cells
To change the number of Diego Cells supported by the overlay network in your Cloud Foundry deployment, edit the `cf_networking.network` property in your `cf-networking-release` manifest, and then re-deploy Cloud Foundry. See the following examples:
| Overlay subnet mask | Number of cells | Containers per cell |
| --- | --- | --- |
| /20 | 15 | 254 |
| /16 | 255 | 254 |
| /12 | 4,095 | 254 |

**Caution**
The overlay network IP address range must not conflict with any other IP addresses in the network. If a conflict exists, Diego Cells cannot reach any endpoint that has a conflicting IP address.

### Configure the number of containers per cell
To change the number of containers per Diego Cell in your Cloud Foundry deployment, edit the `cf_networking.subnet_prefix_length` property in your `cf-networking-release` manifest, and then re-deploy Cloud Foundry. See the following examples:
| Overlay subnet mask | Number of cells | Cell prefix length | Containers per cell |
| --- | --- | --- | --- |
| /16 | 255 | /24 | 254 |
| /16 | 255 | /26 | 62 |
| /16 | 255 | /28 | 14 |

## Manage logging for container-to-container networking
This section describes how to configure logging for container-to-container Networking events by making requests to the running virtual machines (VMs).
You can also activate logging for iptables policy rules by editing the manifest in [Activate on an IaaS](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html#iaas).

### Change log level for debugging
By default, the Policy Server logs events at the `INFO` level.
You can get more information about events by increasing the log level to `DEBUG`.
To change the log level, follow these steps:

1. SSH to either the Policy Server or the VXLAN Policy Agent.

* **Policy Server**: SSH directly to the Policy Server VM.

* **VXLAN Policy Agent**: SSH to the Diego Cell that runs the VXLAN Policy Agent.

2. To change the log level, run:
```
curl -X POST -d 'LOG-LEVEL' localhost:PORT-NUMBER/log-level
```
The `LOG-LEVEL` is `DEBUG` or `INFO`. The `PORT-NUMBER` is `22222` unless you specified a different number when you edited the stub file in [Activate on an IaaS](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html#iaas).
To increase the log level to `DEBUG`, run:
```
$ curl -X POST -d 'DEBUG' localhost:22222/log-level
```
To decrease the log level to `INFO`, run:
```
$ curl -X POST -d 'INFO' localhost:22222/log-level
```

3. The logs are available in:

* **Policy Server**: `/var/vcap/sys/log/policy-server/policy-server.stdout.log`

* **VXLAN Policy Agent**: `/var/vcap/sys/log/vxlan-policy-agent/vxlan-policy-agent.stdout.log`

### Activate logging for container-to-container networking policies
By default, Cloud Foundry does not log iptables policy rules for Container-to-Container network traffic. You can activate logging for iptables policy rules in the manifest in [Activate on an IaaS](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html#iaas), or use following the steps:

1. SSH to the Diego Cell that runs the VXLAN Policy Agent.

2. To change the log level, run:
```
curl -X PUT -d '{"enabled": BOOLEAN}' localhost:PORT-NUMBER/iptables-c2c-logging
```
The `BOOLEAN` is `true` or `false`. The `PORT-NUMBER` is `22222` unless you specified a different number when you edited the stub file in [Activate on an IaaS](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html#iaas).
To activate logging for iptables policy rules, run:
```
$ curl -X PUT -d '{"enabled": true}' localhost:22222/iptables-c2c-logging
```
To deactivate logging for iptables policy rules, run:
```
$ curl -X PUT -d '{"enabled": false}' localhost:22222/iptables-c2c-logging
```

3. Find the logs in `/var/log/kern.log`.

### Use metrics to consume logs
You can stream container-to-container networking component metrics with the [Loggregator Firehose](https://docs.cloudfoundry.org/loggregator/architecture.html#firehose).
Container-to-container networking logs use the following prefixes:

* `netmon`

* `vxlan_policy_agent`

* `policy_server`

## Create and manage networking policies
This section describes how to create and edit container-to-container networking policies using the Cloud Foundry Command Line Interface (cf CLI).

### Prerequisites
Ensure that you are using cf CLI v6.42 or later:
```
$ cf version
```
For more information about updating the cf CLI, see [Installing the cf CLI](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html).

### Grant permissions
Cloud Foundry admins use the following UAA scopes to grant specific users or groups permissions to configure network policies:
| UAA Scope | Suitable for… | Allows users to create policies… |
| --- | --- | --- |
| `network.admin` | operators | for any apps in the Cloud Foundry deployment |
| `network.write` | space developers | for apps in spaces that they can access |
If you are a Cloud Foundry admin, you already have the `network.admin` scope. An admin can also grant the `network.admin` scope to a space developer.
For more information, see [Creating and Managing Users with the UAA CLI (UAAC)](https://docs.cloudfoundry.org/uaa/uaa-user-management.html) and [Orgs, Spaces, Roles, and Permissions](https://docs.cloudfoundry.org/concepts/roles.html).
To grant all Space Developers permissions to configure network policies, edit your BOSH manifest to include the `enable_space_developer_self_service` property in the [cf-networking-release policy-server job](https://github.com/cloudfoundry/cf-networking-release/blob/master/jobs/policy-server/spec) and set that property to `true`.
By default, Space Developers can add a maximum of 150 network policies per
source app.
Operators can change this limit by changing the `max_policies_per_app_source` property in the policy-server job in
the Cloud Foundry deployment manifest.
This limit does not apply to users with the network.admin scope.

### Add a network policy
To add a policy that allows direct network traffic from one app to another, run:
```
cf add-network-policy SOURCE-APP DESTINATION-APP -s DESTINATION-SPACE-NAME -o DESTINATION-ORG-NAME --protocol (tcp | udp) --port RANGE
```
Where:

* `SOURCE-APP` is the name of the app that sends traffic.

* `DESTINATION-APP` is the name of the app that receives traffic.

* `DESTINATION-SPACE-NAME` is the space of the destination app. The default is the targeted space.

* `DESTINATION-ORG-NAME` is the org of the destination app. The default is the targeted org.

* `PROTOCOL` is either: `tcp` or `udp`.

* `RANGE` contains the ports at which to connect to the destination app. The allowed range is from `1` to `65535`. You can specify a single port, such as `8080`, or a range of ports, such as `8080-8090`. Port 61443 is used for TLS communication.
Use the `add-network-policy` command to allows access from the `frontend` app to the `backend` app over TCP at port 8080. Here is an example:
```
$ cf add-network-policy frontend backend --protocol tcp --port 8080
Adding network policy to app frontend in org my-org / space dev as admin...
OK
```
The maximum number of policies that a Space Developer can add in a space is set by the `max_policies_per_app_source` property in the `policy-server` job in the Cloud Foundry deployment manifest. By default, the maximum is 150.
This limit does not apply to users with the `network.admin` scope.
To change the network policy quota for Space Developers, the Cloud Foundry operator must configure the `max_policies_per_app_source` property, then re-deploy Cloud Foundry.

### List policies
You can list all the policies in your space, or just the policies for which a single app is the source:

* To list the all the policies in your space, run `cf network-policies`.
```
$ cf network-policies
```

* To list the policies for an app, run `cf network-policies --source MY-APP`. Replace `MY-APP` with the name of your app.
```
$ cf network-policies --source example-app
```
The following example of the `network-policy` command lists policies for the app `frontend`:
```
$ cf network-policies --source frontend
Listing network policies in org my-org / space dev as admin...
source destination protocol ports destination space destination org
frontend backend tcp 8080 example-space example-org
```

### Remove a network policy
To remove a policy that allows direct network traffic from an app, run:
```
cf remove-network-policy SOURCE-APP DESTINATION-APP -s DESTINATION-SPACE-NAME -o DESTINATION-ORG-NAME --protocol PROTOCOL --port RANGE
```
Where:

* `SOURCE-APP` is the name of the app that sends traffic.

* `DESTINATION-APP` is the name of the app that receives traffic.

* `DESTINATION-SPACE-NAME` is the space of the destination app. The default is the targeted space.

* `DESTINATION-ORG-NAME` is the org of the destination app. The default is the targeted org.

* `PROTOCOL` is either `tcp` or `udp`.

* `PORTS` are the ports connecting the apps. The allowed range is from `1` to `65535`. You can specify a single port, such as `8080`, or a range of ports, such as `8080-8090`.
The `remove-network-policy` command deletes the policy that allows the `frontend` app to communicate with the `backend` app over TCP on port 8080. Here is an example:
```
$ cf remove-network-policy frontend backend --protocol tcp --port 8080
Removing network policy to app frontend in org my-org / space dev as admin...
OK
```

### Deactivate network policy enforcement
You can deactivate Silk network policy enforcement between apps. Deactivating network policy enforcement allows all apps to send network traffic to all other apps in the foundation despite no policy specifically allowing it.
To deactivate network policy enforcement between apps:

1. To target your BOSH deployment, run:
```
bosh target -e MY-ENV -d MY-DEPLOYMENT
```
Where:

* `MY-ENV` is the alias you set for your BOSH Director.

* `MY-DEPLOYMENT` is your deployment name. You can see your deployment name by running `bosh -e MY-ENV deployments`.

2. To download and save the BOSH manifest, run:
```
bosh -e MY-ENV -d MY-DEPLOYMENT manifest > MY-MANIFEST.yml
```
Where `MY-MANIFEST.yml` is the name you choose for the saved manifest.

3. In your BOSH manifest, change the `disable_container_network_policy` value to `false`.

4. To redeploy BOSH using the edited BOSH manifest, run:
```
bosh -e MY-ENV -d MY-DEPLOYMENT deploy MY-MANIFEST.yml
```

## App service discovery
With app service discovery, apps pushed to Cloud Foundry can establish container-to-container communications through a known route served by internal BOSH DNS. This allows front end apps to easily connect with back end apps.

**Note** Admins can create internal domains. For more information, see the [Internal Domains](https://github.com/cloudfoundry/cf-networking-release/blob/develop/docs/app-sd.md#internal-domains) section in the `cf-networking-release` repository on GitHub.
To establish container-to-container communications between a front end and back end app, a developer:

1. Runs a back end app that publishes a local endpoint.

2. Maps a named route to the endpoint.

3. Creates a network policy that allows direct traffic from the front end to the back end app.

4. Run the front end app.
See [Cats and Dogs with Service Discovery](https://github.com/cloudfoundry/cf-networking-examples/blob/master/docs/c2c-with-service-discovery.md) in GitHub for an example, written in Go, that demonstrates communication between front end and back end apps.
To use TLS developer adds a network policy for port 61443. After that the front end app can reach the back end app using HTTPS, `https://backend-app.apps.internal:61443`, for example.

### Activate app service discovery
To activate app service discovery, include the [`enable\_service\_discovery`](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/enable-service-discovery.yml) ops file in your Cloud Foundry deployment, as described in [CF App Service Discovery](https://github.com/cloudfoundry/cf-networking-release/blob/develop/docs/app-sd.md) in the cf-networking-release repository on GitHub.