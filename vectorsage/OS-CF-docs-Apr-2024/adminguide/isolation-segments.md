# Managing Isolation Segments in Cloud Foundry
With Cloud Foundry, you can isolate deployment workloads into dedicated resource pools called isolation segments.

## Isolation Segments overview
To enable isolation segments, an admin can pass in a custom operations file with the BOSH CLI. For the example file used in this topic,
see the [cf-deployment](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/test/add-persistent-isolation-segment-diego-cell.yml) repository in GitHub.
After an admin creates a new isolation segment, the admin can then create and manage relationships between the orgs and spaces
of a Cloud Foundry deployment and the new isolation segment.

## Requirements
Target the API endpoint of your deployment with `cf api` and log in with `cf login` before performing the procedures in this topic. For more information, see [Identifying your Cloud Foundry API Endpoint and Version](http://docs.cloudfoundry.org/running/cf-api-endpoint.html).

## Add an Isolation Segment to your deployment manifest
To add an isolation segment to your deployment manifest:

1. Write a custom operations file. The operations file defines an instance group that supports isolation segments.
For a working example, see the [cf-deployment](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/test/add-persistent-isolation-segment-diego-cell.yml) repository in GitHub. The example sets the following instance group properties:

* Name as `isolated-diego-cell`

* Placement tag as `persistent_isolation_segment`
When you use the cf CLI, the name of the isolation segment corresponds to the placement tag you
specify in the operations file. The commands throughout this topic use `SEGMENT-NAME` as an example isolation segment name.

2. Apply the custom operations file when you deploy Cloud Foundry by running:
```
bosh -e BOSH-ENVIRONMENT -d cf deploy cf-deployment/cf-deployment.yml \

-v system_domain=SYSTEM-DOMAIN \

-o cf-deployment/operations/CUSTOM-OPS-FILE.yml
```
Where:

* `BOSH-ENVIRONMENT` is your BOSH environment alias. For more information about creating an environment alias for BOSH v2 or later, see [Environments](https://bosh.io/docs/cli-envs/) in the BOSH documentation.

* `SYSTEM-DOMAIN` is the system domain of your Cloud Foundry deployment.

* `CUSTOM-OPS-FILE.yml` is your operations file.

## Register an isolation segment
To register an isolation segment in the Cloud Controller database (CCDB), use the cf CLI.
To register an isolation segment in the CCDB:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf create-isolation-segment SEGMENT-NAME
```
Where `SEGMENT-NAME` is the name you give your isolation segment.

**Note** The isolation segment name used in the cf CLI command must match the value specified in the `placement_tags` section of the Diego manifest file. If the names do not match, Cloud Foundry fails to place apps in the isolation segment when apps are started or restarted in the space assigned to the isolation segment.
If successful, the command returns an `OK` message:
```
Creating isolation segment SEGMENT-NAME as admin...
OK
```

## Retrieve isolation segment information
The `cf isolation-segments`, `cf org`, and `cf space` commands retrieve information about isolation segments. The isolation segments you can see depends on your role:

* **Admins** see all isolation segments in the system.

* **Other users** only see the isolation segments that their orgs are entitled to.

### List isolation segments
To see a list of the isolation segments that are available to you:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf isolation-segments
```
The command returns results similar to this example output:
```
Getting isolation segments as admin...
OK
name orgs
SEGMENT-NAME org1, org2
```

### Display isolation segments enabled for an org
An admin can entitle an org to multiple isolation segments.
To view the isolation segments that are available to an org:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf org ORG-NAME
```
Where `ORG-NAME` is the name of your org.
The command returns results similar to this example output:
```
Getting info for org ORG-NAME as user@example.com...
name: ORG-NAME
domains: example.com, apps.example.com
quota: paid
spaces: development, production, sample-apps, staging
isolation segments: SEGMENT-NAME, OTHER-SEGMENT-NAME
```

### Showing the isolation segment assigned to a space
Only one isolation segment can be assigned to a space.
To view the isolation segment assigned to a space:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf space SPACE-NAME
```
Where `SPACE-NAME` is the name of the space to which your isolation segment is assigned.
The command returns results similar to this example output:
```
name: staging
org: ORG-NAME
apps:
services:
isolation segment: SEGMENT-NAME
space quota:
security groups: dns, p-mysql, p.mysql, public_networks, rabbitmq, ssh-logging
```

## Deleting an isolation segment
An isolation segment with deployed apps cannot be deleted.
Only admins can delete isolation segments.
To delete an isolation segment:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf delete-isolation-segment SEGMENT-NAME
```
Where `SEGMENT-NAME` is the name of the isolation segment you want to delete.
If successful, the command returns an `OK` message:
```
$ cf delete-isolation-segment SEGMENT-NAME
Deleting isolation segment SEGMENT-NAME as admin...
OK
```

## Managing isolation segment relationships
The commands listed in the following sections manage the relationships between isolation segments, orgs, and spaces.

### Enabling an org to use isolation segments
Only admins can enable orgs to use isolation segments.
To enable the use of an isolation segment:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf enable-org-isolation ORG-NAME SEGMENT-NAME
```
Where:

* `ORG-NAME` is the name of your org.

* `SEGMENT-NAME` is the name of the isolation segment you want your org to use.
If an org is entitled to use only one isolation segment, that isolation segment does not automatically become the default isolation segment for the org. You must explicitly set the default isolation segment of an org. For more information, see [Set the Default Isolation Segment for an Org](https://docs.cloudfoundry.org/adminguide/isolation-segments.html#set_org_default_is).

### Deactivating an org from using isolation segments
You cannot deactivate an org from using an isolation segment if a space within that org is assigned to the isolation
segment. Additionally, you cannot deactivate an org from using an isolation segment if the isolation segment is configured as the default for that org.
To deactivate an org from using an isolation segment:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf disable-org-isolation ORG-NAME SEGMENT-NAME
```
Where:

* `ORG-NAME` is the name of your org.

* `SEGMENT-NAME` is the name of the isolation segment you want to deactivate the org from using.
If successful, the command returns an `OK` message:
```
Removing entitlement to isolation segment SEGMENT-NAME from org org1 as admin...
OK
```

### Setting the default isolation segment for an org
This section requires cf CLI v6.29.0 or later. To download cf CLI v6.29.0 or later, go to
the [Releases](https://github.com/cloudfoundry/cli/releases/tag/v6.29.0) section of the Cloud Foundry CLI repository on GitHub.
Only admins and org managers can set the default isolation segment for an org.
When an org has a default isolation segment, apps in the spaces belong to the default isolation segment unless you assign them to another isolation segment. You must restart running apps to move them into the default isolation segment.
To set the default isolation segment for an org:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf set-org-default-isolation-segment ORG-NAME SEGMENT-NAME
```
Where:

* `ORG-NAME` is the name of your org.

* `SEGMENT-NAME` is the name of the isolation segment you want to set as your org’s default.
If successful, the command returns an `OK` message:
```
$ cf set-org-default-isolation-segment org1 SEGMENT-NAME
Setting isolation segment SEGMENT-NAME to default on org org1 as admin...
OK
```
To display the default isolation segment for an org:

1. Run:
```
cf org
```

### Assign an isolation segment to a space
Admins and org managers can assign an isolation segment to a space. Apps in that space start in the specified isolation segment.
To assign an isolation segment to a space, you must first activate the space’s org to use the isolation segment. For more information, see [Enable an Org to Use Isolation Segments](https://docs.cloudfoundry.org/adminguide/isolation-segments.html#enable_org_is).
To assign an isolation segment to a space:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf set-space-isolation-segment SPACE-NAME SEGMENT-NAME
```
Where:

* `SPACE-NAME` is the name of your space.

* `SEGMENT-NAME` is the name of the isolation segment you want to assign to your space.

### Resetting the isolation segment assignment for a space
Admins can reset the isolation segment assigned to a space to use the org’s default isolation segment.
To assign the default isolation segment for an org to a space:

1. Log in to your deployment by running:
```
cf login
```

2. Run:
```
cf reset-space-isolation-segment SPACE-NAME
```
Where `SPACE-NAME` is the name of the space to which you want to assign your org’s default isolation segment.