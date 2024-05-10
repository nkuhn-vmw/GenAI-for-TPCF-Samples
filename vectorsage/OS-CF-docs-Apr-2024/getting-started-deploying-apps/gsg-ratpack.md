# Deploying Ratpack apps to Cloud Foundry
This information walks you through deploying a Ratpack app to Cloud Foundry.
If you experience a problem following the steps, check the [Troubleshooting Cloud Foundry](http://docs.cloudfoundry.org/running/troubleshooting.html) topic or refer to the [Troubleshooting Application Deployment and Health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html) topic.
Sample app step
If you want to go through this tutorial using the sample app, run `git clone <https://github.com/cloudfoundry-samples/pong_matcher_groovy.git>` to clone the `pong_matcher_groovy` app from GitHub, and follow the instructions in the Sample app step sections.
Ensure that your Ratpack app runs locally before continuing with this procedure.

## Deploy a Ratpack application
This section describes how to deploy a Ratpack application to Cloud Foundry.

### Prerequisites

* A Ratpack app that runs locally on your workstation

* Intermediate to advanced Ratpack knowledge

* The [Cloud Foundry Command Line Interface (cf CLI)](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html)

* JDK 1.7 or 1.8 for Java 7 or 8 configured on your workstation
You can develop Ratpack applications in Java 7 or 8 or any JVM language. The Cloud Foundry Java buildpack uses JDK 1.8, but you can modify the buildpack and the manifest for your app to compile to JDK 1.7. Refer to Step 8: Configure the Deployment Manifest.

### Step 1: (Optional) Declare app dependencies
Declare all the dependency tasks for your app in the build script of your chosen build tool. The table lists build script information for Gradle and Maven and provides documentation links for each build tool.
| **Build Tool** | **Build Script** | **Documentation** |
| --- | --- | --- |
| Gradle | `build.gradle` | [Gradle User Guide](http://www.gradle.org/docs/current/userguide/userguide.html) |
| Maven | `pom.xml` | [Apache Maven Project Documentation](http://maven.apache.org/guides/) |
You can skip this step. The `build.gradle` file contains the dependencies for the `pong_matcher_groovy` sample app, as the example below shows.
```
dependencies {
// SpringLoaded enables runtime hot reloading.
// It is not part of the app runtime and is not shipped in the distribution.
springloaded "org.springframework:springloaded:1.2.0.RELEASE"
// Default SLF4J binding. Note, this is a blocking implementation.
// See here for a non blocking appender http://logging.apache.org/log4j/2.x/manual/async.html
runtime 'org.slf4j:slf4j-simple:1.7.7'
compile group: 'redis.clients', name: 'jedis', version: '2.5.2', transitive: true
testCompile "org.spockframework:spock-core:0.7-groovy-2.0"
}
```

### Step 2: (Optional) Allocate sufficient memory
Use the `cf push -m` command to specify the amount of memory that should be allocated to the application. Memory allocated this way is done in preset amounts of `64M`, `128M`, `256M`, `512M`, `1G`, or `2G`. For example:
```
$ cf push -m 128M
```
When your app is running, you can use the `cf app APP-NAME` command to see memory utilization.
You can skip this step. In the `manifest.yml` of the `pong_matcher_groovy` sample app, the `memory` sub-block of the `applications` block allocates 512 MB to the app.

### Step 3: (Optional) Provide a JDBC driver
The Java buildpack does not bundle a JDBC driver with your application. If your application accesses a SQL RDBMS, you must do the following:

* Include the appropriate driver in your application.

* Create a dependency task for the driver in the build script for your build tool or IDE.
You can skip this step. The `pong_matcher_groovy` sample app does not require a JDBC driver.

### Step 4: (Optional) Configure a Procfile
Use a Procfile to declare required runtime processes for your web app and to specify your web server. For more information, see the [Configuring a Production Server](https://docs.cloudfoundry.org/buildpacks/prod-server.html) topic.
You can skip this step. The `pong_matcher_groovy` app does not require a Procfile.

### Step 5: Create and bind a service instance for a Ratpack application
Learn how to use the CLI to configure a Redis managed service instance for an app.
Cloud Foundry supports the following types of service instances:

* Managed services integrate with Cloud Foundry through service brokers that offer services and plans and manage the service calls between Cloud Foundry and a service provider.

* User-provided service instances enable you to connect your application to pre-provisioned external service instances.
For more information about creating and using service instances, refer to the [Services Overview](https://docs.cloudfoundry.org/devguide/services/) topic.

#### Creating a service instance

1. View managed and user-provided services and plans available to you by running:
```
cf marketplace
```
The example shows two of the available managed database-as-a-service providers and their offered plans: `postgresql-10-odb` PostgreSQL as a Service and `rediscloud` Enterprise-Class Redis for Developers.
```
$ cf marketplace
Getting services from marketplace in org Cloud-Apps / space development as clouduser@example.com...
OK
service plans description
postgresql-10-odb standalone, standalone-replica, general PostgreSQL as a Service
rediscloud 30mb, 100mb, 1gb, 10gb, 50gb Enterprise-Class Redis for Developers
```

2. Create a service instance for your app by running:
```
cf create-service SERVICE PLAN SERVICE-INSTANCE
```
Where:

* `SERVICE` and `PLAN` are chosen from the output of the previous step.

* `SERVICE-INSTANCE` is a unique name you provide for the service instance.
Run `cf create-service rediscloud 30mb baby-redis`. This creates a service instance named `baby-redis` that uses
the `rediscloud` service and the `30mb` plan, as the following example shows.
```
$ cf create-service rediscloud 30mb baby-redis
Creating service baby-redis in org Cloud-Apps / space development as clouduser@example.com....
OK
```