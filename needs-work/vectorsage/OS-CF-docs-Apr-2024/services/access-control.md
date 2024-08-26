# Managing access to Service Plans
All new service plans from standard brokers are private by default. When you add a new broker, or when you add a new
plan to an existing broker’s catalog, service plans do not immediately become available. This is an admin control which service plans are available to you, and manage limited service availability.
Space scoped brokers are registered to a specific space, and all users within that space can access the broker’s service plans. With space-scoped brokers, service visibility is not managed separately.

## Prerequisites

* CLI v6.4.0

* Cloud Controller API v2.9.0 (cf-release v179)

* Admin user access; the following commands can be run only by an admin user

## Service Plan access
The `service-access` CLI command allows an admin to see the current access control setting for every service plan in the marketplace, across all service brokers.
```
$ cf service-access
getting service access as admin...
broker: elasticsearch-broker
service plan access orgs
elasticsearch standard limited
broker: p-mysql
service plan access orgs
p-mysql 100mb-dev all
```
The `access` column shows values `all`, `limited`, or `none`, defined as follows:

* `all` - The service plan is available to all users, or *public*.

* `none` - No one can use the service plan; it is *private*.

* `limited` - The plan is available only to users within the orgs listed.
The `-b`, `-e`, and `-o` flags let you filter by broker, service, and org.
```
$ cf help service-access
NAME:
service-access - List service access settings
USAGE:
cf service-access [-b BROKER] [-e SERVICE] [-o ORG]
OPTIONS:

-b access for plans of a particular broker

-e access for plans of a particular service offering

-o plans accessible by a particular org
```

## Enabling access to Service Plans
Admins use the `cf enable-service-access` command to give users access to service plans. The command grants access at the org level or across all orgs.
When an org has access to a plan, its users see the plan in the services marketplace (`cf marketplace`) and its Space Developer users can provision instances of the plan in their spaces.

#### Enabling access to a subset of users
The `-p` and `-o` flags to `cf enable-service-access` let the admin limit user access to specific service plans or orgs as follows:

* `-p PLAN` grants all users access to one service plan (access:`all`)

* `-o ORG` grants users in a specified org access to all plans (access: `limited`)

* `-p PLAN -o ORG` grants users in one org access to one plan (access: `limited`)
For example, the following command grants the org dev-user-org access to the p-mysql service.
```
$ cf enable-service-access p-mysql -o dev-user-org
Enabling access to all plans of service p-mysql for the org dev-user-org as admin...
OK
$ cf service-access
getting service access as admin...
broker: p-mysql
service plan access orgs
p-mysql dev-user-org
```
Run `cf help enable-service-access` to review these options from the command line.
Running `cf enable-service-access SERVICE-NAME` without any flags lets all users access every plan carried by the service. For example, the following command grants all-user access to all `p-mysql` service plans:
```
$ cf enable-service-access p-mysql
Enabling access to all plans of service p-mysql for all orgs as admin...
OK
$ cf service-access
getting service access as admin...
broker: p-mysql
service plan access orgs
p-mysql 100mb-dev all
```
When multiple brokers provide two or more services with the same name, you must specify the broker by including the `-b BROKER` flag in the `cf enable-service-access` command.

## Deactivating access to Service Plans
Admins use the `cf disable-service-access` command to deactivate user access to service plans. The command denies access at the org level or across all orgs.

#### Deactivating access to all plans for all users
When you run `cf disable-service-access SERVICE-NAME` without any flags, it deactivates all user access to all plans carried by the service. For example, the following command denies any user access to all `p-mysql` service plans:
```
$ cf disable-service-access p-mysql
Disabling access to all plans of service p-mysql for all orgs as admin...
OK
$ cf service-access
getting service access as admin...
broker: p-mysql
service plan access orgs
p-mysql 100mb-dev none
```

#### Deactivating access for specific orgs or plans
The `-p` and `-o` flags to `cf disable-service-access` allow the admin to deny access to specific service plans or orgs as follows:

* `-p PLAN` Deactivates user access to one service plan.

* `-o ORG` Deactivates access to all plans for users in a specified org.

* `-p PLAN -o ORG` Prevents users in one org from accessing one plan.
Run `cf help disable-service-access` to review these options from the command line.
When multiple brokers provide two or more services with the same name, you must specify the broker by including the `-b BROKER` flag in the `cf disable-service-access` command.

### Limitations

* You cannot deactivate access to a service plan for an org if the plan is currently available to all orgs. You must deactivate access for all orgs and activate access for a particular org.