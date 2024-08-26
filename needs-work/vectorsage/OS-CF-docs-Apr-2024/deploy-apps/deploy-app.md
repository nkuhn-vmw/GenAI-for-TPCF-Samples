# Pushing your app with Cloud Foundry CLI (cf push)
The cf CLI command `cf push` pushes apps to Cloud Foundry. There are two main ways to run the `cf push` command:

* Run `cf push APP-NAME` to push an app using default settings. For more information, see [Push with defaults](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#default-push).

* Run the `cf push` command with flags and helper files to customize:

+ How the pushed app runs, including its route, instance count, disk size limits, memory limits, and log rate limits

+ How push works: whether it’s configured with a manifest, runs a startup script, or limits files uploaded to the Cloud Controller
For more information about custom settings, see [Push with custom settings](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#custom-push).
For an explanation of what Cloud Foundry does when you run `cf push`, see [How Apps are
Staged](https://docs.cloudfoundry.org/concepts/how-applications-are-staged.html).
For information about the life cycle of an app, see [Application container life cycle](https://docs.cloudfoundry.org/devguide/deploy-apps/app-lifecycle.html).

## Prerequisites
Before you push your app to Cloud Foundry, ensure that:

* Your app is “cloud-ready.” Cloud Foundry behaviors related to file storage, HTTP sessions, and port usage might require modifications to your app. To prepare an app to be pushed to Cloud Foundry, see:

+ [Considerations for designing and running an app in the cloud](https://docs.cloudfoundry.org/devguide/deploy-apps/prepare-to-deploy.html)

+ Any [Buildpacks](https://docs.cloudfoundry.org/buildpacks/) guides specific to your app language or framework, such as [Getting started deploying Ruby on Rails apps](https://docs.cloudfoundry.org/buildpacks/ruby/gsg-ror.html)

* Your Cloud Foundry deployment supports the type of app you are going to push, or you have the URL of an externally-available buildpack that can stage the app.

* All required app resources are uploaded. For example, you might need to include a database driver.

* You have your target and credentials:

+ The API endpoint for your Cloud Foundry deployment. Also known as the target URL, this is [the URL of the Cloud Controller in your Cloud Foundry instance](http://docs.cloudfoundry.org/running/cf-api-endpoint.html).

+ Your user name and password for the Cloud Foundry deployment.

* You are logged into your app’s target org and space.

1. Decide the org and space where you want to push your app. You might have access to one or more org and space.

2. Log in to this target org and space with `cf login`.

* Your app can access every service that it uses, because an instance of the service runs in, or is shared with, the app’s space.

+ For information about sharing service instances across spaces, see [Sharing service instances](https://docs.cloudfoundry.org/devguide/services/sharing-instances.html).

+ Typical services that cloud apps use include databases, message queues, and key-value stores.

## Push with defaults
To push an app with default settings:

1. Choose a name for the app. The app name must consist of alphanumeric characters and be unique to your Cloud Foundry deployment.

* To use an app name that is not unique, customize the app’s route as described in [Customize the route](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#custom-route).

* Apps running at their default routes require unique names because default routes are based on app names, and all routes must be globally unique.

2. Run:
```
cf push APP-NAME
```
Where `APP-NAME` is the name of the app.

### Default route
An app’s route is the URL at which it runs. Cloud Foundry assembles the route for a pushed app from a host name and a domain.
By default, Cloud Foundry sets the host name and domain as follows:

* **Hostname:** The name of the app name, as specified in the `cf push` command. If the app name contains underscores, Cloud Foundry converts them to hyphens when creating the app’s route.

* **Domain:** The default apps domain for your Cloud Foundry deployment.
For example, an app named `example-app` running on Cloud Foundry with an apps domain `apps.example.com` runs at the URL
`https://example-app.apps.example.com` by default.
For more information about routes and domains, see [Routes and domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html).

### Example session
The following example output for `cf push example-app` demonstrates how Cloud Foundry assigns default values to an app you push:
```
Creating app example-app in org example-org / space development as a.user@shared-domain.example.com...
OK
Creating route example-app.shared-domain.example.com...
OK
Binding example-app.shared-domain.example.com to example-app...
OK
Uploading example-app...
Uploading app: 560.1K, 9 files
OK
Starting app example-app in org example-org / space development as a.user@shared-domain.example.com...

-----> Downloaded app package (552K)
OK

-----> Using Ruby version: ruby-1.9.3

-----> Installing dependencies using Bundler version 1.3.2
Running: bundle install --without development:test --path
vendor/bundle --binstubs vendor/bundle/bin --deployment
Installing rack (1.5.1)
Installing rack-protection (1.3.2)
Installing tilt (1.3.3)
Installing sinatra (1.3.4)
Using bundler (1.3.2)
Updating files in vendor/cache
Your bundle is complete! It was installed into ./vendor/bundle
Cleaning up the bundler cache.

-----> Uploading droplet (23M)
1 of 1 instances running
App started
Showing health and status for app example-app in org example-org / space development as a.user@shared-domain.example.com...
OK
requested state: started
instances: 1/1
usage: 1G x 1 instances
urls: example-app.shared-domain.example.com
state since cpu memory disk logging

#0 running 2022-09-14 05:07:18 PM 0.0% 18.5M of 1G 52.5M of 1G 3B/s of 1M/s
```

## Push with custom settings
Pushing an app with custom settings typically proceeds as follows:

1. [Customize Basic App Settings (Optional)](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#basic-settings)

2. [Customize the Route (Optional)](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#custom-route)

3. [Limit the Upload Files (Optional)](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#exclude)

4. [Configure App Initialization (Optional)](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#profile)

5. [Custom Push the App](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#custom-cf-push)

6. [Configure App Services (Optional)](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#services)
The following sections detail these steps.

### Customize basic app settings (optional)
Basic settings to customize when pushing an app include:

* **Name:** You can use any series of alphanumeric characters as the name of your app.

* **Instances:** Generally speaking, the more app instances you run, the less downtime your app experiences. If your app is still in development, running a single instance can simplify troubleshooting. For any production app, Cloud Foundry recommends a minimum of two instances.

* **Memory limit:** The maximum amount of memory that each instance of your app can consume. If an app instance exceeds this limit,
Cloud Foundry restarts the instance. If an app instance exceeds its memory limit repeatedly in a short period of time,
Cloud Foundry delays restarting the app instance.

* **Disk space limit:** The maximum amount of disk space that each instance of your app can consume. If an app instance exceeds this limit,
Cloud Foundry restarts the instance. If an app instance exceeds its disk space limit repeatedly in a short period of time,
Cloud Foundry delays restarting the app instance.

* **Log rate limit:** The maximum number of logs that each instance of your app can send to Loggregator. If an app instance exceeds this limit,
Cloud Foundry drops the excess logs and reports doing so.

* **Start command:** This is the command that Cloud Foundry uses to start each instance of your app. This start command differs by app framework.

### Customize the route (optional)
To customize an app’s route:

1. (Optional) Customize the host name by including the `-n` flag followed by a custom host name in your `cf push` command.

2. (Optional) Customize the domain by including the `-d` flag followed by a custom domain in your `cf push` command. The custom domain must be registered,
and mapped to the org that contains the app’s target space.

3. Ensure that the route is unique. The app’s route must be globally unique, whether you customize its host or domain, or allow it to use the default route described in [Default route](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#default-route). To help ensure route uniqueness, include the `--random-route` flag in your `cf push` command. This creates a route that includes the app name and random words.

### Limit the upload files (optional)
By default, Cloud Foundry uploads all app files except version control files and directories with names such as `.svn`, `.git`, and `_darcs`.
Cloud Foundry recommends that you explicitly exclude extraneous files residing within your app directory, particularly if your app is large. For example, if you build your app locally and push it as a binary, you can save resources by not uploading any of the app’s source code.
To exclude files from upload:

1. Create a `.cfignore` file that lists the files to exclude.

2. Save the `.cfignore` file to the directory where you run the `cf push` command.
For more information, see [Ignore Unnecessary Files When Pushing](https://docs.cloudfoundry.org/devguide/deploy-apps/prepare-to-deploy.html#exclude) in *Considerations for Designing and Running an App in the
Cloud*.

### Configure app initialization (optional)
You can configure the `cf push` command to run custom initialization tasks for an app.
These tasks run after Cloud Foundry loads the app droplet but before it starts the app to allow the initialization script to access the app language runtime environment. For example, your script can map values from `$VCAP_SERVICES` into other environment variables or a config file that the app uses.

**Important**
The following notes include important information about configuring app initialization when you use certain buildpacks:

* **Java:** Initialization scripts for the Java buildpack require additional configuration.

* **PHP:** Cloud Foundry does not support initialization scripts for the PHP buildpack versions prior to v4.3.18. If you use
one of these buildpack versions, your app hosts the `.profile` script’s contents. This means that any app staged using the affected buildpack
versions can leak credentials placed in the `.profile` script.
To run initialization tasks:

1. Create a `.profile` script that contains the initialization tasks.

2. Save the `.profile` script to the directory where you run the `cf push` command.
The following example `.profile` file uses `bash` to set a value for the environment variable `LANG`:
```

# Set the default LANG for your apps
export LANG=en_US.UTF-8
```
Setting this value at the operating system level allows the app to find out which language to use for error messages and instructions, collating sequences, and date formats.
Your app root directory might also include a `.profile.d` directory that contains bash scripts that perform initialization tasks for the buildpack. Developers
must not edit these scripts unless they are using a custom buildpack. For more information about custom buildpacks, see [Custom
Buildpacks](https://docs.cloudfoundry.org/buildpacks/custom.html).
Initialization tasks as described here are also called *pre-runtime hooks* and *`.profile` tasks*.

### Custom push the app
To specify custom options when pushing an app with `cf push`, you can include them in one or both of the following:

* The `cf push` command itself.

* A manifest file.

+ The manifest file must be named `manifest.yml` and reside in the directory where you run `cf push`.

+ The manifest can include the app name, which lets you run `cf push` with no arguments.

+ The manifest can also include a `services` block that lists service instances for the app to bind. For more information, see
[Services](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#services-block) in *App Manifest Attribute Reference*.
For information about how app settings change from push to push, including how command-line options, manifests, and commands like `cf scale` interact, see
[Deploying with App Manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html).
For a full list of `cf push` options, see the [Cloud Foundry CLI reference guide](https://cli.cloudfoundry.org/en-US/cf/push.html).

### Configure app services (optional)
If a newly-pushed app has the same name and route as an older app version, the new app retains the service bindings and service configuration of the
previously-pushed version.
For apps that are not already set up for the services that they use:

1. Bind the services to the app. For more information about services, see [Services overview](https://docs.cloudfoundry.org/devguide/services/).

2. (Optional) Configure the app with the service URL and credentials, if needed. For more information, see [Configuring Service
Connections](https://docs.cloudfoundry.org/buildpacks/java/configuring-service-connections.html).

## App updates and downtime
When you push an app that is already running, Cloud Foundry stops all existing instances of that app. Users who try to access the app see a `404 Not Found` message while `cf push` runs.
With some app updates, old and new versions of your code must never run at the same time. A worst-case example is if your app update migrates a database schema, causing old app instances to fail and lose user data. To prevent this, you must stop all running instances of your app before you push the new version.
When old and new versions of your app can run simultaneously, you can avoid app downtime by using the blue-green deployment method to swap routes between app versions running in parallel. For more information, see [Using blue-green deployment to reduce downtime and risk](https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html).

## Troubleshoot app push problems
If your app does not start on Cloud Foundry, first ensure that the app can run locally.
To troubleshoot your app in the cloud using the cf CLI, see [Troubleshoot app deployment and health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html).