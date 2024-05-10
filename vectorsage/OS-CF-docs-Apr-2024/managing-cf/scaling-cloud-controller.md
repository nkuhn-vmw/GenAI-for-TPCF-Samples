# Scaling Cloud Controller
This topic describes how and when to scale BOSH jobs in CAPI, and includes details about some key metrics, heuristics, and logs.

## cloud\_controller\_ng
The `cloud_controller_ng` Ruby process is the primary job in CAPI. It, along with `nginx_cc`, powers the Cloud Controller API that all users of Cloud Foundry interact with. In addition to serving external clients, `cloud_controller_ng` also provides APIs for internal components within Cloud Foundry, such as Loggregator and Networking subsystems.

**Note**
Running `bosh instances --vitals` returns CPU values. The CPU User value corresponds to the `system.cpu.user` metric and is scaled by the number of CPUs. For example, on a 4-core `api` VM, a `cloud_controller_ng` process that is using 100% of a core is listed as using 25% in the `system.cpu.user` metric.

### When to Scale
When determining whether to scale `cloud\_controller\_ng`, look for the following:

#### Key Metrics
Cloud Controller emits the following metrics:

* `cc.requests.outstanding.gauge` or `cc.requests.outstanding` (deprecated) is at or consistently near 20.

* `system.cpu.user` is above 0.85 utilization of a single core on the API VM.

* `cc.vitals.cpu_load_avg` is 1 or higher.

* `cc.vitals.uptime` is consistently low, indicating frequent restarts (possibly due to memory pressure).

#### Heuristic Failures
The following behaviors may occur:

* There is a latency in average response.

* Web UI responsiveness or timeouts are degraded.

* `bosh is --ps --vitals` has elevated CPU usage for the API instance group’s `cloud_controller_ng` job.

#### Relevant Log Files
You can find the above heuristic failures in the following log files:

* `/var/vcap/sys/log/cloud_controller_ng/cloud_controller_ng.log`

* `/var/vcap/sys/log/cloud_controller_ng/nginx-access.log`

### How to Scale
Before and after scaling Cloud Controller API VMs, you should verify that the Cloud Controller database is not overloaded. All Cloud Controller processes are backed by the same database, so heavy load on the database impacts API performance regardless of the number of Cloud Controllers deployed. Cloud Controller supports both PostgreSQL and MySQL, so there is no specific scaling guidance for the database.
In CF deployments with internal MySQL clusters, a single MySQL database VM with CPU usage over ~80% can be considered overloaded. When this happens, the MySQL VMs must be scaled up to prevent the added load of additional Cloud Controllers exacerbating the issue.
Cloud Controller API VMs should primarily be scaled horizontally. Scaling up the number of cores on a single VM is not effective. This is because Ruby’s Global Interpreter Lock (GIL) limits the `cloud_controller_ng` process so that it can only effectively use a single CPU core on a multi-core machine.

**Note**
Since Cloud Controller supports both PostgreSQL and MySQL external databases, there is no absolute guidance about what a healthy database looks like. In general, high database CPU utilization is a good indicator of scaling issues, but always defer to the documentation specific to your database.

## cloud\_controller\_worker\_local
Colloquially known as “local workers,” this job is primarily responsible for handling files uploaded to the API VMs during `cf push`, such as `packages`, `droplets`, and resource matching.

### When to scale
When determining whether to scale `cloud\_controller\_worker\_local`, look for the following:

#### Key metrics
Cloud Controller emits the following metrics:

* `cc.job_queue_length.cc-VM_NAME-VM_INDEX` is continuously growing.

* `cc.job_queue_length.total` is continuously growing.

#### Heuristic failures
The following behaviors may occur:

* `cf push` is intermittently failing.

* `cf push` average time is elevated.

#### Relevant log files
You can find the above heuristic failures in the following log files:

* `/var/vcap/sys/log/cloud_controller_ng/cloud_controller_ng.log`

### How to scale
Because local workers are located with the Cloud Controller API job, they are scaled horizontally along with the API.

## cloud\_controller\_worker
Colloquially known as “generic workers” or just “workers”, this job and VM are responsible for handling asynchronous work, batch deletes, and other periodic tasks scheduled by the `cloud_controller_clock`.

### When to scale
When determining whether to scale `cloud\_controller\_worker`, look for the following:

#### Key metrics
Cloud Controller emits the following metrics:

* `cc.job_queue_length.cc-VM_TYPE-VM_INDEX` (ie. `cc.job_queue_length.cc-cc-worker-0`) is continuously growing.

