# Routing for isolation segments in Cloud Foundry
You can configure and manage routing for isolation segments in Cloud Foundry as described in this topic. You can also deploy a set of Gorouters for each isolation segment to handle requests for apps within the segment.
For more information about how isolation segments work, see [Isolation Segments](https://docs.cloudfoundry.org/concepts/security.html#isolation-segments) in *Cloud Foundry Security*. For more information about creating isolation segments, see [Managing Isolation Segments](https://docs.cloudfoundry.org/adminguide/isolation-segments.html).
The instructions in this topic assume you are using Google Cloud Platform (GCP). The procedures can differ on other IaaSes, but the
concepts must be transferable.

## Isolation segments overview
Isolation segments isolate the compute resources for one group of apps from another. However, these apps still share the same network resources. Requests for apps on all isolation segments, as well as for system components, transit the same load balancers, Cloud Foundry Gorouters, and Cloud Foundry TCP Routers.
When you use isolation segments, Cloud Foundry designates its Diego Cells as belonging to an isolation segment called `shared`. This isolation segment is the default isolation segment assigned to every org and space. This can be overwritten by assigning an explicit default for an organization. For more information about creating isolation segments, see [Managing Isolation Segments](https://docs.cloudfoundry.org/adminguide/isolation-segments.html).
The following illustration shows isolation segments sharing the same network resources:
![Diagram shows two isolation segments that share Gorouter, TCP Router, load balancer, and other CF components.](https://docs.cloudfoundry.org/adminguide/images/routing-is.png)
The two isolation segments each contain a single Diego Cell. These isolation segments use the same Gorouter, TCP Router, and load balancers.
Operators who want to prevent all isolation segments and system components from using the same network resources can deploy an additional set of Gorouters for each isolation segment:
![Diagram shows a set of Gorouters deployed for each isolation segment, while sharing other network resources.](https://docs.cloudfoundry.org/adminguide/images/is-distinct-domains.png)
The two isolation segments each use separate Gorouters and Diego Cells. However, the use of an isolated TCP router in this scenario is not supported.
Use cases include:

* Requests for apps in an isolation segment must not share networking resources with requests for other apps.

* The Cloud Foundry management plane can only be accessible from a private network. As multiple IaaS load balancers cannot typically share the same pool of back ends, such as Cloud Foundry Gorouters, each load balancer requires an additional deployment of Gorouters.

## Step 1: Create networks
Create a network or subnet for each isolation segment on your infrastructure. For example, an operator who wants one isolation segment separated from their Cloud Foundry Diego Cells could create one network named `sample-network` with two subnets named `sample-subnet-cf` and `sample-subnet-is1`.
The following diagram describes the network topology:
```
IaaS network: sample-network
|
|_____ IaaS subnet: sample-subnet-cf
|
|_____ IaaS subnet: sample-subnet-is1
```
Subnets do not generally span IaaS availability zones (AZs), so the same operator with two AZs needs four subnets.
```
IaaS network: sample-network
|
|_____ IaaS subnet: sample-subnet-cf-az1
|
|_____ IaaS subnet: sample-subnet-cf-az2
|
|_____ IaaS subnet: sample-subnet-is1-az1
|
|_____ IaaS subnet: sample-subnet-is1-az2
```
For more information about networks and subnets in GCP, see [Using Networks and Firewalls](https://cloud.google.com/compute/docs/networking) in the GCP documentation.

## Step 2: Configure networks for Gorouters
To configure the subnets with BOSH, use BOSH cloud config subnets. Each subnet in the IaaS must correspond to a BOSH subnet that is labeled with the correct isolation segment. For more information, see [Usage](https://bosh.io/docs/cloud-config.html) in the BOSH documentation.
These are examples of cloud config for GCP and AWS for the four example subnets described in [Step 1: Create Networks](https://docs.cloudfoundry.org/adminguide/routing-is.html#create-networks).

### GCP Cloud Config
```
azs:

- name: z1
cloud_properties:
zone: us-east1-b

- name: z2
cloud_properties:
zone: us-east1-c

- name: z3
cloud_properties:
zone: us-east1-b

- name: z4
cloud_properties:
zone: us-east1-c
networks:

- name: default
type: manual
subnets:

- range: 10.0.0.0/16
gateway: 10.0.0.1
reserved:

- 10.0.16.2-10.0.16.3

- 10.0.31.255
static:

- 10.0.31.190-10.0.31.254
<strong>az: z1</strong>
cloud_properties:
ephemeral_external_ip: true
<strong>network_name: sample-network</strong>
<strong>subnetwork_name: sample-subnet-cf-az1</strong>
tags:

- <strong>sample-cf-is</strong>

- range: 10.1.16.0/20
gateway: 10.1.16.1
reserved:

- 10.1.16.2-10.1.16.3

- 10.1.31.255
static:

- 10.1.31.190-10.1.31.254
<strong>az: z2</strong>
cloud_properties:
ephemeral_external_ip: true
<strong>network_name: sample-network</strong>
<strong>subnetwork_name: sample-subnet-cf-az2</strong>
tags:

- <strong>sample-cf-is</strong>

- range: 10.0.200.0/28
gateway: 10.0.200.1
reserved:

- 10.0.200.2-10.0.200.3

- 10.0.200.15
static:

- 10.0.200.11-10.0.200.15
<strong>az: z3</strong>
cloud_properties:
ephemeral_external_ip: true
<strong>network_name: sample-network</strong>
<strong>subnetwork_name: sample-subnet-is1-az1</strong>
tags:

- <strong>sample-is1</strong>

- range: 10.1.200.0/28
gateway: 10.1.200.1
reserved:

- 10.1.200.2-10.1.200.3

- 10.1.200.15
static:

- 10.1.200.11-10.1.200.15
<strong>az: z4</strong>
cloud_properties:
ephemeral_external_ip: true
<strong>network_name: sample-network</strong>
<strong>subnetwork_name: sample-subnet-is1-az2</strong>
tags:

- <strong>sample-is1</strong>
```

### AWS cloud config
AWS networking requires security groups, which need to be created separately. In the following example, the operator must create the **sample-cf-is** and **sample-is1** security groups.
```
azs:

- name: z1
cloud_properties:
zone: us-east1-b

- name: z2
cloud_properties:
zone: us-east1-c

- name: z3
cloud_properties:
zone: us-east1-b

- name: z4
cloud_properties:
zone: us-east1-c
networks:

- name: default
type: manual
subnets:

- range: 10.0.0.0/16
gateway: 10.0.0.1
reserved:

- 10.0.16.2-10.0.16.3

- 10.0.31.255
static:

- 10.0.31.190-10.0.31.254
<strong>az: z1</strong>
cloud_properties:
security_groups:

- <strong>sample-cf-is</strong>

# with bbl, there is also a cf internal security group
subnet: <strong>sample-subnet-cf-az1</strong>

- range: 10.1.16.0/20
gateway: 10.1.16.1
reserved:

- 10.1.16.2-10.1.16.3

- 10.1.31.255
static:

- 10.1.31.190-10.1.31.254
<strong>az: z2</strong>
cloud_properties:
security_groups:

- <strong>sample-cf-is</strong>

# with bbl, there is also be a cf internal security group
subnet: <strong>sample-subnet-cf-az2</strong>

- range: 10.0.200.0/28
gateway: 10.0.200.1
reserved:

- 10.0.200.2-10.0.200.3

- 10.0.200.15
static:

- 10.0.200.11-10.0.200.15
<strong>az: z3</strong>
cloud_properties:
security_groups:

- <strong>sample-is1</strong>
subnet: <strong>sample-subnet-is1-az1</strong>

- range: 10.1.200.0/28
gateway: 10.1.200.1
reserved:

- 10.1.200.2-10.1.200.3

- 10.1.200.15
static:

- 10.1.200.11-10.1.200.15
<strong>az: z4</strong>
cloud_properties:
security_groups:

- <strong>sample-is1</strong>
subnet: <strong>sample-subnet-is1-az2</strong>
```

## Step 3: Configure additional Gorouters
You must edit the BOSH deployment manifest to include an instance group for each set of Gorouters.
The sample BOSH manifest snippet has an additional instance group for the isolated Gorouters, associated with the isolated BOSH AZs. As a result, Gorouter instances are configured with IP addresses from the isolated subnets. For more information about BOSH manifests, see [Deployment Config](https://bosh.io/docs/manifest-v2.html) in the BOSH documentation.
For a high-availability deployment, assign each instance group to at least two BOSH AZs that correspond to different IaaS AZs. Use at
least two instances of each instance group.
When you deploy with a BOSH v2-style manifest that leverages `instance_groups`, you must enable UAA to
differentiate between links exported by the Gorouters, as it only accepts connections from one instance group of Gorouters.
As you can have multiple isolation segments, Cloud Foundry recommends renaming the instance group used for the system domain.
You must also to specify the name of the link from which UAA consumes the link.
```
instance_groups:

- name: router
instances: 2
azs: [z1,z2]
networks:

- name: default
jobs:

- name: gorouter
provides:
gorouter: {as: router_primary}

- name: uaa
jobs:

- name: uaa
consumes:
router: {from: router_primary}

- name: router-is1
instances: 2
azs: [z3,z4]
networks:

- name: default

- name: cell-is1
instances: 2
azs: [z3,z4]
networks:

- name: default
```

## Step 4: Add Gorouters to load balancer
For some IaaSes such as AWS and GCP, the BOSH cloud config and deployment manifest can be used to instruct BOSH to add Gorouters to the IaaS load balancers automatically. For others, operators must assign static IPs to the Gorouters in the manifest and assign these IPs to the load balancers out of band.
To automatically add load balancers to Gorouters, the `vm_extensions` property is available in BOSH manifests. For example:
```
instance_groups:

- name: router-is1
instances: 2
azs: [z3,z4]
networks:

- name: default
vm_extensions:

- cf-router-sample-is1-network-properties
```
The `vm_extension` is IaaS-specific and defined in the cloud config. This is an example AWS cloud config:
```
vm_extensions:

- name: cf-router-sample-is1-network-properties
elbs: [sample-is1-elb]
security_groups:

- sample-is1

- cf-router-lb-security-group # to allow traffic to the load balancer
```
The load balancer `sample-is1-elb` must be created separately.
If necessary, configure a firewall rule to allow traffic from your load balancer to the Gorouters.

## Step 5: Configure DNS and load balancers
Create a separate domain name for each Gorouter instance group, and configure DNS to resolve these domain names to a load balancer that routes requests to the matching Gorouters.
You must configure your load balancers to forward requests for a given domain to one Gorouter instance group only.
As Gorouter instance groups might be responsible for separate isolation segments, and an app might be deployed to only one isolation segment, requests can only reach a Gorouter that has access to the apps for that domain name. Load balancing requests for a domain across more than Gorouter instance group can result in request failures unless all the Gorouter instance groups have access to the isolation segments where apps for that domain are deployed.

### Shared domain name
It is a common requirement for apps on separate isolation segments to be accessible at domain names that share a domain. For example, `private-domain.com`. To achieve this configuration while also obeying the guideline for forwarding requests for a domain to only one Gorouter instance group, create a new Cloud Foundry domain for a needed subdomain, such as `*.foo.private-domain.com.`
The diagrams illustrate a topology with separate load balancers, but you could also use one load balancer with multiple interfaces.
In this configuration:

* Requests for system domain `*.cf-system.com` and the shared domain `*.shared-apps.com` are forwarded to the Gorouters for the Cloud Foundry Diego Cells.

* Requests for private domain `*.foo.private-domain.com` are forwarded to the Gorouters for IS1. Requests for private domain `*.private-domain.com` are forwarded to the Gorouters for IS2.
![Diagram showing an example shared domain.](https://docs.cloudfoundry.org/adminguide/images/is-sharing-domains.png)
The example has three isolation segments and three Gorouters.
The three isolation segments each use separate Gorouters and load balancers.

## Step 6: Configure firewall rules
Configure firewall rules to allow for necessary ingress and egress traffic for isolation segments and Cloud Foundry Diego Cells. Assuming a default deny-all rule, properly configuring firewall rules prevents a request with a spoofed Host header from being forwarded by a Gorouter to an app in a different isolation segment.
Firewall rules are specific to each IaaS, so the exact definition of `Source` and `Destination` depends on the IaaS. For example:
\* On GCP, a `Source` is a subnet and a `Destination` is a tag.
\* On AWS, both `Source` and `Destination` are security groups.
To configure firewall rules for isolation segment traffic:

1. Configure the firewall rules in the table below:
For information about the processes that use these ports and their corresponding manifest properties, see
[Port Reference Table](https://docs.cloudfoundry.org/adminguide/routing-is.html#port-reference).
| Rule Name | Source | Allowed Protocols/Ports | Destination | Reason |
| --- | --- | --- | --- | --- |
| `cf-to-bosh` | Cloud Foundry Diego Cells | `tcp:4222, 25250, 25777` | BOSH Director | BOSH Agent on VMs in the Cloud Foundry Diego Cells to reach BOSH Director |
| `cf-internal` | Cloud Foundry Diego Cells | `tcp:any, udp:any, icmp:any` | Cloud Foundry Diego Cells | VMs within the Cloud Foundry Diego Cells to reach one another |
| `cf-to-is1` | Cloud Foundry Diego Cells | `tcp:1801, 8853, 53035` | Isolation segment | Diego BBS in Cloud Foundry Diego Cells to reach Diego Cells in isolation segment |
| `is1-to-bosh` | Isolation segment | `tcp:4222, 25250, 25777` | BOSH Director | BOSH Agent on VMs in isolation segment to reach BOSH Director |
| `is1-internal` | Isolation segment | `tcp:all, udp:all, icmp:all` | Isolation segment | VMs within isolation segment to reach one another |
| `is1-to-cf` | Isolation segment | `tcp:3000, 3001, 4003, 4103, 4222, 4224, 4443, 6067, 8080, 8082, 8083, 8443, 8447, 8844, 8853, 8889, 8891, 9000, 9022, 9023, 9090, 9091` | Cloud Foundry Diego Cells | Diego Cells in isolation segment to reach Diego BBS, Diego Auctioneer, and CredHub in Cloud Foundry. Loggregator Agent to reach Doppler. Syslog Agent to reach Log Cache Syslog Server. Gorouters to reach NATS, UAA, and Routing API. Metrics Discovery Registrar to reach NATS. |

2. (Optional) Configure the firewall rules in the following table:
| Rule Name | Source | Allowed Protocols/Ports | Destination | Reason |
| --- | --- | --- | --- | --- |
| `jumpbox-to-is1` | Jumpbox VM | `tcp:22` | Isolation segment | Jumpbox VMs to reach isolation segment through SSH or BOSH SSH. |
| `diego-cell-egress` | Diego Cell VM on isolation segment | `tcp:any, udp:any` | Internet | If Diego Cells must download buildpacks to stage apps, allow egress traffic from all Diego Cell VMs on isolation segments to reach the Internet. |
Additional firewall rules might be necessary to allow logs to egress to application syslog drains. Connections for syslog drains are initiated both from Diego Cells and
Routers.
For more information about ports used by agents to communicate with BOSH, see the [bosh-deployment](https://github.com/cloudfoundry/bosh-deployment) repository on GitHub.
For more information about networks and firewall rules for GCP, see [Using Subnetworks](https://cloud.google.com/compute/docs/subnetworks) in the GCP documentation.

### Port Reference Table
To understand which protocols and ports map to which processes and manifest properties for the preceding rules, see the following table:
| Protocol | Port | Process | Manifest Property |
| --- | --- | --- | --- |
| `tcp` | `1801` | Diego Rep | `diego.rep.listen_addr_securable` |
| `tcp` | `3000` | Routing API | `routing_api.port` |
| `tcp` | `3001` | Routing API | `routing_api.mtls_port` |
| `tcp` | `4003` | VXLAN Policy Agent | `cf_networking.policy_server.internal_listen_port` |
| `tcp` | `4103` | Silk Controller | `cf_networking.silk_controller.listen_port` |
| `tcp` | `4222` | NATS | `nats.nats.port` |
| `tcp` | `4224` | NATS | `nats-tls.nats.port` |
| `tcp` | `4443` | CAPI Blobstore Port - HTTPS | `capi.blobstore.tls.port` |
| `tcp` | `6067` | Log Cache Syslog Server | `log-cache.log-cache-syslog-server.syslog_port` |
| `tcp` | `8080` | CAPI Blobstore Port - HTTP, Diego file server - HTTP | `capi.blobstore.port, diego.file_server.listen_addr` |
| `tcp` | `8082` | Doppler gRPC, Reverse Log Proxy Gateway | `loggregator.doppler.grpc_port, loggregator.reverse_log_proxy.egress.port` |
| `tcp` | `8083` | Log Cache cf-auth-proxy | `log-cache.log-cache-cf-auth-proxy.proxy_port` |
| `tcp` | `8084` | Diego file server - HTTP | `diego.file_server.listen_addr` |
| `tcp` | `8443` | UAA | `uaa.uaa.ssl.port` |
| `tcp` | `8447` | Diego file server - HTTPS | `diego.file_server.https_listen_addr` |
| `tcp` | `8844` | CredHub | `credhub.credhub.port` |
| `tcp` | `8853` | BOSH DNS health | `health.server.port` from `bosh-dns-release` |
| `tcp` | `8889` | Diego BBS | `diego.rep.bbs.api_location` |
| `tcp` | `8891` | Diego Database (Locket) | `diego.locket.listen_addr` |
| `tcp` | `9000` | Loggregator Syslog Binding Cache | `loggr-syslog-binding-cache.external_port` |
| `tcp` | `9022` | Cloud Controller Stager | `capi.stager.cc.external_port` |
| `tcp` | `9023` | Cloud Controller TPS | `capi.tps.cc.external_port` |
| `tcp` | `9090` | Cloud Controller Uploader | `capi.cc_uploader.http_port` |
| `tcp` | `9091` | Cloud Controller Uploader | `capi.cc_uploader.https_port` |
| `tcp` | `53035` | System Metrics Scraper | `system-metrics-scraper.loggr-system-metric-scraper.scrape_port` |
| `tcp` | `25250` | BOSH Blobstore | `bosh.blobstore.port` |
| `tcp` | `25777` | BOSH Registry | `bosh.registry.port` |

## Additional GCP information
For more information, see [Understanding backend services](https://cloud.google.com/compute/docs/load-balancing/http/backend-service) in the GCP documentation and the [BOSH Google CPI Release](https://github.com/cloudfoundry-incubator/bosh-google-cpi-release/tree/master/src/bosh-google-cpi) repository on GitHub.

## Sharding Gorouters for isolation segments
To provide security guarantees in addition to the firewall rules previously described, an operator can configure sharding of the Gorouter’s routing table, resulting in a Gorouter dedicated for an isolation segment having knowledge only of routes for apps in the same isolation segment. The flexibility of the configuration also supports deployment of a Gorouter that is responsible for multiple isolation segments, or that excludes all isolation segments.

### Configure Gorouters for sharding
You can configure Gorouters for sharding using two manifest properties, `routing_table_sharding_mode` and `isolation_segments`.
The three supported values of `routing_table_sharding_mode` are `all`, `cf-and-segments`, and `segments`.

* `all`: All routes are registered. This is the default mode to preserve the Gorouter’s existing behavior.

* `cf-and-segments`: Both routes configured with manifest property `isolation_segments` and routes without an isolation segment specified are registered.

* `segments`: Only routes for the configured isolation segments are registered.
You can provide a list of isolation segments using the manifest property `isolation_segments`.
The following table describes the behaviors that you can achieve with these two properties:
| Sharding Mode | Isolation Segments | Routes Registered |
| --- | --- | --- |
| `all` | `none` | All routes. |
| `all` | `provided` | All routes. |
| `cf-and-segments` | `none` | Routes that are not associated with an isolation segment. |
| `cf-and-segments` | `provided` | Routes that are not associated with an isolation segment, as well as routes for the specified isolation segments. Routes for other isolation segment are excluded. |
| `segments` | `none` | Invalid combination. Deploy fails. |
| `segments` | `provided` | Routes for specified isolation segments only. |
For example, the following configuration in a deployment manifest describes a deployment with one Gorouter in the Cloud Foundry Diego Cells and another Gorouter in a separate isolation segment `is1`:
```
jobs:

- name: router_cf
properties:
router:
isolation_segments: []
routing_table_sharding_mode: cf-and-segments
...

- name: router_is1
properties:
router:
isolation_segments:

- is1
routing_table_sharding_mode: segments
```
The `router_cf` Gorouter registers all routes that do not have an `isolation_segment` value. The `router_is1` Gorouter only registers routes that have an `isolation_segment` value of `is1`.

## Metrics for Gorouters associated with isolation segments
For metrics emitted by the Gorouter, metrics can be distinguished by the name of the job. For example, this line is a metric emitted on `uptime`:
```
origin:"gorouter" eventType:ValueMetric timestamp:1491338040750977602 deployment:"superman.cf-app.com" job:"router_is1" index:"9a4b639c-8f0e-4b2b-b332-4161ee4646e6" ip:"10.0.16.23" valueMetric:<name:"uptime" value:118 unit:"seconds" >
```