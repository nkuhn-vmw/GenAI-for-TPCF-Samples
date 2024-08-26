# Running cf push sub-step commands
The Cloud Foundry Command Line Interface (cf CLI) includes commands that provide detailed control over app pushes. When you use these commands, you can follow only some steps of the `cf push` procedure or you can perform specific actions between the steps that are normally part of running `cf push`.
Here are some example use cases for the sub-step commands:

* Updating a third-party system before staging an app

* Retrying failed stagings without incurring downtime

* Calling external services to report audit data during push

* Scanning a droplet before deploy

* Integrating with a change request system
To support these custom push workflows, Cloud Foundry divides apps into smaller building blocks.
The following table describes the building blocks as resources and lists the command associated with each one.
For information about using these commands, see [Example workflows](https://docs.cloudfoundry.org/devguide/push-sub-commands.html#example-workflows).

**Important**
The cf CLI v6 commands described in this topic are experimental and unsupported, but are supported in cf CLI v7. The latest supported cf CLI release is cf CLI v8. To upgrade to cf CLI v7, see [Upgrading to cf CLI v7](https://docs.cloudfoundry.org/cf-cli/v7.html). To upgrade to cf CLI v8, see [Upgrading to cf CLI v8](https://docs.cloudfoundry.org/cf-cli/v8.html).
| Resource | Description | Command |
| --- | --- | --- |
| App | The top-level resource that represents an app and its configuration.
For more information, see [Apps](https://v3-apidocs.cloudfoundry.org/index.html#apps) in the CAPI documentation. | * **cf CLI v6:** `cf v3-create-app`

* **cf CLI v7:** `cf create-app`
|
| Package | The source code that makes up an app.
For more information, see [Packages](https://v3-apidocs.cloudfoundry.org/index.html#packages) in the CAPI documentation. | * **cf CLI v6:** `cf v3-create-package`

* **cf CLI v7:** `cf create-package`
|
| Build | Staging the app. Creating a build combines a Package with a Buildpack and builds it into an executable resource.
For more information, see [Builds](https://v3-apidocs.cloudfoundry.org/index.html#builds) in the CAPI documentation. | * **cf CLI v6:** `cf v3-stage`

* **cf CLI v7:** `cf stage-package`
|
| Droplet | An executable resource that results from a Build.
For more information, see [Droplet](https://v3-apidocs.cloudfoundry.org/index.html#droplets) in the CAPI documentation. | * **cf CLI v6:** `cf v3-set-droplet`

* **cf CLI v7:** `cf set-droplet`
|
| Manifest | A file used when pushing your app to apply bulk configuration to an app and its underlying processes.
For more information, see [Space Manifest](https://v3-apidocs.cloudfoundry.org/index.html#space-manifest) in the CAPI documentation. | * **cf CLI v6:** `cf v3-apply-manifest`

* **cf CLI v7:** `cf create-app-manifest`, `cf apply-manifest`
|

## Example workflows
The following sections describe example workflows for working with the `cf push` sub-step commands.

### Push an app using sub-step commands
This example workflow describes how to push an app using sub-step commands instead of `cf push`.

1. Create your app with cf CLI:

* If you are using cf CLI v7, run:
```
cf create-app APP-NAME
```
Where `APP-NAME` is the name you give your app.

* If you are using cf CLI v6, run:
```
cf v3-create-app APP-NAME
```
Where `APP-NAME` is the name you give your app.

2. From your app directory, create a package for your app.

* If you are using cf CLI v7, run:
```
cf create-package APP-NAME
```
Where `APP-NAME` is the name of your app.

* If you are using cf CLI v6, run:
```
cf v3-create-package APP-NAME
```
Where `APP-NAME` is the name of your app.

3. Locate and copy the `package guid` from the output of an earlier step. See the following example output:
```
Uploading and creating bits package for app APP-NAME in org test / space test as admin...
package guid: 0dfca85a-8ed4-4f00-90d0-3ab08852dba8
OK
```

4. Stage the package you created:

* If you are using cf CLI v7, run:
```
cf stage-package APP-NAME --package-guid PACKAGE-GUID
```
Where:

+ `APP-NAME` is the name of your app.

+ `PACKAGE-GUID` is the package GUID you recorded in an earlier step.

* If you are using cf CLI v6, run:
```
cf v3-stage APP-NAME --package-guid PACKAGE-GUID
```
Where:

+ `APP-NAME` is the name of your app.

+ `PACKAGE-GUID` is the package GUID you recorded in an earlier step.

5. Locate and copy the `droplet guid` from the output of an earlier step. See the following example output:
```
Staging package for APP-NAME in org test / space test as admin...
...
Package staged
droplet guid: f60d3464-415a-4202-9d40-26a70373a487
state: staged
created: Mon 25 Sep 16:37:45 PDT 2018
```

6. Assign the droplet to your app:

* If you are using cf CLI v7, run:
```
cf set-droplet APP-NAME -d DROPLET-GUID
```
Where:

+ `APP-NAME` is the name of your app.

+ `DROPLET-GUID` is the droplet GUID you recorded in an earlier step.

* If you are using cf CLI v6, run:
```
cf v3-set-droplet APP-NAME -d DROPLET-GUID
```
Where:

+ `APP-NAME` is the name of your app.

+ `DROPLET-GUID` is the droplet GUID you recorded in an earlier step.

7. Start your app:

* If you are using cf CLI v7, run:
```
cf start APP-NAME
```
Where `APP-NAME` is the name of your app.

* If you are using cf CLI v6, run:
```
cf v3-start APP-NAME
```
Where `APP-NAME` is the name of your app.

### Roll back to a previous droplet
This example workflow describes how to roll back to a previous droplet used by your app. You might want to use this, for example, if you update your app and it has a bug that causes it to fail.

1. List the droplets for your app:

* If you are using cf CLI v7, run:
```
cf droplets APP-NAME
```
Where `APP-NAME` is the name of your app.

* If you are using cf CLI v6, run:
```
cf v3-droplets APP-NAME
```
Where `APP-NAME` is the name of your app.

2. In the output, locate and copy the second-to-last GUID.
In the following example, this is `66524145-5502-40e6-b782-47fe68e13c49`.
```
Listing droplets of app APP-NAME in org test / space test as admin...
guid state created
66524145-5502-40e6-b782-47fe68e13c49 staged Mon 25 Sep 16:37:34 PDT 2018
0677ad93-9f77-4aaa-9a6b-44da022dcd58 staged Mon 25 Sep 16:44:55 PDT 2018
```

3. Stop your app:

* If you are using cf CLI v7, run:
```
cf stop APP-NAME
```
Where `APP-NAME` is the name of your app.

* If you are using cf CLI v6, run:
```
cf v3-stop APP-NAME
```
Where `APP-NAME` is the name of your app.

4. Set the app to use the previous droplet:

* If you are using cf CLI v7, run:
```
cf set-droplet APP-NAME -d PREVIOUS-DROPLET-GUID
```
Where:

+ `APP-NAME` is the name of your app.

+ `PREVIOUS-DROPLET-GUID` is the droplet GUID you recorded in an earlier step.
```

* If you are using cf CLI v6, run:
```
cf v3-set-droplet APP-NAME -d PREVIOUS-DROPLET-GUID
```
Where:
<ul>
<li><code>APP-NAME</code> is the name of your app.</li>
<li><code>PREVIOUS-DROPLET-GUID</code> is the droplet GUID you recorded in an earlier step.</li>
</ul>
```

1. Start your app:
```

* If you are using cf CLI v7, run:
```
cf start APP-NAME
```
Where `APP-NAME` is the name of your app.

* If you are using cf CLI v6, run:
```
cf v3-start APP-NAME
```
Where `APP-NAME` is the name of your app.
```