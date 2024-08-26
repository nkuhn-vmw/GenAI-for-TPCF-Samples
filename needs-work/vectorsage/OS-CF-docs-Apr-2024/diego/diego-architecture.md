# Diego components and architecture
This topic tells you about the components that form and interact
with the Diego system in Cloud Foundry.
Cloud Foundry uses the Diego system to manage app containers. Diego components assume app scheduling and management responsibility from the Cloud Controller.
Diego is a self-healing container management system that attempts to keep the correct number of instances running in Diego cells to avoid network failures and crashes. Diego schedules and runs Tasks and Long-Running Processes (LRP). For more information about Tasks and LRPs, see [How the Diego Auction Allocates Jobs](https://docs.cloudfoundry.org/concepts/diego/diego-auction.html).
You can submit, update, and retrieve the desired number of Tasks and LRPs using the Bulletin Board System (BBS) API. For more information, see the [BBS Server](https://github.com/cloudfoundry/bbs) repository on GitHub.

## Learning how Diego runs an app
The following sections describe how Diego handles a request to run an app.
This is only one of the processes that happen in Diego. For example, running an app assumes the app has
already been staged.
For more information about the staging process, see [How Apps are Staged](https://docs.cloudfoundry.org/concepts/how-applications-are-staged.html).
The following illustrations and descriptions do not include all of the components of Diego.
For information about each Diego component, see [Diego Components](https://docs.cloudfoundry.org/concepts/diego/diego-architecture.html#components).
The architecture discussed in the following steps includes the following high level blocks:

* api - cloud\_controller\_ng

* scheduler - auctioneer

* diego-api - bbs

* pxc-mysql - bbs db

* diego-cell - rep/executor, garden, loggregator-agent, route-emitter

* singleton-blobstore - droplets

* doppler - doppler

* log-api - traffic-controller

* gorouter - gorouter

### Step 1: Receiving the request to run an app
Cloud Controller passes requests to run apps to the Diego BBS, which stores information about the request
in its database.
![Block diagram](https://docs.cloudfoundry.org/concepts/images/oss-diego-architecture-1.png)

### Step 2: Passing the request to the auctioneer process
The BBS contacts the Auctioneer to create an auction based on the desired resources for the app.
It references the information stored in its database.
![Block diagram](https://docs.cloudfoundry.org/concepts/images/oss-diego-architecture-2.png)

### Step 3: Performing the auction
Through an auction, the Auctioneer finds a Diego Cell to run the app on.
The Rep job on the Diego Cell accepts the auction request.
![Block diagram](https://docs.cloudfoundry.org/concepts/images/oss-diego-architecture-3.png)

### Step 4: Creating the container and running the app
The in process Executor creates a Garden container in the Diego Cell.
Garden downloads the droplet that resulted from the staging process and runs the app in the container.
![Block diagram](https://docs.cloudfoundry.org/concepts/images/oss-diego-architecture-4.png)

### Step 5: Emitting a route for the app
The `route-emitter` process emits a route registration message to Gorouter for the new app running on the Diego Cell.
![Block diagram](https://docs.cloudfoundry.org/concepts/images/oss-diego-architecture-5.png)

### Step 6: Sending logs to the Loggregator
Loggregator agent forwards app logs, errors, and metrics to the Cloud Foundry Loggregator.
For more information, see [App Logging in Cloud Foundry](https://docs.cloudfoundry.org/devguide/deploy-apps/streaming-logs.html).
![Block diagram](https://docs.cloudfoundry.org/concepts/images/oss-diego-architecture-6.png)

## Diego components
The following table describes the jobs that are part of the Cloud Foundry Diego BOSH release.
| Component | Function |
| --- | --- |
| **Job:** auctioneer

**VM:** scheduler | * Distributes work through auction to Cell Reps over SSL/TLS. For more information, see [How the Diego Auction Allocates Jobs](https://docs.cloudfoundry.org/concepts/diego/diego-auction.html).

* Maintains a lock in Locket to ensure only one auctioneer handles auctions at a time.
|
| **Job:** bbs

**VM:** diego-api | * Maintains a real-time representation of the state of the Diego cluster, including desired LRPs, running LRPs, and in-flight Tasks.

* Provides an RPC-style API over HTTP to Diego Core components for external clients as well as internal clients, including the SSH Proxy and Route Emitter.

* Ensures consistency and fault tolerance for Tasks and LRPs by comparing desired state with actual state.

* Keeps `DesiredLRP` and `ActualLRP` counts synchronized. If the `DesiredLRP` count exceeds the `ActualLRP` count, requests a start auction from the Auctioneer. If the `ActualLRP` count exceeds the `DesiredLRP` count, sends a stop message to the Rep on the Diego Cell hosting an instance
|
| **Job:** file\_server

**VM:** api | * Serves static assets that can include general-purpose App Lifecycle binaries
|
| **Job:** locket

**VM:** diego-api | * Provides a consistent key-value store for maintenance of distributed locks and component presence
|
| **Job:** rep

**VM:** diego-cell | * Represents a Diego Cell in Diego Auctions for Tasks and LRPs

* Runs Tasks and LRPs by creating a container and then running actions in it

* Periodically ensures its set of Tasks and ActualLRPs in the BBS is in sync with the containers actually present on the Diego Cell

* Manages container allocations against resource constraints on the Diego Cell, such as memory and disk space

* Streams stdout and stderr from container processes to the metron-agent running on the Diego Cell, which in turn forwards to the Loggregator system

* Periodically collects container metrics and emits them to Loggregator

* Mediates all communication between the Diego Cell and the BBS

* Maintains a presence record for the Diego Cell in Locket
|
| **Job:** route\_emitter

**VM:** diego-cell | * Monitors `DesiredLRP` and `ActualLRP` states, emitting route registration and unregistration messages to Gorouter when it detects changes.

* Periodically emits the entire routing table to the Cloud Foundry Gorouter.
|
| **Job:** diego-healthchecker

**VM:** diego-cell | * An executable designed to perform TCP/HTTP based health checks of processes managed by monit in BOSH releases.

* Because the version of monit included in BOSH does not support specific tcp/http health checks, we designed this utility to perform health checking and restart processes if they become unreachable.
|
| **Job:** ssh\_proxy

**VM:** scheduler | * Brokers connections between SSH clients and SSH servers

* Runs inside instance containers and authorizes access to app instances based on Cloud Controller roles
|

### Additional information
The following resources provide more information about Diego components:

* The [Diego Release](https://github.com/cloudfoundry/diego-release) repository on GitHub.

* The [Auctioneer](https://github.com/cloudfoundry/auctioneer) repository on GitHub.

* The [Bulletin Board System](https://github.com/cloudfoundry/bbs) repository on GitHub.

* The [File Server](https://github.com/cloudfoundry/file-server) repository on GitHub.

* The [Rep](https://github.com/cloudfoundry/rep) repository on GitHub.

* The [Executor](https://github.com/cloudfoundry/executor) repository on GitHub.

* The [Route-Emitter](https://github.com/cloudfoundry/route-emitter) repository on GitHub.

* [App SSH](https://docs.cloudfoundry.org/concepts/diego/ssh-conceptual.html), [App SSH Overview](https://docs.cloudfoundry.org/devguide/deploy-apps/app-ssh-overview.html), and the [Diego SSH](https://github.com/cloudfoundry-incubator/diego-ssh) repository on GitHub.

## Maximum recommended Diego Cells
The maximum recommended Diego Cells is 250 Cells for each Cloud Foundry deployment. By default, there is a hard limit of 256 addresses for vSphere deployments that use Silk for networking. This hard limit is described in the [Silk Release documentation](https://github.com/cloudfoundry/cf-networking-release/blob/develop/docs/large_deployments.md) on GitHub.
The default CIDR address block for the overlay network is 10.255.0.0/16. Each Diego Cell requires a subnet, and subnets (0-255) for each Diego Cell are allocated out of this network.
Cloud Foundry deployments that do not use Silk for networking do not have a hard limit. However, operating a foundation with more than 250 Diego Cells is not recommended for the following reasons:

* Changes to the foundation can take a long time, potentially days or weeks depending on the `max-in-flight` value. For example, if there is a certificate expiring in a week, there might not be enough time to rotate the certificates before expiry.

* A single foundation still has single points of failure, such as the certificates on the platform. The RAM that 250 Diego Cells provides is enough to host many business-critical apps.

## Components from other releases
The following table describes jobs that interact closely with Diego but are not part of the Diego Cloud Foundry BOSH release.
| Component | Function |
| --- | --- |
| **Job:** bosh-dns-aliases

**VM:** all | * Provides service discovery through colocated DNS servers on all BOSH-deployed VMs

* Provides client-side load-balancing by randomly selecting a healthy VM when multiple VMs are available
|
| **Job:** cc\_uploader

**VM:** api | * Mediates uploads from the Executor to the Cloud Controller

* Translates simple HTTP POST requests from the Executor into complex multipart-form uploads for the Cloud Controller
|
| **Job:** database

**VM:** pxc-mysql | * Provides a consistent key-value data store to Diego
|
| **Job:**loggregator-agent

**VM:** all | * Forwards app logs, errors, and app and Diego metrics to the Loggregator Doppler component
|
| **Job:** cloud\_controller\_clock

**VM:** scheduler | * Runs a Diego sync process to ensure desired app data in Diego is in sync with the Cloud Controller.
|

### App lifecycle binaries
The following platform-specific binaries deploy apps and govern their lifecycle:

* The **Builder**, which stages a Cloud Foundry app. The Builder runs as a Task on every staging request. It performs static analysis on the app code and does any necessary pre-processing before the app is first run.

* The **Launcher**, which runs a Cloud Foundry app. The Launcher is set as the Action on the `DesiredLRP` for the app. It runs the start command with the correct system context, including working directory and environment variables.

* The **Healthcheck**, which performs a status check on running Cloud Foundry app from inside the container. The Healthcheck is set as the CheckDefinition on the `DesiredLRP` for the app.

#### Current implementations

* The buildpack app lifecycle implements the Cloud Foundry buildpack-based deployment strategy. For more information, see the [buildpackapplifecycle](https://github.com/cloudfoundry/buildpackapplifecycle) repository on GitHub.

* The Docker app lifecycle implements a Docker deployment strategy. For more information, see the [dockerapplifecycle](https://github.com/cloudfoundry/dockerapplifecycle) repository on GitHub.

### Additional information
The following resources provide more information about components from other releases that interact closely with Diego:

* The [CC-Uploader](https://github.com/cloudfoundry/cc-uploader) repository on GitHub.

* [Garden](https://docs.cloudfoundry.org/concepts/architecture/garden.html) or the [Garden](https://github.com/cloudfoundry/garden) repository on GitHub.

* The [Loggregator Release](https://github.com/cloudfoundry/loggregator-release/) repository on GitHub.

* The [BOSH DNS documentation](https://bosh.io/docs/dns/).

* The [TPS](https://github.com/cloudfoundry/tps) repository on GitHub.