# Hosted Web Core buildpack
You can configure .NET Framework apps to use with the Hosted Web Core (HWC) buildpack and push
your .NET Framework apps to Cloud Foundry.

## Prerequisites
Using the HWC buildpack requires deploying Microsoft Windows cells with CF.
The HWC buildpack supports the following common app types by default:

* ASP.NET MVC

* ASP.NET Web Forms

* ASP.NET WebAPI Apps

* Windows Communication Foundation (WCF)
For information about deploying different types of .NET apps, follow the links in the following table:
| Type of .NET App | Buildpack |
| --- | --- |
| .NET Console | [Binary](https://docs.cloudfoundry.org/buildpacks/binary/index.html) |
| .NET Core pushed to Linux stack | [.NET Core](https://docs.cloudfoundry.org/buildpacks/dotnet-core/index.html) |
| .NET Core pushed to Windows stack | [Binary](https://docs.cloudfoundry.org/buildpacks/binary/index.html) |

## HWC buildpack overview
The HWC buildpack provides a runtime server that uses the Hosted Web Core API for running .NET Framework applications in Windows Server containers. For more information, see [Hosted Web Core API Reference](https://msdn.microsoft.com/en-us/library/ms693832(v=vs.90).aspx) in the Microsoft documentation.
The HWC buildpack provides access to .NET Framework 4.5.1 and later, made available by the Windows root file system (rootfs).

## Step 1. Configure HWC
HWC relies on `Web.config` and `applicationHost.config` configuration files for configuring the .NET applications.
Most `Web.config` files work immediately with CF, but with the following constraints:

* Integrated Windows Authentication (IWA) is not yet supported on CF.

* SQL server connection strings must use fully qualified domain names.

* Place connection string values in environment variables or [user-provided service instances](https://docs.cloudfoundry.org/devguide/services/user-provided.html).
In addition, the [Shadow Copy Setting](https://docs.cloudfoundry.org/buildpacks/hwc/index.html#shadow-copy), and [Dynamic and Static HTTP Compression](https://docs.cloudfoundry.org/buildpacks/hwc/index.html#http-compression) `Web.config` settings can be customized as needed.
The HWC buildpack includes a default configuration for the `applicationHost.config`, similar to IIS.

## Step 2. Add a global error handler
Before you push your app for the first time, add a global error handler to receive log information from your app if it crashes on startup.

## Step 3. Pushing an app
Follow these steps to push your application:

1. Build your HWC app in Visual Studio.

2. On the command line, go to the directory containing the app files.

3. To push your HWC app, run the following `cf push` command:
```
cf push APP-NAME -s windows -b hwc_buildpack
```
Where `APP-NAME` is the name you want to give your app.
For example:
```
$ cf push my-app -s windows -b hwc_buildpack
Creating app my-app in org sample-org / space sample-space as username@example.com...
OK
...
requested state: started
instances: 1/1
usage: 1 GB x 1 instances
urls: my-app.example.com
```

4. Confirm your application is running by going to your app’s URL in the push command output. In the previous example, `my-app.example.com` is the URL of your app.

## Features
You can use the following features with HWC buildpack:

* Context Path Routing

* Shadow Copy Setting

* Dynamic and Static HTTP Compression

* URL Rewrite

* Profile Scripts

### Context path routing
With context path routing you can implement multiple apps to share the same route hostname.
For example, `app1.example.com/app2`. The context path routing feature is analogous to IIS virtual directories.
Making an application accessible under another app’s URL requires pushing both apps and applying a map-route correlation between them.
To define a context path route, for example, `app1.example.com/app2`, run the following commands:

1. To push the primary app, run the following command:
```
cf push TOP-LEVEL-APP-NAME -s windows -b hwc_buildpack
```
Where `TOP-LEVEL-APP-NAME` is your top-level app’s name.

2. To push the secondary app and deactivate the app’s starting and default routing, run the following command:
```
cf push LOWER-LEVEL-APP-NAME --no-start --no-route -s windows -b hwc_buildpack
```
Where `LOWER-LEVEL-APP-NAME` is the name of the lower-level app.

3. To map routes between the primary and secondary apps, run the following command:
```
cf map-route LOWER-LEVEL-APP-NAME APP-DOMAIN --hostname TOP-LEVEL-APP-NAME --path LOWER-LEVEL-APP-NAME
```
Where:

* `TOP-LEVEL-APP-NAME` is your top-level app’s name.

* `LOWER-LEVEL-APP-NAME` is your lower-level app’s name.

* `APP-DOMAIN` is your site’s public domain name.

4. To start the secondary app, run the following command:
```
cf start LOWER-LEVEL-APP-NAME
```
Where `LOWER-LEVEL-APP-NAME` is your lower-level app’s name.
For example, the following commands define context path routing for two HWC apps, `app1` and `app2`, where `app2` is made accessible under `app1` as `app1.example.com/app2`:
```
$ cf push app1 -s windows -b hwc_buildpack
$ cf push app2 --no-start --no-route -s windows -b hwc_buildpack
$ cf map-route app2 example.com --hostname app1 --path app2
$ cf start app2
```
HWC-hosted apps use the `VCAP_APPLICATION` environment variable
to read out the bound app URIs. Any context path that exists underneath the root in the
app’s bound route corresponds to the `applicationHost.config`.

### Shadow Copy setting
[Shadow Copy](https://msdn.microsoft.com/en-us/library/ms228159(v=vs.100).aspx)
is a hosting option that copies assemblies for an app in the `bin` directory
to the app’s temporary files directory. This feature is turned off and
is unnecessary for apps running under Cloud Foundry. An app can override this
setting in its `Web.config` file.

### Dynamic and static HTTP compression
The HWC buildpack implements dynamic and static HTTP compression by default.
You can deactivate HTTP compression in your app’s `Web.config` file.
Dynamic HTTP compression is hardcoded at level 4.
Static HTTP compression is hardcoded at level 9.

### URL rewrite
The HWC buildpack supports the URL Rewrite module.
It’s preinstalled in the Windows file system.

### Profile scripts
With the HWC buildpack you can provide `.profile.bat` scripts with your applications.
You can use a `.profile.bat` script to perform app-specific initialization tasks. For example, setting custom environment variables.
For information about configuring `.profile.bat` scripts, see [Configure Pre-Runtime Hooks](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html#profile) section of *Pushing an App*.

## Buildpack support
A number of channels exist to assist you with using the HWC buildpack, or developing your own HWC buildpack.

* **HWC Buildpack Repository in GitHub**: For more information about using and extending the HWC buildpack in the [HWC buildpack repository] see, (<https://github.com/cloudfoundry/hwc-buildpack>) in GitHub.

* **Release Notes**: For more information about this buildpack, see [HWC buildpack release page](https://github.com/cloudfoundry/hwc-buildpack/releases) in GitHub.

* **Slack**: Join the #buildpacks channel in the [Cloud Foundry Slack community](http://slack.cloudfoundry.org/).