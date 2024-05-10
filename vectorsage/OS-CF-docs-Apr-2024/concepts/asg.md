# App security groups in Cloud Foundry
App Security Groups (ASGs) are a collection of egress rules that enable you to specify the protocols,
ports, and IP address ranges where app or task instances send traffic.
ASGs define **allow** rules, and their order of evaluation is unimportant when multiple ASGs apply to the same space or deployment. The platform sets up rules to filter and log outbound network traffic
from app and task instances. ASGs apply to both buildpack-based and Docker-based apps and tasks.

## Staging and running ASGs
Admins can define a `staging` ASG for app and task staging, and a `running` ASG for app and task runtime.
When apps or tasks begin staging, they require traffic rules permissive enough to allow
them to pull resources from the network. A running app or task no longer needs to pull resources,
so traffic rules can be more restrictive and secure.
To distinguish between these two security requirements, you can define a `staging` ASG for app and task
staging with more permissive rules, and a `running` ASG for app and task runtime with less permissive rules.

### Platform wide and space scoped ASGs
To provide granular control when securing a deployment, you can assign platform-wide ASGs that apply
to all app and task instances for the entire deployment, or space-scoped ASGs that apply only to apps and tasks in a particular space.
In environments with both platform-wide and space-specific ASGs, the ASGs for a particular space are combined with the platform ASGs to determine the effective rules for that space. Any of the
permitted traffic in the set of applicable ASGs is then effectively permitted for that app.

