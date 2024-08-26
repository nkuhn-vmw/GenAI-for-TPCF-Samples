# Using Cloud Foundry health checks
Cloud Foundry provides support for liveness and readiness health checks.
Liveness health checks are performed to validate that app instances are running.
When liveness health checks fail, the app instance is marked as crashed and is
restarted. Readiness health checks are performed to validate that app instances are
ready to serve requests. When readiness health checks fail, the app instance is
marked as not ready and removed from the route pool for the app.
You can configure a liveness health check for an app using the Cloud Foundry
Command Line Interface (cf CLI) or by specifying a combination of the
`health-check-http-endpoint`, `health-check-type`,
`health-check-invocation-timeout`, and `health-check-interval` fields in an
[app manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html).
Readiness health checks are only configurable through the [app manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#optional-attributes).
To use readiness health checks, you must have:

* garden-runc-release 1.37.0

* diego-release 2.81.0

* capi-release 1.158.0
To configure a health check using the cf CLI, see:

* [Configure health checks when creating or updating](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html#setting-health-checks)

* [Configure health checks for an existing app](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html#set-health-checks-exist).
For more information about using an app manifest to configure a health check, see these sections in *Deploying with app manifests*.

* [health-check-type](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#health-check-type)

* [health-check-interval](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#health-check-interval)

* [health-check-http-endpoint](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#health-check-http-ep)

* [health-check-invocation-timeout](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#health-check-invoc-time)

* [readiness-health-check-type](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#readiness-health-check-type)

* [readiness-health-check-interval](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#readiness-health-check-interval)

* [readiness-health-check-http-endpoint](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#readiness-health-check-http-ep)

* [readiness-health-check-invocation-timeout](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#readiness-health-check-invoc-time)
App health checks function as part of the app life cycle managed by Diego architecture. For more
information, see [Diego components and architecture](https://docs.cloudfoundry.org/concepts/diego/diego-architecture.html).

## Configure liveness health checks when creating or updating an app
To configure a health check while creating or updating an app, run:
```
cf push APP-NAME --health-check-type LIVENESS-HEALTH-CHECK-TYPE --app-start-timeout LIVENESS-HEALTH-CHECK-TIMEOUT
```
Where:

* `APP-NAME` is the name of your app.

* `LIVENESS-HEALTH-CHECK-TYPE` is the type of liveness health check that you want to configure. Valid health check
types are `port`, `process`, and `http`. For more information, see [Health check types](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html#types).

* `LIVENESS-HEALTH-CHECK-TIMEOUT` is the amount of time allowed to elapse between starting an app and the
first healthy response. For more information, see [Health check timeouts](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html#health_check_timeout).
For more information about the `cf push` command, see
[push](http://cli.cloudfoundry.org/en-US/cf/push.html) in the Cloud Foundry CLI Reference Guide.

**Important**
The health check configuration that you provide with
`cf push` overrides any configuration in the app manifest.

## Configure liveness health checks for an existing app
To configure a liveness health check for an existing app or to add a custom HTTP endpoint, run:
```
cf set-health-check APP-NAME LIVENESS-HEALTH-CHECK-TYPE --endpoint CUSTOM-HTTP-ENDPOINT
```
Where:

* `APP-NAME` is the name of your app.

* `LIVENESS-HEALTH-CHECK-TYPE` is the type of the liveness health check that you want to configure. Valid health check types are `port`, `process`, and `http`. For more information, see [Health check types](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html#types).

* `CUSTOM-HTTP-ENDPOINT` is the custom HTTP endpoint that you want to add to the health check. By default, an `http` health check uses `/` as its endpoint unless you specify a custom endpoint. For more information, see [Health check HTTP endpoints](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html#health_check_uri).
You can also change the health check invocation timeout for
an app. If you are using cf CLI v6, use `cf v3-set-health-check`. If you have cf CLI v7, use `cf set-health-check`. This option also requires restarting the app. For more information, see [Apps](https://cli.cloudfoundry.org/en-US/v7/apps.html) in the Cloud Foundry CLI Reference Guide.
For more information about the `cf set-health-check` command, see
[set-health-check](http://cli.cloudfoundry.org/en-US/cf/set-health-check.html) in
the Cloud Foundry CLI Reference Guide.

**Important**
After you set the health check configuration of a deployed
app with the `cf set-health-check` command, you must restart the app for the change to
take effect.

## Understanding health checks

### Health check life cycle
The following table describes how app health checks work.
| Stage | Description |
| --- | --- |
| 1 | When deploying the app to Cloud Foundry, the developer specifies a liveness and/or a readiness health check, and optionally, a startup timeout with the app manifest. |
| 2 | Cloud Controller creates an LRP for Diego with the specified health check definitions. If no liveness health check is provided, Cloud Controller configures a `port` liveness health check type. If no readiness health check is provided, Cloud Controller configures a `process` readiness health check type. |
| 3 | When Diego starts an app instance, a separate startup app health check runs every 2 seconds until a response indicates that the app instance is healthy or until the startup timeout elapses. The startup health check uses the same configuration (type, http endpoint, and invocation timeout) as the liveness health check, except for the non-configurable 2-second polling interval. |
| 4 | After the startup health check succeeds, the app instance is marked as Running and Diego begins performing the liveness and readiness health checks. Liveness and readiness health checks are run according to their configured health check interval, with a default of 30 seconds. |
| 5 | After the readiness health check succeeds, the app instance route is advertised. |
| 6 | The app instance is alive, marked as Running, and is routable. The app instance is fully operational. |
| 7 | If the readiness health check fails, then the route to the app instance is removed. |
| 8 | If the liveness health check fails, Diego considers that particular instance to be unhealthy. Diego stops and deletes the app instance, then reschedules a new app instance. This process of stopping and deleting the app instance is reported back to the Cloud Controller as a crash event. |
| 9 | When an app instance fails, Diego immediately attempts to restart the app instance. After three failed restarts, Cloud Foundry waits 30 seconds before attempting another restart. The wait time doubles each restart until the ninth restart, and remains at that duration until the 200th restart. After the 200th restart, Cloud Foundry stops trying to restart the app instance. |

### Health check types
The following table describes the types of health checks available for apps and recommended
circumstances in which to use them:
| Health check type | Recommended use case | Explanation |
| --- | --- | --- |
|| `http` | The app can provide an `HTTP 200` response. | The `http` health check performs a GET request to the configured HTTP endpoint
on the app’s default port. When the health check receives an `HTTP 200` response,
the app is declared healthy. Cloud Foundry recommends that you use the
`http` health check type whenever possible. A healthy HTTP response ensures that the
web app is ready to serve HTTP requests. The configured endpoint must respond within one second
to be considered healthy.

**Important**
To prevent false
negatives, use a dedicated endpoint for health checks where response time and result do not
depend on business logic. |
| `port` | The app can receive TCP connections, including HTTP web apps. | A health check makes a TCP connection to the port or ports configured for the app. For apps
with multiple ports, a health check monitors each port. If you do not specify a health
check type for your app, then monitoring uses a `port` health
check by default. The TCP connection must be established within one second to be considered healthy. |
| `process` | The app does not support TCP connections. An example of such an app is a worker. | For a `process` health check, Diego ensures that any process declared for the
app stays running. If the process and all its children exit, Diego stops and deletes the app instance. |

### Health check timeouts
The startup timeout value configured for the app process is the amount of time
allowed to elapse between starting an app and the first healthy response from
the app. If the health check does not receive a healthy response within the
configured timeout, then the app is declared unhealthy.
In Cloud Foundry, the default timeout is 60 seconds and the default maximum configurable timeout is 180 seconds. Your Cloud Foundry operator can set other values for these defaults.

### Health check HTTP endpoints
Only used by `http` type, the `--endpoint` flag of the `cf set-health-check` command specifies the
path portion of a URI that must be served by the app and return `HTTP 200` when the app is healthy.
This command only checks the health of the default port of the app.

**Important**
For HTTP apps, Cloud Foundry recommends setting the health check type to `http` instead of a simple port check.