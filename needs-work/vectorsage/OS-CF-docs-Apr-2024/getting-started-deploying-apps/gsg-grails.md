# Deploying your Grails apps to Cloud Foundry
This information walks you through deploying a Grails app to Cloud Foundry.
If you experience a problem following the steps, refer to the [Troubleshooting Cloud Foundry](http://docs.cloudfoundry.org/running/troubleshooting.html) or [Troubleshooting Application Deployment and Health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html) topics for more information.
If you want to go through this tutorial using the sample app, run `git clone <https://github.com/cloudfoundry-samples/pong_matcher_grails.git>` to clone the `pong_matcher_grails` app from GitHub, and follow the instructions in the Sample app step sections.
Ensure that your Grails app runs locally before continuing with this procedure.

## Deploy a Grails application
This section describes how to deploy a Grails application to Cloud Foundry.

### Prerequisites

* A Grails app that runs locally on your workstation

* Intermediate to advanced Grails knowledge

* The [Cloud Foundry Command Line Interface (cf CLI)](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html)

* JDK 1.7 or 1.8 for Java 7 or 8 configured on your workstation
You can develop Grails applications in Groovy, Java 7 or 8, or any JVM language. The Cloud Foundry Java buildpack uses JDK 1.8, but you can modify the buildpack and the manifest for your app to compile to JDK 1.7 as described in *Step 8: Configure the Deployment Manifest* of this topic.

### Step 1: (Optional) Declare app dependencies
Declare all the dependency tasks for your app in the build script of your chosen build tool. The table lists build script information for Gradle, Grails, and Maven, and provides documentation links for each build tool.
| **Build Tool** | **Build Script** | **Documentation** |
| --- | --- | --- |
| Gradle | `build.gradle` | [Gradle User Guide](http://www.gradle.org/docs/current/userguide/userguide.html) |
| Grails | `BuildConfig.groovy` | [Grails: Configuration - Reference Documentation](http://grails.org/doc/latest/guide/conf.html) |
| Maven | `pom.xml` | [Apache Maven Project Documentation](http://maven.apache.org/guides/) |
You can skip this step. The `pong_matcher_grails/app/grails-app/conf/BuildConfig.groovy` file contains the dependencies for the `pong_matcher_grails` sample app, as shown in the following example.
```
dependencies {
// specify dependencies here under either 'build', 'compile', 'runtime', 'test' or 'provided' scopes e.g.
// runtime 'mysql:mysql-connector-java:5.1.29'
// runtime 'org.postgresql:postgresql:9.3-1101-jdbc41'
test "org.grails:grails-datastore-test-support:1.0-grails-2.4"
runtime 'mysql:mysql-connector-java:5.1.33'
}
```

### Step 2: (Optional) Allocate sufficient memory
Run the Cloud Foundry Command Line Interface (cf CLI) `cf push -m` command to specify the amount of memory that should be allocated to the application. Memory allocated this way is done in preset amounts of `64M`, `128M`, `256M`, `512M`, `1G`, or `2G`. For example:
```
$ cf push -m 128M
```
When your app is running, you can use the `cf app APP-NAME` command to see memory utilization.
You can skip this step. In the `manifest.yml` of the `pong_matcher_grails` sample app, the `memory` sub-block of the `applications` block allocates 1 GB to the app.

### Step 3: (Optional) Provide a JDBC driver
The Java buildpack does not bundle a JDBC driver with your application. If your application accesses a SQL RDBMS, you must do the following:

* Include the appropriate driver in your application.

* Create a dependency task for the driver in the build script for your build tool or IDE.
You can skip this step. The `pong_matcher_grails` sample app declares a MySQL JDBC driver in the `pong_matcher_grails/app/grails-app/conf/DataSource.groovy` file because the app uses ClearDB, which is a database-as-service for MySQL-powered apps. The example below shows this declaration.
```
dataSource {
pooled = true
jmxExport = true
driverClassName = "com.mysql.jdbc.Driver"
dialect = org.hibernate.dialect.MySQL5InnoDBDialect
uri = new URI(System.env.DATABASE_URL ?: "mysql://foo:bar@localhost")
username = uri.userInfo ? uri.userInfo.split(":")[0] : ""
password = uri.userInfo ? uri.userInfo.split(":")[1] : ""
url = "jdbc:mysql://" + uri.host + uri.path
properties {
dbProperties {
autoReconnect = true
}
}
}
```

### Step 4: (Optional) Configure a Procfile
Use a Procfile to declare required runtime processes for your web app and to specify your web server. For more information, see the [Configuring a Production Server](https://docs.cloudfoundry.org/buildpacks/prod-server.html) topic.
You can skip this step. The `pong_matcher_grails` app does not require a Procfile.

### Step 5: Create and bind a service instance for a Grails application
This section describes using the cf CLI to configure a ClearDB managed service instance for an app.
Cloud Foundry supports two types of service instances:

* Managed services integrate with Cloud Foundry through service brokers that offer services and plans and manage the service calls between Cloud Foundry and a service provider.

* User-provided service instances enable you to connect your application to pre-provisioned external service instances.
For more information about creating and using service instances, refer to the [Services Overview](https://docs.cloudfoundry.org/devguide/services/) topic.

#### Create a service instance

1. View managed and user-provided services and plans available to you by running:
```
cf marketplace
```
The example shows two of the available managed database-as-a-service providers and their offered plans: `cleardb` database-as-a-service for MySQL-powered apps and `postgresql-10-odb` PostgreSQL as a Service.
```
$ cf marketplace
Getting services from marketplace in org Cloud-Apps / space development as clouduser@example.com...
OK
service plans description
cleardb spark, boost, amp Highly available MySQL for your apps
postgresql-10-odb standalone, standalone-replica, general PostgreSQL as a Service
```

2. Create a service instance for your app by running:
```
cf create-service SERVICE PLAN SERVICE-INSTANCE
```
Where:

* `SERVICE` and `PLAN` are chosen from the output of the previous step.

* `SERVICE-INSTANCE` is a unique name you provide for the service instance.

**Note**
Run `cf create-service cleardb spark mysql`. This creates a service instance named `mysql` that uses the `cleardb` service and the `spark` plan, as the example below shows.
```
$ cf create-service cleardb spark mysql
Creating service mysql in org Cloud-Apps / space development as clouduser@example.com....
OK
```

#### (Optional) Bind a service instance
When you bind an app to a service instance, Cloud Foundry writes information about the service instance to the `VCAP_SERVICES` app environment variable. The app can use this information to integrate with the service instance.
Most services support bindable service instances. Refer to your service provider’s documentation to confirm if they support this functionality.
You can bind a service to an application with the command `cf bind-service APPLICATION SERVICE-INSTANCE`.
Alternately, you can configure the deployment manifest file by adding a `services` sub-block to the `applications` block and specifying the service instance. For more information and an example on service binding using a manifest, see the Sample App step.
You can skip this step because the service instance is already bound. Open the `manifest.yml` file in a text editor to view the bound service instance information. Locate the file in the app root directory and search for the `services` sub-block in the `applications` block, as the example below shows.
```

---
applications:
...
services:

- mysql
```

### Step 6: (Optional) Configure the deployment manifest file
You can specify deployment options in the `manifest.yml` that the `cf push` command uses when deploying your app.
Refer to the [Deploying with application manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html) topic for more information.
You can skip this step. The `manifest.yml` file for the `pong_matcher_grails` sample app does not require any additional configuration to deploy the app.

### Step 7: Log in and target the API endpoint
Enter your log in credentials, and select a space and org.
```
cf login -a API-ENDPOINT
```
Where `API-ENDPOINT` is [the URL of the Cloud Controller in your Cloud Foundry instance](http://docs.cloudfoundry.org/running/cf-api-endpoint.html).

**Note**
You must do this step to run the sample app.

### Step 8: Deploy the application
You must use the cf CLI to deploy apps.
From the root directory of your application, run the following command to deploy your application:
```
cf push APP-NAME -p PATH-TO-FILE.war
```
You must deploy the `.war` artifact for a Grails app, and you must include the path to the `.war` file in the `cf push` command using the `-p` option if you do not declare the path in the `applications` block of the manifest file. For more information, refer to the [Grails section](https://docs.cloudfoundry.org/buildpacks/java/java-tips.html#grails) in the Tips for Java Developers topic.
The `cf push` command creates a URL route to your application in the form `HOST.DOMAIN`,
where `HOST` is your `APP-NAME` and `DOMAIN` is specified by your administrator.
Your `DOMAIN` is`shared-domain.example.com`.
For example, `cf push my-app` creates the URL `my-app.shared-domain.example.com`.
The URL for your app must be unique from other apps that Cloud Foundry hosts or the push will fail. Use the following options to help create a unique URL:

* `-n` to assign a different HOST name for the app

* `--random-route` to create a URL that includes the app name and random words

* `cf help push` to view other options for this command
If you want to view log activity while the app deploys, launch a new terminal window and run `cf logs APP-NAME`.
Once your app deploys, browse to your app URL. Search for the `urls` field in the `App started` block in the output of the `cf push` command. Use the URL to access your app online.

**Note**

1. Change to the `app`directory, and run `./grailsw war` to build the app.

2. Run `cf push pong_matcher_grails -n HOST-NAME` to push the app.
Example: `cf push pong_matcher_grails -n my-grails-app`

**This example works for cf CLI v6. The `-n` flag is not supported for cf CLI v7/v8. Hostname must be set using the `routes` property in the manifest.**
You do not have to include the `-p` flag when you deploy the sample app. The sample app manifest declares the path to the archive that `cf push` uses to upload the app files.
The following example shows the terminal output of deploying the `pong_matcher_grails` app. `cf push` uses the instructions in the manifest file to create the app, create and bind the route, and upload the app. It then binds the app to the `mysql` service and follows the instructions in the manifest to start two instances of the app, allocating 1 GB of memory between the instances. After the instances start, the output displays their health and status.
This example works for cf CLI v6. The `-n` flag is not supported for cf CLI v7/v8. Hostname must be set using the `routes` property in the manifest.
```
$ cf push pong_matcher_grails -n my-grails-app
Using manifest file /Users/example/workspace/pong_matcher_grails/app/manifest.yml
Creating app pong_matcher_grails in org Cloud-Apps / space development as clouduser@example.com...
OK
Creating route my-grails-app.cfapps.io...
OK
Binding my-grails-app.cfapps.io to pong_matcher_grails...
OK
Uploading pong_matcher_grails...
Uploading app files from: /Users/example/workspace/pong_matcher_grails/app/target/pong_matcher_grails-0.1.war
Uploading 4.8M, 704 files
OK
Binding service mysql to app pong_matcher_grails in org Cloud-Apps / space development as clouduser@example.com...
OK
Starting app pong_matcher_grails in org Cloud-Apps / space development as clouduser@example.com...
OK

-----> Downloaded app package (38M)

-----> Java Buildpack Version: v2.5 | https://github.com/cloudfoundry/java-buildpack.git#840500e

-----> Downloading Open Jdk JRE 1.8.0_25 from https://download.run.pivotal.io/openjdk/lucid/x86_64/openjdk-1.8.0_25.tar.gz (1.5s)
Expanding Open Jdk JRE to .java-buildpack/open_jdk_jre (1.1s)

-----> Downloading Spring Auto Reconfiguration 1.5.0_RELEASE from https://download.run.pivotal.io/auto-reconfiguration/auto-reconfiguration-1.5.0_RELEASE.jar (0.0s)
Modifying /WEB-INF/web.xml for Auto Reconfiguration

-----> Downloading Tomcat Instance 8.0.14 from https://download.run.pivotal.io/tomcat/tomcat-8.0.14.tar.gz (0.4s)
Expanding Tomcat to .java-buildpack/tomcat (0.1s)

-----> Downloading Tomcat Lifecycle Support 2.4.0_RELEASE from https://download.run.pivotal.io/tomcat-lifecycle-support/tomcat-lifecycle-support-2.4.0_RELEASE.jar (0.0s)

-----> Downloading Tomcat Logging Support 2.4.0_RELEASE from https://download.run.pivotal.io/tomcat-logging-support/tomcat-logging-support-2.4.0_RELEASE.jar (0.0s)

-----> Downloading Tomcat Access Logging Support 2.4.0_RELEASE from https://download.run.pivotal.io/tomcat-access-logging-support/tomcat-access-logging-support-2.4.0_RELEASE.jar (0.0s)

-----> Uploading droplet (83M)
0 of 2 instances running, 2 starting
0 of 2 instances running, 2 starting
0 of 2 instances running, 2 starting
2 of 2 instances running
App started
Showing health and status for app pong_matcher_grails in org Cloud-Apps / space development as clouduser@example.com...
OK
requested state: started
instances: 2/2
usage: 1G x 2 instances
urls: my-grails-app.cfapps.io
state since cpu memory disk

#0 running 2014-11-10 05:07:33 PM 0.0% 686.4M of 1G 153.6M of 1G

#1 running 2014-11-10 05:07:36 PM 0.0% 677.2M of 1G 153.6M of 1G
```

### Step 9: Test your deployed app
Use the cf CLI to review information and administer your app and your Cloud Foundry account. For example, you can edit the `manifest.yml` to increase the number of app instances from 1 to 3, and redeploy the app with a new app name and host name.
See the [Manage Your Application with the cf CLI](https://docs.cloudfoundry.org/buildpacks/java/getting-started-deploying-apps/gsg-grails.html#cli-manage) section for more information.
To test the sample app, do the following:

1. To export the test host, run `export HOST=SAMPLE-APP-URL`, substituting the URL for your app for `SAMPLE-APP-URL`.

2. To clear the database from any previous tests, run:
`curl -v -X DELETE $HOST/all`
You should get a response of `200`.

3. To request a match as “andrew”, run:
`curl -v -H "Content-Type: application/json" -X PUT $HOST/match_requests/firstrequest -d '{"player": "andrew"}'`
You should again get a response of `200`.

4. To request a match as a different player, run:
`curl -v -H "Content-Type: application/json" -X PUT $HOST/match_requests/secondrequest -d '{"player": "navratilova"}'`

5. To check the status of the first match request, run:
`curl -v -X GET $HOST/match_requests/firstrequest`
The last line of the output shows the `match_id`.

6. Replace `MATCH_ID` with the `match_id` value from the previous step in the following command:
```
curl -v -H "Content-Type: application/json" -X POST $HOST/results -d '
{
"match_id":"MATCH_ID",
"winner":"andrew",
"loser":"navratilova"
}'
```
You receive a `201 Created` response.

## Manage your application with the cf CLI
Run the `cf help` command to view a complete list of commands, grouped by task categories, and run `cf help COMMAND` for detailed information about a specific command. For more information about using the cf CLI, refer to the Cloud Foundry Command Line Interface (cf CLI) topics, especially the [Getting Started with the cf CLI](http://docs.cloudfoundry.org/cf-cli/getting-started.html) topic.
You cannot perform certain tasks in the CLI because these are commands that only an administrator can run. If you are not an administrator, the following message displays for these types of commands:
`error code: 10003, message: You are not authorized to perform the requested action`

## Troubleshooting
If your application fails to start, verify that the application starts in your local environment. Refer to the [Troubleshooting Application Deployment and Health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html) topic to learn more about troubleshooting.

### App deploy fails
Even when the deploy fails, the app might exist on Cloud Foundry. Run `cf apps` to review the apps in the currently targeted org and space. You might be able to correct the issue using the CLI, or you might have to delete the app and redeploy it.

### App requires a unique URL
Cloud Foundry requires that each app that you deploy have a unique URL. Otherwise, the new app URL collides with an existing app URL and Cloud Foundry cannot successfully deploy the app. You can fix this issue by running `cf push` with the `--random-route` flag to create a unique URL. Using `--random-route` to create a URL that includes the app name and random words might create a long URL, depending on the number of words that the app name includes.