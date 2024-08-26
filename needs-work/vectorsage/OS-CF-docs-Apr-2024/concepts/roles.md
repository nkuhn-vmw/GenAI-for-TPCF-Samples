# Orgs, spaces, roles, and permissions in Cloud Foundry
This topic tells you about orgs and spaces in Cloud Foundry foundations. It also describes the default permissions for user roles in Cloud Foundry.
Cloud Foundry uses a role-based access control (RBAC) system to grant appropriate permissions to Cloud Foundry users.
Admins, Org Managers, and Space Managers can assign user roles using the Cloud Foundry Command Line Interface (cf CLI). For more information, see [Users and Roles](https://docs.cloudfoundry.org/cf-cli/getting-started.html#user-roles) in *Getting Started with the cf CLI*.

## Orgs
An org is a development account that an individual or multiple collaborators can own and use. All collaborators access an org with user accounts, which have roles such as Org Manager, Org Auditor, and Org Billing Manager. Collaborators in an org share a resource quota plan, apps, services availability, and custom domains.
By default, an org has the status of *active*. An admin can set the status of an org to *suspended* for various reasons such as failure to provide payment or misuse. When an org is suspended, users cannot perform certain activities within the org, such as push apps, modify spaces, or bind services.
For more information about the actions that each role can perform, see [User Roles](https://docs.cloudfoundry.org/concepts/roles.html#roles) and [User Role Permissions](https://docs.cloudfoundry.org/concepts/roles.html#permissions).
For details on what activities are allowed for suspended orgs, see [Roles and Permissions for Suspended Orgs](https://docs.cloudfoundry.org/concepts/roles.html#suspendedroles).

## Spaces
A space provides users with access to a shared location for app development, deployment, and maintenance. An org can contain multiple spaces. Every app, service, and route is scoped to a space. Roles provide access control for these resources and each space role applies only to a particular space.
Org managers can set quotas on the following for a space:

* Usage of paid services

* Number of app instances

* Number of service keys

* Number of routes

* Number of reserved route ports

* Memory used across the space

* Memory used by a single app instance

* Log volume per second used across the space

## User roles
A user account represents an individual person within the context of a Cloud Foundry foundation. A user can have one or more roles. These roles define the user’s permissions in orgs and spaces.
Roles can be assigned different scopes of User Account and Authentication (UAA) privileges. For more information about UAA scopes, see [Scopes](https://docs.cloudfoundry.org/concepts/architecture/uaa.html#scopes) in *User Account and Authentication (UAA) Server*.
The following describes each type of user role in Cloud Foundry:

* **Admin**: Perform operational actions on all orgs and spaces using the Cloud Controller API. Assigned the `cloud_controller.admin` scope in UAA.

* **Admin Read-Only**: Read-only access to all Cloud Controller API resources. Assigned the `cloud_controller.admin_read_only` scope in UAA.

* **Global Auditor**: Read-only access to all Cloud Controller API resources except for secrets, such as environment variables. The Global Auditor role cannot access those values. Assigned the `cloud_controller.global_auditor` scope in UAA.

* **Org Managers**: Administer the org.

* **Org Auditors**: Read-only access to user information and org quota usage
information.

* **Org Billing Managers**: Create and manage billing account and payment information.

**Note** The Billing Manager role is only relevant for Cloud Foundry environments deployed with a billing engine.

* **Org Users**: Read-only access to the list of other org users and their roles. In the v2 Cloud Controller API, when an Org Manager gives a person an Org or Space role, that person automatically receives Org User status in that org. This is no longer the case in the V3 Cloud Controller API.

* **Space Managers**: Manage a space within an org.

* **Space Developers**: Manage apps, services, and space-scoped service brokers in a space.

* **Space Auditors**: Read only access to a space.

* **Space Supporters**: Troubleshoot and debug apps and service bindings in a space.
The Space Supporter role is only available for the Cloud Controller V3 API. If a user with this role tries
to access a V2 endpoint, the API returns a 403.
For non-admin users, the `cloud_controller.read` scope is required to view resources, and the `cloud_controller.write` scope is required to create, update, and delete resources.
Before you assign a space role to a user, you must assign an org role to the user. The error message `Server error, error code: 1002, message: cannot set space role because user is not part of the org` occurs when you try to set a space role before setting an org role for the user.

## User role permissions
Each user role includes different permissions in a Cloud Foundry foundation. The following sections describe the permissions associated with each user role in both active and suspended orgs in Cloud Foundry.

### Roles and permissions for active orgs
The following table describes the default permissions for various Cloud Foundry roles in active orgs.
You can use feature flags to edit some of the default permissions in the following table.
For more information, see [Using Feature Flags](https://docs.cloudfoundry.org/adminguide/listing-feature-flags.html).
| Activity | Admin | Admin Read-Only | Global Auditor | Org Manager | Org Auditor | Org Billing Manager | Org User | Space Manager | Space Developer | Space Auditor | Space Supporter |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Scope of operation | Org | Org | Org | Org | Org | Org | Org | Space | Space | Space | Space |
| Assign user roles | Yes | | | Yes | | | | Yes | | | |
| View users and roles | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Create and assign org quota plans | Yes | | | | | | | | | | |
| View org quota plans | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Create orgs | Yes | | | **1** | **1** | **1** | **1** | **1** | **1** | **1** | **1** |
| View all orgs | Yes | Yes | Yes | | | | | | | | |
| View orgs where user is member | Yes**2** | Yes**2** | Yes**2** | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Edit, rename, and delete orgs | Yes | | | Yes**3** | | | | | | | |
| Suspend or activate an org | Yes | | | | | | | | | | |
| Create and assign space quota plans | Yes | | | Yes | | | | | | | |
| Create spaces | Yes | | | Yes | | | | | | | |
| View spaces | Yes | Yes | Yes | Yes | | | | Yes | Yes | Yes | Yes |
| Edit spaces | Yes | | | Yes | | | | Yes | | | |
| Delete spaces | Yes | | | Yes | | | | | | | |
| Rename spaces | Yes | | | Yes | | | | Yes | | | |
| View the status, number of instances, service bindings, and resource use of apps | Yes | Yes | Yes | Yes | | | | Yes | Yes | Yes | Yes |
| Add private domains**4** | Yes | | | Yes | | | | | | | |
| Share private domains with other orgs | Yes | | | Yes**5** | | | | | | | |
| Deploy, run, and manage apps | Yes | | | | | | | | Yes | | Limited**9** |
| View app logs | Yes | Yes | Yes | Yes | | | | Yes | Yes | Yes | Yes |
| Use app SSH**6** | Yes | | | | | | | | Yes | | |
| Instantiate services | Yes | | | | | | | | Yes | | |
| Bind services to apps | Yes | | | | | | | | Yes | | Yes |
| Manage global service brokers | Yes | | | | | | | | | | |
| Manage space-scoped service brokers | Yes | | | | | | | | Yes | | |
| Associate routes**4**, modify resource allocation of apps | Yes | | | | | | | | Yes | | Yes |
| Rename apps | Yes | | | | | | | | Yes | | |
| Create and manage Application Security Groups | Yes | | | | | | | | | | |
| Manage Application Security Groups for all spaces in an org | Yes | | | Yes | | | | | | | |
| Manage Application Security Groups for an individual space | Yes | | | | | | | Yes | | | |
| Create, update, and delete an isolation segment | Yes | | | | | | | | | | |
| List all isolation segments for an org | Yes | Yes | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** |
| Entitle or revoke an isolation segment | Yes | | | | | | | | | | |
| List all orgs entitled to an isolation segment | Yes | Yes | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** | Yes**7** |
| Assign a default isolation segment to an org | Yes | | | Yes | | | | | | | |
| List and manage isolation segments for spaces | Yes | | | Yes | | | | | | | |
| List entitled isolation segments for a space | Yes | Yes | Yes | Yes | | | | Yes | Yes | Yes | Yes |
| List the isolation segment on which an app runs | Yes | Yes | Yes | Yes | | | | Yes | Yes | Yes | Yes |
| List app and service usage events | Yes | Yes | Yes | | | | | | Yes | Yes | Yes |
| Create, delete, and list container-to-container networking policies | Yes | | | | | | | | Yes**8** | | |

**1**Not by default, unless feature flag `user_org_creation` is set to `true`.

**2**Admin, admin read-only, and global auditor roles do not need to be added as members of orgs or spaces to view resources.

**3**Org Managers can rename their orgs and edit some fields. They cannot delete orgs.

**4**Unless deactivated by feature flags.

**5**The user attempting to share must have permissions in both the source and target orgs.

**6**This assumes that SSH is enabled for the platform, space, and app. For more information, see [SSH Access Control Hierarchy](https://docs.cloudfoundry.org/devguide/deploy-apps/app-ssh-overview.html#ssh-access-control-hierarchy) in *App SSH Overview*.

**7**Applies only to orgs they belong to.

**8**Space Developers can optionally be granted these permissions. For more information, see [Grant Permissions](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html#-grant-permissions) in *Configuring Container-to-Container Networking*.

**9**Cannot create packages or delete resources. For more information, see the [Cloud Controller V3 Documentation](https://v3-apidocs.cloudfoundry.org/).

### Roles and permissions for suspended orgs
The following table describes roles and permissions applied after an operator sets the status of an org to *suspended*.
| User Role | Admin | Admin Read-Only | Global Auditor | Org Manager | Org Auditor | Org Billing Manager | Org User | Space Manager | Space Developer | Space Auditor |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Scope of operation | Org | Org | Org | Org | Org | Org | Org | Space | Space | Space |
| Assign user roles | Yes | | | | | | | | | |
| View users and roles | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Create and assign org quota plans | Yes | | | | | | | | | |
| View org quota plans | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Create orgs | Yes | | | | | | | | | |
| View all orgs | Yes | Yes | Yes | | | | | | | |
| View orgs where user is a member | Yes\*\* | Yes\*\* | Yes\*\* | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Edit, rename, and delete orgs | Yes | | | | | | | | | |
| Suspend or activate an org | Yes | | | | | | | | | |
| Create and assign space quota plans | Yes | | | | | | | | | |
| Create spaces | Yes | | | | | | | | | |
| View spaces | Yes | Yes | Yes | Yes | | | | Yes | Yes | Yes |
| Edit spaces | Yes | | | | | | | | | |
| Delete spaces | Yes | | | | | | | | | |
| Rename spaces | Yes | | | | | | | | | |
| View the status, number of instances, service bindings, and resource use of apps | Yes | Yes | Yes | Yes | | | | Yes | Yes | Yes |
| Add private domains† | Yes | | | | | | | | | |
| Deploy, run, and manage apps | Yes | | | | | | | | | |
| Instantiate and bind services to apps | Yes | | | | | | | | | |
| Associate routes†, modify resource allocation of apps | Yes | | | | | | | | | |
| Rename apps | Yes | | | | | | | | | |
| Create and manage Application Security Groups | Yes | | | | | | | | | |
†Unless disabled by feature flags.
\*\*Admin, admin read-only, and global auditor roles do not need to be added as members of orgs or spaces to view resources.