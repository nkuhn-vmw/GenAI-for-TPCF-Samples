# Cloud Foundry API app revisions
A revision represents code and configuration used by an app at a specific time. It is a Cloud Foundry API (CAPI) object that can contain references to a droplet, a custom start command, and environment variables. The most recent revision for a running app represents code and configuration running in Cloud Foundry.
For additional information about app revisions, see [Revisions](http://v3-apidocs.cloudfoundry.org/version/release-candidate/#revisions) in the Cloud Foundry API (CAPI) documentation.

**Important**
CAPI v3 is the recommended API version for revisions. While revisions work with CAPI v2, there are several inconsistencies. For example, revision descriptions for apps with multiple processes can be inaccurate because CAPI v2 does not support apps with multiple processes. Additionally, pushing an app for the first time with revisions in CAPI v2 creates two revisions.

**Caution**
The app revisions API is experimental, and future releases might have breaking changes.

## Revisions use cases
Some use cases for revisions include:

* **Viewing revisions for an app:** This can help you understand how your app has changed over time.

* **Rolling back to a previous revision:** This allows you to deploy a version of the app that you had running previously without needing to track that previous state yourself or have multiple apps running. When you create a deployment and reference a revision, the revision deploys as the current version of your app.

### Events that trigger revisions
Revisions are generated through these events:

* A new droplet is created for an app.

* An app’s environment variables are changed.

* The custom start command for an app is added or changed.

* An app rolls back to a prior revision.
By default, CAPI retains a maximum of 100 revisions per app.

### Revision descriptions
Each revision includes a description of what changed in your app at the time the revision was created. The description includes one or more of these descriptions:

* `Process type removed`

* `New process type added`

* `Rolled back to revision X`

* `Custom start command removed`

* `Custom start command updated`

* `Custom start command added`

* `New environment variables deployed`

* `New droplet deployed`

### Droplet storage considerations
By default, Cloud Foundry retains the five most recent staged droplets in its droplets bucket. This means that you can roll back to revisions as long as they are using one of those five droplets. Not all revisions include a change in droplet.
Operators can configure Cloud Foundry to retain more droplets if necessary using the `system_blobstore_ccdroplet_max_staged_droplets_stored` property in the Cloud Foundry manifest.

## View revisions
This section describes how to use CAPI endpoints for viewing revisions.

### List revisions for an app
To list revisions for an app:

1. Retrieve the GUID of the app by running:
```
cf app APP-NAME --guid
```
Where `APP-NAME` is the name of your app.

2. Run:
```
cf curl /v3/apps/GUID/revisions
```
Where `GUID` is the GUID you retrieved in an earlier step.

### List deployed revisions for an app
Deployed revisions are revisions linked to started processes in an app. To list deployed revisions:

1. Retrieve the GUID of the app by running:
```
cf app APP-NAME --guid
```
Where `APP-NAME` is the name of your app.

2. Run:
```
cf curl /v3/apps/GUID/revisions/deployed
```
Where `GUID` is the GUID you retrieved in an earlier step.

### Retrieve a revision
To retrieve a revision:

1. Run:
```
cf curl /v3/revisions/GUID
```
Where `GUID` is the GUID of the revision.

## Roll back to a previous revision
To roll back to a previous revision:

1. Retrieve the GUID of the app by running:
```
cf app APP-NAME --guid
```
Where `APP-NAME` is the name of your app.

2. Retrieve the GUID of the revision. See [Retrieve a revision](https://docs.cloudfoundry.org/devguide/revisions.html#get).

3. Create a deployment using CAPI by running:
```
cf curl v3/deployments \

-X POST \

-d '{
"revision": {
"guid": "REVISION-GUID"
},
"relationships": {
"app": {
"data": {
"guid": "APP-GUID"
}
}
}
}'
```
Where:

* `REVISION-GUID` is the GUID of the revision.

* `APP-GUID` is the GUID of the app.

## Add metadata to a revision
To add metadata to a revision, see [Add metadata to an object](https://docs.cloudfoundry.org/adminguide/metadata.html).

## Deactivate revisions for an app
CAPI activates app revisions by default. To deactivate revisions for an app, you must manually turn them off.
To deactivate revisions for an app:

1. Retrieve the GUID of the app by running:
```
cf app APP-NAME --guid
```
Where `APP-NAME` is the name of your app.

2. Run:
```
cf curl /v3/apps/GUID/features/revisions -X PATCH -d '{ "enabled": false }'
```
Where `GUID` is the GUID you retrieved in an earlier step.