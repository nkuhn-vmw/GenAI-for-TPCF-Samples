# Deploying Spring apps to Cloud Foundry
This guide walks you through deploying a Spring app to Cloud Foundry. You can choose whether to push a sample app, your own app, or both.
If you experience a problem following the steps, see the [Troubleshooting Cloud Foundry](http://docs.cloudfoundry.org/running/troubleshooting.html) topic, or refer to the [Troubleshooting Application Deployment and Health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html) topic.
If you want to go through this tutorial using the sample app, run `git
clone <https://github.com/cloudfoundry-samples/pong_matcher_spring>` to clone the `pong_matcher_spring` app from GitHub, and
follow the instructions in the Sample app step sections.
Ensure that your Spring app runs locally before continuing with this procedure.

## Deploy a Spring application
This section describes how to deploy your Spring application to Cloud Foundry.

### Prerequisites

* A Spring app that runs locally on your workstation

* Intermediate to advanced Spring knowledge

* The [Cloud Foundry Command Line Interface (cf CLI)](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html)

* JDK 1.6, 1.7, or 1.8 for Java 6, 7, or 8 configured on your workstation
The Cloud Foundry Java buildpack uses JDK 1.8, but you can modify the buildpack and the manifest for your app to compile to an earlier version. For more information, see [Creating custom buildpacks](https://docs.cloudfoundry.org/buildpacks/custom.html).

### Step 1: (Optional) Declare app dependencies
Make sure to declare all the dependency tasks for your app in the build script of your chosen build tool.
The [Spring Getting Started Guides](https://spring.io/guides) demonstrate features and functionality you can add to your app, such as consuming RESTful services or integrating data. These guides contain Gradle and Maven build script examples with dependencies. You can copy the code for the dependencies into your build script.
The following table lists build script information for Gradle and Maven and provides documentation links for each build tool.
| **Build Tool** | **Build Script** | **Documentation** |
| --- | --- | --- |
| Gradle | `build.gradle` | [Gradle User Guide](http://www.gradle.org/docs/current/userguide/userguide.html) |
| Maven | `pom.xml` | [Apache Maven Project Documentation](http://maven.apache.org/guides/) |
You can skip this step. The `pom.xml` file contains the dependencies for the `pong_matcher_spring` sample app, as the following example shows.
```
<dependencies>
<dependency>
<groupId>mysql</groupId>
<artifactId>mysql-connector-java</artifactId>
</dependency>
<dependency>
<groupId>org.flywaydb</groupId>
<artifactId>flyway-core</artifactId>
</dependency>
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-data-jpa</artifactId>
</dependency>
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-test</artifactId>
</dependency>
<dependency>
<groupId>org.springframework.boot</groupId>
<artifactId>spring-boot-starter-web</artifactId>
</dependency>
<dependency>
<groupId>com.h2database</groupId>
<artifactId>h2</artifactId>
<scope>test</scope>
</dependency>
<dependency>
<groupId>com.jayway.jsonpath</groupId>
<artifactId>json-path</artifactId>
<scope>test</scope>
</dependency>
</dependencies>
```
Make sure you are not building [fully executable jars](https://docs.spring.io/spring-boot/docs/current/reference/html/deployment-install.html) because application push might fail.

### Step 2: (Optional) Allocate sufficient memory
Use the `cf push -m` command to specify the amount of memory that should be allocated to the application. Memory allocated this way is done in preset amounts of `64M`, `128M`, `256M`, `512M`, `1G`, or `2G`. For example:
```
$ cf push -m 128M
```
When your app is running, you can use the `cf app APP-NAME` command to see memory utilization.
You can skip this step. The Cloud Foundry Java buildpack uses settings declared in the sample app to allocate 1 GB of memory to the app.

### Step 3: Provide a JDBC driver
The Java buildpack does not bundle a JDBC driver with your application. If your application accesses a SQL RDBMS, you must do the following:

* Include the appropriate driver in your application.

* Create a dependency task for the driver in the build script for your build tool or IDE.
You can skip this step. In the `pong_matcher_spring` sample app, the `src/main/resources/application.yml` file declares the JDBC driver, and the `pom.xml` file includes the JDBC driver as a dependency.

### Step 4: (Optional) Configure service connections for a Spring app
Cloud Foundry provides extensive support for creating and binding a Spring application to services such as MySQL, PostgreSQL, MongoDB, Redis, and RabbitMQ. For more information about creating and binding a service connection for your app, refer to [Configuring Service Connections](https://docs.cloudfoundry.org/buildpacks/java/configuring-service-connections.html).

**Note**
Run `cf create-service cleardb spark mysql`. This creates a service instance named `mysql` that uses the `cleardb` service and the `spark` plan, as this example shows.
```
$ cf create-service cleardb spark mysql
Creating service mysql in org Cloud-Apps / space development as a.user@example.com....
OK
```
You can skip this step because the service instance is already bound. Open the `manifest.yml` file in a text editor to view the bound service instance information. Locate the file in the app root directory and search for the `services` sub-block in the `applications` block, as the example below shows.
```

---
applications:
...
services:

- mysql
```

### Step 5: Configure the deployment manifest
You can specify deployment options in a manifest file `manifest.yml` that the `cf push` command uses when deploying your app.
Refer to the [Deploying with Application Manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html) topic for more information.
You can skip this step. The `manifest.yml` file for the `pong_matcher_spring` sample app does not require any additional configuration to deploy the app.

### Step 6: Log in and target the API endpoint
Enter your log in credentials, and select a space and org.
```
cf login -a API-ENDPOINT
```
Where `API-ENDPOINT` is [the URL of the Cloud Controller in your Cloud Foundry instance](http://docs.cloudfoundry.org/running/cf-api-endpoint.html).
You must do this step to run the sample app.

### Step 7: Deploy your app
You must use the cf CLI to deploy apps.
From the root directory of your app, run the following command to deploy your application.
```
cf push APP-NAME -p PATH-TO-FILE.jar
```
Most Spring apps include an artifact, such as a `.jar`, `.war`, or `.zip` file. You must include the path to this file in the `cf push` command using the `-p` option if you do not declare the path in the `applications` block of the manifest file. The example shows how to specify a path to the `.jar` file for a Spring app. Refer to the [Tips for Java Developers](https://docs.cloudfoundry.org/buildpacks/java/java-tips.html) topic for CLI examples for specific build tools, frameworks, and languages that create an app with an artifact.
The `cf push` command creates a URL route to your application in the form `HOST.DOMAIN`,
where `HOST` is your `APP-NAME` and `DOMAIN` is specified by your administrator.
Your `DOMAIN` is `shared-domain.example.com`.
For example, `cf push my-app` creates the URL `my-app.shared-domain.example.com`.
The URL for your app must be unique from other apps that Cloud Foundry hosts or the push fails.
Use the following options to help create a unique URL:

* `-n` to assign a different HOST name for the app

* `--random-route` to create a URL that includes the app name and random words

* `cf help push` to view other options for this command
If you want to view log activity while the app deploys, launch a new terminal window and run `cf logs APP-NAME`.
Once your app deploys, go to your app URL. Search for the `urls` field in the `App started` block in the output of the `cf push` command. Use the URL to access your app online.

#### Sample app step

1. Run `brew install maven`.

2. Change to the `app` directory, and run `mvn package` to build the app.

3. Run `cf push pong_matcher_spring -n HOSTNAME` to push the app.
Example: `cf push pong_matcher_spring -n my-spring-app`.
This example works for cf CLI v6. The `-n` flag is not supported for cf CLI v7/v8. Hostname must be set using the `routes` property in the manifest.
You do not have to include the `-p` flag when you deploy the sample app. The sample app manifest declares the path to the archive that `cf push` uses to upload the app files.
The following example shows the terminal output of deploying the `pong_matcher_spring` app. `cf push` uses the instructions in the manifest file to create the app, create and bind the route, and upload the app. It then binds the app to the `mysql` service and starts one instance of the app with 1 GB of memory. After the app starts, the output displays
the health and status of the app. This example works for cf CLI v6. The `-n` flag is not supported for cf CLI v7/v8. Hostname must be set using the `routes` property in the manifest.
```
$ cf push pong_matcher_spring -n spring1119
Using manifest file /Users/example/workspace/pong_matcher_spring/manifest.yml
Creating app pong_matcher_spring in org Cloud-Apps / space development as a.user@example.com...
OK
Creating route spring1119.cfapps.io...
OK
Binding spring1119.cfapps.io to pong_matcher_spring...
OK
Uploading pong_matcher_spring...
Uploading app files from: /Users/example/workspace/pong_matcher_spring/target/pong-matcher-spring-1.0.0.BUILD-SNAPSHOT.jar
Uploading 797.5K, 116 files
OK
Binding service mysql to app pong_matcher_spring in org Cloud-Apps / space development as a.user@example.com...
OK
Starting app pong_matcher_spring in org Cloud-Apps / space development as a.user@example.com...
OK

-----> Downloaded app package (25M)

-----> Downloading Open Jdk JRE 1.8.0_25 from https://download.run.pivotal.io/openjdk/lucid/x86_64/openjdk-1.8.0_25.tar.gz (1.2s)
Expanding Open Jdk JRE to .java-buildpack/open_jdk_jre (1.1s)

-----> Downloading Spring Auto Reconfiguration 1.5.0_RELEASE from https://download.run.pivotal.io/auto-reconfiguration/auto-reconfiguration-1.5.0_RELEASE.jar (0.1s)

-----> Uploading droplet (63M)
0 of 1 instances running, 1 starting
1 of 1 instances running
App started
Showing health and status for app pong_matcher_spring in org Cloud-Apps / space development as a.user@example.com...
OK
requested state: started
instances: 1/1
usage: 1G x 1 instances
urls: spring1119.cfapps.io
state since cpu memory disk

#0 running 2014-11-19 12:29:27 PM 0.0% 553.6M of 1G 127.4M of 1G
```

### Step 8: Test your deployed app
Use the cf CLI to review information and administer your app and your Cloud Foundry account. For example, you can edit the `manifest.yml` to increase the number of app instances from 1 to 3, and redeploy the app with a new app name and host name.
See [Manage your application with the cf CLI](https://docs.cloudfoundry.org/buildpacks/java/getting-started-deploying-apps/gsg-spring.html#cli-manage) for more information.
Sample app step: To test the sample app, do the following:

1. To export the test host, run `export HOST=SAMPLE-APP-URL`, substituting the URL for your app for `SAMPLE-APP-URL`.

1. To clear the database from any previous tests, run:
`curl -v -X DELETE $HOST/all`
You should get a response of 200.

1. To request a match as “andrew”, run:
`curl -v -H "Content-Type: application/json" -X PUT $HOST/match_requests/firstrequest -d '{"player": "andrew"}'`
You should again get a response of `200`.

1. To request a match as a different player, run:
`curl -v -H "Content-Type: application/json" -X PUT $HOST/match_requests/secondrequest -d '{"player": "navratilova"}'`

1. To check the status of the first match request, run:
`curl -v -X GET $HOST/match_requests/firstrequest`
The last line of the output shows the `match_id`.

1. Replace `MATCH_ID` with the `match_id` value from the previous step in the following command:
```
curl -v -H "Content-Type: application/json" -X POST $HOST/results -d '
{
"match_id":"MATCH_ID",
"winner":"andrew",
"loser":"navratilova"
}'
```
You should receive a `201 Created` response.

## Manage your app with the cf CLI
Run `cf help` to view a complete list of commands, grouped by task categories, and run `cf help COMMAND` for detailed information about a specific command. For more information about using the cf CLI, refer to the Cloud Foundry Command Line Interface (cf CLI) topics, especially the [Getting Started with the cf CLI](http://docs.cloudfoundry.org/cf-cli/getting-started.html) topic.
You cannot perform certain tasks in the CLI because these are commands that only an administrator can run. If you are not an administrator, the following message displays for these types of commands:
`error code: 10003, message: You are not authorized to perform the requested action`

## Troubleshooting
If your application fails to start, verify that the application starts in your local environment. Refer to the [Troubleshooting Application Deployment and Health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html) topic to learn more about troubleshooting.

### App deploy fails
Even when the deploy fails, the app might exist on Cloud Foundry. Run the `cf apps` command to review the apps in the targeted org and space. You might be able to correct the issue using the CLI, or you might have to delete the app and redeploy it.

### App requires a Content-Type
If you specify a `Content-Encoding` header of `gzip` but do not specify a `Content-Type` within your application, Cloud Foundry might send a `Content-Type` of `application/x-gzip` to the browser. This scenario might cause the deploy to fail if it conflicts with the actual encoded content of your app. To avoid this issue, be sure to explicitly set `Content-Type` within your app.

### App requires a unique URL
Cloud Foundry requires that each app that you deploy have a unique URL. Otherwise, the new app URL collides with an existing app URL and Cloud Foundry cannot successfully deploy the app. You can fix this issue by running `cf push` with the `--random-route` flag to create a unique URL. Using `--random-route` to create a URL that includes the app name and random words might create a long URL, depending on the number of words that the app name includes.