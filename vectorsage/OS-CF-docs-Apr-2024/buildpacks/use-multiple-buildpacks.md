# Pushing an app with multiple buildpacks
You can push an app with multiple buildpacks using the Cloud Foundry Command Line Interface (cf CLI).
As an alternative to the cf CLI procedure, you can specify multiple
buildpacks in your app manifest. This is not compatible with deprecated app manifest features. For more information, see [Deploying with App Manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html).
For more information about pushing apps, see [Pushing an App](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html).

## Specifying buildpacks with the cf CLI
To push an app with multiple buildpacks using the cf CLI:

**Note**
You must use cf CLI v6.38 or later.

1. Ensure that you are using the cf CLI v6.38 or later by running:
```
cf version
```
For more information about upgrading the cf CLI, see [Installing the cf CLI](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html).

2. To push your app with multiple buildpacks, specify each buildpack with a `-b` flag by running:
```
cf push YOUR-APP -b BUILDPACK-NAME-1 -b BUILDPACK-NAME-2 ... -b BUILDPACK-NAME-3
```
Where:

* `YOUR-APP` is the name of your app.

* `BUILDPACK-NAME-1`, `BUILDPACK-NAME-2`, and `BUILDPACK-NAME-3` are the names of the buildpacks you want to push with your app.
The last buildpack you specify is the **final buildpack**, which modifies the launch environment and sets the start command.
To see a list of available buildpacks, run:
```
cf buildpacks
```
For more information on multi buildpack order, see [How buildpacks work](https://docs.cloudfoundry.org/buildpacks/understand-buildpacks.html).
For more information about using the cf CLI, see [Using the cf CLI Cloud Foundry command line interface](https://docs.cloudfoundry.org/cf-cli/).