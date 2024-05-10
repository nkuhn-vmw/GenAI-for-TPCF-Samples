# Container security in Cloud Foundry
This topic tells you about how Cloud Foundry secures the containers
that host app instances on Linux.
For an overview of other Cloud Foundry security features, see [Cloud Foundry Security](https://docs.cloudfoundry.org/concepts/security.html).
The sections in this topic provide the following information:

* [Container Mechanics](https://docs.cloudfoundry.org/concepts/container-security.html#mechanics) provides an overview of container isolation.

* [Inbound and Outbound Traffic from Cloud Foundry](https://docs.cloudfoundry.org/concepts/container-security.html#networking) provides an overview of container networking and describes how Cloud Foundry admins customize container network traffic rules for their deployment.

* [Container Security](https://docs.cloudfoundry.org/concepts/container-security.html#security) describes how Cloud Foundry secures containers by running app instances in unprivileged containers and by hardening them.

## Container mechanics
Each instance of an app deployed to Cloud Foundry runs within its own self-contained environment, a Garden container. This container isolates processes, memory, and the filesystem using operating system features and the characteristics of the virtual and physical infrastructure where Cloud Foundry is deployed. For more information about Garden containers, see [Garden](https://docs.cloudfoundry.org/concepts/architecture/garden.html).
Cloud Foundry achieves container isolation by namespacing kernel resources that would otherwise be shared. The intended level of isolation is set to prevent multiple containers that are present on the same host from detecting each other. Every container includes a private root filesystem, which includes a Process ID (PID), namespace, network namespace, and mount namespace.
Cloud Foundry creates container filesystems using the Garden Rootfs (GrootFS) tool. It stacks the following using OverlayFS:

* A **read-only base filesystem**: This filesystem has the minimal set of operating system packages and Garden-specific modifications common to all containers. Containers can share the same read-only base filesystem because all writes are applied to the read-write layer.

* A **container-specific read-write layer**: This layer is unique to each container and its size is limited by XFS project quotas. The quotas prevent the read-write layer from overflowing into unallocated space.
For more information about GrootFS, see [Garden RootFS (GrootFS)](https://docs.cloudfoundry.org/concepts/architecture/garden.html#garden-rootfs) in *Garden*.
Resource control is managed using Linux control groups. Associating each container with its own cgroup or job object limits the amount of memory that the container might use. Linux cgroups also require the container to use a fair share of CPU compared to the relative CPU share of other containers.
Cloud Foundry does not support a RedHat Enterprise Linux OS stemcell. This is due to an
inherent security issue with the way RedHat handles user namespacing and container isolation.

### CPU
Each container is placed in its own cgroup. Cgroups make each container use a fair share of CPU relative to the other containers. This prevents oversubscription on the host VM where one or more containers hog the CPU and leave no computing resources to the others.
The way cgroups allocate CPU time is based on shares. CPU shares do not work as direct percentages of total CPU usage. Instead, a share is relative in a given time window to the shares held by the other containers. The total amount of CPU that can be overall divided among the cgroups is what is left by other processes that might run in the host VM.
Generally, cgroups offers two possibilities for limiting the CPU usage: *CPU affinity* and *CPU bandwidth*, the latter of which is used in Cloud Foundry.

* CPU affinity consists of binding a cgroup to certain CPU cores. The actual amount of CPU cycles that can be consumed by the cgroup is thus limited to what is available on the bound CPU cores.

* CPU bandwidth sets the weight of a cgroup with the process scheduler. The process scheduler divides the available CPU cycles among cgroups depending on the shares held by each cgroup, relative to the shares held by the others.
For example, consider two cgroups, one holding two shares and one holding four. Assuming the process scheduler gets to administer 60 CPU cycles, the first cgroup with two shares will get one third of those available CPU cycles, as it holds one third of the overall shares. Similarly, the second cgroup will get 40 cycles, as it holds two thirds of the collective shares.
The calculation of the CPU usage based on the percentage of the total CPU power available is quite sophisticated and is performed regularly as the CPU demands of the various containers fluctuates. Specifically, the percentage of CPU cycles a cgroup gets can be calculated by dividing the `cpu.shares` it holds by the sum of the `cpu.shares` of all the cgroups that are currently doing CPU activity, as shown in the following calculation:
```
process_cpu_share_percent = cpu.shares / sum_cpu_shares * 100
```
In Cloud Foundry, cgroup shares range from 10 to 1024, with 1024 being the default. The actual amount of shares a cgroup gets can be read from the `cpu.shares` file of the cgroup configurations pseudo-file-system available in the container at `/sys/fs/cgroup/cpu`.
The amount of shares given to an apps cgroup depends on the amount of memory the app declares to need in the manifest. Cloud Foundry scales the number of allocated shares linearly with the amount of memory, with an app instance requesting 8 GB of memory getting the upper limit of 1024 shares, as shown in the following calculation:
```
process_cpu.shares = min( 1024*(application_memory / 8 GB), 1024)
```
The next example helps to illustrate this better. Consider three processes: P1, P2 and P3, which are assigned `cpu.shares` of 5, 20 and 30, respectively.
P1 is active, while P2 and P3 require no CPU. Hence, P1 might use the whole CPU. When P2 joins in and is doing some actual work, such as when a request comes in, the CPU share between P1 and P2 is calculated as follows:

* P1 -> 5 / (5+20) = 0.2 = 20%

* P2 -> 20 / (5+20) = 0.8 = 80%

* P3 (idle)
At some point, process P3 joins in. Then the distribution is recalculated again:

* P1 -> 5 / (5+20+30) = 0.0909 = ~9%

* P2 -> 20 / (5+20+30) = 0.363 = ~36%

* P3 -> 30 / (5+20+30) = 0.545 = ~55%
If P1 become idle, the following recalculation between P2 and P3 takes place:

* P1 (idle)

* P2 -> 20 / (20+30) = 0.4 = 40%

* P3 -> 30 / (20+30) = 0.6 = 60%
If P3 finishes or becomes idle, then P2 can consume all the CPU, as another recalculation is performed.
In summary, the cgroup shares are the minimum guaranteed CPU share that the process can get. This limitation becomes effective only when processes on the same host compete for resources.

## Inbound and outbound traffic from Cloud Foundry
Learn about container networking and how Cloud Foundry admins customize
container network traffic rules for their deployment.

### Networking overview
A host VM has a single IP address. If you configure the deployment with the cluster on a VLAN, as Cloud Foundry recommends, then all traffic goes through the following levels of network address translation, as shown in the following diagram:

* **Inbound** requests flow from the load balancer through the router to the host Diego Cell, then into the app container. The router determines which app instance receives each request.

* **Outbound** traffic flows from the app container to the Diego Cell, then to the gateway on the Diego Cell’s virtual network interface. Depending on your IaaS, this gateway might be a NAT to external networks.
![Networking Architecture diagram](https://docs.cloudfoundry.org/concepts/images/security/sysbound2.png)
The networking diagram shows the following:

* Inbound requests go to Load Balancer

* Outbound traffic come from NAT

+ Cloud Foundry on right side

* Load balancer goes to router and to the app container inside the Diego Cell

* App container response goes to NAT

### Network traffic rules
Admins configure rules to govern container network traffic. This is how containers send traffic outside of Cloud Foundry and receive traffic from outside, the Internet. These rules can prevent system access from external networks and between internal components and determine if apps can establish connections over the virtual network interface.
Admins configure these rules at two levels:

* Application Security Groups (ASGs) apply network traffic rules at the container level. For more information about ASGs, see [App Security Groups](https://docs.cloudfoundry.org/adminguide/app-sec-groups.html).

* Container-to-container networking policies determine app-to-app communication. Within Cloud Foundry, apps can communicate directly with each other, but the containers are isolated from outside Cloud Foundry. For information about administering container-to-container network policies, see [Configuring Container-to-Container Networking](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html).

## Container security
Cloud Foundry secures containers through the following measures:

* Running app instances in unprivileged containers by default. For more information about app instances, see [Types](https://docs.cloudfoundry.org/concepts/container-security.html#types).

* Hardening containers by limiting function and access rights. For more information about hardening containers, see [Hardening](https://docs.cloudfoundry.org/concepts/container-security.html#hardening).

* Only allowing outbound connections to public addresses from app containers. This is the original default. Admins can change this behavior by configuring ASGs. For more information about ASGs, see [App Security Groups](https://docs.cloudfoundry.org/adminguide/app-sec-groups.html).

### Types
Garden has the following container types:

* unprivileged

* privileged
Currently, Cloud Foundry runs all app instances and staging tasks in unprivileged containers by default. This measure increases security by eliminating the threat of root escalation inside the container.
Although all application instances and staging tasks now run by default in unprivileged containers,
operators can override these defaults by customizing their Diego deployment manifest and redeploying.

* To enable privileged containers for buildpack-based apps, set the `capi.nsync.diego_privileged_containers` property
to `true` in the Diego manifest.

* To enable privileged containers for staging tasks, set the `capi.stager.diego_privileged_containers` property
to `true` in the Diego manifest.

### Hardening
Cloud Foundry mitigates against container breakout and denial of service attacks in
the following ways:

* Cloud Foundry uses the full set of Linux namespaces - IPC, Network, Mount, PID, User, UTS - to provide isolation between containers running on the same host. The User namespace is not used for privileged containers. For more information about Linux namespaces, see [namespaces - overview of Linux namespaces](http://manpages.ubuntu.com/manpages/xenial/en/man7/namespaces.7.html) in the Ubuntu documentation.

* In unprivileged containers, Cloud Foundry maps UID/GID 0 (root) inside the container user namespace to a different UID/GID on the host to prevent an app from inheriting UID/GID 0 on the host if it breaks out of the container.

+ Cloud Foundry uses the same UID/GID for all containers.

+ Cloud Foundry maps all UIDs except UID 0 to themselves. Cloud Foundry maps UID 0 inside the container namespace to `MAX_UID-1` outside of the container namespace.

+ Container Root does not grant Host Root permissions.

* Cloud Foundry mounts `/proc` and `/sys` as read-only inside containers.

* Cloud Foundry disallows `dmesg` access for unprivileged users and all users in unprivileged containers.

* Cloud Foundry uses `chroot` when importing docker images from docker registries.

* Cloud Foundry establishes a container-specific overlay filesystem mount. Cloud Foundry uses `pivot_root` to move the root filesystem into this overlay, in order to isolate the container from the host system’s filesystem. For more information about `pivot_root`, see [pivot\_root - change the root filesystem](http://manpages.ubuntu.com/manpages/trusty/man2/pivot_root.2.html) in the Ubuntu documentation.

* Cloud Foundry does not call any binary or script inside the container filesystem, in order to eliminate any dependencies on scripts and binaries inside the root filesystem.

* Cloud Foundry avoids side-loading binaries in the container through bind mounts or other methods. Instead, it runs the same binary again by reading it from `/proc/self/exe` whenever it needs to run a binary in a container.

* Cloud Foundry establishes a virtual ethernet pair for each container for network traffic. For more information, see [Container Network Traffic](https://docs.cloudfoundry.org/concepts/container-security.html#config-traffic). The virtual ethernet pair has the following features:

+ One interface in the pair is inside the container’s network namespace, and is the only non-loopback interface accessible inside the container.

+ The other interface remains in the host network namespace and is bridged to the container-side interface.

+ Egress allow list rules are applied to these interfaces according to ASGs configured by the admin.

+ First-packet logging rules might also be activated on the TCP allow list rules.

+ DNAT rules are established on the host to enable traffic ingress from the host interface to allowed ports on the container-side interface.

* Cloud Foundry applies disk quotas using container-specific XFS quotas with the specified disk-quota capacity.

* Cloud Foundry applies a total memory usage quota through the memory cgroup and destroys the container if the memory usage exceeds the quota.

* Cloud Foundry applies a fair-use limit to CPU usage for processes inside the container through the `cpu.shares` control group.

* Cloud Foundry allows admins to rate limit the maximum bandwidth consumed by single-app containers, configuring `rate` and `burst` properties on the `silk-cni` job.

* Cloud Foundry limits access to devices using cgroups but explicitly allows the following safe device nodes:

+ `/dev/full`

+ `/dev/fuse`

+ `/dev/null`

+ `/dev/ptmx`

+ `/dev/pts/*`

+ `/dev/random`

+ `/dev/tty`

+ `/dev/tty0`

+ `/dev/tty1`

+ `/dev/urandom`

+ `/dev/zero`

+ `/dev/tap`

+ `/dev/tun`

* Cloud Foundry drops the following Linux capabilities for all container processes. Every dropped capability limits the actions the root user can perform.

+ `CAP_DAC_READ_SEARCH`

+ `CAP_LINUX_IMMUTABLE`

+ `CAP_NET_BROADCAST`

+ `CAP_NET_ADMIN`

+ `CAP_IPC_LOCK`

+ `CAP_IPC_OWNER`

+ `CAP_SYS_MODULE`

+ `CAP_SYS_RAWIO`

+ `CAP_SYS_PTRACE`

+ `CAP_SYS_PACCT`

+ `CAP_SYS_BOOT`

+ `CAP_SYS_NICE`

+ `CAP_SYS_RESOURCE`

+ `CAP_SYS_TIME`

+ `CAP_SYS_TTY_CONFIG`

+ `CAP_LEASE`

+ `CAP_AUDIT_CONTROL`

+ `CAP_MAC_OVERRIDE`

+ `CAP_MAC_ADMIN`

+ `CAP_SYSLOG`

+ `CAP_WAKE_ALARM`

+ `CAP_BLOCK_SUSPEND`

+ `CAP_SYS_ADMIN` for unprivileged containers
For more information about Linux capabilities, see [capabilities - overview of Linux capabilities](http://manpages.ubuntu.com/manpages/xenial/en/man7/capabilities.7.html) in the Ubuntu documentation.