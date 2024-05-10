# Cloud Foundry Services
This topic tells you about the services in Cloud Foundry.

## Services and service instances
Cloud Foundry offers a marketplace of services that operators can use to provision reserved resources on demand.
Marketplace services include resources such as databases on a shared or dedicated server, or accounts on a SaaS app.
These resources are known as service instances and the systems that deliver and operate these resources are known as services.
For a service to be available in the Marketplace, an operator must integrate the service with Cloud Foundry using APIs.
For more information about provisioning service instances and other life cycle operations, see
[Managing Service Instances](https://docs.cloudfoundry.org/devguide/services/managing-services.html).
Cloud Foundry enables users to use services that are not available
in the Marketplace using user provided service instances (UPSI).
For more information, see [User-Provided Service Instances](https://docs.cloudfoundry.org/devguide/services/user-provided.html).

## Architecture and terminology
Services are integrated with Cloud Foundry by using a documented API for which the Cloud Controller is the client, called the Service Broker API.
This cannot be confused with the Cloud Controller API (CAPI), often used to refer to the version of Cloud Foundry.
The Service Broker API is versioned independently of CAPI.
The component of the service that uses the Service Broker API is called the *service broker*.
This component was formerly referred to as a service gateway.
However, as traffic between apps and services does not flow through the service broker, the term caused confusion.
Although “gateway” still appears in old code, the term “broker” is used in conversation, in new code, and in documentation.
Service brokers advertise a catalog of service offerings and service plans, as well as interpreting calls for provision, bind, unbind, and deprovision.
What a broker does with each call can vary between services. In general, ‘provision’ reserves resources on a service and 'bind’ delivers information to an app necessary for accessing the resource. The reserved resource is called a *service instance*. What a service instance represents can vary by service. It could be a single database on a multi-tenant server, a dedicated cluster, or even an account on a web app.
![Services interact with the Cloud Foundry. The diagram shows the following components: 'Service Broker', 'cloud controller', 'App environment', and 'service instances.](https://docs.cloudfoundry.org/services/images/managed-services.png)

## Service Instance credentials
Cloud Foundry enables users to provision credentials needed to interface with a service instance. You can use app binding to deliver these credentials to your Cloud Foundry app. For external and local clients, you can use service keys to generate credentials to communicate directly with a service instance.

### Binding Apps
Service instance credentials can be delivered to apps running on
Cloud Foundry in an environment variable. For more information, see
[Delivering Service Credentials to an App](https://docs.cloudfoundry.org/devguide/services/application-binding.html).
For information about binding to a specific app development framework, see [Buildpacks](https://docs.cloudfoundry.org/buildpacks/index.html).

### Service keys
Credentials managed manually are known as service keys. Use service keys when you want a set of credentials for use by clients other than the app in the same space. For instance, you can use service keys to connect to a service instance from a local client, or from an app in another space, or even from outside of Cloud Foundry.
For more information about creating a user-provided service instance with service keys,
see the [User-Provided Service Instances](https://docs.cloudfoundry.org/devguide/services/user-provided.html) topic.
For more information about service keys, see the [Managing Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html) topic.
Not all services support service keys. Some services support credentials through app binding only.

## Implementation and deployment
How a service is implemented is up to the service provider or developer. Cloud Foundry only requires that the service provider implement the Service Broker API. A broker can be implemented as a separate app, or by adding the required HTTP endpoints to an existing service.
Because Cloud Foundry only requires that a service implements the Service Broker API to be available to Cloud Foundry end users, many deployment models are possible. The following are examples of valid deployment models:

* Entire service packaged and deployed by BOSH alongside Cloud Foundry

* Service broker packaged and deployed by BOSH alongside Cloud Foundry, rest of the service deployed and maintained by other means

* Broker (and optionally service) pushed as an app to Cloud Foundry user space

* Entire service, including broker, deployed and maintained outside of Cloud Foundry by other means

## Communication between Apps and Service Instances
To allow an app to communicate with a service external to Cloud Foundry, you might need to configure the service to accept connections from your app based on its outbound IP address.
In your external service configuration, you must do one of the following:

* Add the entire IP address range for the Diego Cell where the app is deployed to your allow list.

* Derive the app IP address from its DNS name using a command-line tool such as `dig`, `host`, or `nslookup`. In your external service configuration, add the IP address or range of the app instance to your allow list.

## Streaming App Logs to Log Management Services
To learn how your app logs can be streamed to third-party log management services, see
[Streaming App Logs to Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html).
User provided service instances can be used to drain app logs to a service not available in the Marketplace.
This is also known as setting up a syslog drain.
For guidance on configuring some third party log management services, see
[Service-Specific Instructions for Streaming App Logs](https://docs.cloudfoundry.org/devguide/services/log-management-thirdparty-svc.html).

## Managing App Requests with Route Services
To learn how Marketplace services (and user-provided service instances) can be
used to perform preprocessing on app requests, see
[Managing App Requests with Route Services](https://docs.cloudfoundry.org/devguide/services/route-binding.html).

## Migrating a Database Schema
If your app relies on a relational database, you must apply schema changes periodically. To perform database schema migrations on Cloud Foundry-managed services, run a database migration task with the Cloud Foundry Command Line Interface (cf CLI) tool.
For more information about running cf CLI tasks, see
[Running Tasks](https://docs.cloudfoundry.org/devguide/using-tasks.html).
To run tasks with the cf CLI, you must install cf CLI v6.23.0 or later. For information about downloading, installing, and uninstalling
the cf CLI, see .
To run a database schema migration with the cf CLI:

1. Push the app:
```
$ cf push APP-NAME
```
Where `APP-NAME` is the name of the app.
To run a task without starting the app, you can push the app with `cf push -i 0` and then run the task. You can run the app later
by scaling up the instance count.

2. Run database schema migration as a task on the app:
```
$ cf run-task APP-NAME --command "bin/rails db:migrate" --name TASK-NAME
Creating task for app APP-NAME in org jdoe-org / space development as jdoe@pivotal.io...
OK
Task 1 has been submitted and ran successfully.
```
Where:

* `APP-NAME` is the name of the app.

* `TASK-NAME` is the name of the task.