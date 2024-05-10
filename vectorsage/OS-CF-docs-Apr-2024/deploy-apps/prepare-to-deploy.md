# Designing and running your app in the cloud
These are best practices for developing modern apps for cloud platforms. For more detailed reading about good app design for the cloud, see [The Twelve-Factor App](http://www.12factor.net).
Following these guidelines facilitates app deployment to Cloud Foundry and other cloud platforms, and apps written in supported frameworks often run unmodified.
For more information about the features of HTTP routing handled by the Gorouter in Cloud Foundry,
see [HTTP routing](https://docs.cloudfoundry.org/concepts/http-routing.html).
For more information about the life cycle of application containers, see [Application container life cycle](https://docs.cloudfoundry.org/devguide/deploy-apps/app-lifecycle.html).

## Avoid writing to the local file system
Apps running on Cloud Foundry must not write files to the local file system because:

* **Local file system storage is short-lived.** When an app instance fails or stops, the resources assigned to that instance are reclaimed by the platform, including any local disk changes made since the app started. When the instance is restarted, the app starts with a new disk image. Although your app can write local files while it is running, the files disappear after the app restarts.

* **Instances of the same app do not share a local file system.** Each app instance runs
in its own isolated container.
Therefore, a file written by one instance is not visible to other instances of the same app.
If the files are temporary, this is not be a problem.
However, if your app needs the data in the files to persist across app restarts,
or the data must be shared across all running instances of the app,
the local file system must not be used. Cloud Foundry recommends
using a shared data service like a database or blobstore for this purpose.
For example, instead of using the local file system, you can use a Cloud Foundry service
such as the MongoDB document database or a relational database like MySQL or PostgreSQL.
Another option is to use cloud storage providers such as [Amazon S3](http://aws.amazon.com/s3/),
[Google Cloud Storage](https://cloud.google.com/products/cloud-storage),
[Dropbox](https://www.dropbox.com/developers), or [Box](http://developers.box.com/).
If your app must communicate across different instances of itself,
consider a cache like Redis or a messaging-based architecture with RabbitMQ.
If you must use a file system for your app because, for example, your app interacts
with other apps through a network attached file system or because your app is based on legacy code
that you cannot rewrite, consider using volume services to bind a network attached file system to your app.
For more information, see [Using an external file system (volume services)](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html).

## Cookies accessible across apps
In an environment with shared domains, cookies might be accessible across apps.
Many tracking tools such as Google Analytics and Mixpanel use the highest available domain to set their cookies.
For an app using a shared domain such as `example.com`, a cookie set to use the highest domain has a `Domain` attribute of `.example.com` in its HTTP response header.
For example, an app at `my-app.shared-domain.example.com` might be able to access the cookies for an app at `your-app.shared-domain.example.com`.
You must decide whether you want your apps or tools that use cookies to set and store the cookies at the highest available domain.

## Port considerations
Clients connect to apps running on Cloud Foundry by making requests to URLs associated with the app.
Cloud Foundry allows HTTP requests to apps on ports 80 and 443.
For more information, see [Routes and domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html).
Cloud Foundry also supports WebSocket handshake requests over HTTP containing the `Upgrade` header.
The Cloud Foundry router handles the upgrade and initiates a TCP connection
to the app to form a WebSocket connection.
To support WebSockets, the operator must configure the load balancer correctly. Depending on the configuration, clients may have to use a different port for WebSocket connections, such as port 4443, or a different domain name. For more information, see [Supporting WebSockets](https://docs.cloudfoundry.org/adminguide/supporting-websockets.html).

## Cloud Foundry updates and your app
For app management purposes, Cloud Foundry might need to stop and restart your app instances.
If this occurs, Cloud Foundry performs the following steps:

1. Cloud Foundry sends a single `termination signal` to the root process
that your start command runs.

2. Cloud Foundry waits 10 seconds to allow your app to cleanly shut down any child processes
and handle any open connections.

3. After 10 seconds, Cloud Foundry shuts down your app.
Your app must accept and handle the termination signal to ensure that it shuts down gracefully. To achieve this, the app is expected to do these steps when shutting down:

1. App receives termination signal

2. App closes listener so that it stops accepting new connections

3. App finishes serving in-flight requests

4. App closes existing connections as their requests complete

5. App is stopped or shut down
For an implementation of the expected shutdown behavior in Golang, see the [Sample HTTP App](https://github.com/cloudfoundry/sample-http-app) repository on GitHub.

## Ignore unnecessary files when pushing
By default, when you push an app, all files in the app’s project directory tree are uploaded
to your Cloud Foundry instance, except version control and configuration files
or directories with these names:

* `.cfignore`

* `_darcs`

* `.DS_Store`

* `.git`

* `.gitignore`

* `.hg`

* `manifest.yml`

* `.svn`
In addition to these, if API request diagnostics are directed to a log file and the file is within the project directory tree, it is excluded from the upload. You can direct these API request diagnostics to a log file using `cf config --trace` or the `CF_TRACE` environment variable.
If the app directory contains other files, such as `temp` or `log` files, or complete subdirectories that are not required to build and run your app, you might want to add them to a `.cfignore` file to exclude them from upload. Especially with a large app, uploading unnecessary files can slow app deployment.
To use a `.cfignore` file, create a text file named `.cfignore` in the root of your app directory structure. In this file, specify the files or file types you wish to exclude from upload. For example, these lines in a `.cfignore` file exclude the “tmp” and “log” directories.
```
tmp
log
```
The file types you might want to exclude vary, based on the app frameworks you use. For examples of commonly-used `.gitignore` files, see the [gitignore](https://github.com/github/gitignore) repository on GitHub.

## Run multiple instances to increase availability
Singleton apps might become temporarily unavailable for reasons that include:

* During an upgrade, Cloud Foundry gracefully shuts down the apps running on each Diego Cell
and restarts them on another Diego Cell. Single app instances might become temporarily unavailable if the replacement instance does not become healthy within the Diego Cell’s evacuation timeout. The default timeout is 10 minutes.

* Unexpected faults in Cloud Foundry system components or underlying infrastructure,
such as container-host VMs or IaaS availability zones, might cause lone app instances to disappear
or become unroutable for a minute or two.
To avoid the risk of an app becoming temporarily unavailable, developers can run more than one instance of the app.

## Using buildpacks
A buildpack consists of bundles of detection and configuration scripts that provide framework
and runtime support for your apps.
When you deploy an app that requires a buildpack, Cloud Foundry installs the buildpack
on the Diego Cell where the app runs.
For more information, see [Buildpacks](https://docs.cloudfoundry.org/buildpacks/).