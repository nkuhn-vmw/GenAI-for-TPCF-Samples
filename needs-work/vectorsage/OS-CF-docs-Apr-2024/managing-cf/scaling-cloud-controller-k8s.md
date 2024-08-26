# Scaling Cloud Controller (cf-for-k8s)
This topic describes how and when to scale CAPI in cf-for-k8s, and includes details about some key metrics, heuristics, and logs.

## cf-api-server
The `cf-api-server` is the primary container in CAPI. It, along with `nginx`, powers the Cloud Controller API that all users of Cloud Foundry interact with. In addition to serving external clients, `cf-api-server` also provides APIs for internal components within Cloud Foundry, such as logging and networking subsystems.

### When to scale
When determining whether to scale `cf-api-server`, look for the following:

#### Key metrics
Cloud Controller emits the following metrics:

* `sum(rate(container_cpu_usage_seconds_total{container="cf-api-server"}[1m])) by (pod)` is above 0.85 utilization of a single pod’s CPU allocation.

* `cc_vitals_uptime` is consistently low, indicating frequent restarts (possibly due to memory pressure).

#### Heuristic failures
The following behaviors may occur:

* There is a latency in average response.

* Web UI responsiveness or timeouts are degraded.

#### Relevant logs
You can find the above heuristic failures in the following logs:

* `kapp logs -a cf -m 'cf-api-server%' -c cf-api-server`

* `kapp logs -a cf -m 'cf-api-server%' -c nginx`

### How to scale
Before and after scaling Cloud Controller API pods, you should verify that the Cloud Controller database is not overloaded. All Cloud Controller processes are backed by the same database, so heavy load on the database impacts API performance regardless of the number of Cloud Controllers deployed. Cloud Controller supports both PostgreSQL and MySQL, so there is no specific scaling guidance for the database.
Cloud Controller API pods should primarily be scaled horizontally. Scaling up the number of compute resources requested past one CPU is not effective. This is because Ruby’s Global Interpreter Lock (GIL) limits the `cloud_controller_ng` process so that it can only effectively use a single CPU core on a multi-core machine.

**Note**
Since Cloud Controller supports both PostgreSQL and MySQL external databases, there is no absolute guidance about what a healthy database looks like. In general, high database CPU utilization is a good indicator of scaling issues, but always give precedence to the documentation specific to your database.

## cf-api-local-worker
Known as “local workers,” this container is primarily responsible for handling files uploaded to the API pods during `cf push`, such as `packages`, `droplets`, and resource matching.

### When to scale
When determining whether to scale `cf-api-local-worker`, look for the following:

#### Key metrics
Cloud Controller emits the following metrics:

* `cc_job_queue_length_cc-CF_API_SERVER_POD_NAME` is continuously growing.

* `cc_job_queue_length_total` is continuously growing.

#### Heuristic failures
The following behaviors may occur:

* `cf push` is intermittently failing.

* `cf push` average time is elevated.

#### Relevant logs
You can find the above heuristic failures in the following logs:

* `kapp logs -a cf -m 'cf-api-server%' -c cf-api-server`

### How to scale
Because local workers are co-located with the Cloud Controller API pod, they are scaled horizontally along with the API.

## cf-api-worker
Known as “generic workers” or just “workers”, these pods are responsible for handling asynchronous work, batch deletes, and other periodic tasks scheduled by the `cf-api-clock`.

### When to scale
When determining whether to scale `cf-api-worker`, look for the following:

#### Key metrics
Cloud Controller emits the following metrics:

* `cc_job_queue_length_cc-CF_API_WORKER_POD_NAME` (for example, `cc_job_queue_length_cc_cf_api_worker_565c45df86_h2nsp`) is continuously growing.

* `cc_job_queue_length_total` is continuously growing.

#### Heuristic failures
The following behaviors may occur:

* `cf delete-org ORG_NAME` appears to leave its contained resources around for a long time.

* Users report slow deletes for other resources.

* cf-acceptance-tests succeed generally, but fail during cleanup.

#### Relevant logs
You can find the above heuristic failures in the following log files:

* `kapp logs -m 'cf-api-worker%' -c cf-api-worker`

### How to scale
The `cf-api-worker` pod can safely scale horizontally in all deployments.

## cf-api-clock and cf-api-deployment-updater
The `cf-api-clock` job runs the Eirini sync process and schedules periodic background jobs. The `cf-api-deployment-updater` job is responsible for handling v3 rolling app deployments. For more information, see [Rolling App Deployments (Beta)](https://docs.cloudfoundry.org/devguide/deploy-apps/rolling-deploy.html).

### When to scale
When determining whether to scale `cf-api-clock` and `cf-api-deployment-updater`, look for the following:

#### Key metrics
Cloud Controller emits the following metrics:

* `sum(rate(container_cpu_usage_seconds_total{container="cf-api-clock"}[1m])) by (pod)` is high (approaching 1.0).

#### Heuristic failures
The following behaviors may occur:

* The number of workload pods in the `cf-workloads` namespace does not match the total process instance count reported through the Cloud Controller APIs.

* Deployments are slow to increase and decrease instance count.

#### Relevant logs
You can find the above heuristic failures in the following log files:

* `kapp logs -m 'cf-api-clock%' -c cf-api-clock`

* `kapp logs -m 'cf-api-deployment-updater%' -c cf-api-deployment-updater`

### How to scale
Both of these pods are singletons, so extra instances are for failover high availability rather than scalability. Performance issues are likely due to database overloading.