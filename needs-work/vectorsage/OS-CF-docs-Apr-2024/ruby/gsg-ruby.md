# Deploying Ruby apps
Learn how to deploy a Ruby app to
Cloud Foundry.
If you experience a problem following the steps, check the
[Troubleshooting Cloud Foundry](http://docs.cloudfoundry.org/running/troubleshooting.html) topic, or refer to the [Troubleshooting application deployment and health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html)
topic.
If you want to go through this tutorial using the sample app, run `git clone <https://github.com/cloudfoundry-samples/pong_matcher_ruby.git>` to clone the `pong_matcher_ruby` app from GitHub, and follow the instructions in the Sample app step sections.
Ensure that your Ruby app runs locally before continuing with this procedure.

## Deploy a Ruby app
You can deploy a Ruby application to
Cloud Foundry, and use the output from a sample app to show specific
steps of the deployment process.

### Prerequisites

* A Ruby 2.x application that runs locally on your workstation

* [Bundler](http://bundler.io) configured on your workstation

* Basic to intermediate Ruby knowledge

* The [Cloud Foundry Command Line Interface (cf CLI)](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html) installed on your
workstation

### Step 1: Create and bind a service instance for a Ruby app
Use the cf CLI to configure a Redis Cloud managed service instance for an app.
Cloud Foundry supports the following types of service instances:

* Managed services integrate with Cloud Foundry through service
brokers that offer services and plans and manage the service calls between
Cloud Foundry and a service provider.

* User-provided service instances enable you to connect your application to
pre-provisioned external service instances.
For more information about creating and using service instances, refer to the
[Services Overview](https://docs.cloudfoundry.org/devguide/services/) topic.

#### Creating a service instance
To create a service instance:

1. View managed and user provided services and plans that are available to you by running:
```
cf marketplace
```
The example shows three of the available managed database-as-a-service providers
and the plans that they offer: `cleardb` MySQL and `postgresql-10-odb` PostgreSQL as a
Service.
```
$ cf marketplace
Getting services from marketplace in org Cloud-Apps / space development as clouduser@example.com...
OK
service plans description
...
cleardb spark, boost, amp, shock Highly available MySQL for your Apps
...
postgresql-10-odb standalone, standalone-replica, general PostgreSQL as a Service
...
```

2. Create a service instance for your app.
```
cf create-service SERVICE PLAN SERVICE-INSTANCE
```
Choose a `SERVICE` and `PLAN` from the list, and provide a unique name for the
`SERVICE-INSTANCE`.

**Note**
Run `cf create-service rediscloud 30mb redis`. This creates a service instance named `redis` that uses the `rediscloud` service and the `30mb` plan, as the example below shows.
```
$ cf create-service rediscloud 30mb redis
Creating service redis in org Cloud-Apps / space development as clouduser@example.com....
OK
```

#### (Optional) Bind a service instance
When you bind an app to a service instance, Cloud Foundry writes
information about the service instance to the `VCAP_SERVICES` app environment
variable.
The app can use this information to integrate with the service instance.
Most services support bindable service instances.
Refer to your service provider’s documentation to confirm if they support this
functionality.
You can bind a service to an application by running:
```
cf bind-service APPLICATION SERVICE-INSTANCE
```
Alternately, you can configure the deployment manifest file by adding a
`services` block to the `applications` block and specifying the service
instance.
For more information and an example on service binding using a manifest, see the
Sample app step.
You can skip this step. The `manifest.yml` for the sample app contains a `services` sub-block in the `applications` block, as the example below shows. This binds the `redis` service instance that you created in the previous step.
```
services:

- redis
```

### (Optional) Step 2: Configure deployment options

#### Configure the deployment manifest file
You can specify app deployment options in a manifest that the `cf push` command uses. For more information about application manifests and supported attributes, refer to the [Deploying with Application Manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html) topic.

#### Configure a production server
Cloud Foundry uses the default standard Ruby web server library, WEBrick, for Ruby and RoR apps. However, Cloud Foundry can support a more robust production web server, such as Phusion Passenger, Puma, Thin, or Unicorn. If your app requires a more robust web server, refer to the [Configuring a Production Server](https://docs.cloudfoundry.org/buildpacks/prod-server.html) topic for help configuring a server other than WEBrick.
You can skip this step. The `manifest.yml` file for `pong_matcher_ruby` does not require any additional configuration to deploy the app.

### Step 3: Log in and target the API endpoint
Enter your login credentials, and select a space
and org.
```
cf login -a API-ENDPOINT
```
The API endpoint is [the URL of the Cloud Controller in your Cloud Foundry instance](http://docs.cloudfoundry.org/running/cf-api-endpoint.html).

**Note**
You must do this step to run the sample app.

### Step 4: Deploy an app
You must use the cf CLI to deploy apps.
Deploy your application by running the following command from the root directory of your application:
```
cf push APP-NAME
```
This command creates a URL route to your application in the form
`HOST.DOMAIN`, where `HOST` is your `APP-NAME` and `DOMAIN` is specified by your
administrator.
Your `DOMAIN` is`shared-domain.example.com`.
For example, `cf push my-app` creates the URL `my-app.shared-domain.example.com`.
The URL for your app must be unique from other apps that Cloud Foundry
hosts or the push fails.
Use the following options to help create a unique URL:

* `-n` to assign a different HOST name for the app.

* `--random-route` to create a URL that includes the app name and random words.

* `cf help push` to view other options for this command.
If you want to view log activity while the app deploys, launch a new terminal
window and run `cf logs APP-NAME`.
Once your app deploys, browse to your app URL.
Search for the `urls` field in the `App started` block in the output of the `cf push` command.
Use the URL to access your app online.
Run `cf push pong_matcher_ruby -n HOST_NAME`.
Example: `cf push
pong_matcher_ruby -n pongmatch-ex12`
The following example shows the terminal output of
deploying the `pong_matcher_ruby` app. The n`cf push` command uses the instructions in
the manifest file to create the app, create and bind the route, and upload the app. It then binds the app to
the `redis` service and follows the instructions in the manifest to start one instance of the
app with 256M. After the app starts, the output displays the health and status of the app.
These examples work for cf CLI v6. The `-n` flag is not supported for cf CLI v7/v8. Hostname must
be set using the `routes` property in the manifest.
The `pong_matcher_ruby` app does not include a web interface. To interact with
the `pong_matcher_ruby` app, see the interaction instructions on GitHub: [<https://github.com/cloudfoundry-samples/pong_matcher_ruby>](https://github.com/cloudfoundry-samples/pong_matcher_ruby).
```
$ cf push pong_matcher_ruby -n pongmatch-ex12
Using manifest file /Users/clouduser/workspace/pong_matcher_ruby/manifest.yml
Creating app pong_matcher_ruby in org Cloud-Apps / space development as clouduser@example.com...
OK
Creating route pongmatch-ex12.shared-domain.example.com
Binding pongmatch-ex12.shared-domain.example.com to pong_matcher_ruby...
OK
Uploading pong_matcher_ruby...
Uploading app files from: /Users/clouduser/workspace/pong_matcher_ruby
Uploading 8.8K, 12 files
OK
Binding service redis to app pong_matcher_ruby in org Cloud-Apps / space development as clouduser@example.com...
OK
Starting app pong_matcher_ruby in org Cloud-Apps / space development as clouduser@example.com...
OK
...
0 of 1 instances running, 1 starting
1 of 1 instances running
App started
Showing health and status for app pong_matcher_ruby in org Cloud-Apps / space development as clouduser@example.com...
OK
requested state: started
instances: 1/1
usage: 256M x 1 instances
urls: pongmatch-ex12.cfapps.io
state since cpu memory disk

#0 running 2014-12-09 10:04:40 AM 0.0% 35.2M of 256M 45.8M of 1G
```

### Step 5: Test a deployed app
You’ve deployed an app to Cloud Foundry!
Use the cf CLI to review information and administer your
app and your account.
For example, you could edit the `manifest.yml` to increase the number of app
instances from 1 to 3, and redeploy the app with a new app name and host name.
See the [Manage Your Application with the cf CLI](https://docs.cloudfoundry.org/buildpacks/ruby/gsg-ruby.html#cli-manage) section for more information.

## Manage your application with the cf CLI
Run `cf help` to view a complete list of commands, grouped by task categories,
and run `cf help COMMAND` for detailed information about a specific command.
For more information about using the cf CLI, refer to the Cloud Foundry Command Line Interface (cf CLI) topics, especially the [Getting Started with the cf CLI](http://docs.cloudfoundry.org/cf-cli/getting-started.html) topic.
You cannot perform certain tasks in the CLI because these are commands that
only an administrator can run. If you are not an administrator, the following message displays for these types of commands:
`error code: 10003, message: You are not authorized to perform the requested action`

## Troubleshooting
If your application fails to start, verify that the application starts in your
local environment.
Refer to the [Troubleshooting Application Deployment and Health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html) topic to
learn more about troubleshooting.

### App deploy fails
Even when deploying an app fails, the app might exist on
Cloud Foundry.
Run `cf apps` to review the apps in the targeted org and space.
You might be able to correct the issue using the CLI, or you
might have to delete the app and redeploy it.
Common reasons deploying an app fails include:

* You did not successfully create and bind a needed service instance to the app,
such as a PostgreSQL service instance.
Refer to Step 2: Create and Bind a Service Instance for a Ruby Application.

* You did not successfully create a unique URL for the app.
Refer to the troubleshooting tip **App Requires Unique URL**.

### App requires unique URL
Cloud Foundry requires that each app that you deploy has a unique
URL.
Otherwise, the new app URL collides with an existing app URL and
Cloud Foundry cannot successfully deploy the app.
You can fix this issue by running `cf push` with the `--random-route` flag to create a unique URL. Using `--random-route` to create a URL that includes the app name and random words might create a long URL, depending on the number of words that the app name includes.