# The application container life cycle on the Diego architecture
The life cycle stages of an application container for your Cloud Foundry deployments running on the Diego architecture include deployment, failure events, evacuation, and shutdown.

## Deployment
App deployment involves uploading, staging, and starting the app in a container. Your app must complete each of these phases within a certain time limit. The default time limits for the phases are:

* Upload: 15 minutes

* Stage: 15 minutes

* Start: 60 seconds
Your administrator can change these default settings. Check with your administrator for the actual time limits set for app deployment.
Developers can change the time limit for starting apps through an app manifest or on the command line. For more information, see [Deploying with app manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html) and [Using app health checks](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html).

## Crash events
If an app instance fails, Cloud Foundry restarts it by rescheduling the instance on another container three times. After three failed restarts, Cloud Foundry waits 30 seconds before attempting another restart. The wait time doubles each restart until the ninth restart, and remains at that duration until the 200th restart. After the 200th restart, Cloud Foundry stops trying to restart the app instance.

## Evacuation
Some actions require restarting VMs with containers hosting app instances. For example, you can update stemcells or install a new version of Cloud Foundry. You must restart all the VMs in a deployment.
Cloud Foundry relocates the instances on VMs that are shutting down through a process called evacuation. Cloud Foundry recreates the app instances on another VM, waits until they are healthy, and then shuts down the old instances. During an evacuation, you might see the app instances in a duplicated state for a brief time.
During app duplication, singleton app instances might become temporarily unavailable if the replacement instance does not become healthy within the evacuation timeout of the Diego Cell (the default is ten minutes). App developers with a low tolerance for downtime might prefer to run several instances of their app. See [Run multiple instances to increase availability](https://docs.cloudfoundry.org/devguide/deploy-apps/prepare-to-deploy.html#increase-availability).

## Shutdown
Cloud Foundry requests a shutdown of your app instance when:

* A user runs `cf scale`, `cf stop`, `cf push`, `cf delete`, or `cf restart-app-instance`.

* A system event occurs, such as the replacement procedure during Diego Cell evacuation or when an app instance stops because of a failed health check probe.
To stop the app, Cloud Foundry sends the app process in the container a SIGTERM. By default, the process has ten seconds to shut down gracefully. If the process has not exited after ten seconds, Cloud Foundry sends a SIGKILL.
By default, apps must finish their in-flight jobs within ten seconds of receiving the SIGTERM before Cloud Foundry stops the app with a SIGKILL. For example, a web app must finish processing existing requests and stop accepting new requests.
To change the timeout period, change the BOSH property `containers.graceful_shutdown_interval_in_seconds` on the replacement jobs.
This might increase the time it takes to drain Diego Cells, which causes increased deployment time.

**Note**
An exception to the cases previously mentioned is when monit restarts a Diego Cell replacement or Garden server that has failed. In this case, Cloud Foundry immediately stops the apps that are still running using SIGKILL.