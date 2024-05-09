# Managing Service Brokers
This page assumes you are using cf CLI v6.16 or later.
In order to run many of the commands, you must be authenticated with Cloud Foundry as an admin user or
as a space developer.

## Quick start
Given a service broker that has implemented the [Service Broker API](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md), two steps are required to
make its services available to end users in all orgs or a limited number of orgs by service plan.

1. [Registering a broker](https://docs.cloudfoundry.org/services/managing-service-brokers.html#register-broker)

2. [Making plans public](https://docs.cloudfoundry.org/services/managing-service-brokers.html#make-plans-public)

## Registering a broker
Registering a broker causes Cloud Controller to fetch and validate the catalog
from your broker, and save the catalog to the Cloud Controller database.
The basic auth username and password which are provided when adding a broker are
encrypted in Cloud Controller database, and used by the Cloud Controller to
authenticate with the broker when making all API calls.
Your service broker can validate the username and password sent in every
request; otherwise, anyone could curl your broker to delete service instances. When the broker is registered with an URL having the scheme `https`, Cloud Controller makes all calls to the broker over HTTPS.
As of cf-release 229, CC API 2.47.0, Cloud Foundry supports two types of brokers: *standard brokers* and *space-scoped brokers*. A list of their differences follows:

**Standard Brokers**

* Publish service plans to specific orgs or all orgs in the deployment. Can also keep plans unavailable, or *private*.

* Created by admins, with the command `cf create-service-broker`
```
$ cf create-service-broker mybrokername someuser somethingsecure https://mybroker.example.com
```

* Managed by admins

* Service plans are created private. Before anyone can use them, an admin must explicitly [make them available](https://docs.cloudfoundry.org/services/managing-service-brokers.html#make-plans-public) within an org or across all orgs.

**Space-scoped brokers**

* Publish service plans only to users within the space they are created. Plans are unavailable outside of this space.

* Created by space developers using the command `cf create-service-broker` with the `--space-scoped` flag
```
$ cf create-service-broker mybrokername someuser somethingsecure https://mybroker.example.com --space-scoped
```
If a space developer runs `cf create-service-broker` without the `--space-scoped` flag, they receive an error.

* Managed by space developers

* Newly created plans are published to all users in their space.

### Making plans public
After an admin creates a new service plan from a standard broker, no one can use it until the admin explicitly makes it available to users within a specific org or all orgs in the deployment.
See the [Access Control](https://docs.cloudfoundry.org/services/access-control.html#enable-access) topic for how to make standard broker service plans available to users.

### Multiple brokers, services and plans
Many service brokers can be added to a Cloud Foundry instance, each offering
many services and plans.
Keep the following constraints in mind:

* It is not possible to have multiple brokers with the same name.

* Prior to Cloud Foundry API (CAPI) v1.71, the service ID and plan IDs of each service advertised by the broker must be unique across Cloud Foundry.

* With CAPI v1.71 or later, the service ID and plan IDs of each service advertised by the broker must be unique only within the broker and can overlap ids defined in other brokers.

* GUIDs are recommended for the service ID and plan IDs of each service.

**Important**
If your deployment uses CAPI v1.71 or later, you can add multiple brokers with the same URL. In this case, the brokers must have different names. CAPI v1.70 and
earlier do not support this feature.
See [Possible errors](https://docs.cloudfoundry.org/services/managing-service-brokers.html#possible-errors) for error messages and what do to
when you see them.

## Listing service brokers
```
$ cf service-brokers
Getting service brokers as admin...
OK
Name URL
my-service-broker https://mybroker.example.com
```

## Updating a broker
Updating a broker is how to ingest changes a broker author has made into Cloud
Foundry.
Similar to adding a broker, update causes Cloud Controller to fetch the catalog
from a broker, validate it, and update the Cloud Controller database with any
changes found in the catalog.
Update also provides a means to change the basic auth credentials cloud
controller uses to authenticate with a broker, as well as the base URL of the
broker’s API endpoints.
```
$ cf update-service-broker mybrokername someuser somethingsecure https://mybroker.example.com
```

## Renaming a broker
A service broker can be renamed with the `rename-service-broker`
command.
This name is used only by the Cloud Foundry operator to identify brokers, and
has no relation to configuration of the broker itself.
```
$ cf rename-service-broker mybrokername mynewbrokername
```

## Removing a broker
When you remove a service broker, all services and plans in the broker’s catalog are removed from the Cloud Foundry Marketplace.
```
$ cf delete-service-broker mybrokername
```
When you attempt to remove a service broker it can fail if there are service instances for any service plan in its catalog. When you are planning to shut down or
delete a broker, make sure to remove all service instances first. Failure to do so
leaves [orphaned service instances](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#orphans) in the Cloud Foundry database. If a
service broker has been shut down without first deleting service instances, you can remove the instances with the CLI, see [Purge a Service](https://docs.cloudfoundry.org/services/managing-service-brokers.html#purge-service).

### Purging a service
If a service broker has been shut down or removed without first deleting service instances from Cloud Foundry, you can be unable to remove the service broker or its services and plans from the Marketplace. In development environments, broker authors often destroy their broker deployments and need a way to clean up the Cloud Controller database.
The following command deletes a service offering, all of its plans, and all associated service instances and bindings from the Cloud Controller database, without making any API calls to a service broker. Once all services for a broker have been purged, the broker can be removed normally.
```
$ cf purge-service-offering service-test
Warning: This operation assumes that the service broker responsible for this
service offering is no longer available, and all service instances have been
deleted, leaving orphan records in Cloud Foundry's database. All knowledge of
the service can be removed from Cloud Foundry, including service instances and
service bindings. No attempt is made to contact the service broker; running
this command without destroying the service broker causes orphan service
instances. After running this command you might want to run either
delete-service-auth-token or delete-service-broker to complete the cleanup.
Really purge service offering service-test from Cloud Foundry? y
OK
```

### Purging a service instance
The following command deletes a single service instance, its service bindings and its service keys from the Cloud Controller database, without making any API calls to a service broker.
This helps in instances when a Service Broker is not conforming to the Service Broker API and not returning a 200 or 410 to requests to delete the service instance.
```
$ cf purge-service-instance mysql-dev
WARNING: This operation assumes that the service broker responsible for this
service instance is no longer available or is not responding with a 200 or 410,
and the service instance has been deleted, leaving orphan records in Cloud
Foundry's database. All knowledge of the service instance is removed from
Cloud Foundry, including service bindings and service keys.
Really purge service instance mysql-dev from Cloud Foundry?> y
Purging service mysql-dev...
OK
```
`purge-service-instance` requires cf-release v218 and cf CLI 6.14.0.
When multiple brokers provide two or more service instances with the same name, you must specify the broker by including
the `-b BROKER` flag in the `cf purge-service-instance` command.

## Catalog validation behaviors
When Cloud Foundry fetches a catalog from a broker, and compares the
broker’s id for services and plans with the `unique_id` values for services and
plans in the Cloud Controller database.
| Event | Action |
| --- | --- |
| The catalog fails to load or validate. | Cloud Foundry returns a meaningful error that the broker could not be reached or the catalog was not valid. |
| A service or plan in the broker catalog has an ID that is not present among the `unique_id` values in the marketplace database. | A new record must be added to the marketplace database. |
| A service or plan in the marketplace database are found with a `unique_id` that matches the broker catalog’s ID. | The marketplace must update the records to match the broker’s catalog. |
| The database has plans that are not found in the broker catalog, and there are no associated service instances. | The marketplace must remove these plans from the database, and then delete services that do not have associated plans from the database.
|
| The database has plans that are not found in the broker catalog, but there are provisioned instances. | The marketplace must mark the plan inactive and no longer allow it to be provisioned. |

## Possible errors
If incorrect basic auth credentials are provided:
```
Server error, status code: 500, error code: 10001, message: Authentication
failed for the service broker API.
Verify that the username and password are correct:
https://github-broker.a1-app.example.com/v2/catalog
```
If you receive the following errors, check your broker logs.
You might have an internal error.
```
Server error, status code: 500, error code: 10001, message:
The service broker response was not understood
Server error, status code: 500, error code: 10001, message:
The service broker API returned an error from
https://github-broker.a1-app.example.com/v2/catalog: 404 Not Found
Server error, status code: 500, error code: 10001, message:
The service broker API returned an error from
https://github-broker.primo.example.com/v2/catalog: 500 Internal Server Error
```
If your broker’s catalog of services and plans violates validation of presence,
uniqueness, and type, you can receive meaningful errors.
```
Server error, status code: 502, error code: 270012, message: Service broker catalog is invalid:
Service service-name-1
service id must be unique
service description is required
service "bindable" field must be a boolean, but has value "true"
Plan plan-name-1
plan metadata must be a hash, but has value [{"bullets"=>["bullet1", "bullet2"]}]
```