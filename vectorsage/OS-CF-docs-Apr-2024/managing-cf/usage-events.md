# Usage events and billing
This topic describes types of usage events and how you can use them to construct billing information for apps and service instances.

## Usage events
You can use usage events to construct billing information for apps and service instances.
Despite being similar in name, usage events are different from Cloud Foundry audit events. You should not use the audit events stored in the events table for billing purposes. Audit events are recorded regardless of the action succeeding and are not guaranteed to be in the correct order.

### App usage events
App usage events provide information about when users create, delete, and update apps. They also include information about the app to enable you to bill based on resource usage.
App usage events expire after 31 days by default. You can configure a custom expiration period using the cf-deployment manifest property `cc.app_usage_events.cutoff_age_in_days`.

#### Endpoint
To retrieve information about app usage events, run:
```
GET /v2/app_usage_events
```
This command returns app usage events in output similar to the example below:
```
$ GET /v2/app_usage_events
{
"total_results": 2,
"total_pages": 2,
"prev_url": null,
"next_url": "/v2/app_usage_events?after_guid=5a3416b0-cf3c-425a-a14c-45a317c497ed&order-direction=asc&page=2&results-per-page=1",
"resources": [
{
"metadata": {
"guid": "b32241a5-5508-4d42-893c-360e42a300b6",
"url": "/v2/app_usage_events/b32241a5-5508-4d42-893c-360e42a300b6",
"created_at": "2016-06-08T16:41:33Z"
},
"entity": {
"state": "STARTED",
"previous_state": null,
"memory_in_mb_per_instance": 564,
"previous_memory_in_mb_per_instance": null,
"instance_count": 1,
"previous_instance_count": null,
"app_guid": "guid-d9fbb7f8-cba5-44a2-b720-c24f1fe5e1c4",
"app_name": "name-1663",
"space_guid": "guid-5e28f12f-9d80-473e-b826-537b148eb338",
"space_name": "name-1664",
"org_guid": "guid-036444f4-f2f5-4ea8-a353-e73330ca0f0a",
"buildpack_guid": "guid-df37754c-819b-4697-a523-4b457d3c83dd",
"buildpack_name": "name-1665",
"package_state": "STAGED",
"previous_package_state": null,
"parent_app_guid": null,
"parent_app_name": null,
"process_type": "web",
"task_name": null,
"task_guid": null
}
}
]
}
```
For more information, see [List all app usage events](https://apidocs.cloudfoundry.org/6.7.0/app_usage_events/list_all_app_usage_events.html) in the Cloud Foundry API documentation.

#### Event states
App usage events have the following valid states: `STARTED`, `STOPPED`, `TASK_STARTED`, `TASK_STOPPED`, and `BUILDPACK_SET`.
Multiple `STARTED` events can occur in a row, so as to indicate updates to the app. You can parse the response to determine the specific difference.
Multiple `STOPPED` events cannot occur without ‘STARTED’ events between them.
The app usage events for `TASK_STARTED` and `TASK_STOPPED` events do not indicate app state. Instead, they indicate that a one-off task was executed.
The app usage events with the `BUILDPACK_SET` state do not represent an actual app state. Instead, they signify that a buildpack has been used for the app. You can use these app usage events to charge for buildpack usage.

### Service usage events
Service usage events provide information about when users create, update, and delete service instances.
Service usage events expire after 31 days by default in cf-deployment. You can configure a custom expiration period using the cf-deployment manifest property `cc.service_usage_events.cutoff_age_in_days`.

#### Endpoint
To retrieve information about service usage events, run:
```
GET /v2/service_usage_events
```
This command returns service usage events in output similar to the example below:
```
$ GET /v2/service_usage_events
{
"total_results": 2,
"total_pages": 2,
"prev_url": null,
"next_url": "/v2/service_usage_events?after_guid=0947a8ec-2b8b-42d6-98a4-8708f7f2ce9f&order-direction=asc&page=2&results-per-page=1",
"resources": [
{
"metadata": {
"guid": "985c09c5-bf5a-44eb-a260-41c532dc0f1d",
"url": "/v2/service_usage_events/985c09c5-bf5a-44eb-a260-41c532dc0f1d",
"created_at": "2016-06-08T16:41:39Z"
},
"entity": {
"state": "CREATED",
"org_guid": "guid-396a8cb9-5524-4a2b-8e9e-2bfc70edb58d",
"space_guid": "guid-be1f6fe3-e63a-41a3-b196-3fc084022823",
"space_name": "name-1981",
"service_instance_guid": "guid-f93250f7-7ef5-4b02-8d33-353919ce8358",
"service_instance_name": "name-1982",
"service_instance_type": "type-5",
"service_plan_guid": "guid-e9d2d5a0-69a6-46ef-bac5-43f3ed177614",
"service_plan_name": "name-1983",
"service_guid": "guid-34916716-31d7-40c1-9afd-f312996c9654",
"service_label": "label-64",
"service_broker_name": "name-2929",
"service_broker_guid": "guid-7cc11646-bf38-4f4e-b6e0-9581916a74d9"
}
}
]
}
```
For more information, see [List service usage events](http://apidocs.cloudfoundry.org/12.24.0/service_usage_events/list_service_usage_events.html) in the Cloud Foundry API documentation.

#### Event states
Service usage events have the following valid states: `CREATED`, `DELETED`, and `UPDATED`. These states signify the desired state of the service.

#### Managed service instances versus user-provided service instances
Service usage events include the `service_instance_type` field to distinguish between managed service instances, or service instances backed by a broker, and user-provided service instances. You likely do not need to consider user-provided service instances for billing purposes.

## Using usage events
These sections describe how to use usage events.

### Ordering usage events
The order of events returned from the API are guaranteed to match the sequence of events that occurred in the system.
You should not use the timestamps on events to sequence events. They may come from different Cloud Controller instances whose time could be slightly mismatched. Unless you are billing on the millisecond, they are precise enough for normal usage.

### Querying for events
To only fetch events that you have not yet seen, use the `after_guid` query parameter. This only returns usage events that occurred after the event with the provided GUID.
For example:
```
GET /v2/app_usage_events?after_guid=7a63d717-3316-402f-bf12-a2a63211d1b9
```
Using the `after_guid` query parameter can result in lost events. Usage events are guaranteed to be in the correct order based on when the event creation started, but some event transactions take longer than others to complete.
If you always use the last event GUID for `after_guid`, you may miss events that occurred before that event, but that were still processing at the time of your query.
Cloud Foundry recommends that you select yourr `after_guid` from an event far enough back in time to ensure that all hanging transactions finish. The exact buffer period depends on the expected transaction time of a particular Cloud Foundry installation, but 1 minute is typically sufficient to prevent data loss.

### External warehouse
To generate accurate billing information, you must maintain your own external data warehouses. These warehouses can persist app usage events and service usage events for longer than their expiration periods and prevent you from having to continuously make expensive usage event queries.
Commonly, you generate aggregate billing events from the raw Cloud Foundry usage events to reduce the number of raw events you need to store.

### Creating your billing epoch
When you first start billing, there may be apps or instances without start events due to event expiration or other reasons. To seed the usage events with start events for all apps, use the purge endpoints.
To seed the app usage events with start events, run:
```
POST /v2/app_usage_events/destructively_purge_all_and_reseed_started_apps
```
For more information, see [Purge and reseed app usage events](http://apidocs.cloudfoundry.org/latest-release/app_usage_events/purge_and_reseed_app_usage_events.html) in the Cloud Foundry API documentation.
To seed the service usage events with start events, run:
```
POST /v2/service_usage_events/destructively_purge_all_and_reseed_existing_instances
```
For more information, see [Purge and reseed service usage events](http://apidocs.cloudfoundry.org/latest-release/service_usage_events/purge_and_reseed_service_usage_events.html) in the Cloud Foundry API documentation.
The purge endpoints create initial events for all apps or service instances. The seeded events all have the current timestamp, rather than the time the app was actually started.

**Note**
The purge endpoints delete all existing events, so it is important to use them only once when you start to record usage events for the first time. The purge endpoints are not intended to be called multiple times. Calling these events multiple times may result in lost events.