# Creating and managing users with the UAA CLI (UAAC)
Using the Cloud Foundry User Account and Authentication Command Line Interface (UAAC), you can create
users in the UAA server.
The UAAC only creates users in UAA, and does not assign roles in the Cloud Controller database
(CCDB). In general, admins create users using the Cloud Foundry Command Line Interface (cf CLI). The cf CLI both creates user records in
the UAA and associates them with org and space roles in the CCDB. Before admins can assign roles to the
user, the user must log in through Apps Manager or the cf CLI for the user record to populate the CCDB.
For more information on creating and managing users, see [Creating and Managing Users with the cf CLI](https://docs.cloudfoundry.org/adminguide/cli-user-management.html).
For more information, see [UAA Overview](https://docs.cloudfoundry.org/concepts/architecture/uaa.html), [UAA Sysadmin Guide](https://github.com/cloudfoundry/uaa/blob/master/docs/Sysadmin-Guide.rst) in the UAA repository on GitHub, and [Docs](https://github.com/cloudfoundry/uaa/tree/master/docs) in the UAA repository on GitHub.

**Important**
UAAC requires Ruby v2.3.1 or later. If you have an earlier version of Ruby installed, install
Ruby v2.3.1 or later before using the UAAC.
For more information about which roles can perform various operations in Cloud Foundry, see [User roles](https://docs.cloudfoundry.org/concepts/roles.html#roles) in *Orgs, Spaces, Roles, and Permissions*.

## Create an admin user
To create an admin user for UAA:

1. Install the UAAC by running:
```
gem install cf-uaac
```

2. Target your UAA server by running:
```
uaac target uaa.UAA-DOMAIN
```
Where `UAA-DOMAIN` is the domain of your UAA server.

3. Record the `uaa:admin:client_secret` from your deployment manifest.

4. Authenticate and obtain an access token for the admin client from the UAA server by running:
```
uaac token client get admin -s ADMIN-CLIENT-SECRET
```
Where `ADMIN-CLIENT-SECRET` is the admin secret you recorded in the previous step.
UAAC stores the token in `~/.uaac.yml`.

5. Display the users and apps authorized by the UAA server, as well as the permissions granted to each user and app, by running:
```
uaac contexts
```

6. In the output from `uaac contexts`, check the `scope` section of the `client_id: admin` user for `scim.write`. The value `scim.write` represents sufficient permissions to create accounts.

7. If the admin user lacks permissions to create accounts, add the permissions:

1. Add the necessary permissions to the admin user account on the UAA server by running:
```
uaac client update admin --authorities "EXISTING-PERMISSIONS scim.write"
```
Where `EXISTING-PERMISSIONS` is the current contents of the `scope` section from the output from `uaac contexts`.

2. Delete the local token by running:
```
uaac token delete
```

3. Obtain an updated access token from the UAA server by running:
```
uaac token client get admin
```

8. Create an admin user by running:
```
uaac user add NEW-ADMIN-USERNAME -p NEW-ADMIN-PASSWORD --emails NEW-ADMIN-EMAIL
```
Where:

* `NEW-ADMIN-USERNAME` is the username you want to give the admin user.

* `NEW-ADMIN-PASSWORD` is the password you want to give the admin user.

* `NEW-ADMIN-EMAIL` is the email address of the admin user.

9. Add the new admin user to the groups `cloud_controller.admin`, `uaa.admin`, `scim.read`, and `scim.write` by running:
```
uaac member add GROUP NEW-ADMIN-USERNAME
```
Where:

* `GROUP` is the name of the group to which you want to add the new admin user.

* `NEW-ADMIN-USERNAME`is the username of the new admin user.

### Create an admin read-only user
The admin read-only account can view but not modify almost all Cloud Controller API resources. The admin read-only account cannot view process `stats` or `logs`.
To create an admin read-only user account:

1. Obtain the credentials of the admin client you created in [Create an Admin User](https://docs.cloudfoundry.org/uaa/uaa-user-management.html#creating-admin-users), or see the `uaa: scim` section of your deployment manifest for the user name and password of an admin user.

2. Authenticate and obtain an access token for the admin client from the UAA server by running:
```
uaac token client get admin -s ADMIN-CLIENT-SECRET
```
Where `ADMIN-CLIENT-SECRET` is the admin secret you recorded in the previous step.
UAAC stores the token in `~/.uaac.yml`.

3. Create an admin read-only user by running:
```
uaac user add NEW-ADMIN-RO-USERNAME -p NEW-ADMIN-RO-PASSWORD --emails NEW-ADMIN-RO-EMAIL
```
Where:

* `NEW-ADMIN-RO-USERNAME` is the username you want to give the admin read-only user.

* `NEW-ADMIN-RO-PASSWORD` is the password you want to give the admin read-only user.

* `NEW-ADMIN-RO-EMAIL` is the email address of the admin read-only user.

4. Add the new admin user to the groups `cloud_controller.admin_read_only` and `scim.read` by running:
```
uaac member add GROUP NEW-ADMIN-RO-USERNAME
```
Where:

* `GROUP` is the name of the group to which you want to add the new admin read-only user.

* `NEW-ADMIN-RO-USERNAME`is the username of the new admin read-only user.

### Create a global auditor
The global auditor account has read-only access to almost all Cloud Controller API resources but cannot access secret data such as environment variables. The global auditor account cannot view process `stats` or `logs`.
To create a global auditor account:

1. Obtain the credentials of the admin client you created in [Create an admin user](https://docs.cloudfoundry.org/uaa/uaa-user-management.html#creating-admin-users), or see the `uaa: scim` section of your deployment manifest for the user name and password of an admin user.

2. Authenticate and obtain an access token for the admin client from the UAA server by running:
```
uaac token client get admin -s ADMIN-CLIENT-SECRET
```
Where `ADMIN-CLIENT-SECRET` is the admin secret you recorded in the previous step.
UAAC stores the token in `~/.uaac.yml`.

3. Create a global auditor user by running:
```
uaac user add NEW-GLOBAL-AUDITOR-USERNAME -p NEW-GLOBAL-AUDITOR-PASSWORD --emails NEW-GLOBAL-AUDITOR-EMAIL
```
Where:

* `NEW-GLOBAL-AUDITOR-USERNAME` is the username you want to give the admin read-only user.

* `NEW-GLOBAL-AUDITOR-PASSWORD` is the password you want to give the admin read-only user.

* `NEW-GLOBAL-AUDITOR-EMAIL` is the email address of the admin read-only user.

4. To ensure that the `cloud_controller.global_auditor` group exists, run:
```
uaac group add cloud_controller.global_auditor
```

5. Add the new global auditor user to the `cloud_controller.global_auditor` group by running:
```
uaac member add GROUP NEW-GLOBAL-AUDITOR-USERNAME
```
Where:

* `GROUP` is the name of the group to which you want to add the new global auditor user.

* `NEW-GLOBAL-AUDITOR-USERNAME` is the username of the new global auditor user.

## Grant admin permissions to an external group (SAML, LDAP, or OIDC)
To grant all users under an external group admin permissions:

1. Obtain the credentials of the admin client you created in [Create an Admin User](https://docs.cloudfoundry.org/uaa/uaa-user-management.html#creating-admin-users), or see the `uaa: scim` section of your deployment manifest for the user name and password of an admin user.

2. Authenticate and obtain an access token for the admin client from the UAA server by running:
```
uaac token client get admin -s ADMIN-CLIENT-SECRET
```
Where `ADMIN-CLIENT-SECRET` is the admin secret you recorded in the previous step.
UAAC stores the token in `~/.uaac.yml`.

3. Follow the procedure that corresponds to your use case:

* [Grant Admin Permissions for LDAP](https://docs.cloudfoundry.org/uaa/uaa-user-management.html#grant-admin-ldap)

* [Grant Admin Permissions for SAML and OIDC](https://docs.cloudfoundry.org/uaa/uaa-user-management.html#grant-admin-saml)
The UAA does not grant scopes for users in external groups until the next time the user logs in. This means that users granted
scopes from external group mappings must log out from Cloud Foundry and log back in before their new scope takes effect.

### Grant admin permissions for LDAP
To grant admin permissions to all users under the mapped LDAP group:

1. Run:
```
uaac group map --name scim.read "GROUP-DISTINGUISHED-NAME"
```
Where `GROUP-DISTINGUISHED-NAME` is the name of the LDAP group.

2. Run:
```
uaac group map --name scim.write "GROUP-DISTINGUISHED-NAME"
```
Where `GROUP-DISTINGUISHED-NAME` is the name of the LDAP group.

3. Run:
```
uaac group map --name cloud_controller.admin "GROUP-DISTINGUISHED-NAME"
```
Where `GROUP-DISTINGUISHED-NAME` is the name of the LDAP group.

### Grant admin permissions for SAML and OIDC
To grant admin permissions to all users under the mapped SAML or OIDC group:

1. Retrieve the name of your SAML provider by opening your Cloud Foundry manifest and recording the value of the `login.saml.providers.provider-name` property.

2. Grant all users under the mapped SAML or OIDC group admin permissions by running:
```
uaac group map --name scim.read "GROUP-NAME" --origin PROVIDER-NAME
uaac group map --name scim.write "GROUP-NAME" --origin PROVIDER-NAME
uaac group map --name cloud_controller.admin "GROUP-NAME" --origin PROVIDER-NAME
```
Where:

* `GROUP-NAME` is the name of the SAML or OIDC group.

* `PROVIDER-NAME` is the name of your SAML or OIDC IDP.
For OIDC, make sure you configure the IDP’s attribute mappings and map `external_groups` to the groups field in the
OIDC ID Token issued by the IDP.

## Create users
To create new users:

1. Obtain the credentials of the admin client you created in [Create an Admin User](https://docs.cloudfoundry.org/uaa/uaa-user-management.html#creating-admin-users), or see the `uaa: scim` section of your deployment manifest for the username and password of an admin user.

2. Log in to your UAA API by running:
```
cf login -u ADMIN-USERNAME -p ADMIN-PASSWORD
```
Where:

* `ADMIN-USERNAME` is the username of the admin user.

* `ADMIN-PASSWORD` is the password of the admin user.

3. Create a new user by running:
```
cf create-user NEW-USERNAME NEW-USER-PASSWORD
```
Where:

* `NEW-USERNAME` is the username you give the new user.

* `NEW-USER-PASSWORD` is the password you give the new user.
As of cf CLI v7, you can use the `--password-prompt` option to prompt for the password. This enhances security by removing the requirement to type the password on the command line.

## Change passwords
To change the password of a user:

1. Obtain the credentials of the admin client you created in [Create an Admin User](https://docs.cloudfoundry.org/uaa/uaa-user-management.html#creating-admin-users), or see the `uaa: scim` section of your deployment manifest for the user name and password of an admin user.

2. Authenticate and obtain an access token for the admin client from the UAA server by running:
```
uaac token client get admin -s ADMIN-CLIENT-SECRET
```
Where `ADMIN-CLIENT-SECRET` is the admin secret you recorded in the previous step.
UAAC stores the token in `~/.uaac.yml`.

3. Display the users and apps authorized by the UAA server, as well as the permissions granted to each user and app, by running:
```
uaac contexts
```

4. In the output from `uaac contexts`, check the `scope` section of the `client_id: admin` user for `password.write`. The value `password.write` represents sufficient permissions to change passwords.

5. If the admin user lacks permissions to change passwords, add the permissions:

1. Add the necessary permissions to the admin user account on the UAA server by running:
```
uaac client update admin --authorities "EXISTING-PERMISSIONS password.write"
```
Where `EXISTING-PERMISSIONS` is the current contents of the `scope` section from the output from `uaac contexts`.

2. Delete the local token by running:
```
uaac token delete
```

3. Obtain an updated access token from the UAA server by running:
```
uaac token client get admin
```

6. Change an existing user password to a temporary password by running:
```
uaac password set USERNAME -p TEMP-PASSWORD
```
Where:

* `USERNAME` is the username of the user whose password you want to change.

* `TEMP-PASSWORD` is the temporary password you set.

7. Provide the temporary password to the user and instruct the user to run:
```
cf target api.UAA-DOMAIN
cf login -u USERNAME -p TEMP-PASSWORD
cf passwd
```
Where:

* `UAA-DOMAIN` is the domain of your UAA server.

* `USERNAME` is the username of the user.

* `TEMP-PASSWORD` is the temporary password you provided the user.

## Retrieve user email addresses
Some Cloud Foundry components, like Cloud Controller, only use GUIDs for user identification. You can use UAA to retrieve the emails of your Cloud Foundry instance users either as a list or, for a specific user, with that user’s GUID.

1. Target your UAA server by running:
```
uaac target uaa.UAA-DOMAIN
```
Where `UAA-DOMAIN` is the domain of your UAA server.

2. Record the `uaa:admin:client_secret` from your deployment manifest.

3. Authenticate and obtain an access token for the admin client from the UAA server by running:
```
uaac token client get admin -s ADMIN-CLIENT-SECRET
```
Where `ADMIN-CLIENT-SECRET` is the admin secret you recorded in the previous step.
UAAC stores the token in `~/.uaac.yml`.

4. Display the users and apps authorized by the UAA server, as well as the permissions granted to each user and app, by running:
```
uaac contexts
```

5. In the output from `uaac contexts`, check the `scope` section of the `client_id: admin` user for `scim.write`. The value `scim.write` represents sufficient permissions to query the UAA server for user information.

6. If the admin user lacks permissions to change passwords, add the permissions:

1. Add the necessary permissions to the admin user account on the UAA server by running:
```
uaac client update admin --authorities "EXISTING-PERMISSIONS scim.write"
```
Where `EXISTING-PERMISSIONS` is the current contents of the `scope` section from the output from `uaac contexts`.

2. Delete the local token by running:
```
uaac token delete
```

3. Obtain an updated access token from the UAA server by running:
```
uaac token client get admin
```

7. To list your Cloud Foundry instance users, run:
```
uaac users
```
By default, the `uaac users` command returns information about each user account, including GUID, name, permission groups, activity status, and metadata. To limit the output of `uaac users` to email addresses, run:
```
uaac users --attributes emails
```

8. To retrieve a specific user’s email address, run:
```
uaac users "id eq GUID" --attributes emails
```
Where `GUID` is the GUID of a specific user.