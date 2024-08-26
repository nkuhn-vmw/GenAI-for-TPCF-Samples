# Cloud Foundry Component Metrics
This topic lists and describes the metrics available for Cloud Foundry system components. These metrics are streamed from the Loggregator Firehose. For more information about the Firehose, see [Loggregator architecture](https://docs.cloudfoundry.org/loggregator/architecture.html).
The Cloud Foundry component metric names and descriptions listed in this topic may be out of date because Cloud Foundry component metrics change often. If you have questions about Cloud Foundry component metrics, consider contacting the component teams directly on their respective channels in the [Cloud Foundry Slack](https://cloudfoundry.slack.com) organization. For example, you can contact the Diego team at **#diego**.

## Cloud Controller
Default Origin Name: cc
| Metric Name | Description |
| --- | --- |
| deployments.deploying | Number of deployments in the `DEPLOYING` state. Emitted every 30 seconds. |
| deployments.update.duration | Time in milliseconds that it took to complete an update of app deployments. Emitted every 5 seconds. |
| diego\_sync.invalid\_desired\_lrps | Number of invalid DesiredLRPs found during Cloud Foundry apps and Diego DesiredLRPs periodic synchronization. Emitted every 30 seconds. |
| diego\_sync.duration | Time in milliseconds that it took to synchronize Cloud Foundry apps and Diego DesiredLRPs. Emitted every 30 seconds. |
| failed\_job\_count.<VM\_NAME>-<VM\_INDEX> | Number of failed jobs in the <VM\_NAME>-<VM\_INDEX> queue. This is the number of delayed jobs where the `failed at` column is populated with the time of the most recently failed attempt at the job. The failed job count is not specific to the jobs run by the Cloud Controller worker. By default, Cloud Controller deletes failed jobs after 31 days. Emitted every 30 seconds per VM. |
| failed\_job\_count.cc-generic | Number of failed jobs in the cc-generic queue. By default, Cloud Controller deletes failed jobs after 31 days. Emitted every 30 seconds per VM. |
| failed\_job\_count.total | Number of failed jobs in all queues. By default, Cloud Controller deletes failed jobs after 31 days. Emitted every 30 seconds per VM. |
| http\_status.1XX | Number of HTTP response status codes of type 1xx (informational). This resets when the Cloud Controller process is restarted and is incremented at the end of each request cycle. |
| http\_status.2XX | Number of HTTP response status codes of type 2xx (success). This resets when the Cloud Controller process is restarted and is incremented at the end of each request cycle. Emitted for each Cloud Controller request. |
| http\_status.3XX | Number of HTTP response status codes of type 3xx (redirection). This resets when the Cloud Controller process is restarted and is incremented at the end of each request cycle. Emitted for each Cloud Controller request. |
| http\_status.4XX | Number of HTTP response status codes of type 4xx (client error). This resets when the Cloud Controller process is restarted and is incremented at the end of each request cycle. Emitted for each Cloud Controller request. |
| http\_status.5XX | Number of HTTP response status codes of type 5xx (server error). This resets when the Cloud Controller process is restarted and is incremented at the end of each request cycle. |
| job\_queue\_length.cc-<VM\_NAME>-<VM\_INDEX> | Number of background jobs in the <VM\_NAME>-<VM\_INDEX> queue that have yet to run for the first time. Emitted every 30 seconds per VM. |
| job\_queue\_length.cc-generic | Number of background jobs in the cc-generic queue that have yet to run for the first time. Emitted every 30 seconds per VM. |
| job\_queue\_length.total | Total number of background jobs in the queues that have yet to run for the first time. Emitted every 30 seconds per VM. |
| job\_queue\_load.cc-<VM\_NAME>-<VM\_INDEX> | Number of background jobs in the <VM\_NAME>-<VM\_INDEX> queue that are ready to run now. Emitted every 30 seconds per VM. |
| job\_queue\_load.cc-generic | Number of background jobs in the cc-generic queue that are ready to run now. Emitted every 30 seconds per VM. |
| job\_queue\_load.total | Total number of background jobs in the queues that are ready to run now. Emitted every 30 seconds per VM. |
| log\_count.all | Total number of log messages, sum of messages of all severity levels. The count resets when the Cloud Controller process is restarted. Emitted every 30 seconds per VM. |
| log\_count.debug | Number of log messages of severity “debug.” The count resets when the Cloud Controller process is restarted. Emitted every 30 seconds per VM. |
| log\_count.debug1 | Not used. |
| log\_count.debug2 | Number of log messages of severity “debug2.” The count resets when the Cloud Controller process is restarted. Emitted every 30 seconds per VM. |
| log\_count.error | Number of log messages of severity “error.” Error is the most severe level. It is used for failures and during error handling. Most errors can be found under this log level, eg. failed unbinding a service, failed to cancel a task, Diego app crashed error, staging completion errors, staging errors, and resource not found. The count resets when the Cloud Controller process is restarted. Emitted every 30 seconds per VM. |
| log\_count.fatal | Number of log messages of severity “fatal.” The count resets when the Cloud Controller process is restarted. Emitted every 30 seconds per VM. |
| log\_count.info | Number of log messages of severity “info.” Examples of info messages are droplet created, copying package, uploading package, access denied due to insufficient scope, job logging, blobstore actions, staging requests, and app running requests. The count resets when the Cloud Controller process is restarted. Emitted every 30 seconds per VM. |
| log\_count.off | Number of log messages of severity “off.” The count resets when the Cloud Controller process is restarted. Emitted every 30 seconds per VM. |
| log\_count.warn | Number of log messages of severity “warn.” Warn is also used for failures and during error handling, eg. diagnostics written to file, failed to capture diagnostics, app rollback failed, service broker already deleted, and UAA token problems. The count resets when the Cloud Controller process is restarted. Emitted every 30 seconds per VM. |
| requests.completed | Number of requests that have been processed. Emitted for each Cloud Controller request. |
| requests.outstanding | DEPRECATED in favor of requests.outstanding.gauge |
| requests.outstanding.gauge | Number of requests that are currently being processed. Emitted for each Cloud Controller request. |
| staging.requested | Cumulative number of requests to start a staging task handled by each Cloud Controller. |
| staging.succeeded | Cumulative number of successful staging tasks handled by each Cloud Controller. Emitted every time a staging task completes successfully. |
| staging.succeeded\_duration | Time in milliseconds that the successful staging task took to run. Emitted each time a staging task completes successfully. |
| staging.failed | Cumulative number of failed staging tasks handled by each Cloud Controller. Emitted every time a staging task fails. |
| staging.failed\_duration | Time in milliseconds that the failed staging task took to run. Emitted each time a staging task fails. |
| tasks\_running.count | Number of currently running tasks. Emitted every 30 seconds per VM. This metric is only seen in version 3 of the Cloud Foundry API. |
| tasks\_running.memory\_in\_mb | Memory being consumed by all currently running tasks. Emitted every 30 seconds per VM. This metric is only seen in version 3 of the Cloud Foundry API. |
| thread\_info.event\_machine.connection\_count | Number of open connections to event machine. Emitted every 30 seconds per VM. |
| thread\_info.event\_machine.resultqueue.num\_waiting | Number of scheduled tasks in the result. Emitted every 30 seconds per VM. |
| thread\_info.event\_machine.resultqueue.size | Number of unscheduled tasks in the result. Emitted every 30 seconds per VM. |
| thread\_info.event\_machine.threadqueue.num\_waiting | Number of scheduled tasks in the threadqueue. Emitted every 30 seconds per VM. |
| thread\_info.event\_machine.threadqueue.size | Number of unscheduled tasks in the threadqueue. Emitted every 30 seconds per VM. |
| thread\_info.thread\_count | Total number of threads that are either runnable or stopped. Emitted every 30 seconds per VM. |
| total\_users | Total number of users ever created, including inactive users. Emitted every 10 minutes per VM. |
| vcap\_sinatra.recent\_errors | 50 most recent errors. DEPRECATED |
| vitals.cpu | Average lifetime CPU% utilization of the Cloud Controller process according to ps. Usually misleading, prefer `vitals.cpu_load_average`. Emitted every 30 seconds per VM. |
| vitals.cpu\_load\_avg | System CPU load averaged over the last 1 minute according to the OS’s vmstat metrics. Emitted every 30 seconds per VM. |
| vitals.mem\_bytes | The RSS bytes (resident set size) or real memory of the Cloud Controller process. Emitted every 30 seconds per VM. |
| vitals.mem\_free\_bytes | Total memory available according to the OS. Emitted every 30 seconds per VM. |
| vitals.mem\_used\_bytes | Total memory used (active + wired) according to the OS. Emitted every 30 seconds per VM. |
| vitals.num\_cores | The number of CPUs of a host machine. Emitted every 30 seconds per VM. |
| vitals.uptime | The uptime of the Cloud Controller process in seconds. Emitted every 30 seconds per VM. |
[Top](https://docs.cloudfoundry.org/running/all_metrics.html#top)

## Diego
Diego metrics have the following origin names:

* [auctioneer](https://docs.cloudfoundry.org/running/all_metrics.html#auctioneer)

* [bbs](https://docs.cloudfoundry.org/running/all_metrics.html#bbs)

* [file\_server](https://docs.cloudfoundry.org/running/all_metrics.html#fileserver)

* [locket](https://docs.cloudfoundry.org/running/all_metrics.html#locket)

* [rep](https://docs.cloudfoundry.org/running/all_metrics.html#rep)

* [route\_emitter](https://docs.cloudfoundry.org/running/all_metrics.html#routeemitter)

* [ssh\_proxy](https://docs.cloudfoundry.org/running/all_metrics.html#sshproxy)

* [garden-linux](https://docs.cloudfoundry.org/running/all_metrics.html#garden-linux)
Default Origin Name: auctioneer
| Metric Name | Description |
| --- | --- |
| AuctioneerFailedCellStateRequests | Cumulative number of cells the auctioneer failed to query for state. Emitted during each auction. |
| AuctioneerFetchStatesDuration | Time in nanoseconds that the auctioneer took to fetch state from all the cells when running its auction. Emitted every 30 seconds during each auction. |
| AuctioneerLRPAuctionsFailed | Cumulative number of LRP instances that the auctioneer failed to place on Diego Cells. Emitted every 30 seconds during each auction. |
| AuctioneerLRPAuctionsStarted | Cumulative number of LRP instances that the auctioneer successfully placed on Diego Cells. Emitted every 30 seconds during each auction. |
| AuctioneerTaskAuctionsFailed | Cumulative number of Tasks that the auctioneer failed to place on Diego Cells. Emitted every 30 seconds during each auction. |
| AuctioneerTaskAuctionsStarted | Cumulative number of Tasks that the auctioneer successfully placed on Diego Cells. Emitted every 30 seconds during each auction. |
| LockHeld | Whether an auctioneer holds the auctioneer lock (in locket): 1 means the lock is held, and 0 means the lock was lost. Emitted periodically by the active auctioneer. |
| LockHeld.v1-locks-auctioneer\_lock | Whether an auctioneer holds the auctioneer lock: `1` means the lock is held, and `0` means the lock was lost. Emitted every 30 seconds by the active auctioneer. |
| LockHeldDuration.v1-locks-auctioneer\_lock | Time in nanoseconds that the active auctioneer has held the auctioneer lock. Emitted every 30 seconds by the active auctioneer. |
| memoryStats.lastGCPauseTimeNS | Duration in nanoseconds of the last garbage collector pause. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| numGoRoutines | Instantaneous number of active goroutines in the process. |
| RequestCount | Cumulative number of requests the auctioneer has handled through its API. Emitted periodically. |
| RequestLatency | Time the auctioneer took to handle requests to its API endpoints. Emitted when the auctioneer handles requests. |
Default Origin Name: bbs
| Metric Name | Description |
| --- | --- |
| BBSMasterElected | Emitted once when the BBS is elected as master. |
| ConvergenceLRPDuration | Time in nanoseconds that the BBS took to run its LRP convergence pass. Emitted every 30 seconds when LRP convergence runs. |
| ConvergenceLRPRuns | Cumulative number of times BBS has run its LRP convergence pass. Emitted every 30 seconds. |
| ConvergenceTaskDuration | Time in nanoseconds that the BBS took to run its Task convergence pass. Emitted every 30 seconds when Task convergence runs. |
| ConvergenceTaskRuns | Cumulative number of times the BBS has run its Task convergence pass. Emitted every 30 seconds. |
| ConvergenceTasksKicked | Cumulative number of times the BBS has updated a Task during its Task convergence pass. Emitted every 30 seconds. |
| ConvergenceTasksPruned | Cumulative number of times the BBS has deleted a malformed Task during its Task convergence pass. Emitted every 30 seconds. |
| CrashedActualLRPs | Total number of LRP instances that have crashed. Emitted every 30 seconds. |
| CrashingDesiredLRPs | Total number of DesiredLRPs that have at least one crashed instance. Emitted every 30 seconds. |
| DBOpenConnections | Number of open connections to the SQL database. Emitted every 60 seconds. |
| DBQueriesFailed | Cumulative number of SQL queries that failed. Emitted every 60 seconds. |
| DBQueriesInFlight | Maximum number of concurrent in flight queries in the last 60 seconds. Emitted every 60 seconds. |
| DBQueriesTotal | Cumulative number of SQL queries executed, including `BEGIN`, `COMMIT`, and `ROLLBACK` statements. Emitted every 60 seconds. |
| DBQueriesSucceeded | Cumulative number of SQL queries that finished successfully. Emitted every 60 seconds. |
| DBQueryDurationMax | Maximum duration of all queries that have run in the last 60 seconds. Emitted every 60 seconds. |
| DBWaitDuration | The total time blocked waiting for a new connection. Emitted every 60 seconds. |
| DBWaitCount | The total number of connections waited for. Emitted every 60 seconds. |
| Domain. | Whether the `<domain-name>` domain is up-to-date, so that instances from that domain have been synchronized with DesiredLRPs for Diego to run. 1 means the domain is up-to-date, no data means it is not. Emitted periodically. |
| EncryptionDuration | Time the BBS took to ensure all BBS records are encrypted with the current active encryption key. Emitted each time a BBS becomes the active master. |
| LockHeld | Whether a BBS holds the BBS lock (in locket): 1 means the lock is held, and 0 means the lock was lost. Emitted periodically by the active BBS server. |
| LockHeld.v1-locks-bbs\_lock | Whether a BBS holds the BBS lock: `1` means the lock is held, and `0` means the lock was lost. Emitted every 30 seconds by the active BBS server. |
| LockHeldDuration.v1-locks-bbs\_lock | Time in nanoseconds that the active BBS has held the BBS lock. Emitted every 30 seconds by the active BBS server. |
| LRPsClaimed | Total number of LRP instances that have been claimed by some cell. Emitted every 30 seconds. |
| LRPsDesired | Total number of LRP instances desired across all LRPs. Emitted periodically. |
| LRPsExtra | Total number of LRP instances that are no longer desired but still have a BBS record. Emitted every 30 seconds. |
| LRPsMissing | Total number of LRP instances that are desired but have no record in the BBS. Emitted every 30 seconds. |
| LRPsRunning | Total number of LRP instances that are running on cells. Emitted every 30 seconds. |
| LRPsUnclaimed | Total number of LRP instances that have not yet been claimed by a cell. Emitted every 30 seconds. |
| memoryStats.lastGCPauseTimeNS | Duration in nanoseconds of the last garbage collector pause. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| MigrationDuration | Time in nanoseconds that the BBS took to run migrations against its persistence store. Emitted each time a BBS becomes the active master. |
| numGoRoutines | Instantaneous number of active goroutines in the process. |
| OpenFileDescriptors | Current (non-cumulative) number of open file descriptors held by the BBS. Emitted periodically. |
| PresentCells | Total number of Diego Cells that are maintaining presence with Locket. Emitted periodically. |
| RequestCount | Cumulative number of requests the BBS has handled through its API. Emitted for each BBS request. |
| RequestLatency | Time in nanoseconds that the BBS took to handle requests to its API endpoints. Emitted when the BBS API handles requests. |
| SuspectCells | Total number of cells that are not maintaining their presences with Locket but for which the BBS has a record of at least one ActualLRP. Emitted periodically. |
| SuspectClaimedActualLRPs | Total number of Suspect LRP instances that have been claimed by some Diego Cell. Emitted periodically. |
| SuspectRunningActualLRPs | Total number of Suspect LRP instances that are running on Diego Cells. Emitted periodically. |
| TasksCompleted | Total number of Tasks that have completed. Emitted every 30 seconds. |
| TasksPending | Total number of Tasks that have not yet been placed on a Diego Cell. Emitted every 30 seconds. |
| TasksResolving | Total number of Tasks locked for deletion. Emitted every 30 seconds. |
| TasksRunning | Total number of Tasks running on Diego Cells. Emitted every 30 seconds. |
| TasksSucceeded | Cumulative number of tasks completed successfully. This metric has a `cell-id` tag that can be used to get the per Cell metric. |
| TasksFailed | Cumulative number of tasks that failed. This metric has a `cell-id` tag that can be used to get the per Cell metric. |
| TasksStarted | Cumulative number of tasks that has started so far. This metric has a `cell-id` tag that can be used to get the per Cell metric. |
Default Origin Name: file\_server
| Metric Name | Description |
| --- | --- |
| memoryStats.lastGCPauseTimeNS | Duration in nanoseconds of the last garbage collector pause. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| numGoRoutines | Instantaneous number of active goroutines in the process. |
Default Origin Name: locket
| Metric Name | Description |
| --- | --- |
| ActiveLocks | Total number of active locks. Emitted periodically. |
| ActivePresences | Total number of active presences. Emitted periodically. |
| DBOpenConnections | Number of open connections to the SQL database. Emitted every 60 seconds. |
| DBQueriesFailed | Cumulative number of SQL queries that failed. Emitted every 60 seconds. |
| DBQueriesInFlight | Maximum number of concurrent in flight queries in the last 60 seconds. Emitted every 60 seconds. |
| DBQueriesTotal | Cumulative number of SQL queries executed, including `BEGIN`, `COMMIT`, and `ROLLBACK` statements. Emitted every 60 seconds. |
| DBQueriesSucceeded | Cumulative number of SQL queries that finished successfully. Emitted every 60 seconds. |
| DBQueryDurationMax | Maximum duration of all queries that have run in the last 60 seconds. Emitted every 60 seconds. |
| LocksExpired | Cumulative number of locks that have expired. Emitted every 60 seconds. |
| memoryStats.lastGCPauseTimeNS | Duration in nanoseconds of the last garbage collector pause. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| numGoRoutines | Instantaneous number of active goroutines in the process. |
| PresenceExpired | Cumulative number of presences that have expired. Emitted every 60 seconds. |
| RequestsCancelled | Cumulative number of requests of a particular type that have been cancelled by the client. Currently tracking `Lock`, `Release`, `Fetch`, and `FetchAll` requests. Emitted every 60 seconds. |
| RequestsStarted | Cumulative number of requests of a particular type that have been made. Currently tracking `Lock`, `Release`, `Fetch`, and `FetchAll` requests. Emitted every 60 seconds. |
| RequestsSucceeded | Cumulative number of requests of a particular type that have completed successfully. Currently tracking `Lock`, `Release`, `Fetch`, and `FetchAll` requests. Emitted every 60 seconds. |
| RequestsFailed | Cumulative number of requests of a particular type that have failed for any reason. Currently tracking `Lock`, `Release`, `Fetch`, and `FetchAll` requests. Emitted every 60 seconds. |
| RequestsInFlight | Number of requests of a particular type currently being handled by locket. Currently tracking `Lock`, `Release`, `Fetch`, and `FetchAll` requests. Emitted every 60 seconds. |
| RequestLatencyMax | Maximum request latency emitted by a request of a particular type in the last 60 seconds. Currently tracking `Lock`, `Release`, `Fetch`, and `FetchAll` requests. Emitted every 60 seconds. |
Default Origin Name: rep (applies to rep and rep\_windows jobs)
| Metric Name | Description |
| --- | --- |
| AppInstanceExceededLogRateLimitCount | Number of application instances that have exceeded the app log rate limit. Emitted once for each application instance that exceeds the log rate limit within the last 5 minute interval. This metric is only emitted if an operator has configured an app log rate limit and an app instance has exceeded that limit. |
| CapacityAllocatedDisk | Amount of disk allocated to containers on this Diego Cell. Emitted periodically. |
| CapacityAllocatedMemory | Amount of memory allocated to containers on this Diego Cell. Emitted periodically. |
| CapacityRemainingContainers | Remaining number of containers this Diego Cell can host. Emitted periodically. |
| CapacityRemainingDisk | Remaining amount of disk available for this Diego Cell to allocate to containers. Emitted periodically. |
| CapacityRemainingMemory | Remaining amount of memory available for this Diego Cell to allocate to containers. Emitted periodically. |
| CapacityTotalContainers | Total number of containers this Diego Cell can host. Emitted periodically. |
| CapacityTotalDisk | Total amount of disk available for this Diego Cell to allocate to containers. Emitted periodically. |
| CapacityTotalMemory | Total amount of memory available for this Diego Cell to allocate to containers. Emitted periodically. |
| ContainerCompletedCount | Number of containers exited on this Diego Cell. Emitted after container exits. |
| ContainerCount | Number of containers hosted on the Diego Cell. Emitted periodically. |
| ContainerExitedOnTimeoutCount | Number of containers on this Diego Cell exited after graceful shutdown interval. Emitted after container exits. |
| ContainerUsageDisk | Amount of disk used by containers on this Diego Cell. Emitted periodically. |
| ContainerUsageMemory | Amount of memory used by containers on this Diego Cell. Emitted periodically. |
| CredCreationFailedCount | Count of failed instance identity credential creations. Emitted after every failed credential creation. |
| CredCreationSucceededCount | Count of successful instance identity credential creations. Emitted after every successful credential creation. |
| CredCreationSucceededDuration | Time the rep took to create instance identity credentials. Emitted after every successful credential creation. |
| ContainerSetupSucceededDuration | Time the rep took to setup a container with the Garden back end. Emitted after every successful container setup. |
| ContainerSetupFailedDuration | Time the rep took to setup a container with the Garden back end. Emitted after every failed container setup. |
| GardenContainerCreationFailedDuration | Time the rep’s Garden back end took to create a container. Emitted after every failed container creation. |
| GardenContainerCreationSucceededDuration | Time the rep’s Garden back end took to create a container. Emitted after every successful container creation. |
| GardenContainerDestructionFailedDuration | Time the rep’s Garden back end took to destroy a container. Emitted after every failed container destruction. |
| GardenContainerDestructionSucceededDuration | Time the rep’s Garden back end took to destroy a container. Emitted after every successful container destruction. |
| GardenHealthCheckFailed | Whether the cell has failed to pass its healthcheck against the garden back end. 0 signifies healthy, and 1 signifies unhealthy. Emitted periodically. |
| memoryStats.lastGCPauseTimeNS | Duration in nanoseconds of the last garbage collector pause. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| numGoRoutines | Instantaneous number of active goroutines in the process. |
| RepBulkSyncDuration | Time the Diego Cell rep took to synchronize the ActualLRPs it has claimed with its actual Garden containers. Emitted periodically by each rep. |
| RequestsStarted | Cumulative number of requests of a particular type that have been made. Currently tracking `CancelTask`, `ContainerMetrics`, `Perform`, `Reset`, `State`, and `StopLRPInstance` requests. Emitted every 60 seconds. |
| RequestsSucceeded | Cumulative number of requests of a particular type that have completed successfully. Currently tracking `CancelTask`, `ContainerMetrics`, `Perform`, `Reset`, `State`, and `StopLRPInstance` requests. Emitted every 60 seconds. |
| RequestsFailed | Cumulative number of requests of a particular type that have failed for any reason. Currently tracking `CancelTask`, `ContainerMetrics`, `Perform`, `Reset`, `State`, and `StopLRPInstance` requests. Emitted every 60 seconds. |
| RequestsInFlight | Cumulative number of requests of a particular type that are in-flight by rep. Currently tracking `CancelTask`, `ContainerMetrics`, `Perform`, `Reset`, `State`, and `StopLRPInstance` requests. Emitted every 60 seconds. |
| RequestLatencyMax | Maximum request latency emitted by a request of a particular type in the last 60 seconds. Currently tracking `CancelTask`, `ContainerMetrics`, `Perform`, `Reset`, `State`, and `StopLRPInstance` requests. Emitted every 60 seconds. |
| StalledGardenDuration | Time the rep is waiting on its Garden back end to become healthy during startup. Emitted only if garden not responsive when the rep starts up. |
| StartingContainerCount | Number of containers currently in a Reserved, Initializing, or Created state. Emitted periodically. |
| StrandedEvacuatingActualLRPs | Evacuating ActualLPRs that timed out during the evacuation process. Emitted when evacuation does not complete successfully. |
| VolmanMountDuration | Time volman took to mount a volume. Emitted by each rep when volumes are mounted. |
| VolmanMountDurationFor | Time volman took to mount a volume with a specific volume driver. Emitted by each rep when volumes are mounted. |
| VolmanMountErrors | Count of failed volume mounts. Emitted periodically by each rep. |
| VolmanUnmountDuration | Time volman took to unmount a volume. Emitted by each rep when volumes are mounted. |
| VolmanUnmountDurationFor | Time volman took to unmount a volume with a specific volume driver. Emitted by each rep when volumes are mounted. |
| VolmanUnmountErrors | Count of failed volume unmounts. Emitted periodically by each rep. |
Default Origin Name: route\_emitter (applies to route\_emitter and route\_emitter\_windows jobs)
| Metric Name | Description |
| --- | --- |
| AddressCollisions | Number of detected conflicting routes. A conflicting route is a set of two distinct instances with the same IP address on the routing table. |
| HTTPRouteCount | Number of HTTP route associations (route-endpoint pairs) in the route-emitter’s routing table. Emitted periodically when emitter is in local mode. |
| HTTPRouteNATSMessagesEmitted | Cumulative number of HTTP routing messages the route-emitter sends over NATS to the gorouter. |
| InternalRouteNATSMessagesEmitted | Cumulative number of internal routing messages the route-emitter sends over NATS to the service discovery controller. |
| LockHeld.v1-locks-route\_emitter\_lock | Whether a route-emitter holds the route-emitter lock: `1` means the lock is held, and `0` means the lock was lost. Emitted every 30 seconds by the active route-emitter. |
| LockHeldDuration.v1-locks-route\_emitter\_lock | Time in nanoseconds that the active route-emitter has held the route-emitter lock. Emitted every 30 seconds by the active route-emitter. |
| memoryStats.lastGCPauseTimeNS | Duration in nanoseconds of the last garbage collector pause. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| numGoRoutines | Instantaneous number of active goroutines in the process. |
| RouteEmitterSyncDuration | Time in nanoseconds that the active route-emitter took to perform its synchronization pass. Emitted every 60 seconds. |
| RoutesRegistered | Cumulative number of route registrations emitted from the route-emitter as it reacts to changes to LRPs. Emitted every 30 seconds. |
| RoutesSynced | Cumulative number of route registrations emitted from the route-emitter during its periodic route-table synchronization. Emitted every 30 seconds. |
| RoutesTotal | Number of routes in the route-emitter’s routing table. Emitted every 30 seconds. |
| RoutesUnregistered | Cumulative number of route unregistrations emitted from the route-emitter as it reacts to changes to LRPs. Emitted every 30 seconds. |
| TCPRouteCount | Number of TCP route associations (route-endpoint pairs) in the route-emitter’s routing table. Emitted periodically when emitter is in local mode. |
Default Origin Name: ssh\_proxy
| Metric Name | Description |
| --- | --- |
| ssh-connections | Total number of SSH connections an SSH proxy has established. Emitted periodically by each SSH proxy. |
| memoryStats.lastGCPauseTimeNS | Duration in nanoseconds of the last garbage collector pause. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| numGoRoutines | Instantaneous number of active goroutines in the process. |
Default Origin Name: garden-linux
| Metric Name | Description |
| --- | --- |
| UnkillableContainers | Total number of containers that could not be killed/cleaned up on a Diego Cell. If this is non-zero, that cell MUST be rebooted before the next BOSH deploy. Typically this is a result of apps losing connection to NFS when using volume services. Diego cell logs can be searched for `failed-deleting-container` to find App IDs responsible. |
[Top](https://docs.cloudfoundry.org/running/all_metrics.html#top)

## DopplerServer
Default Origin Name: DopplerServer
| Metric Name | Description |
| --- | --- |
| dropsondeListener.currentBufferCount | DEPRECATED |
| dropsondeListener.receivedByteCount | DEPRECATED in favor of DopplerServer.udpListener.receivedByteCount. |
| dropsondeListener.receivedMessageCount | DEPRECATED in favor of DopplerServer.udpListener.receivedMessageCount. |
| dropsondeUnmarshaller.containerMetricReceived | Lifetime number of ContainerMetric messages unmarshalled. |
| dropsondeUnmarshaller.counterEventReceived | Lifetime number of CounterEvent messages unmarshalled. |
| dropsondeUnmarshaller.errorReceived | Lifetime number of Error messages unmarshalled. |
| dropsondeUnmarshaller.heartbeatReceived | DEPRECATED |
| dropsondeUnmarshaller.httpStartStopReceived | Lifetime number of HttpStartStop messages unmarshalled. |
| dropsondeUnmarshaller.logMessageTotal | Lifetime number of LogMessage messages unmarshalled. |
| dropsondeUnmarshaller.unmarshalErrors | Lifetime number of errors when unmarshalling messages. |
| dropsondeUnmarshaller.valueMetricReceived | Lifetime number of ValueMetric messages unmarshalled. |
| httpServer.receivedMessages | Number of messages received by Doppler’s internal MessageRouter. Emitted every 5 seconds. |
| LinuxFileDescriptor | Number of file handles for the Doppler’s process. |
| memoryStats.lastGCPauseTimeNS | Duration of the last Garbage Collector pause in nanoseconds. |
| memoryStats.numBytesAllocated | Instantaneous count of bytes allocated and still in use. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| memoryStats.numFrees | Lifetime number of memory deallocations. |
| memoryStats.numMallocs | Lifetime number of memory allocations. |
| messageRouter.numberOfContainerMetricSinks | Instantaneous number of container metric sinks known to the SinkManager. Emitted every 5 seconds. |
| messageRouter.numberOfDumpSinks | Instantaneous number of dump sinks known to the SinkManager. Emitted every 5 seconds. |
| messageRouter.numberOfFirehoseSinks | Instantaneous number of Firehose sinks known to the SinkManager. Emitted every 5 seconds. |
| messageRouter.numberOfSyslogSinks | Instantaneous number of syslog sinks known to the SinkManager. |
| messageRouter.numberOfWebsocketSinks | Instantaneous number of WebSocket sinks known to the SinkManager. Emitted every 5 seconds. |
| messageRouter.totalDroppedMessages | Lifetime number of messages dropped inside Doppler for various reasons (downstream consumer cannot keep up internal object was not ready for message, etc.). |
| sentMessagesFirehose.<SUBSCRIPTION\_ID> | Number of sent messages through the firehose per subscription ID. Emitted every 5 seconds. |
| udpListener.receivedByteCount | Lifetime number of bytes received by Doppler’s UDP Listener. |
| udpListener.receivedMessageCount | Lifetime number of messages received by Doppler’s UDP Listener. |
| udpListener.receivedErrorCount | Lifetime number of errors encountered by Doppler’s UDP Listener while reading from the connection. |
| tcpListener.receivedByteCount | Lifetime number of bytes received by Doppler’s TCP Listener. Emitted every 5 seconds. |
| tcpListener.receivedMessageCount | Lifetime number of messages received by Doppler’s TCP Listener. Emitted every 5 seconds. |
| tcpListener.receivedErrorCount | Lifetime number of errors encountered by Doppler’s TCP Listener while handshaking, decoding or reading from the connection. |
| tlsListener.receivedByteCount | Lifetime number of bytes received by Doppler’s TLS Listener. Emitted every 5 seconds. |
| tlsListener.receivedMessageCount | Lifetime number of messages received by Doppler’s TLS Listener. Emitted every 5 seconds. |
| tlsListener.receivedErrorCount | Lifetime number of errors encountered by Doppler’s TLS Listener while handshaking, decoding or reading from the connection. |
| TruncatingBuffer.DroppedMessages | Number of messages intentionally dropped by Doppler from the sink for the specific sink. This counter event corresponds with log messages “Log message output is too high.” Emitted every 5 seconds. |
| TruncatingBuffer.totalDroppedMessages | Lifetime total number of messages intentionally dropped by Doppler from all of its sinks due to back pressure. Emitted every 5 seconds. |
| listeners.totalReceivedMessageCount | Total number of messages received across all of Doppler’s listeners (UDP, TCP, TLS). |
| numCpus | Number of CPUs on the machine. |
| numGoRoutines | Instantaneous number of active goroutines in the Doppler process. |
| signatureVerifier.invalidSignatureErrors | Lifetime number of messages received with an invalid signature. |
| signatureVerifier.missingSignatureErrors | Lifetime number of messages received that are too small to contain a signature. |
| signatureVerifier.validSignatures | Lifetime number of messages received with valid signatures. |
| Uptime | Uptime for the Doppler’s process. |
[Top](https://docs.cloudfoundry.org/running/all_metrics.html#top)

## Metron Agent
Default Origin Name: MetronAgent
| Metric Name | Description |
| --- | --- |
| MessageAggregator.counterEventReceived | Lifetime number of CounterEvents aggregated in Metron. |
| MessageBuffer.droppedMessageCount | Lifetime number of intentionally dropped messages from Metron’s batch writer buffer. Batch writing is performed over TCP/TLS only. |
| DopplerForwarder.sentMessages | Lifetime number of messages sent to Doppler regardless of protocol. Emitted every 30 seconds. |
| dropsondeAgentListener.currentBufferCount | Instantaneous number of Dropsonde messages read by UDP socket but not yet unmarshalled. |
| dropsondeAgentListener.receivedByteCount | Lifetime number of bytes of Dropsonde messages read by UDP socket. |
| dropsondeAgentListener.receivedMessageCount | Lifetime number of Dropsonde messages read by UDP socket. |
| dropsondeMarshaller.containerMetricMarshalled | Lifetime number of ContainerMetric messages marshalled. |
| dropsondeMarshaller.counterEventMarshalled | Lifetime number of CounterEvent messages marshalled. |
| dropsondeMarshaller.errorMarshalled | Lifetime number of Error messages marshalled. |
| dropsondeMarshaller.heartbeatMarshalled | Lifetime number of Heartbeat messages marshalled. |
| dropsondeMarshaller.httpStartStopMarshalled | Lifetime number of HttpStartStop messages marshalled. |
| dropsondeMarshaller.logMessageMarshalled | Lifetime number of LogMessage messages marshalled. |
| dropsondeMarshaller.marshalErrors | Lifetime number of errors when marshalling messages. |
| dropsondeMarshaller.valueMetricMarshalled | Lifetime number of ValueMetric messages marshalled. |
| dropsondeUnmarshaller.containerMetricReceived | Lifetime number of ContainerMetric messages unmarshalled. |
| dropsondeUnmarshaller.counterEventReceived | Lifetime number of CounterEvent messages unmarshalled. |
| dropsondeUnmarshaller.errorReceived | Lifetime number of Error messages unmarshalled. |
| dropsondeUnmarshaller.heartbeatReceived | DEPRECATED |
| dropsondeUnmarshaller.httpStartStopReceived | Lifetime number of HttpStartStop messages unmarshalled. |
| dropsondeUnmarshaller.logMessageTotal | Lifetime number of LogMessage messages unmarshalled. |
| dropsondeUnmarshaller.unmarshalErrors | Lifetime number of errors when unmarshalling messages. |
| dropsondeUnmarshaller.valueMetricReceived | Lifetime number of ValueMetric messages unmarshalled. |
| legacyAgentListener.currentBufferCount | Instantaneous number of Legacy messages read by UDP socket but not yet unmarshalled. |
| legacyAgentListener.receivedByteCount | Lifetime number of bytes of Legacy messages read by UDP socket. |
| legacyAgentListener.receivedMessageCount | Lifetime number of Legacy messages read by UDP socket. |
| memoryStats.lastGCPauseTimeNS | Duration of the last Garbage Collector pause in nanoseconds. |
| memoryStats.numBytesAllocated | Instantaneous count of bytes allocated and still in use. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| memoryStats.numFrees | Lifetime number of memory deallocations. |
| memoryStats.numMallocs | Lifetime number of memory allocations. |
| numCpus | Number of CPUs on the machine. |
| numGoRoutines | Instantaneous number of active goroutines in the Doppler process. |
| tcp.sendErrorCount | Lifetime number of errors if writing to Doppler over TCP fails. |
| tcp.sentByteCount | Lifetime number of sent bytes to Doppler over TCP. |
| tcp.sentMessageCount | Lifetime number of sent messages to Doppler over TCP. |
| tls.sendErrorCount | Lifetime number of errors if writing to Doppler over TLS fails. |
| tls.sentByteCount | Lifetime number of sent bytes to Doppler over TLS. Emitted every 30 seconds. |
| tls.sentMessageCount | Lifetime number of sent messages to Doppler over TLS. Emitted every 30 seconds. |
| udp.sendErrorCount | Lifetime number of errors if writing to Doppler over UDP fails. |
| udp.sentByteCount | Lifetime number of sent bytes to Doppler over UDP. |
| udp.sentMessageCount | Lifetime number of sent messages to Doppler over UDP. |
[Top](https://docs.cloudfoundry.org/running/all_metrics.html#top)

## Routing
Routing Release metrics have following origin names:

* [gorouter](https://docs.cloudfoundry.org/running/all_metrics.html#gorouter)

* [routing\_api](https://docs.cloudfoundry.org/running/all_metrics.html#routing_api)

* [tcp\_emitter](https://docs.cloudfoundry.org/running/all_metrics.html#tcp_emitter)

* [tcp\_router](https://docs.cloudfoundry.org/running/all_metrics.html#tcp_router)
Default Origin Name: gorouter
| Metric Name | Description |
| --- | --- |
| memoryStats.lastGCPauseTimeNS | Duration of the last Garbage Collector pause in nanoseconds. Emitted every 10 seconds. |
| memoryStats.numBytesAllocated | Instantaneous count of bytes allocated and still in use. Emitted every 10 seconds. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. Emitted every 10 seconds. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. Emitted every 10 seconds. |
| memoryStats.numFrees | Lifetime number of memory deallocations. Emitted every 10 seconds. |
| memoryStats.numMallocs | Lifetime number of memory allocations. Emitted every 10 seconds. |
| numCPUS | Number of CPUs on the machine. Emitted every 10 seconds. |
| numGoRoutines | Instantaneous number of active goroutines in the gorouter process. Emitted every 10 seconds. |
| logSenderTotalMessagesRead | Lifetime number of application log messages. Emitted every 5 seconds. |
| backend\_exhausted\_conns | Lifetime number of requests that have been rejected due to the limit on number of connections per back end having been reached for all back ends tried. Emitted every 5 seconds. |
| bad\_gateways | Lifetime number of bad gateways at the Gorouter. Emitted every 5 seconds. |
| latency | Total round trip time, in milliseconds, for requests through the Gorouter. This includes time spent by back end app to process requests. Emitted per router request. |
| latency.{component} | Time in milliseconds that the Gorouter took to handle requests from each component to its endpoints. Emitted per router request. |
| route\_registration\_latency | Time in milliseconds between when an actual LRP is started and when the app is routable via Gorouter. Emitted per route-register message of new LRPs. This metric might be a negative value up to ~30 ms due to clock skew between the machines this metric is derived from. |
| registry\_message.{component} | Lifetime number of route register messages received for each component. Emitted per route-register message. |
| unregistry\_message.{component} | Lifetime number of route unregister messages received for each component. Emitted per route-unregister message. |
| rejected\_requests | Lifetime number of bad requests received on the Gorouter. Bad requests occur when the route does not exist, when the value of the `X-Cf-App-Instance` header is invalid, or when the host header on the request is empty. Emitted every 5 seconds. |
| requests.{component} | Lifetime number of requests received for each component. Emitted per router request. |
| responses | Lifetime number of HTTP responses returned by the back end app. Emitted every 5 seconds. |
| responses.2xx | Lifetime number of 2xx HTTP responses returned by the back end app. Emitted every 5 seconds. |
| responses.3xx | Lifetime number of 3xx HTTP responses returned by the back end app. Emitted every 5 seconds. |
| responses.4xx | Lifetime number of 4xx HTTP responses returned by the back end app. Emitted every 5 seconds. |
| responses.5xx | Lifetime number of 5xx HTTP responses returned by the back end app. Emitted every 5 seconds. |
| responses.xxx | Lifetime number of other(non-(2xx-5xx)) HTTP responses returned by the back end app. Emitted every 5 seconds. |
| route\_lookup\_time | Time in nanoseconds to look up a request URL in the route table. Emitted per router request. |
| websocket\_upgrades | Lifetime number of WebSocket upgrades. Emitted every 5 seconds. |
| websocket\_failures | Lifetime number of WebSocket failures. Emitted every 5 seconds. |
| routed\_app\_requests | The collector sums up requests for all dea-{index} components for its output metrics. Emitted every 5 seconds. |
| total\_requests | Lifetime number of requests received. Emitted every 5 seconds. |
| ms\_since\_last\_registry\_update | Time in millisecond since the last route register has been been received. Emitted every 30 seconds. |
| total\_routes | Current number of routes registered. Emitted every 30 seconds. |
| uptime | Uptime for router. Emitted every second. |
| file\_descriptors | Number of file descriptors currently used by the Gorouter. Emitted every 5 seconds. |
| routes\_pruned | Lifetime number of stale routes that have been automatically pruned by the Gorouter. Emitted every 5 seconds. |
| backend\_tls\_handshake\_failed | Lifetime number of failed TLS handshakes when connecting to a back end registered with TLS port. Corresponds to HTTP 525 error response from the Gorouter. Emitted every 5 seconds. |
| backend\_invalid\_id | Lifetime number of requests that were rejected because the back end presents a certificate with an invalid ID. Corresponds to HTTP 503 error response from the Gorouter. Emitted every 5 seconds. |
| backend\_invalid\_tls\_cert | Lifetime number of requests that were rejected because the back end presents a certificate that is not trusted by the Gorouter. Corresponds to HTTP 526 error response from Gorouter. Emitted every 5 seconds. |
| buffered\_messages | Current number of messages in the Gorouter’s NATS client’s buffer. Emitted every 5 seconds. |
| total\_dropped\_messages | Lifetime number of messages that have been dropped by the Gorouter’s NATS client due to a full buffer. Emitted every 5 seconds. |
Default Origin Name: routing\_api
| Metric Name | Description |
| --- | --- |
| memoryStats.lastGCPauseTimeNS | Duration of the last Garbage Collector pause in nanoseconds. Emitted every 10 seconds. |
| memoryStats.numBytesAllocated | Instantaneous count of bytes allocated and still in use. Emitted every 10 seconds. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. Emitted every 10 seconds. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. Emitted every 10 seconds. |
| memoryStats.numFrees | Lifetime number of memory deallocations. Emitted every 10 seconds. |
| memoryStats.numMallocs | Lifetime number of memory allocations. Emitted every 10 seconds. |
| numCPUS | Number of CPUs on the machine. Emitted every 10 seconds. |
| numGoRoutines | Instantaneous number of active goroutines in the routing\_api process. Emitted every 10 seconds. |
| key\_refresh\_events | Total number of events when fresh token was fetched from UAA. Emitted every 30 seconds. |
| total\_http\_routes | Number of HTTP routes in the routing table. Emitted every 30 seconds, or when there is a new HTTP route added. Interval for emitting this metric can be configured with manifest property `metrics_reporting_interval`. |
| total\_http\_subscriptions | Number of HTTP routes subscriptions. Emitted every 30 seconds. Interval for emitting this metric can be configured with manifest property `metrics_reporting_interval`. |
| total\_tcp\_routes | Number of TCP routes in the routing table. Emitted every 30 seconds, or when there is a new TCP route added. Interval for emitting this metric can be configured with manifest property `metrics_reporting_interval`. |
| total\_tcp\_subscriptions | Number of TCP routes subscriptions. Emitted every 30 seconds. Interval for emitting this metric can be configured with manifest property `metrics_reporting_interval`. |
| total\_token\_errors | Total number of UAA token errors. Emitted every 30 seconds. Interval for emitting this metric can be configured with manifest property `metrics_reporting_interval`. |
Default Origin Name: tcp\_emitter
| Metric Name | Description |
| --- | --- |
| memoryStats.lastGCPauseTimeNS | Duration of the last Garbage Collector pause in nanoseconds. Emitted every 10 seconds. |
| memoryStats.numBytesAllocated | Instantaneous count of bytes allocated and still in use. Emitted every 10 seconds. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. Emitted every 10 seconds. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. Emitted every 10 seconds. |
| memoryStats.numFrees | Lifetime number of memory deallocations. Emitted every 10 seconds. |
| memoryStats.numMallocs | Lifetime number of memory allocations. Emitted every 10 seconds. |
| numCPUS | Number of CPUs on the machine. Emitted every 10 seconds. |
| numGoRoutines | Instantaneous number of active goroutines in the tcp\_emitter process. Emitted every 10 seconds. |
Default Origin Name: tcp-router
| Metric Name | Description |
| --- | --- |
| memoryStats.lastGCPauseTimeNS | Duration of the last Garbage Collector pause in nanoseconds. Emitted every 10 seconds. |
| memoryStats.numBytesAllocated | Instantaneous count of bytes allocated and still in use. Emitted every 10 seconds. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. Emitted every 10 seconds. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. Emitted every 10 seconds. |
| memoryStats.numFrees | Lifetime number of memory deallocations. Emitted every 10 seconds. |
| memoryStats.numMallocs | Lifetime number of memory allocations. Emitted every 10 seconds. |
| numCPUS | Number of CPUs on the machine. Emitted every 10 seconds. |
| numGoRoutines | Instantaneous number of active goroutines in the tcp\_router process. Emitted every 10 seconds. |
| {session\_id}.ConnectionTime | Average connection time to back end in current session. Emitted every 60 seconds per session ID. Interval value for this metric can be configured with manifest property `tcp_router.tcp_stats_collection_interval`. |
| {session\_id}.CurrentSessions | Total number of current sessions. Emitted every 60 seconds per session ID. Interval value for this metric can be configured with manifest property `tcp_router.tcp_stats_collection_interval`. |
| AverageConnectTimeMs | Average back end response time (in ms). Emitted every 60 seconds. Interval value for this metric can be configured with manifest property `tcp_router.tcp_stats_collection_interval`. |
| AverageQueueTimeMs | Average time spent in queue (in ms). Emitted every 60 seconds. Interval value for this metric can be configured with manifest property `tcp_router.tcp_stats_collection_interval`. |
| TotalBackendConnectionErrors | Total number of back end connection errors. Emitted every 60 seconds. Interval value for this metric can be configured with manifest property `tcp_router.tcp_stats_collection_interval`. |
| TotalCurrentQueuedRequests | Total number of requests unassigned in queue. Emitted every 60 seconds. Interval value for this metric can be configured with manifest property `tcp_router.tcp_stats_collection_interval`. |
[Top](https://docs.cloudfoundry.org/running/all_metrics.html#top)

## Syslog Drain Binder
Default Origin Name: syslog\_drain\_binder
| Metric Name | Description |
| --- | --- |
| memoryStats.lastGCPauseTimeNS | Duration of the last Garbage Collector pause in nanoseconds. |
| memoryStats.numBytesAllocated | Instantaneous count of bytes allocated and still in use. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| memoryStats.numFrees | Lifetime number of memory deallocations. |
| memoryStats.numMallocs | Lifetime number of memory allocations. |
| numCPUS | Number of CPUs on the machine. |
| numGoRoutines | Instantaneous number of active goroutines in the Doppler process. |
| pollCount | Number of times the syslog drain binder has polled the Cloud Controller for syslog drain bindings. Emitted every 30 seconds. |
| totalDrains | Number of syslog drains returned by Cloud Controller. Emitted every 30 seconds. |
[Top](https://docs.cloudfoundry.org/running/all_metrics.html#top)

## Traffic Controller
Default Origin Name: LoggregatorTrafficController
| Metric Name | Description |
| --- | --- |
| dopplerProxy.containermetricsLatency | Duration for serving container metrics via the containermetrics endpoint (milliseconds). Emitted every 30 seconds. |
| dopplerProxy.recentlogsLatency | Duration for serving recent logs via the recentLogs endpoint (milliseconds). Emitted every 30 seconds. |
| memoryStats.lastGCPauseTimeNS | Duration of the last Garbage Collector pause in nanoseconds. |
| memoryStats.numBytesAllocated | Instantaneous count of bytes allocated and still in use. |
| memoryStats.numBytesAllocatedHeap | Instantaneous count of bytes allocated on the main heap and still in use. |
| memoryStats.numBytesAllocatedStack | Instantaneous count of bytes used by the stack allocator. |
| memoryStats.numFrees | Lifetime number of memory deallocations. |
| memoryStats.numMallocs | Lifetime number of memory allocations. |
| numCPUS | Number of CPUs on the machine. |
| numGoRoutines | Instantaneous number of active goroutines in the Doppler process. |
| Uptime | Uptime for the Traffic Controller’s process. Emitted every 30 seconds. |
| LinuxFileDescriptor | Number of file handles for the TrafficController’s process. |
[Top](https://docs.cloudfoundry.org/running/all_metrics.html#top)

## User Account and Authentication (UAA)
Default Origin Name: uaa
| Metric Name | Description |
| --- | --- |
| audit\_service.client\_authentication\_count | Number of successful client authentication attempts since the last startup. Emitted every 30 seconds. |
| audit\_service.client\_authentication\_failure\_count | Number of failed client authentication attempts since the last startup. Emitted every 30 seconds. |
| audit\_service.principal\_authentication\_failure\_count | Number of failed non-user authentication attempts since the last startup. Emitted every 30 seconds. |
| audit\_service.principal\_not\_found\_count | Number of times non-user was not found since the last startup. Emitted every 30 seconds. |
| audit\_service.user\_authentication\_count | Number of successful authentications by the user since the last startup. Emitted every 30 seconds. |
| audit\_service.user\_authentication\_failure\_count | Number of failed user authentication attempts since the last startup. Emitted every 30 seconds. |
| audit\_service.user\_not\_found\_count | Number of times the user was not found since the last startup. Emitted every 30 seconds. |
| audit\_service.user\_password\_changes | Number of successful password changes by the user since the last startup. Emitted every 30 seconds. |
| audit\_service.user\_password\_failures | Number of failed password changes by the user since the last startup. Emitted every 30 seconds. |
[Top](https://docs.cloudfoundry.org/running/all_metrics.html#top)
For information about metrics related to UAA’s performance, see [UAA performance metrics](https://docs.cloudfoundry.org/uaa/uaa-metrics.html).