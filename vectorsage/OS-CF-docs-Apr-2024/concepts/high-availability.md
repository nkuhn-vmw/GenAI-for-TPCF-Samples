# High Availability in Cloud Foundry
This topic tells you about the components used to ensure high availability in Cloud Foundry, vertical and horizontal scaling, and the infrastructure
required to support scaling component VMs for high availability.
A system with high availability provides higher than typical uptime through redundancy of apps and component VMs. You can create the redundancy required for
high availability in several ways, such as running VMs in multiple availability zones and using external blob storage solutions.
This topic provides you guidance on configuring
your Cloud Foundry deployment for high availability.

## Components of high availability deployments
You can use availability zones, external load balancers, and
external blob storage to ensure high availability for your deployment.

### Availability zones
Availability Zones (AZs) are locations where public cloud services offer data centers.
You can assign and scale components in multiple AZs to help maintain high availability through redundancy. To configure sufficient redundancy, deploy
Cloud Foundry across three or more AZs and assign multiple component instances to different AZs.
Always use an odd number of AZs. This ensures that your deployment remains available as long as greater than half of the AZs are available.
For example, a deployment with three AZs stays available when one AZ is unavailable. A deployment with five AZs stays available when two AZs are unavailable.

### External load balancers
External load balancers distribute traffic coming from the internet to your internal network.
To ensure high availability for production environments, use a highly available customer provided external load balancing solution that does the following:

* Provides load balancing to each of the Cloud Foundry router IP addresses.

* Supports SSL termination with wildcard DNS location.

* Adds appropriate `x-forwarded-for` and `x-forwarded-proto HTTP` headers to incoming requests.

* (Optional) Supports WebSockets.

### External blob storage
Blobs are large binary files, such as PDFs or images. To store blobs for high availability, use external storage such as Amazon S3 or an S3-compatible
service.
You can also store blobs internally using WebDAV or NFS. These components run as single instances and you cannot scale them. For these deployments, use the
high availability features of your IaaS to immediately recover your WebDAV or NFS server VM if it fails.
If you need assistance,
contact [Support.](https://www.vmware.com/support/services.html)
The singleton Collector and Compilation components do not affect platform availability.

## Scaling platform capacity
You can scale platform capacity in the following ways:

* **Vertical scaling:** Add memory and disk to each VM.

* **Horizontal scaling:** Add more VMs that run instances of Cloud Foundry components.
The type of apps you host on Cloud Foundry determines whether you scale vertically or horizontally.
For more information about scaling apps and maintaining app uptime, see [Scaling an app using cf scale](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-scale.html) and [Using
Blue-Green Deployment to Reduce Downtime and Risk](https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html)

### Scaling vertically
Scaling vertically means adding memory and disk to your component VMs.
To scale vertically, allocate and maintain the following:

* Free space on host Diego Cell VMs so that apps expected to deploy can successfully be staged and run.

* Disk space and memory in your deployment so that if one host VM is down, all instances of apps can be placed on the remaining host VMs.

* Free space to handle one AZ going down if deploying in multiple AZs.

### Scaling horizontally
Scaling horizontally means increasing the number of instances of VMs that run a functional component of a system.
You can horizontally scale most Cloud Foundry component VMs to multiple instances for high availability.
You must also distribute the instances of components across different AZs to minimize downtime during ongoing operation, product updates, and platform
upgrades. For more information about using AZs, see [Availability Zones](https://docs.cloudfoundry.org/concepts/high-availability.html#azs).

## Recommended instance counts for high availability
The following table provides recommended instance counts for a high-availability deployment. You can
decrease the footprint of your deployment by specifying fewer instances and combining multiple components onto a
single VM.
| **Component** | **Total Instances** | **Notes** |
| --- | --- | --- |
| Diego Cell | ≥ 2 | The optimal balance between CPU/memory sizing and instance count depends on the performance characteristics of the apps that run on Diego cells. Scaling vertically with larger Diego cells makes for larger points of failure, and more apps go down when a cell fails. On the other hand, scaling horizontally decreases the speed at which the system rebalances apps. Rebalancing 100 cells takes longer and demands more processing overhead than rebalancing 20 cells. |
| Diego Brain | ≥ 2 | One per AZ, or two if only one AZ. |
| Diego BBS | ≥ 2 | One per AZ, or two if only one AZ. |
| PostgreSQL Server | 0 or 1 | `0` if Postgres database is external. |
| MySQL Proxy | ≥ 2 | |
| NATS Server | ≥ 2 | You might run a single NATS instance if you lack the resources to deploy two stable NATS servers. Components using NATS are resilient to message failures and the BOSH resurrector recovers the NATS VM quickly if it becomes non-responsive. NATS includes metrics as well as route registration and deregistration messages. Cloud Foundry recommends scaling NATS VMs to 2 or more CPU. |
| Cloud Controller API | ≥ 2 | Scale the Cloud Controller to accommodate the number of requests to the API and the number of apps in the system. |
| Cloud Controller Worker | ≥ 2 | Scale the Cloud Controller to accommodate the number of asynchronous requests to the API and background jobs. |
| Router | ≥ 2 | Scale the router to accommodate the number of incoming requests. Additional instances increase available bandwidth. In general, this load is much less than the load on host VMs. |
| UAA | ≥ 2 | |
| Doppler Server | ≥ 2 | Deploying additional Doppler servers splits traffic across them. For high availability, use at least two per Availability Zone (AZ). |
| Loggregator TC | ≥ 2 | Deploying additional Loggregator Traffic Controllers allows you to direct traffic to them in a round-robin manner. For high availability, use at least two per AZ. |
| Log Cache | ≥ 1 | Deploying additional Log Cache instances increases the total storage, sharding data by app ID. If app logs and metrics are sharded to an unavailable instance, they are unavailable when the designated instance is unavailable regardless of the number of instances or AZs. |

## Infrastructure for component scaling
The ability to scale component VMs is important for high availability. To scale component VMs, you must make sure that the surrounding infrastructure of your
deployment supports VM scaling.
Learn about the infrastructure required to support scaling component VMs for high availability.

### Settingmax\_in\_flightvalues
For each component, the variable `max_in_flight` limits how many instances of that component are restarted simultaneously during updates or upgrades. You set `max_in_flight` in the manifest as a system-wide value, plus any component-specific overrides. Values for `max_in_flight` can be any integer between 1 and 100.
To ensure zero downtime during updates, set `max_in_flight` for each component to a number low enough to prevent overburdening the component instances left running. Here are some guidelines:

* For host VMs, the closer their resource usage is to 100%, the lower you set `max_in_flight`, allows non migrating cells to pick up the work of cells stopping and restarting for migration. If resource usage is already close to 100%, scale up your host VMs before any updates.

* For quorum-based components like etcd and Diego BBS, set `max_in_flight` to `1`.

* For other components, set `max_in_flight` to the number of instances that you can afford to have down at any one time. This depends on
your capacity planning. With higher redundancy, you can make the number high so that updates run faster. But if your components are at
high utilization, you must keep the number low.
Never set `max_in_flight` to a value greater than or equal to the number of instances you have running for a component.

### Resource pools
Each IaaS has different ways of limiting resource consumption for scaling VMs. Consult with your IaaS administrator to ensure additional VMs and related
resources, like IPs and storage, are available to scale.
For more information about configuring your resource pools according to the requirements of your deployment, see [Building a Manifest](https://bosh.io/docs/deployment-basics/) in the BOSH documentation.

### Databases
For database services deployed outside Cloud Foundry, use the high availability features included with your infrastructure. Also, configure
backup and restore where possible.
Data services might have single points of failure depending on their configuration.