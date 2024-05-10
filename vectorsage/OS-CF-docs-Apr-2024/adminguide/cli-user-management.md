# Creating and managing users with the cf CLI
You can manage users with the cf CLI. Learn how to view users by role, assign roles, and remove roles from a user.
Cloud Foundry uses role-based access control, with each role granting
permissions in either an organization or an application space.
For more information, see [Organizations, spaces, roles, and permissions](https://docs.cloudfoundry.org/concepts/roles.html).

## About roles
To manage all users, organizations, and roles with the Cloud Foundry Command Line Interface (cf CLI), log in with your
admin credentials. In your Cloud Foundry deployment manifest, see the `uaa scim` section for the admin name and password.
If the feature flag `set_roles_by_username` is activated, Org Managers can [assign org roles](https://docs.cloudfoundry.org/adminguide/cli-user-management.html#org-roles) to existing users in their org and Space Managers can [assign space roles](https://docs.cloudfoundry.org/adminguide/cli-user-management.html#space-roles) to existing users in their space. For more information about using feature flags, see the [Feature Flags](https://docs.cloudfoundry.org/adminguide/listing-feature-flags.html) topic.

## Creating and deleting users
docs-dev-guide
| **FUNCTION** | **COMMAND** | **EXAMPLE** |
| --- | --- | --- |
| Create a new user | cf create-user USERNAME PASSWORD | `cf create-user Alice pa55w0rd` |
| Create a new user, and prompt for password for better security | cf create-user USERNAME –password-prompt | `cf create-user Alice` |
| Create a new user, specifying LDAP as an external identity provider | cf create-user USERNAME –origin ORIGIN | `cf create-user Aayah ldap` |
Create a new user, specifying SAML or OpenID Connect as an external identity provider |
cf create-user USERNAME –origin ORIGIN |
`cf create-user Aiko provider-alias` |
| Delete a user | cf delete-user USERNAME | `cf delete-user Alice` |

### Creating administrator accounts
To create a new administrator account, use the [UAA CLI](https://docs.cloudfoundry.org/uaa/uaa-user-management.html#creating-admin-users).

**Note**
The cf CLI cannot create new administrator accounts.

## Org and app space roles
You can have one or more roles.
The combination of these roles defines your overall permissions in the org
and within specific app spaces in that org.

### Org roles
Valid [org roles](https://docs.cloudfoundry.org/concepts/roles.html#roles) are OrgManager, BillingManager, and OrgAuditor.
| **FUNCTION** | **COMMAND** | **EXAMPLE** |
| --- | --- | --- |
| View the organizations belonging to an account. | cf orgs | `cf orgs` |
| View all users in an organization by role. | cf org-users ORGANIZATION-NAME | `cf org-users my-example-org` |
| Assign an org role to a user. | cf set-org-role USERNAME ORGANIZATION-NAME ROLE | `cf set-org-role Alice my-example-org OrgManager` |
| Remove an org role from a user. | cf unset-org-role USERNAME ORGANIZATION-NAME ROLE | `cf unset-org-role Alice my-example-org OrgManager` |
If multiple accounts share a username, `set-org-role` and `unset-org-role` return an error. See
[Identical Usernames in Multiple Origins](https://docs.cloudfoundry.org/cf-cli/getting-started.html#multi-origin) for details.

### App space roles
Each app space role applies to a specific app space.
Valid [app space roles](https://docs.cloudfoundry.org/concepts/roles.html#roles) are SpaceManager, SpaceDeveloper, and SpaceAuditor.
| **FUNCTION** | **COMMAND** | **EXAMPLE** |
| --- | --- | --- |
| View the spaces in an org. | cf spaces | `cf spaces` |
| View all users in a space by role. | cf space-users ORGANIZATION-NAME SPACE-NAME | `cf space-users my-example-org development` |
| Assign a space role to a user. | cf set-space-role USERNAME ORGANIZATION-NAME SPACE-NAME ROLE | `cf set-space-role Alice my-example-org development SpaceAuditor` |
| Remove a space role from a user. | cf unset-space-role USERNAME ORGANIZATION-NAME SPACE-NAME ROLE | `cf unset-space-role Alice my-example-org development SpaceAuditor` |
If multiple accounts share a username, `set-space-role` and `unset-space-role` return an error. See
[Identical Usernames in Multiple Origins](https://docs.cloudfoundry.org/cf-cli/getting-started.html#multi-origin) for details.