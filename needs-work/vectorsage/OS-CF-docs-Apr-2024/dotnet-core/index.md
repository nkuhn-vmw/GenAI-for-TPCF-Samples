# .NET Core buildpack
You can push Cloud Foundry apps to Linux Diego Cells using the .NET Core buildpack.
To find supported ASP.NET Core versions, see [.NET Core buildpack release notes](https://github.com/cloudfoundry/dotnet-core-buildpack/releases).
The .NET Core buildpack can only be used to deploy apps to Linux Diego Cells.
To deploy .NET Core apps to Windows Diego Cells, use the Binary buildpack.
For more information about the Binary buildpack, see [Binary Buildpack](https://docs.cloudfoundry.org/buildpacks/binary/index.html).
Buildpacks provide needed dependencies to Cloud Foundry apps.
Cloud Foundry automatically uses the .NET Core buildpack when one or more of the following conditions are met:

* The pushed app contains one or more `*.csproj` or `*.fsproj` files.

* The app is pushed from the output directory of the `dotnet publish` command.
For information about deploying different types of .NET apps, follow the links in the following table:
| Type of .NET App | Buildpack |
| --- | --- |
|
ASP.NET MVC
ASP.NET Web Forms
ASP.NET WebAPI Apps
Windows Communication Foundation (WCF)
| [HWC](https://docs.cloudfoundry.org/buildpacks/hwc/index.html) |
| .NET Console | [Binary](https://docs.cloudfoundry.org/buildpacks/binary/index.html) |
| .NET Core pushed to Windows stack | [Binary](https://docs.cloudfoundry.org/buildpacks/binary/index.html) |

## Push a .NET Core app
To push a .NET Core app to a Linux Diego Cell:

1. Run:
```
cf push APP-NAME
```
Where `APP-NAME` is the name you want to give your app.
If your Cloud Foundry deployment does not have the .NET Core buildpack installed or the installed version is out of date,
run the same command with the `-b` option to specify the buildpack:
```
cf push APP-NAME -b https://github.com/cloudfoundry/dotnet-core-buildpack.git
```
Where `APP-NAME` is the name you want to give your app.

2. Find the URL of your app in the output of the `cf push` command.

3. Open a browser and navigate to the URL to see your app running.
For a basic sample app, see [ASP.NET Core Getting Started App](https://github.com/IBM-Bluemix/aspnet-core-helloworld) in GitHub.

## Source-based, non-published deployments
For a source-based, non-published deployment, you push your app’s source code, not the output directory of the `dotnet publish` command.
The source-based, non-published workflow ensures the buildpack can keep all your dependencies in sync and up to date. See the following sections.
The source-based deployment workflow also uses the
`cf push` command to push source-based apps to Cloud Foundry.

### Deploying apps with multiple projects
If you are deploying an app containing multiple projects, you must specify which of the app’s projects is the main project.
To specify the main project in a multi-project deployment:

1. Create a `.deployment` file in your app’s root folder and open the new file in a text editor.

2. Designate the main project’s path by configuring the file, using the following format:
```
[config]
project = PATH-TO-YOUR-MAIN-PROJECT
```
Where `PATH-TO-YOUR-MAIN-PROJECT` is the location of your main project’s `*.csproj` or `*.fsproj` file.
For example:
```
[config]
project = src/MyApp.Web/MyApp.Web.csproj
```
In this example, by pointing to the `MyApp.Web` `*.csproj` file, `MyApp.Web` is configured as the main project.

3. Save the revised `.deployment` file.
When deployed, the buildpack attempts to run the main project using the `dotnet run` command, `dotnet run -p PATH-TO-YOUR-MAIN-PROJECT`, and automatically compiles all projects listed as dependencies in the main project’s `*.csproj` or `*.fsproj` file.
For example: Suppose your `.deployment` file is configured as previously noted and you have an app `src` folder containing three projects: `MyApp.Web`, `MyApp.DAL` and `MyApp.Services`. If your `MyApp.Web.csproj` file lists the `MyApp.DAL` and `MyApp.Services` projects as dependencies, the two additional projects are compiled by the buildpack.

### Use non-Default package sources
If you want to deploy an app that uses non-default package sources, you must specify those package sources in the `NuGet.Config` file. For information about `NuGet.Config`, see [nuget.config reference](https://docs.microsoft.com/en-us/nuget/reference/nuget-config-file) in the Microsoft documentation.

### Deactivating and clearing your NuGet package cache
You might need to deactivate NuGet package caching or clear NuGet packages cached in the staging environment in one of the following scenarios:

* Your app fails to stage because it runs out of space, exceeding the maximum allowable disk quota.

* You have added pre-release packages to test a new feature and then decided to revert back to the main NuGet feed. You might need to remove the packages you changed from the cache to avoid conflicts.
Deactivating NuGet caching clears any existing NuGet dependencies from the staging cache and prevents the buildpack from adding NuGet dependencies to the staging cache.
NuGet package caching is deactivated by default. If the default is not explicitly overridden, no additional NuGet caching configuration is required.
To deactivate NuGet package caching:

1. Confirm the `CACHE_NUGET_PACKAGES` environment variable is not set to `true` in your app manifest by locating the `manifest.yml` file and confirming `CACHE_NUGET_PACKAGES` is not set to `true`.

2. If needed, set `CACHE_NUGET_PACKAGES` to `false` in the `manifest.yml` file by setting the `CACHE_NUGET_PACKAGES` environment variable to `false`.
For example:
```

---
applications:

- name: sample-aspnetcore-app
memory: 512M
env:
CACHE_NUGET_PACKAGES: false
```

3. To alternatively configure the setting to `false` in the environment variables settings, run the following command:
```
cf set-env APP-NAME CACHE_NUGET_PACKAGES false
```
Where `APP-NAME` is the name of your app.
For more information, see [Environment Variables](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#env-block) in *Deploying with App Manifests*.

## Framework dependent deployments
For a framework-dependent deployment (FDD), you deploy only your app and third-party dependencies. Cloud Foundry recommends using this workflow if you deploy an app in an offline setting.
For information about deploying FDDs, see [Framework-dependent deployments (FDD)](https://docs.microsoft.com/en-us/dotnet/core/deploying/index#framework-dependent-deployments-fdd) in the Microsoft documentation.
Deploy a FDD using the buildpack:

1. Publish the app by running:
```
dotnet publish [-f FRAMEWORK-NAME] [-c Release]
```
Where `FRAMEWORK-NAME` is your target framework.

2. Prepare to push your app with one of these methods:

* If your app uses a `manifest.yml`, specify a path to the output folder of `dotnet publish`. This allows you to push your app from any directory.

* If not, go to `bin/Debug|Release/FRAMEWORK-NAME/RUNTIME-NAME/publish` directory, where `FRAMEWORK-NAME` is your target framework, and `RUNTIME-NAME` is the runtime you are using to push your app.

3. Push your app.

## Self contained deployments
For a self-contained deployment (SCD), you deploy your app, third-party dependencies, and the version of .NET Core that you used to build your app.
For information about SCDs, see [Self-contained deployments (SCD)](https://docs.microsoft.com/en-us/dotnet/core/deploying/#self-contained-deployments-scd) in the Microsoft documentation.

**Important**
Cloud Foundry does not recommend using the SCD workflow. The buildpack is unable to keep
dependencies in sync and up to date for workflows that deploy a pre-published binary.
When using the SCD workflow for deploying your app, you must:
\* Specify a runtime in the `dotnet publish` command. For example:
“`console
dotnet publish -r ubuntu14.04-x64
”`
\* Include the specified runtime in the `RuntimeIdentifiers` section of the project file.

## Specify .NET Core SDKs
To pin the .NET Core SDK to a specific version or version line, create a `buildpack.yml` file at the app root and add your SDK version in one of the following formats:
“`yaml
dotnet-core:
sdk: 2.1.201
”`
“`
dotnet-core:
sdk: 2.1.x
”`
“`
dotnet-core:
sdk: 2.x
”`
The buildpack chooses what SDK to install based on the files present at the app root in the following order of precedence:

1. `buildpack.yml`

1. `global.json`

1. `\*.fsproj`
The app respects the SDK version specified in `global.json` at runtime. If you provide versions in
both `global.json` and `buildpack.yml` files, make sure you specify the same versions in both files.

## Specify .NET Runtime versions
This section explains how to specify a .NET Runtime version for source-based and framework-dependent apps.

### Source-based apps
If you want to lock the .NET Runtime version, configure your `.csproj` or `.fsproj` file to lock your app to the desired version.
For example, the following configuration locks the runtime to 2.1:
“`xml
netcoreapp2.1

2.1.\*
”`
For source-based apps, specify a minor version of the .NET Runtime. Do not specify a patch version, because buildpacks contain only
the two most recent patch versions of each minor version.

### Framework-dependent apps
Your app is configured to use the latest .NET Runtime patch version by default.
If you want your app to maintain a specific .NET Runtime version, you must modify your app’s `.runtimeconfig.json` file to include the `applyPatches` property and set the property to `false`.
For example:
“`json
{
"runtimeOptions”: {
“tfm”: “netcoreapp2.0”,
“framework”: {
“name”: “Microsoft.NETCore.App”,
“version”: “2.0.0”
},
“applyPatches”: false
}
}
“`
Set `applyPatches: false` in `*.runtimeconfig.json` only if you want to pin your .NET Framework to a specific version. This prevents your
app from receiving updates to the runtime version and assemblies.

## Push an app in a disconnected environment
For offline environments, Cloud Foundry recommends using the Framework-Dependent Deployment workflow. This workflow enables the deployed app to use the latest runtime provided by the offline buildpack. For more information, see [Framework-Dependent Deployments](#framework-dependent) above.

## Maintain ASP.NET Core assemblies
This section applies only to source-based and framework-dependent deployments.
For maintaining ASP.NET Core assemblies, Cloud Foundry recommends one of these methods:
\* Configure your app as a fully vendored app requiring fewer buildpack updates. Add the following to your `.csproj` file:
”`xml
false
“`
\* Keep your SDK up to date, by setting `buildpack.yml` to the .NET SDK line you want to use. For example:
”`yaml
—
dotnet-core:
sdk: 2.0.x
“`
`2.0.x` ASP.NET Core assemblies are released in the `2.1.200`-`2.1.299` SDK versions, and `2.1.x` assemblies are
released in the `2.1.300` and higher SDK versions.

## Configuring the listen port
Cloud Foundry sets the `$PORT` environment variable automatically.
For your .NET Core app to work on Cloud Foundry, you must configure the app to listen on the environment’s specified port.
For C# apps, the following modifications activate the buildpack to pass the correct port from `$PORT` environment variable to the app when you run the initial startup command:

1. Open the file that contains your `Main` method.

1. Add a `using` statement to the top of the file:
”`c#
using Microsoft.Extensions.Configuration;
“`

1. Add the following lines before the line `var host = new WebHostBuilder()`:
”`c#
var config = new ConfigurationBuilder()
.AddCommandLine(args)
.Build();
“`

1. Add the following line after `.UseKestrel()`:
”`c#
.UseConfiguration(config)
“`
The `Main` method resembles the following example:
”`c#
public static void Main(string[] args)
{
var config = new ConfigurationBuilder()
.AddCommandLine(args)
.Build();
var host = new WebHostBuilder()
.UseKestrel()
.UseConfiguration(config)
.UseContentRoot(Directory.GetCurrentDirectory())
.UseStartup()
.Build();
host.Run();
}
“`

1. Save your changes.

1. Add `Microsoft.Extensions.Configuration.CommandLine` as a dependency in `\*.csproj`:
”`xml
VERSION
“`
Where `VERSION` is the version of the package to use. For a list of valid versions, navigate to https://www.nuget.org.

1. If your app requires any other files at runtime, such as JSON configuration files, add them to the `include` section of `copyToOutput`.

1. Save your changes.
With these changes, the `dotnet run` command copies your app `Views` to the build output where the .NET CLI can find them.

## Add custom libraries
If your app requires external shared libraries that are not provided by the rootfs or the buildpack, you must place the libraries in an `ld\_library\_path` directory at the app root.
You must keep these libraries up to date. They do not update automatically.
The .NET Core buildpack adds the directory `APP-ROOT/ld\_library\_path` to `LD\_LIBRARY\_PATH`, where `APP-ROOT` is the app root, so your app can access these libraries at runtime.

## Known issue workaround: NTLM authentication failures on cflinuxfs4
There is a [known issue](https://github.com/dotnet/runtime/issues/67353) in .NET Core related to NTLM authentication on Ubuntu 22.04, which can affect builds using the .NET Core buildpack on the Ubuntu 22.04-based `cflinuxfs4` stack. The issue is related to incompatibilities between OpenSSL 3.0 and the older cryptographic algorithms involved in NTLM authentication.
In general, the best practice and recommended option is to upgrade to an authentication protocol in the application that does not rely on using widely-discouraged legacy cryptographic algorithms.
If you are affected by this issue, you might see failures with your .NET Core application running on the `cflinuxfs4` stack related to GSSAPI/NTLM, such as:
”`
GSSAPI operation failed with error - Unspecified GSS failure. Minor code may provide more information (Crypto routine failure).
“`
If you cannot upgrade to a different authentication protocol, the only workaround in the buildpack at this time is to load and activate the legacy provider in OpenSSL 3.
Important
Use of the legacy provider is not considered secure, because it enables deprecated or outdated algorithms. You should be aware of the risk involved in leveraging this workaround.
To enable the workaround:

1. Ensure that the .NET Core buildpack version is v2.4.24 or later

2. Set the `BP_OPENSSL_ACTIVATE_LEGACY_PROVIDER` environment variable to `true` in the `manifest.yml` or using `cf set-env`

3. Push the application
These steps add an `openssl.cnf` file to your application directory during the build. This file contains the following lines, which load and activate the legacy SSL provider in OpenSSL 3 on the base image:
```
[provider_sect]
default = default_sect
legacy = legacy_sect
[default_sect]
activate = 1
[legacy_sect]
activate = 1
```