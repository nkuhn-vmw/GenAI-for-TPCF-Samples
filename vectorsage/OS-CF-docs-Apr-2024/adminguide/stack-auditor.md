# Using Stack Auditor in Cloud Foundry
Stack Auditor is a cf CLI plug-in that allows you to list apps and their stacks, migrate apps to a new stack, and delete a stack. Learn how to use it on this page.
A typical use for Stack Auditor is migrating a large number of apps to a new stack.
This includes moving apps from `cflinuxfs3` to `cflinuxfs4` in preparation to upgrade your deployment
to a version that does not contain `cflinuxfs3`.
The following table describes the workflow you can use:
| Stage | Description |
| --- | --- |
| 1 | Operator audits stack usage to determine which apps need to be migrated. See [List Apps and Their Stacks](https://docs.cloudfoundry.org/adminguide/stack-auditor.html#list-stacks). |
| 2 | Operator communicates with developers that they must migrate their existing apps to a new stack and begin pushing all new apps to the new stack. |
| 3 | Developers migrate their apps to the new stack. See [Change Stacks](https://docs.cloudfoundry.org/adminguide/stack-auditor.html#change-stacks). |
| 4 | Operator confirms apps have been migrated. |
| 5 | Operator deletes buildpacks associated with the old stack. |
| 6 | Operator deletes the old stack. See [Delete a Stack](https://docs.cloudfoundry.org/adminguide/stack-auditor.html#delete-stacks).
If you upgrade your deployment to a version that contains the stack you deleted, the stack returns on upgrade. |
| 7 | If applicable, operator upgrades the deployment to the version that does not contain the old stack. |

## Install Stack Auditor
To install Stack Auditor:

1. Download the Stack Auditor binary for your OS from [Releases](https://github.com/cloudfoundry/stack-auditor/releases) in the Stack Auditor repository on GitHub.

2. Install the plug-in with the cf CLI:
```
cf install-plugin PATH-TO-BINARY
```

## Using Stack Auditor
The following sections describe how to use Stack Auditor.

### List apps and their stacks
With Stack Auditor, you can get a list of the apps in each org and space and see what stack they are using.
To see which apps are using which stack, run the following command. The output lists apps for each org you have access to. To see all the apps in your deployment, be sure to log in to the cf CLI as a user who can access all orgs.
```
cf audit-stack
```
Here is example output:
```
$ cf audit-stack
first-org/development/first-app cflinuxfs3
first-org/staging/first-app cflinuxfs3
first-org/production/first-app cflinuxfs3
second-org/development/second-app cflinuxfs4
second-org/staging/second-app cflinuxfs4
second-org/production/second-app cflinuxfs4
...
```

### Change stacks for a single app
Stack Auditor allows you to change the stack that an app uses. Stack Auditor rebuilds the app onto the new stack without a change in the source code of the app. If you want to move the app to a new stack with updated source code, follow the procedure in [Changing Stacks](https://docs.cloudfoundry.org/devguide/deploy-apps/stacks.html).
To change the stack an app uses:

1. Target the org and space of the app:
```
cf target -o ORG -s SPACE
```
Where:

* `ORG` is the org the app is in.

* `SPACE` is the space the app is in.

2. Run the following command:
```
cf change-stack APP-NAME STACK-NAME
```
Where:

* `APP-NAME` is the app that you want to move to a new stack.

* `STACK-NAME` is the stack you want to move the app to.Here is example output:
```
$ cf change-stack my-app cflinuxfs4
Attempting to change stack to cflinuxfs4 for my-app...
Starting app my-app in org pivotal-pubtools / space pivotalcf-staging as ljarzynski@pivotal.io...
Downloading staticfile_buildpack...
. . .
requested state: started
instances: 1/1
usage: 64M x 1 instance
urls: example.com
last uploaded: Thu Mar 28 17:44:46 UTC 2019
stack: cflinuxfs4
buildpack: staticfile_buildpack
state since cpu memory disk details

#0 running 2019-04-02 03:18:57 PM 0.0% 8.2M of 64M 6.9M of 1G
Application my-app was successfully changed to Stack cflinuxfs4
```

**Important**
If the app is in a `stopped` state, it remains stopped after changing stacks. Also, when attempting to change stacks, your app is stopped. If the app fails on `cflinuxfs4`, Stack Auditor attempts to restage your app on `cflinuxfs3`.

### Change stacks for all apps in a space
Stack Auditor also allows you to migrate all apps in a space to a new stack. For example, using jq you can write a script to find all apps in a space and migrate them to cflinuxfs4:
```
cf audit-stack --json | jq -r 'map(select(.stack == "cflinuxfs3")) | .[] |"cf target -o \(.org) -s \(.space) && cf change-stack \(.name) cflinuxfs4"' | xargs -i{} bash -c {}
```

### Delete a stack
Stack Auditor allows you to delete a stack from your deployment. You must be an admin user to delete a stack.

1. To delete a stack, run the following command. This action cannot be undone, with the following exception: If you upgrade your deployment to a version that contains the stack you deleted, the stack returns on upgrade.
```
cf delete-stack STACK-NAME
```
Where `STACK-NAME` is the name of the stack you want to delete.
Here is example output:
```
<pre class="terminal">
$ cf delete-stack cflinuxfs3
Are you sure you want to remove the cflinuxfs3 stack? If so, type the name of the stack [cflinuxfs3]
>cflinuxfs3
Deleting stack cflinuxfs3...
Stack cflinuxfs3 has been deleted.
</pre>
If you have any apps still running on `cflinuxfs3`, the command returns the following error:
<pre class="terminal">
Failed to delete stack cflinuxfs3 with error: Please delete the app associations for your stack.
</pre>
```

### Contacting users of apps
If you are having problems with an app and need help, you can use the cf CLI to get a list of email addresses of users in a space. For example, run:
```
cf space-users ORG-NAME SPACE-NAME
```
Where:

* `ORG-NAME` is the org the app is in.

* `SPACE-NAME` is the space the app is in.

## Known issues
The following are known issues with changing stacks from cflinuxfs3 to cflinuxfs4.

### OpenSSL1.1 is not included in cflinuxfs4
cflinuxfs4 does not include OpenSSL1.1. If your application depends on OpenSSL1.1, for example, a static file buildpack containing an executable but using the system libraries for SSL, it will fail to run. Ensure that your application can be rebuilt against OpenSSL3 or include the OpenSSL1.1 libraries with your application.

### .NET 6 and GSS requires legacy provider
If your application is .NET 6 and uses GSS, you may see the following error message:
```
GSSAPI operation failed with error - Unspecified GSS failure. Minor code may provide more information (Crypto routine failure).
```
There is an existing .NET issue about this failure, which is related to legacy usage of OpenSSL3. For more information, see [GSS failures in System.Net.Http.Functional.Tests on Ubuntu 22.04re](https://github.com/dotnet/runtime/issues/67353) on GitHub. The workaround is listed [on the same page](https://github.com/dotnet/runtime/issues/67353#issuecomment-1085003764) and involves explicitly loading the legacy provider.

### .NET Core apps and LDAP
If your application is .NET Core and using LDAP connectivity, you may see the following error message if you are using cflinuxfs4 prior to v1.45.0:
```
"ThreadName": ".NET ThreadPool Worker", "Message": "#414 Failed to establish connection to domain: [{\"Domain\":\"myldap-domain.com\",\"Host\":\"dc=emea,dc=org,dc=com\",\"Base\":\"emea\",\"Name\":\"EUROPE\"}] exception: The type initializer for 'Ldap' threw an exception.", "Description": "#414 Failed to establish connection to domain: [{\"Domain\":\"myldap-domain.com\",\"Host\":\"dc=emea,dc=org,dc=com\",\"Base\":\"emea\",\"Name\":\"EUROPE\"}] exception: The type initializer for 'Ldap' threw an exception.", "Environment": "ge4-sit", "Exception": " ", "RequestHandler": "Controller: Action:", "CallStack": "Org.DSA.Shared.Logger.ApiLogger.Log" }
```
The issue is related to a stack-level LDAP package that wasn’t available in cflinuxfs4 until v1.45.0 and its interaction with the `System.DirectoryServices.Protocols` package.
To resolve the problem:
\* Upgrade the cflinuxfs4 stack.
\* Upgrade the `System.DirectoryServices` NuGet package to version 8.0.0 or higher. You can do this in the application using the following command:
```
<pre class="terminal">
<PackageReference Include="System.DirectoryServices.Protocols" Version="8.0.0" />
</pre>
```

### Ruby 3.1 or later is required
Ruby 3.1, introduced in Ruby buildpack v1.8.51, or later is required for the Ruby buildpack running on cflinuxfs4. Upgrade your application to work with Ruby 3.1 or later by specifying it in your application’s Gemfile and working through any issues that result. If an application specifies a version of Ruby in its Gemfile not included in the buildpack, it results in the following error message:
```

**ERROR** Unable to determine ruby: Unable to determine ruby version: Running ruby: No Matching versions, ruby = 2.7.6 not found in this buildpack ·······
Failed to compile droplet: Failed to run all supply scripts: exit status 15
```
This happens because Ruby v2.7 and v3.0 are incompatible with OpenSSL3, which is the version of OpenSSL in cflinuxfs4.