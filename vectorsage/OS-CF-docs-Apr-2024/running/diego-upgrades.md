# Configuring Diego for upgrades
Cloud Foundry supports rolling upgrades in high availability environments. A rolling upgrade means that you can continue to operate an existing Cloud Foundry deployment and its running app instances while upgrading the platform.

**Important**
Rolling upgrade is available in your deployment only if you have configured your deployment to be highly available. See [High availability in Cloud Foundry](https://docs.cloudfoundry.org/concepts/high-availability.html).

## Upgrading Diego Cells
To upgrade Cloud Foundry, BOSH must drain all Diego Cell VMs that host app instances. BOSH manages this process by upgrading a batch of cells at a time.
The number of cells that undergo upgrade simultaneously (either in a state of shutting down or coming back online) is controlled by the `max_in_flight` value of the Diego Cell job. For example, if `max_in_flight` is set to `10%` and your deployment has 20 Diego Cell job instances, then the maximum number of cells that BOSH can upgrade at a single time is `2`.
When BOSH triggers an upgrade, each Diego Cell undergoing upgrade enters “evacuation” mode. Evacuation mode means that the cell stops accepting new work and signals the rest of the Diego system to schedule replacements for its app instances. This scheduling is managed by the [Diego auctioneer process](https://docs.cloudfoundry.org/concepts/diego/diego-auction.html).
The evacuating cells continue to interact with the Diego system as replacements come online. The cell undergoing upgrade waits until either its app instance replacements run successfully before shutting down the original local instances, or for the evacuation process to time out. This “evacuation timeout” defaults to 10 minutes.
If cell evacuation exceeds this timeout, then the cell stops its app instances and shuts down. The Diego system continues to re-emit start requests for the app replacements.

## Prevent overload
A potential issue arises if too many app instance replacements are slow to start or do not start successfully at all.
If too many app instances are starting concurrently, then the load of these starts on the rest of the system can cause other applications that are already running to crash and be rescheduled. These events can result in a cascading failure.
To prevent overload, Cloud Foundry provides two major throttle configurations:

* **The maximum number of starting containers that Diego can start in Cloud Foundry**: This is a deployment-wide limit. The default value and ability to override this configuration depends on the version of Cloud Foundry deployed.

* **The `max_in_flight` setting for the Diego Cell job configured in the BOSH manifest**: This configuration, expressed as a percentage or an integer, sets the maximum number of job instances that can be upgraded simultaneously. For example, if your deployment is running 10 Diego Cell job instances and the configured `max_in_flight` value is `20%`, then only 2 Diego Cell job instances can start up at a single time. For more information, see the [Update Block](https://bosh.io/docs/deployment-manifest.html#update) section of the *Deployment Manifest v1* topic in the BOSH documentation.

## Set a maximum number of starting containers
This topic describes how to use the auctioneer job to configure the maximum number of app instances starting at a given time. This prevents Diego from scheduling too much new work for your platform to handle concurrently. A lower default can prevent server overload during cold start, which may be important if your infrastructure is not sized for a large number of concurrent cold starts.
The auctioneer only schedules a fixed number of app instances to start concurrently. This limit applies to both single and multiple Diego Cells. For example, if you set the limit to five starting instances, it does not matter if you have one Diego Cell with ten instances or five Diego Cells with two instances each. The auctioneer will not allow more than five instances to start at the same time.
If you are using a cloud-based IaaS, rather than a smaller on-premise solution, Cloud Foundry recommends leaving the default at `0`.
You can configure the maximum number of started instances by changing the `diego.auctioneer.starting_container_count_maximum` property in the Diego manifest.

1. Open the Diego manifest in a text editor.

2. Find the `diego.auctioneer.starting_container_count_maximum` property.

3. Set the maximum number of instances the auctioneer should allow to start.

4. Save the changes and redeploy BOSH.
For example, the following Diego manifest excerpt shows the `diego.auctioneer.starting_container_count_maximum` property set to `100`.
```
diego.auctioneer.starting_container_count_maximum:
description: "Maximum number of inflight container starts allowed globally. Value of 0 or less indicates no limit."
default: 100
```