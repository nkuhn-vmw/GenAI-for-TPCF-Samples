# Audit Events

## Overview
Audit events help Cloud Foundry operators monitor actions taken against resources (such as apps) via user or system actions.

### Differences from Other Types of Events
Despite being similar in name, audit events are different from [Cloud Foundry usage events](https://docs.cloudfoundry.org/running/managing-cf/usage-events.html).
Unlike usage events, audit events are not suitable for app and service billing.
Another tool to help administrators monitor user actions on Cloud Foundry is [Security event logging](https://docs.cloudfoundry.org/loggregator/cc-uaa-logging.html).
Unlike Security Event Logs, audit events do not cover all API endpoints, but provide more details about a user’s actions.

### View Events
The easiest way to view events for an app is to use the [Cloud Foundry CLI](https://docs.cloudfoundry.org/cf-cli/):
`cf events APP_NAME`
This results in the following output:
```
time event actor description
2018-09-04T17:03:49.00-0700 audit.app.droplet.create admin
2018-09-04T17:03:28.00-0700 audit.app.update admin state: STARTED
2018-09-04T17:03:27.00-0700 audit.app.build.create admin
2018-09-04T17:03:24.00-0700 audit.app.upload-bits admin
2018-09-04T17:03:24.00-0700 audit.app.map-route admin
2018-09-04T17:03:24.00-0700 audit.app.create admin instances: 1, state: STOPPED, environment_json: [PRIVATE DATA HIDDEN]
```
This command shows the 50 most recent events for that app.
To see more events, or events that are not attributed to an app, use the following Cloud Foundry API endpoint:
`GET /v3/audit_events`
```
$ cf curl /v3/audit_events
{
"pagination": {
"total_results": 1,
"total_pages": 1,
"first": {
"href": "https://api.example.org/v3/audit_events?page=1&per_page=2"
},
"last": {
"href": "https://api.example.org/v3/audit_events?page=1&per_page=2"
},
"next": null,
"previous": null
},
"resources": [
{
"guid": "a595fe2f-01ff-4965-a50c-290258ab8582",
"created_at": "2016-06-08T16:41:23Z",
"updated_at": "2016-06-08T16:41:26Z",
"type": "audit.app.update",
"actor": {
"guid": "d144abe3-3d7b-40d4-b63f-2584798d3ee5",
"type": "user",
"name": "admin"
},
"target": {
"guid": "2e3151ba-9a63-4345-9c5b-6d8c238f4e55",
"type": "app",
"name": "my-app"
},
"data": {
"request": {
"recursive": true
}
},
"space": {
"guid": "cb97dd25-d4f7-4185-9e6f-ad6e585c207c"
},
"organization": {
"guid": "d9be96f5-ea8f-4549-923f-bec882e32e3c"
},
"links": {
"self": {
"href": "https://api.example.org//v3/audit_events/a595fe2f-01ff-4965-a50c-290258ab8582"
}
}
}
]
}
```
For documentation about using this endpoint, see the [API documentation](https://v3-apidocs.cloudfoundry.org/index.html#list-audit-events).

**Note**
`get-events` is a community-contributed
cf CLI plug-in. The plug-in provides convenient flags to list events that took place today,
from yesterday, or from a particular date. `get-events` also provides useful output
formatting options. For more information, see
[get-events](https://plugins.cloudfoundry.org/#get-events) in cf CLI Plugins.

## Using audit events
The following describes some of the intended use cases of audit events.

### Resource history
Audit events allow users, administrators, and operators a view a resource’s history. For example, by looking at usage events for an app, an operator can see information such as when it was last updated or if it has crashed recently.

### Querying for events
You can query the events endpoint with various filters. For example, you can query for all events of a given type, or all events associated with a resource since a given timestamp.
For a list of allowed filters, see [List audit events](https://v3-apidocs.cloudfoundry.org/index.html#list-audit-events) in the API documentation.
The following example shows a query with multiple filters. The request gets `audit.app.unmap-route` events from a particular time period.
```
$ cf curl '/v3/audit_events?types=audit.app.unmap-route&created_ats[gt]=2021-11-10T01:08:24Z&created_ats[lt]=2021-11-15T01:08:24Zℴ_by=created_at'
```

### External auditing warehouse
For auditing and compliance reasons, some operators may wish to keep a record of all audit events that have occurred. Because audit events expire and may be purged during a deploy, these operators must maintain an external data warehouse. This way they can store and access events across expiration events and conform to their own compliance requirements.

## Types of audit events

### App lifecycle (audit.app.\*)

* audit.app.apply\_manifest

* audit.app.build.create

* audit.app.copy-bits

* audit.app.create

* audit.app.delete-request

* audit.app.deployment.cancel

* audit.app.deployment.create

* audit.app.droplet.create

* audit.app.droplet.delete

* audit.app.droplet.download

* audit.app.droplet.mapped

* audit.app.droplet.upload

* audit.app.environment.show

* audit.app.environment\_variables.show

* audit.app.map-route

* audit.app.package.create

* audit.app.package.delete

* audit.app.package.download

* audit.app.package.upload

* audit.app.process.crash

* audit.app.process.create

* audit.app.process.delete

* audit.app.process.ready

* audit.app.process.not-ready

* audit.app.process.rescheduling

* audit.app.process.scale

* audit.app.process.terminate\_instance

* audit.app.process.update

* audit.app.restage

* audit.app.restart

* audit.app.revision.create

* audit.app.revision.environment\_variables.show

* audit.app.ssh-authorized

* audit.app.ssh-unauthorized

* audit.app.start

* audit.app.stop

* audit.app.task.cancel

* audit.app.task.create

* audit.app.unmap-route

* audit.app.update

* audit.app.upload-bits

### Organization lifecycle (audit.organization.\*)

* audit.organization.create

* audit.organization.delete-request

* audit.organization.update

### Route lifecycle (audit.route.\*)

* audit.route.create

* audit.route.delete-request

* audit.route.update

* audit.route.share

* audit.route.unshare

* audit.route.transfer-owner

### Service lifecycle (audit.service.\*)

* audit.service.create

* audit.service.delete

* audit.service.update

### Service binding lifecycle (audit.service\_binding.\*)

* audit.service\_binding.create

* audit.service\_binding.delete

* audit.service\_binding.start\_create

* audit.service\_binding.start\_delete

* audit.service\_binding.update

* audit.service\_binding.show

### Service broker lifecycle (audit.service\_broker.\*)

* audit.service\_broker.create

* audit.service\_broker.delete

* audit.service\_broker.update

### Service dashboard client lifecycle (audit.service\_dashboard\_client.\*)

* audit.service\_dashboard\_client.create

* audit.service\_dashboard\_client.delete

### Service instance lifecycle (audit.service\_instance.\*)

* audit.service\_instance.bind\_route

* audit.service\_instance.create

* audit.service\_instance.delete

* audit.service\_instance.share

* audit.service\_instance.unbind\_route

* audit.service\_instance.unshare

* audit.service\_instance.update

* audit.service\_instance.show

* audit.service\_instance.start\_create

* audit.service\_instance.start\_update

* audit.service\_instance.start\_delete

* audit.service\_instance.purge

### Service route lifecycle (audit.service\_route\_binding.\*)

* audit.service\_route\_binding.create

* audit.service\_route\_binding.delete

* audit.service\_route\_binding.start\_create

* audit.service\_route\_binding.start\_delete

* audit.service\_route\_binding.update

### Service key lifecycle (audit.service\_key.\*)

* audit.service\_key.create

* audit.service\_key.delete

* audit.service\_key.start\_create

* audit.service\_key.start\_delete

* audit.service\_key.update

* audit.service\_key.show

### Service plan visibility lifecycle (audit.service\_plan\_visibility.\*)

* audit.service\_plan.create

* audit.service\_plan.update

* audit.service\_plan.delete

* audit.service\_plan\_visibility.create

* audit.service\_plan\_visibility.delete

* audit.service\_plan\_visibility.update

### Space lifecycle (audit.space.\*)

* audit.space.create

* audit.space.delete-request

* audit.space.update

### User lifecycle (audit.user.\*)

* audit.user.organization\_auditor\_add

* audit.user.organization\_auditor\_remove

* audit.user.organization\_billing\_manager\_add

* audit.user.organization\_billing\_manager\_remove

* audit.user.organization\_manager\_add

* audit.user.organization\_manager\_remove

* audit.user.organization\_user\_add

* audit.user.organization\_user\_remove

* audit.user.space\_auditor\_add

* audit.user.space\_auditor\_remove

* audit.user.space\_supporter\_add

* audit.user.space\_supporter\_remove

* audit.user.space\_developer\_add

* audit.user.space\_developer\_remove

* audit.user.space\_manager\_add

* audit.user.space\_manager\_remove

### User-provided service instance lifecycle (audit.user\_provided\_service\_instance.\*)

* audit.user\_provided\_service\_instance.create

* audit.user\_provided\_service\_instance.delete

* audit.user\_provided\_service\_instance.update

* audit.user\_provided\_service\_instance.show

### Special events

* audit.app.crash

* blob.remove\_orphan

## When are events created?
Most events are created when a user acts upon a resource.
For example, a user issuing a `cf stop APP_NAME` command causes an `audit.app.stop` event to be created and associated with that user.

* **Service events** (`audit.service*`) are created after the service broker has approved an interaction.

* **Crash and rescheduling events** (`audit.app.crash`, `audit.app.process.crash|rescheduling`) are created when Diego marks an app instance as crashed or evacuates app instances from cells on Diego Cell VM restarts.

* **Blob events** (`blob.remove_orphan`) are created by a daily clean up job and do not represent user action.

## Considerations
Audit events can be created at any point during the execution of the action they describe. This means the action associated with the event is not guaranteed to have succeeded.
The audit events table can grow to be very large. So, for performance considerations, certain database migrations may result in the truncation of this table.
In other words, this means that a deployment with such a migration will result in a loss of events.
These migrations are exceedingly rare and any release of capi-release that includes one will note this behavior prominently in its [release notes](https://github.com/cloudfoundry/capi-release/releases).
The order of audit events returned from the API may not match the sequence of events that occurred in the system.
Do not rely on timestamps to sequence events; they may come from different Cloud Controller instances whose times could be slightly mismatched.
Audit events expire after 31 days by default. This is configurable using the capi-release manifest property `cc.audit_events.cutoff_age_in_days`.