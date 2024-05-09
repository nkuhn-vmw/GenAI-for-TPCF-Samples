# How Cloud Foundry maintains high availability
Cloud Foundry deployments make up several layers of high availability to keep your apps running during system failure.
These layers include AZs, app health management, process monitoring, and VM resurrection.

## Availability zones
Cloud Foundry supports deploying apps instances across multiple AZs. This level of high availability requires that you define AZs in your IaaS. Cloud Foundry balances the apps you deploy across the AZs you defined. If an AZ goes down, you still have app instances running in another.

## Health management for app instances
If you lose app instances for any reason, such as a bug in the app or an AZ going down, Cloud Foundry restarts new instances to maintain capacity. Under Diego architecture, the nsync, BBS, and Cell Rep components track the number of instances of each app that are running across all of the Diego cells. When these components detect a discrepancy between the actual state of the app instances in the cloud and the desired state as known by the Cloud Controller, they advise the Cloud Controller of the difference and the Cloud Controller initiates the deployment of new app instances.
For more information about the nsync, BBS, and Cell Rep components, see the [nsync, BBS, and Cell Rep](https://docs.cloudfoundry.org/concepts/architecture/#nsync-bbs) section of the *Cloud Foundry Components* topic.

## Process monitoring
Cloud Foundry uses a BOSH agent, monit, to monitor the processes on the component VMs that work together to keep your apps running, such as nsync, BBS, and Cell Rep. If monit detects a failure, it restarts the process and notifies the BOSH agent on the VM. The BOSH agent notifies the BOSH Health Monitor, which starts the responders through plug-ins. For example, email notifications or paging.

## Resurrector VMs
BOSH detects if a VM is present by listening for heartbeat messages that
are sent from the BOSH agent every 60 seconds. The BOSH Health Monitor listens for
those heartbeats. When the Health Monitor finds that a VM is not responding, it passes an alert
to the Resurrector component. If the Resurrector is enabled,
it sends the IaaS a request to create a new VM instance to replace the one that failed.
For more information about the Resurrector, see [Auto-healing Capabilities](https://bosh.io/docs/resurrector.html) in the BOSH documentation.