# Configuring rolling app deployments
You can use Cloud Foundry Command Line Interface (cf CLI) commands
or the Cloud Foundry API (CAPI) to push your apps to Cloud Foundry using a rolling deployment.
For information about the traditional method for addressing app downtime while pushing app updates,
see [Using blue-green deployment to reduce downtime and risk](https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html).
For more information about CAPI, see the
[Cloud Foundry API (CAPI) documentation](https://v3-apidocs.cloudfoundry.org/).

## Prerequisites
The procedures in this topic require one of the following:

* **cf CLI v7:** Install cf CLI v7.

* **cf CLI v6:** If you use cf CLI v6:

+ You must install cf CLI v6.40 or later.

+ The rolling deployment feature must be activated for your deployment. Use capi-release v0.168.0 or later and deploy the [cc\_deployment\_updater](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/experimental/add-deployment-updater.yml). For this ops file, there are also [external-db](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/experimental/add-deployment-updater-external-db.yml) and [postgres](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/experimental/add-deployment-updater-postgres.yml) variants.

* **CAPI V3:** If you use CAPI V3, you must install the cf CLI.

## Commands
This section describes the commands for working with rolling app deployments.

### Deploy an app
To deploy an app without incurring downtime:

**Caution**
Review the limitations of this feature before running the command. For more information, see
[Limitations](https://docs.cloudfoundry.org/devguide/deploy-apps/rolling-deploy.html#limitations).

* **For cf CLI v7, run:**
```
cf push APP-NAME --strategy rolling
```
Where `APP-NAME` is the name that you want to give your app.

**Note**
cf CLI v7 exits when one instance of each process is healthy.
It also includes a `--no-wait` flag on push for users who don’t want to wait
for the operation to complete.
`cf push` used with the `--no-wait` flag exits as soon as one instance is healthy.
If the deployment stops and doesn’t restart, cancel it and run it again as described in an earlier step.
To cancel, see [Cancel a deployment](https://docs.cloudfoundry.org/devguide/deploy-apps/rolling-deploy.html#cancel).

* **For cf CLI v6, run:**
```
cf v3-zdt-push APP-NAME
```
Where `APP-NAME` is the name that you want to give your app.

**Important**
This command is experimental and unsupported. Upgrade to cf CLI v7 ([Upgrading to cf CLI v7](https://docs.cloudfoundry.org/cf-cli/v7.html)) or or cf CLI v8 ([Upgrading to cf CLI v8](https://docs.cloudfoundry.org/cf-cli/v8.html)).

* **For CAPI V3:**

1. Log in to the cf CLI.
```
cf login
```

2. Create an empty app by running the following `curl` command with `POST /v3/apps`. Record the
app GUID from the output.
```
cf curl /v3/apps \

-X POST \

-H "Content-type: application/json" \

-d '{
"name": "APP-NAME",
"relationships": {
"space": {
"data": {
"guid": "SPACE-GUID"
}
}
}
}'
```
Where:

+ `APP-NAME` is the name that you want to give your app.

+ `SPACE-GUID` is the space identifier that you want to associate with your app.

3. Create a package with the following `curl` command with `POST /v3/packages`. Record the package
GUID from the output.
```
cf curl /v3/packages \

-X POST \

-H "Content-type: application/json" \

-d '{
"type": "bits",
"relationships": {
"app": {
"data": {
"guid": "APP-GUID"
}
}
}
}'
```
Where `APP-GUID` is the app GUID that you recorded in an earlier step. This app GUID is a
unique identifier for your app.

4. Upload the package bits by running the following `curl` command with
`POST /v3/packages/PACKAGE-GUID/upload`.
```
cf curl /v3/packages/PACKAGE-GUID/upload \

-X POST \

-F bits=@"PACKAGED-APP" \
```
Where:

+ `PACKAGE-GUID` is the package GUID that you recorded in an earlier step.

+ `PACKAGED-APP` is your app packaged in a file such as `.zip`.

5. Create the build by running the following `curl` command with `POST /v3/builds`. Record the
droplet GUID from the output.
```
cf curl /v3/builds \

-X POST \

-H "Content-type: application/json" \

-d '{
"package": {
"guid": PACKAGE-GUID"
}
}'
```
Where `PACKAGE-GUID` is the package GUID that you recorded in an earlier step.

6. Deploy your app by running the following `curl` command with `POST /v3/deployments`. To verify
the status of the deployment or take action on the deployment, record the deployment GUID from the
output.
```
cf curl /v3/deployments \

-X POST \

-H "Content-type: application/json" \

-d '{
"droplet": {
"guid": "DROPLET-GUID"
},
"strategy": "rolling",
"relationships": {
"app": {
"data": {
"guid": "APP-GUID"
}
}
}
}'
```
Where `DROPLET-GUID` and `APP-GUID` are the GUIDs that you recorded in earlier steps.
For more information about this command, see [How it works](https://docs.cloudfoundry.org/devguide/deploy-apps/rolling-deploy.html#how-it-works).

### Cancel a deployment
To stop the deployment of an app that you pushed:

* **For cf CLI v7, run:**
```
cf cancel-deployment APP-NAME
```
Where `APP-NAME` is the name of the app.

* **For cf CLI v6, run:**
```
cf v3-cancel-zdt-push APP-NAME
```
Where `APP-NAME` is the name of the app.

**Important**
This command is experimental and unsupported. Upgrade to cf CLI v7 ([Upgrading to cf CLI v7](https://docs.cloudfoundry.org/cf-cli/v7.html)) or or cf CLI v8 ([Upgrading to cf CLI v8](https://docs.cloudfoundry.org/cf-cli/v8.html)).

* **For CAPI V3, run:**
```
cf curl /v3/deployments/DEPLOYMENT-GUID/actions/cancel" -X POST
```
Where `DEPLOYMENT-GUID` is the GUID of the deployment that you recorded after following the
CAPI procedure in [Deploy an app](https://docs.cloudfoundry.org/devguide/deploy-apps/rolling-deploy.html#deploy).
This reverts the app to its state from before the deployment started by:

* Scaling up the original web process

* Removing any deployment artifacts

* Resetting the `current_droplet` on the app

**Note**
The cancel command is designed to revert the app to its
original state as quickly as possible and does not guarantee zero downtime. Additionally, changes
to environment variables and service bindings will not be reverted.

### Restart an app
To restart your app without downtime, run the appropriate command. Restart an app to apply
configuration updates that require a restart, such as environment variables or service bindings.

* **For cf CLI v7, run:**
```
cf restart APP-NAME --strategy rolling
```
Where `APP-NAME` is the name of the app.

* **For cf CLI v6, run:**
```
cf v3-zdt-restart APP-NAME
```
Where `APP-NAME` is the name of the app.

**Important**
This command is experimental and unsupported. Upgrade to cf CLI v7 ([Upgrading to cf CLI v7](https://docs.cloudfoundry.org/cf-cli/v7.html)) or or cf CLI v8 ([Upgrading to cf CLI v8](https://docs.cloudfoundry.org/cf-cli/v8.html)).

* **For CAPI V3, run:**
```
cf curl /v3/deployments \

-X POST \

-H "Content-type: application/json" \

-d '{
"droplet": {
"guid": "DROPLET-GUID"
},
"strategy": "rolling",
"relationships": {
"app": {
"data": {
"guid": "APP-GUID"
}
}
}
}'
```
Where `DROPLET-GUID` and `APP-GUID` are the GUIDs that you recorded in earlier steps.

## How it works
This section describes the rolling deployments and their limitations.

### Rolling deployment
This section describes pushing an app with a rolling deployment strategy.

1. The `cf push APP-NAME --strategy rolling` command:

1. Stages the updated app package.

2. Creates a droplet with the updated app package.

3. Creates a deployment with the new droplet and any new configuration.

* This starts a new process with one instance that shares the route with the old process.

* Now, if you run `cf app` on your app, you see multiple `web` processes.
For more information about the deployment object, see the [Deployments](http://v3-apidocs.cloudfoundry.org/index.html#deployments) section of the CAPI V3 documentation.

2. After the command creates the deployment, the `cc_deployment_updater` BOSH job runs in the
background, updating deployments as follows:

1. Adds another instance of the new web process and removes an instance from the old web process. This step repeats until the new web process reaches the required number of instances.

**Important**
This happens only if all instances of the new web process are running.

2. Removes the old web process. The new web process now fully replaces the old web process.

3. Restarts all non-web processes of the app.

4. Sets the deployment to `DEPLOYED`.

### Limitations
The following table describes the limitations of when using rolling deployments.
| Limitation | Description |
| --- | --- |
| App manifests | The `cf v3-zdt-push` command does not support providing an app manifest with the
`-f` flag. If you have a `manifest.yml` file in your app directory, it is
ignored. This limitation only applies to cf CLI v6. |
| SSH to app instances | Pushing updates to your app with a `cf v3-zdt-push` command causes the new web process
and app GUID to mismatch. `cf ssh` does not handle this scenario. You must use the
`cf v3-ssh` command instead. This limitation only applies to cf CLI v6. |
| Multiple app versions | During a deployment, Cloud Foundry serves both the old and new version of your app at the
same route. This can lead to user issues if you push backwards-incompatible API changes. |
| Database migrations | Deployments do not handle database migrations. Migrating an app database when the existing
app is not compatible with the migration can result in downtime. |
| Non-web processes | Rolling deployments only run web processes through the rolling update sequence described
earlier. The commands restart worker and other non-web processes in bulk after updating all web
processes.
The CAPI V3 API introduces the concept of processes as runnable units of an app. Each app has a
web process by default. You can specify additional processes with a Procfile, and in some cases
buildpacks create additional processes. For more information about processes, see
[Processes](http://v3-apidocs.cloudfoundry.org/index.html#processes) in the CAPI V3
documentation. |
| Quotas | Pushing updates to your app using a rolling deployment strategy creates an extra instance
of your app. If you lack sufficient quota, the deployment fails. Administrators might need to increase
quotas to accommodate rolling deployments. |
| Simultaneous apps when interrupting a push | If you push app before your previous push command for the same app has completed, your
first push gets interrupted. Until the last deployment completes, there might be many versions
of the app running at the same time. Eventually, the app runs the code from your most recent
push. |
| V3 APIs | During a rolling deploy for an app, requests to the V3 APIs for scaling or updating a process fail with an error message
like `Cannot scale this process while a deployment is in flight.`. For more information, see [Scale a process](https://v3-apidocs.cloudfoundry.org/version/3.109.0/index.html#scale-a-process)
or [Update a process](https://v3-apidocs.cloudfoundry.org/version/3.109.0/index.html#update-a-process) in the CAPI V3 documentation. |

## View the status of rolling deployments
You can use CAPI to view the status of rolling deployments.
To view the status of a rolling deployment:

1. Log in to the cf CLI:
```
cf login
```

2. Find the GUID of your app by running:
```
cf app APP-NAME --guid
```
Where `APP-NAME` is the name of the app.

3. Find the deployment for that app by running:
```
cf curl GET /v3/deployments?app_guids=APP-GUID&status_values=ACTIVE
```
Where `APP-GUID` is the GUID of the app. Deployments are listed in chronological order, with
the latest deployment displayed as the last in a list.

4. Run:
```
cf curl GET /v3/deployments/DEPLOYMENT-GUID
```
Where `DEPLOYMENT-GUID` is the GUID of the rolling deployment.
`cf curl GET /v3/deployments/DEPLOYMENT-GUID` returns these status properties for rolling deployments:

* `status.value`: Indicates if the deployment is `ACTIVE` or `FINALIZED`.

* `status.reason`: Provides detail about the deployment status.

* `status.details`: Provides the timestamp for the most recent successful health check.
The value of the `status.details` property can be `nil` with no successful health check
for the deployment. For example, there might be no successful health check if the deployment was
cancelled.
The following table describes the possible values for the `status.value` and `status.reason`
properties:
`status.value` | `status.reason` | Description || `ACTIVE` | `DEPLOYING` | The deployment is deploying. |
| `ACTIVE` | `CANCELLING` | The deployment is cancelling. |
| `FINALIZED` | `DEPLOYED` | The deployment was deployed. |
| `FINALIZED` | `CANCELLED` | The deployment was cancelled. |
| `FINALIZED` | `SUPERSEDED` | The deployment was stopped and did not finish deploying because there was another
deployment created for the app.
|
| `FINALIZED` | `DEGENERATE` | The deployment was created incorrectly by the system. |