### Dynamic ASGs
Dynamic ASGs allow ASGs to be applied to apps without the need for an application restart. Containers using the [Silk CNI](https://github.com/cloudfoundry/silk-release) or NSX-T update their ASGs dynamically; Windows apps and apps using other CNIs do not support Dynamic ASGs at this time.
Dynamic ASGs are enabled with cf deployment v20.0.0 and higher through [cf-networking-release 3.0.0](https://github.com/cloudfoundry/cf-networking-release/releases/tag/3.0.0). It is recommended to use Dynamic ASGs with capi-release v1.126.0 or later for improved
performance on the /v3/security\_groups APIs.
To deactivate Dynamic ASGs: use the ops file `operations/disable-dynamic-asgs.yml` from [cf-deployment v20.0.0](https://github.com/cloudfoundry/cf-deployment/releases/tag/v20.0.0) or higher.

### Simplifying ASGs with a services subnet
ASGs can be complicated to configure correctly, especially when the specific IP addresses listed in a group change.
To simplify securing a deployment while still allowing apps reach external services, operators can deploy the services into a subnet that is separate from their Cloud Foundry deployment, then create ASGs
for the apps that allow those service subnets, while denying access to any VM hosting other apps.
For examples of typical ASGs, see [Typical ASGs](https://docs.cloudfoundry.org/concepts/asg.html#typical-groups).

### Default ASGs
Cloud Foundry preconfigures two ASGs: `public_networks` and `dns`.
Unless you modify these before your initial deployment, these ASGs are applied by default to all containers in your deployment.

* `public_networks`: This group allows access to public networks, and blocks access to private networks and link local addresses. Cloud
Foundry blocks outgoing traffic to the following IP address ranges by specifically allowing traffic to all other addresses:

+ 10.0.0.0 - 10.255.255.255

+ 169.254.0.0 - 169.254.255.255

+ 172.16.0.0 - 172.31.255.255

+ 192.168.0.0 - 192.168.255.255

* `dns`: This group allows access to DNS on port 53 for any IP address. The default ASGs are defined in the `cf-deployment.yml` file as follows:
```
security_group_definitions:

- name: public_networks
rules:

- destination: 0.0.0.0-9.255.255.255
protocol: all

- destination: 11.0.0.0-169.253.255.255
protocol: all

- destination: 169.255.0.0-172.15.255.255
protocol: all

- destination: 172.32.0.0-192.167.255.255
protocol: all

- destination: 192.169.0.0-255.255.255.255
protocol: all

- name: dns
rules:

- destination: 0.0.0.0/0
ports: '53'
protocol: tcp

- destination: 0.0.0.0/0
ports: '53'
protocol: udp
```
Modify the default ASGs to block outbound traffic as necessary for your installation. To see how the ASGs are defined by
default, see the [cf-deployment.yml](https://github.com/cloudfoundry/cf-deployment/blob/main/cf-deployment.yml#L604-L627) file on GitHub.

### ASG sets
ASGs are applied by configuring ASG sets differentiated by *scope*, platform-wide or space specific, and *lifecycle*, staging or running.
Currently, the following ASG sets exist in Cloud Foundry:

* Platform-wide staging ASG set, also called “default-staging”

* Platform-wide running ASG set, also called “default-running”

* Space-scoped staging ASG set

* Space-scoped running ASG set
In environments with both platform-wide and space-specific ASG sets, combine the ASG sets for a
particular space with the platform ASG sets to determine the rules for that space.
The following table indicates the differences between the four sets:
| When an ASG is bound to the… | the ASG rules are applied to… |
| --- | --- |
| Platform-wide staging ASG set | the staging lifecycle for all apps and tasks. |
| Platform-wide running ASG set | the running lifecycle for all app and task instances. |
| Space-scoped staging ASG set | the staging lifecycle for apps and tasks in a particular space. |
| Space-scoped running ASG set | the running lifecycle for app and task instances in a particular space. |
Typically, ASGs applied during the staging lifecycle are more permissive than the ASGs applied during the running lifecycle. This is because staging often requires access to different resources, such as dependencies.
You use different commands to apply an ASG to each of the four sets.
To apply a staging ASG to apps within a space, you must use
cf CLI v6.28.0 or later.
For more information, see [Managing ASGs with the cf CLI](https://docs.cloudfoundry.org/concepts/asg.html#procedures).

### Structure and attributes of ASGs
ASG rules are specified as a JSON array of ASG objects. An ASG object has the following attributes:
| Attribute | Description | Notes |
| --- | --- | --- |
| `protocol` | `tcp`, `udp`, `icmp`, or `all` | Required |
| `destination` | A single IP address, an IP address range like `192.0.2.0-192.0.2.50`, or a CIDR block that can receive traffic | |
| `ports` | A single port, multiple comma-separated ports, or a single range of ports that can receive traffic. Examples: `443`, `80,8080,8081`, `8080-8081` | Only possible if `protocol` is `tcp` or `udp`. |
| `code` | ICMP code | Required when `protocol` is `icmp`. A value of `-1` allows all codes. |
| `type` | ICMP | Required when `protocol` is `icmp`. A value of `-1` allows all types. |
| `log` | Set to `true` to enable logging. For more information about how to configure system logs to be sent to a syslog drain, see [Using Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html). | Logging is only supported with protocol type `tcp`. |
| `description` | An optional field for operators managing ASG rules | |

## Managing ASGs
The following table outlines the flow of tasks that you implement over the lifecycle of ASGs.
For information about procedures for each of these tasks, see [Managing ASGs with cf CLI](https://docs.cloudfoundry.org/concepts/asg.html#procedures).
| | Task | For more information, see: |
| --- | --- | --- |
| 1. | Review the existing ASGs. If this is a new deployment, these consist of only the default ASGs. | [View ASGs](https://docs.cloudfoundry.org/concepts/asg.html#viewing) |
| 2. | Create new ASGs. | [Create ASGs](https://docs.cloudfoundry.org/concepts/asg.html#asg-individual) |
| 3. | Update the existing ASGs. | [Update ASGs](https://docs.cloudfoundry.org/concepts/asg.html#updating-groups) |
| 4. | Bind ASGs to an ASG set. | [Bind ASGs](https://docs.cloudfoundry.org/concepts/asg.html#binding-groups) |
| 5. | If you need to delete an ASG, first unbind it, then delete it. | [Unbind ASGs](https://docs.cloudfoundry.org/concepts/asg.html#unbinding-asgs) and [Delete ASGs](https://docs.cloudfoundry.org/concepts/asg.html#deleting-groups) |

## Managing ASGs with cf CLI
Learn about the commands you need to create and manage ASGs.
Many of the following procedures require the Cloud Foundry Command Line Interface (cf CLI).
To download the cf CLI, see [Installing the cf CLI](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html).

### Viewing ASGs
To view information about existing ASGs, run the following commands:
| Command | Output |
| --- | --- |
| `cf security-groups` | All ASGs |
| `cf staging-security-groups` | All ASGs applied to the platform-wide staging ASG set |
| `cf running-security-groups` | All ASGs applied to the platform-wide running ASG set |
| `cf security-group ASG` | All rules in the specified ASG, where `ASG` is the name of the ASG |

### Creating ASGs
To create an ASG:

1. Create a rules file: a JSON-formatted single array containing objects that describe the rules. See the
following example, which allows ICMP traffic of code `1` and type `0` to all destinations, and TCP traffic to `10.0.11.0/24` on ports `80` and `443`. For more information, see [The Structure and Attributes of ASGs](https://docs.cloudfoundry.org/concepts/asg.html#creating-groups).
```
[
{
"protocol": "icmp",
"destination": "0.0.0.0/0",
"type": 0,
"code": 0
},
{
"protocol": "tcp",
"destination": "10.0.11.0/24",
"ports": "80,443",
"log": true,
"description": "Allow http and https traffic to ZoneA"
}
]
```

2. Run:
```
cf create-security-group ASG PATH-TO-RULES-FILE.json
```
Where:

* `ASG` is the name of your ASG.

* `PATH-TO-RULES-FILE.json` is the absolute or relative path to a rules file.
In the following example, `EXAMPLE-ASG` is the name of an ASG, and `~/workspace/example-asg.json` is the path to a rules file:
```
cf create-security-group EXAMPLE-ASG ~/workspace/example-asg.json
```
After the ASG is created, you must bind it to an ASG set before it takes effect. For more information, see [Bind ASGs](https://docs.cloudfoundry.org/concepts/asg.html#binding-groups).

### Binding ASGs
Binding an ASG does not affect started apps unless you have [Dynamic ASGs](https://docs.cloudfoundry.org/concepts/asg.html#dynamic-asgs)
enabled. If deactivated, you need to run `cf restart` for each app. To restart all of the apps in an org or a space, use
the [app-restarter](https://github.com/cloudfoundry-incubator/app-restarter) cf CLI plug-in.
To apply an ASG, you must bind it to an ASG set.

#### Platform-wide staging ASG set
To bind an ASG to the platform wide staging ASG set:

1. Run:
```
cf bind-staging-security-group ASG
```
Where `ASG` is the name of your ASG.

#### Platform-wide running ASG set
To bind an ASG to the platform-wide running ASG set:

1. Run:
```
cf bind-running-security-group ASG
```
Where `ASG` is the name of your ASG.

#### Space-scoped running ASG set
To bind an ASG to a space-scoped running ASG set:

1. Run:
```
cf bind-security-group ASG ORG --space SPACE
```
Where:

* `ASG` is the name of your ASG.

* `ORG` is the name of the org where you want to bind the ASG set.

* `SPACE` is the name of the space where you want to bind the ASG set.

#### Space-scoped staging ASG set
To bind an ASG to a space scoped staging ASG set:

1. Run:
```
cf bind-security-group ASG ORG --space SPACE --lifecycle staging
```
Where:

* `ASG` is the name of your ASG.

* `ORG` is the name of the org where you want to bind the ASG set.

* `SPACE` is the name of the space where you want to bind the ASG set.

### Update ASGs
Updating an ASG does not affect started apps unless you have [Dynamic ASGs](https://docs.cloudfoundry.org/concepts/asg.html#dynamic-asgs)
activated. If deactivated, you need to restart the apps. To restart all of the apps in an org or a space,
use the [app-restarter](https://github.com/cloudfoundry-incubator/app-restarter) cf CLI plug-in.
To update an existing ASG:

1. Edit the ASG rules in the JSON file you created in [Create ASGs](https://docs.cloudfoundry.org/concepts/asg.html#asg-individual).

1. Run:
```
cf update-security-group ASG PATH-TO-RULES-FILE.json
```
Where:

* `ASG` is name of the existing ASG you want to change.

* `PATH-TO-RULES-FILE.json` is the absolute or relative path to a rules file.
In the following example, `example-asg` is the name of an ASG, and `~/workspace/example-asg-v2.json` is the path to a rules file:
```
cf update-security-group example-asg ~/workspace/example-asg-v2.json
```

### Unbind ASGs
Unbinding an ASG does not affect started apps unless you have [Dynamic ASGs](https://docs.cloudfoundry.org/concepts/asg.html#dynamic-asgs)
enabled. If deactivated, you need to restart the apps. To restart all of the apps in an org or a space,
use the [app-restarter](https://github.com/cloudfoundry-incubator/app-restarter) cf CLI plug-in.

#### Platform-wide staging ASG set
To unbind an ASG from the platform-wide staging ASG set:

1. Run:
```
cf unbind-staging-security-group ASG
```
Where `ASG` is the name of your ASG.

#### Platform-wide running ASG set
To unbind an ASG from the platform-wide running ASG set:

1. Run:
```
cf unbind-running-security-group ASG
```
Where `ASG` is the name of your ASG.

#### Space-scoped ASG set
To unbind an ASG from a specific space:

1. Run:
```
cf unbind-security-group ASG ORG --space SPACE --lifecycle running
```
Where:

* `ASG` is the name of your ASG.

* `ORG` is the org where you want to unbind the ASG set.

* `SPACE` is the space where you want to unbind the ASG set.

* To unbind from the staging ASG set, replace `running` with `staging`.

### Delete ASGs
You can only delete unbound ASGs. To unbind ASGs, see [Unbind ASGs](https://docs.cloudfoundry.org/concepts/asg.html#unbinding-groups).
To delete an ASG:

1. Run:
```
cf delete-security-group ASG
```
Where `ASG` is the name of your ASG.

## Typical ASGs
The following table describes examples of typical ASGs. Configure your ASGs in accordance with your organization’s network access policy for untrusted apps.
| ASG | For access to: |
| --- | --- |
| `dns` | DNS, either public or private |
| `public-networks` | Public networks, excluding IaaS metadata endpoints |
| `private-networks` | Private networks in accordance with [RFC-1918](https://tools.ietf.org/html/rfc1918#section-3) |
| `load-balancers` | The internal Cloud Foundry load balancer and others |
| `internal-proxies` | Internal proxies |
| `internal-databases` | Internal databases |

### DNS
To resolve hostnames to IP addresses, apps require DNS server connectivity, which typically use port 53. Admins must create or update a `dns` ASG with appropriate rules. Admins can further restrict the DNS servers to specific IP addresses or ranges of IP addresses.
The following is an example `dns` ASG:
```
[
{
"protocol": "tcp",
"destination": "0.0.0.0/0",
"ports": "53"
},
{
"protocol": "udp",
"destination": "0.0.0.0/0",
"ports": "53"
}
]
```

### Public networks
Apps often require public network connectivity to retrieve app dependencies, or to integrate with services available on public networks. Example app dependencies include public Maven repositories, NPM, RubyGems, and Docker registries.
You must exclude IaaS metadata endpoints. For example, `169.254.169.254`, because the
metadata endpoint can expose sensitive environment information to untrusted apps. The following `public_networks` example accounts for this recommendation.
The following is an example `public_networks` ASG:
```
[
{
"destination": "0.0.0.0-9.255.255.255",
"protocol": "all"
},
{
"destination": "11.0.0.0-169.253.255.255",
"protocol": "all"
},
{
"destination": "169.255.0.0-172.15.255.255",
"protocol": "all"
},
{
"destination": "172.32.0.0-192.167.255.255",
"protocol": "all"
},
{
"destination": "192.169.0.0-255.255.255.255",
"protocol": "all"
}
]
```

### Private networks
Network connections that are commonly allowable in private networks include endpoints such as proxy servers, Docker registries, load balancers, databases, messaging servers, directory servers, and file servers. Configure appropriate private network ASGs as appropriate. You might find it helpful to use a naming convention with `private_networks` as part of the ASG name, such as `private_networks_databases`.
You must exclude any private networks and IP addresses that app and task instances must not have access to.
The following is an example `private_networks` ASG:
```
[
{
"protocol": "tcp",
"destination": "10.0.0.0-10.255.255.255",
"ports": "443"
},
{
"protocol": "tcp",
"destination": "172.16.0.0-172.31.255.255",
"ports": "443"
},
{
"protocol": "tcp",
"destination": "192.168.0.0-192.168.255.255",
"ports": "443"
}
]
```

### ASGs and Performance on Windows
Each ASG bound to an app results in one or more network policy created on the
Host, depending on the number of destinations (ranges and CIDRs count as one
destination each). Windows apps with ASGs to many destinations will experience
increased latency when the app is starting. Windows apps with ASGs to more than
1000 destinations may fail to start.

### Marketplace Services
Each installed Marketplace Service requires its own set of ASG rules to function properly. To determine which
ASG rules it requires, see the installation instructions for each installed Marketplace Service. For more information about how to provision and integrate services, see [Services Overview](https://docs.cloudfoundry.org/devguide/services/).

## About the ASG Creator tool
The ASG Creator is a command line tool that you can use to create JSON rules files. The ASG Creator lets you specify IP addresses, CIDRs, and IP address ranges that you want to disallow traffic to, as well as the addresses that you want to allow traffic to. Based on these disallow/allow (exclude/include) lists that you provide as input, the ASG Creator formulates a JSON file of allow rules.
In turn, the JSON file is the input for the `cf create-security-group` command that creates an ASG.
To download the latest release of the ASG Creator, see the [Cloud Foundry Incubator](https://github.com/cloudfoundry-incubator/asg-creator/releases/latest) repository on GitHub.

## ASG logging
For information about how you can use ASGs to correlate emitted logs back to an app, see [How to use Application Security Group (ASG) logging](https://community.pivotal.io/s/article/How-to-use-Application-Security-Group-ASG-Logging) in the Tanzu Support Hub.