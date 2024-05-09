# Using metadata in Cloud Foundry
You can use metadata in Cloud Foundry and gives you instructions for adding, updating, removing, and viewing metadata.

## About metadata
Cloud Foundry allows you to add metadata to resources such as spaces and apps. You can use metadata to provide additional information about the resources in your Cloud Foundry deployment. This can help with operating, monitoring, and auditing.
For example, you can tag resources with metadata that describes the type of environment they belong to. You can also use metadata to describe app characteristics, such as front end or back end. Other examples include billing codes, points of contact, resource consumption, and information about security or risk.

### Methods of adding metadata
You can add metadata to resources using any of the following methods:

* **Cloud Foundry Command Line Interface (cf CLI) v7:** For procedures using this method of adding metadata, see [cf CLI Procedures](https://docs.cloudfoundry.org/adminguide/metadata.html#cf-cli-procedures). For more information about cf CLI v7, see [Upgrading to cf CLI v7](https://docs.cloudfoundry.org/cf-cli/v7.html).

* **Cloud Foundry API (CAPI):** For procedures using this method of adding metadata, see [API procedures](https://docs.cloudfoundry.org/adminguide/metadata.html#api-procedures). For more information about adding metadata with CAPI, see [Metadata](http://v3-apidocs.cloudfoundry.org/version/3.78.0/index.html#metadata) in the CAPI documentation.

### Types of metadata
You can add two types of metadata to resources in Cloud Foundry:

* **Labels:** Labels allow you to identify and select Cloud Foundry resources. For example, if you label all apps running in production or all spaces that contain Internet-facing apps, you can then search for them.

* **Annotations:** Annotations allow you to add non-identifying metadata to Cloud Foundry resources. You cannot query based on annotations. Also, there are fewer restrictions for key-value pairs of annotations than there are for labels. For example, you can include contact information of persons responsible for the resource, or tool information for debugging purposes.

#### Annotations sent to service brokers
For installations using CAPI v1.108.0 and later, Cloud Foundry sends annotations with key prefixes to service brokers when service instances and service bindings are created.
When a service instance is created, Cloud Foundry sends the following annotations to service brokers:

* `organization_annotations`

* `space_annotations`

* `instance_annotations`
When a service instance is bound to an app, Cloud Foundry also sends `app_annotations` to service brokers.
For more information about the annotations listed above, see [Cloud Foundry Context Object](https://github.com/openservicebrokerapi/servicebroker/blob/master/profile.md#cloud-foundry-context-object) in the Open Service Broker API Profile on GitHub.
For more general information about annotations, see [Annotations](https://v3-apidocs.cloudfoundry.org/#annotations) in the CAPI documentation.

### Metadata Requirements
The following tables describe requirements for creating metadata.

#### Requirements for labels
The following table describes the requirements for creating labels:
| Label requirements |
| --- |
| Part of Label | Length in characters | Allowed characters | Other Requirements |
| (Optional) Key Prefix | 0-253 | * Alphanumeric ( \[a-z0-9A-Z\] )

* `-`

* `.`

* DNS subdomain format, with at least one `.`

* Must end with `/`
| |
| Key Name | 1-63 | * Alphanumeric ( \[a-z0-9A-Z\] )

* `-`

* `_`

* `.`
| Must begin and end with an alphanumeric character |
| Value | 0-63 | * Alphanumeric

* `-`

* `_`

* `.`
| * Must begin and end with an alphanumeric character

* Empty values allowed
|

#### Requirements for annotations
The following table describes the requirements for creating annotations:
| Annotation Requirements |
| --- |
| Part of Annotation | Length in characters | Allowed characters | Other Requirements |
| (Optional) Key Prefix | 0-253 | * Alphanumeric ( \[a-z0-9A-Z\] )

* `-`

* `.`

* DNS subdomain format, with at least one `.`

* Must end with `/`
| |
| Key Name | 1-63 | * Alphanumeric ( \[a-z0-9A-Z\] )

* `-`

* `_`

* `.`
| Must begin and end with an alphanumeric character |
| Value | 0-5000 | Any unicode character | n/a |

### Metadata key prefixes
You can ensure that a label or annotation key is easily differentiated from other keys by using a prefix. A prefix is a namespacing pattern that helps you more clearly identify resources. Prefixes are in DNS subdomain format. For example, `prefix.example.com`.
Consider an example in which you have two scanner tools: one for security and one for compliance. Both tools use a `scanned` label or annotation. You can disambiguate between the two tools using a prefix. The security tool can prefix a label or annotation with `security.example.com/scanned` and the compliance tool can prefix a label or annotation with `compliance.example.com/scanned`.

## cf CLI procedures
The following sections describe how to add, update, view, and list metadata using the cf CLI.
To see which resources are supported for this feature, run `cf labels -h`.
cf CLI v7 supports adding labels to apps, orgs, spaces, buildpacks, stacks, routes, domains, and various service resources.

### Add metadata to a resource
This section describes how to add metadata using the cf CLI.

#### Add a label
To add a label to a resource:

1. Run:
```
cf set-label RESOURCE RESOURCE-NAME KEY=VALUE
```
Where:

* `RESOURCE` is the type of resource you want to label, such as `app` or `space`.

* `RESOURCE-NAME` is the name of the resource you want to label, such as `example-app`.

* `KEY` is the key for the label.

* `VALUE` is the corresponding value for the label key. You can enter multiple key-value pairs in the same command.

### Update metadata for a resource
To update metadata for a resource, follow the procedure for adding metadata and provide a new value for an existing key. For more information, see [Add metadata to a resource](https://docs.cloudfoundry.org/adminguide/metadata.html#add-cli).

### Remove metadata from a resource
This section describes how to remove metadata using the cf CLI.

#### Remove a label
To remove a label from a resource:

1. Run:
```
cf unset-label RESOURCE RESOURCE-NAME KEY
```
Where:

* `RESOURCE` is the type of resource you want to remove the label from, such as `app` or `space`.

* `RESOURCE-NAME` is the name of the resource you want to remove the label from , such as `example-app`.

* `KEY` is the key for the label.

### View metadata for a resource
This section describes how to view metadata with the cf CLI.

#### View labels
To view labels for a resource:

1. Run:
```
cf labels RESOURCE RESOURCE-NAME
```
Where:

* `RESOURCE` is the type of resource you want to remove the label from, such as `app` or `space`.

* `RESOURCE-NAME` is the name of the resource you want to remove the label from , such as `example-app`.

#### Select resources by labels
To select resources by labels:

1. Run:
```
cf apps --labels 'environment in (production,staging),tier in (backend)'
```

## API procedures
The following sections describe how to add, update, remove, list, and query metadata using CAPI.

### Add metadata to a resource
The following sections describe how to add labels and annotations to resources.

#### Add a label
To add a label to a resource using CAPI:

1. Run:
```
cf curl v3/RESOURCE-ENDPOINT/GUID \

-X PATCH \

-d '{
"metadata": {
"labels": {
"LABEL-KEY": "LABEL-VALUE"
}
}
}'
```
Where:

* `RESOURCE-ENDPOINT` is the CAPI endpoint for the type of resource you want to label, such as `apps` or `organizations`.

* `GUID` is the GUID of the resource you want to label.

* `LABEL-KEY` is the key for the label.

* `LABEL-VALUE` is the corresponding value for the label key.

#### Add an annotation
To add an annotation:

1. Run:
```
cf curl v3/RESOURCE-ENDPOINT/GUID \

-X PATCH \

-d '{
"metadata": {
"annotations": {
"ANNOTATION-KEY": "ANNOTATION-VALUE"
}
}
}'
```
Where:

* `RESOURCE-ENDPOINT` is the CAPI endpoint for the type of resource you want to label, such as `apps` or `organizations`.

* `GUID` is the GUID of the resource you want to label.

* `ANNOTATION-KEY` is the key for the label.

* `ANNOTATION-VALUE` is the corresponding value for the annotation key.

### Update metadata for a resource
To update metadata for a resource, follow the procedure for adding metadata and provide a new value for an existing key. For more information, see [Add metadata to a resource](https://docs.cloudfoundry.org/adminguide/metadata.html#add).

### Remove metadata from a resource
To remove metadata from a resource, follow the procedure for adding metadata and provide a `null` value for an existing key. For more information, see [Add metadata to a resource](https://docs.cloudfoundry.org/adminguide/metadata.html#add).

### View metadata for a resource
To view metadata using the list endpoint of a resource:

1. Run:
```
cf curl /v3/RESOURCE-ENDPOINT/GUID
```
Where:

* `RESOURCE-ENDPOINT` is the CAPI endpoint for the type of resource you want to view, such as `apps` or `organizations`.

* `GUID` is the GUID of the resource you want to view.

### List resources by querying labels
To list resources by querying label metadata:

1. To query a resource by using the `label_selector` parameter on its list endpoint, run:
```
cf curl /v3/RESOURCE-ENDPOINT/?label_selector=SELECTOR-REQUIREMENTS
```
Where:

* `RESOURCE-ENDPOINT` is the CAPI endpoint for the type of resource you want to view, such as `apps` or `organizations`.

* `SELECTOR-REQUIREMENTS` is one of requirement types specified in [Selector Requirement Reference](https://docs.cloudfoundry.org/adminguide/metadata.html#requirements-reference). You can add multiple selector requirements using a comma-separated list.
Ensure that this part of the URL is appropriately escaped.

#### Selector requirement reference
The following table describes how to form selector requirements:
| Requirement | Format | Description |
| --- | --- | --- |
| existence | `KEY` | Returns all resources labeled with the given key |
| inexistence | `!KEY` | Returns all resources not labeled with the given key |
| equality | `KEY==VALUE` or `KEY=VALUE` | Returns all resources labeled with the given key and value |
| inequality | `KEY!=VALUE` | Returns all resources not labeled with the given key and value |
| set inclusion | `KEY in (VALUE1,VALUE2...)` | Returns all resources labeled with the given key and one of the specified values |
| set exclusion | `KEY notin (VALUE1,VALUE2...)` | Returns all resources not labeled with the given key and one of the specified values |

## Example: Label resources with a git commit
This section provides the following:

* A procedure for labeling an app, package, and droplet with a Git commit SHA. For more information, see [Manually Label Resources](https://docs.cloudfoundry.org/adminguide/metadata.html#manual).

* A script that automates the procedure. For more information, see [Automate Labeling Resources](https://docs.cloudfoundry.org/adminguide/metadata.html#example-script).
Labeling your app and related resources with a Git commit SHA allows you to track which version of your code is running on Cloud Foundry.
For more information about app packages and droplets, see the [CAPI documentation](https://v3-apidocs.cloudfoundry.org/version/3.68.0/index.html).

### Manually label resources
To label an app, droplet, and package with a Git commit SHA:

1. Run:
```
cf app APP-NAME --guid
```
Where `APP-NAME` is the name of the app.

2. Record the app GUID you retrieved in the previous step,

3. Return the GUID of the droplet and package associated with the app by running:
```
cf curl /v3/apps/APP-GUID/droplets/current
```
Where `APP-GUID` is the GUID of the app.

4. Record the GUID of the droplet and package:

* The droplet GUID is the value for the `"guid"` key.

* The package GUID is the end of the `"href"` URL for the `"package"` key.For example, the droplet and package GUIDs are highlighted in blue in the following output:
```
{
"guid": "fd35633f-5c5c-4e4e-a5a9-0722c970a9d2",
...
"links": {
"package": {
"href": "https://api.run.pivotal.io/v3/packages/fd35633f-5c5c-4e4e-a5a9-0722c970a9d2"
}
}
```

5. Label the app with a Git commit SHA by running:
```
cf curl /v3/apps/APP-GUID -X PATCH -d '{"metadata": { "labels": { "commit": COMMIT-SHA } } }'
```
Where:

* `APP-GUID` is the GUID of the app.

* `COMMIT-SHA` is the SHA of the Git commit.

6. Label the app droplet with the same Git commit SHA by running:
```
cf curl /v3/droplets/DROPLET-GUID -X PATCH -d '{"metadata": { "labels": { "commit": COMMIT-SHA } } }'
```
Where:

* `DROPLET-GUID` is the GUID of the droplet.

* `COMMIT-SHA` is the SHA of the Git commit.

7. Label the app package with the same Git commit SHA by running:
```
cf curl /v3/packages/PACKAGE-GUID -X PATCH -d '{"metadata": { "labels": { "commit": COMMIT-SHA } } }'
```
Where:

* `PACKAGE-GUID` is the GUID of the package.

* `COMMIT-SHA` is the SHA of the Git commit.

### Automate labeling resources
You can automate labeling resources by running a script either programmatically or manually in the app repository.

#### Prerequisite
To run the following example script, you must install `jq`. To download `jq`, see [jq](https://stedolan.github.io/jq/).

#### Example script
The following script retrieves the GUID of the app, droplet, and package. It then `curls` CAPI to label each resource with the current Git commit SHA.
Replace `APP-NAME` with the name of your app.
```

#!/usr/bin/env bash
set -ex
APP\_GUID="$(cf app APP-NAME --guid)"
APP\_URI="/v3/apps/${APP\_GUID}"
DROPLET\_GUID="$(cf curl "/v3/apps/${APP\_GUID}/droplets/current" | jq -r .guid)"
DROPLET\_URI="/v3/droplets/${DROPLET\_GUID}"
PACKAGE\_GUID="$(cf curl "/v3/droplets/${DROPLET\_GUID}" | jq -r .links.package.href | xargs basename)"
PACKAGE\_URI="/v3/packages/${PACKAGE\_GUID}"
COMMIT\_SHA="$(git rev-parse --short HEAD)"
REQUEST\_BODY="$(jq -nc --arg commit "${COMMIT\_SHA}" '{"metadata": { "labels": { "commit": $commit } } }')"
cf curl "${APP\_URI}" -X PATCH -d "${REQUEST\_BODY}"
cf curl "${PACKAGE\_URI}" -X PATCH -d "${REQUEST\_BODY}"
cf curl "${DROPLET\_URI}" -X PATCH -d "${REQUEST\_BODY}"
```

## Example: Add custom tags to log and metric envelopes
Log and metric envelopes emitted by applications are tagged with information about the application, such as the
application name, for example.
You can define additional custom log and metric tags by adding a label with a specific prefix. The default prefix
is `metric.tag.cloudfoundry.org`. Following a restart of the application, the custom metric tag is
visible in the logs and metrics emitted for processes associated with that application.
The following commands add a tag named `custom_tag` with the value `some_value` for logs and metrics emitted for the
application `sample-app`:
```
$ cf set-label app sample-app metric.tag.cloudfoundry.org/custom_tag=some_value
$ cf restart sample-app
```
You can verify that the custom tag has been applied by querying Log Cache with the log-cache cf CLI plug-in. The
following commands assume that you have the `jq` command line utility.
```
$ cf install-plugin -r CF-Community 'log-cache'
$ cf tail sample-app --json --follow | jq -r '.tags.custom_tag'
some_value
some_value
some_value
```