* `cc.job_queue_length.total` is continuously growing.

#### Heuristic failures
The following behaviors may occur:

* `cf delete-org ORG_NAME` appears to leave its contained resources around for a long time.

* Users report slow deletes for other resources.

* cf-acceptance-tests succeed generally, but fail during cleanup.

#### Relevant log files
You can find the above heuristic failures in the following log files:

* `/var/vcap/sys/log/cloud_controller_worker/cloud_controller_worker.log`

### How to scale
The cc-worker VM can safely scale horizontally in all deployments, but if your worker VMs have CPU/memory headroom, you can also use the `cc.jobs.generic.number_of_workers` BOSH property to increase the number of worker processes on each VM.

## cloud\_controller\_clock and cc\_deployment\_updater
The `cloud_controller_clock` job runs Diego sync process and schedules periodic background jobs. The `cc_deployment_updater` job is responsible for handling v3 rolling app deployments.

**Note**
Running `bosh instances --vitals` returns CPU values. The CPU User value corresponds to the `system.cpu.user` metric and is scaled by the number of CPUs. For example, on a 4-core `api` VM, a `cloud_controller_ng` process that is using 100% of a core is listed as using 25% in the `system.cpu.user` metric.

### When to scale
When determining whether to scale `cloud\_controller\_clock` and `cc\_deployment\_updater`, look for the following:

#### Key metrics
Cloud Controller emits the following metrics:

* `cc.Diego_sync.duration` is continuously increasing over time.

* `system.cpu.user` is high on the scheduler VM.

#### Heuristic failures
The following behaviors may occur:

* Diego domains frequently lack freshness. For more information, see the [Domain Freshness](https://github.com/cloudfoundry/bbs/blob/master/doc/domains.md#domain-freshness) section in the *Overview of Domains* topic on GitHub.

* The Diego Desired LRP count is larger than the total process instance count reported through the Cloud Controller APIs.

* Deployments are slow to increase and decrease instance count.

#### Relevant log files
You can find the above heuristic failures in the following log files:

* `/var/vcap/sys/log/cloud_controller_clock/cloud_controller_clock.log`

* `/var/vcap/sys/log/cc_deployment_updater/cc_deployment_updater.log`

### How to scale
Both of these jobs are singletons, so extra instances are for failover HA rather than scalability. Performance issues are likely due to database overloading or greedy neighbors on the scheduler VM.

## blobstore\_nginx
The internal WebDAV blobstore that comes included with Cloud Foundry by default. It is used by the platform to store `packages`, staged `droplets`, `buildpacks`, and cached app resources. Files are typically uploaded to the internal blobstore through the Cloud Controller local workers and downloaded by Diego when app instances are started.

### When to scale
When determining whether to scale `blobstore_nginx`, look for the following:

#### Key metrics
Cloud Controller emits the following metrics:

* `system.cpu.user` is consistently high on the `singleton-blobstore` VM.

* `system.disk.persistent.percent` is high, indicating that the blobstore is running out of room for additional files.

#### Heuristic failures
The following behaviors may occur:

* `cf push` is intermittently failing.

* `cf push` average time is elevated.

* App droplet downloads are timing out or failing on Diego.

#### Relevant log files
You can find the above heuristic failures in the following log files:

* `/var/vcap/sys/log/blobstore/internal_access.log`

### How to scale
The internal WebDAV blobstore cannot be scaled horizontally, not even for availability purposes, because of its reliance on the `singleton-blobstore` VM’s persistent disk for file storage. For this reason, it is not recommended for environments that require high availability. For these environments, you should use an external blobstore. For more information, see [Cloud Controller blobstore configuration](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html) and the [Blob storage](https://docs.cloudfoundry.org/concepts/high-availability.html#blobstore) section of the *High Availability in Cloud Foundry* topic.
The internal WebDAV blobstore can be scaled vertically, so scaling up the number of CPUs or adding faster disk storage can improve the performance of the internal WebDAV blobstore if it is under high load.
High numbers of concurrent app container starts on Diego can cause stress on the blobstore. This typically happens during upgrades in environments with a large number of apps and Diego Cells. If vertically scaling the blobstore or improving its disk performance is not an option, limiting the max number of concurrent app container starts can mitigate the issue. For more information, see the [starting\_container\_count\_maximum](https://bosh.io/jobs/auctioneer?source=github.com/cloudfoundry/diego-release&version=2.29.0#p%3ddiego.auctioneer.starting_container_count_maximum) section in the *auctioneer job from diego/2.29.0* topic in the BOSH documentation.