# Getting started with the cf CLI
The cf CLI is the official command line client for Cloud Foundry. You can use the cf CLI to manage apps, service instances, orgs, spaces, and users in your environment.

## Prerequisite
To follow the procedures in this topic, you must download and install the latest version of the cf CLI v7 or v8. For more information, see [Installing the Cloud Foundry command line interface](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html).

## Log in with the CLI
The `cf login` command uses the syntax described below to specify a target API endpoint, login credentials, an org, and a space.
The cf CLI prompts for credentials as needed. If you are a member of multiple orgs or spaces, `cf login` prompts you to specify the org or space to which you
want to log in. Otherwise, it targets your org and space automatically.
To log in to the cf CLI:

1. In a terminal window, run:
```
cf login -a API-URL -u USERNAME -p PASSWORD -o ORG -s SPACE
```
Where:

* `API-URL` is your API endpoint, [the URL of the Cloud Controller in your Cloud Foundry instance](http://docs.cloudfoundry.org/running/cf-api-endpoint.html).

* `USERNAME` is your username.

* `PASSWORD` is your password. Cloud Foundry discourages using the `-p` option, because it records your password in your shell history.

* `ORG` is the org where you want to deploy your apps.

* `SPACE` is the space in the org where you want to deploy your apps.
When you successfully log in, you see output similar to the following example:
```
API endpoint: https://api.example.com
Password>
Authenticating...
OK
Targeted org example-org
Targeted space development
API endpoint: https://api.example.com
User: username@example.com
Org: example-org
Space: development
```
Alternatively, you can write a script to log in and set your target using the non-interactive [cf api](http://cli.cloudfoundry.org/en-US/cf/api.html), [cf auth](http://cli.cloudfoundry.org/en-US/cf/auth.html), and [cf target](http://cli.cloudfoundry.org/en-US/cf/target.html) commands. See [UAAC](https://github.com/cloudfoundry/cf-uaac/blob/master/README.md) for setting up `client_id` and `client_secret`.

## Log in with the API
You can write a script to log in to the cf CLI. This allows you to avoid manually logging in to the cf CLI each time you use it.
To write a script to log in:

1. In a terminal window, target your API by running:
```
cf api API-URL
```
Where `API-URL` is your API endpoint, [the URL of the Cloud Controller in your Cloud Foundry instance](http://docs.cloudfoundry.org/running/cf-api-endpoint.html).
For more information about the `cf api` command, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/api.html).

2. Authenticate by running:
```
cf auth USERNAME PASSWORD
```
Where:

* `USERNAME` is your username.

* `PASSWORD` is your password. Cloud Foundry discourages using the `-p` option, because it records your password in your shell history.
For more information about the `cf auth` command, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/auth.html).

3. Target your org or space by running:
```
cf target -o ORG -s SPACE
```
Where:

* `ORG` is the org you want to target.

* `SPACE` is the space you want to target.
For more information about the `cf target` command, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/target.html).
After you log in, the cf CLI saves a `config.json` file that contains your API endpoint, org, space values, and access token. If you change these settings,
the `config.json` file is updated accordingly.
By default, `config.json` is located in the `~/.cf` directory. You can relocate the `config.json` file using the `CF_HOME` environment variable.

## Localize the cf CLI
The cf CLI translates terminal output into the language that you select. The default language is `en-US`.
The cf CLI supports these languages:

* Chinese (simplified): `zh-Hans`

* Chinese (traditional): `zh-Hant`

* English: `en-US`

* French: `fr-FR`

* German: `de-DE`

* Italian: `it-IT`

* Japanese: `ja-JP`

* Korean: `ko-KR`

* Portuguese (Brazil): `pt-BR`

* Spanish: `es-ES`
For more information about the `cf config --locale` command, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/config.html).
Localizing the cf CLI affects only messages that the cf CLI generates.
To set the language of the cf CLI:

1. In a terminal window, log in to the cf CLI:
```
cf login
```

2. Run:
```
cf config --locale LANGUAGE
```
Where `LANGUAGE` is code of the language you want to set. Valid values are `zh-Hans`, `zh-Hant`, `en-US`, `fr-FR`, `de-DE`, `it-IT`, `ja-JP`, `ko-KR`,
`pt-BR`, and `es-ES`.

3. Confirm the language change by running:
```
cf help
```
The above command returns output similar to the example below:
```
NOME:
cf - Uma ferramenta de linha de comando para interagir com Cloud Foundry
```
USO:
cf [opções globais] comando [argumentos...] [opções de comando]
VERSÃO:

6.14.1
...

## Manage users and roles
The cf CLI includes commands that list users and assign roles in orgs and spaces.

### List users
To list all users in an org or a space:

1. In a terminal window, log in to the cf CLI:
```
cf login
```

2. Run one of these commands:

* To list org users, run:
```
cf org-users ORG
```
Where `ORG` is the name of the org for which you want to see the list of users.
The above command returns output similar to the example below:
```
Getting users in org example-org as username@example.com...
```
ORG MANAGER
username@example.com
BILLING MANAGER
huey@example.com
dewey@example.com
ORG AUDITOR
louie@example.com

* To list space users, run:
```
cf space-users ORG SPACE
```
Where:

+ `ORG` is the name of the org that contains the space for which you want to see the list of users.

+ `SPACE` is the name of the space for which you want to see the list of users.
The above command returns output similar to the example below:
```
Getting users in org example-org / space example-space as username@example.com...
```
SPACE MANAGER
username@example.com
SPACE DEVELOPER
huey@example.com
dewey@example.com
SPACE AUDITOR
louie@example.com
For more information about the `cf org-users` command, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/org-users.html). For
more information about the `cf space-users` command, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/space-users.html).

### Manage roles
You use the commands listed below to manage roles in the cf CLI. These commands require admin permissions and take `username`, `org` or `space`, and `role` as
arguments:

* `cf set-org-role`
For more information, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/set-org-role.html).

* `cf unset-org-role`
For more information, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/unset-org-role.html).

* `cf set-space-role`
For more information, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/set-space-role.html).

* `cf unset-space-role`
For more information, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/unset-space-role.html).
The available roles are:

* `OrgManager`

* `BillingManager`

* `OrgAuditor`

* `SpaceManager`

* `SpaceDeveloper`

* `SpaceAuditor`
For more information about user roles, see [Orgs, Spaces, Roles, and Permissions](https://docs.cloudfoundry.org/concepts/roles.html).
The following example shows the terminal output for `cf set-org-role huey@example.com example-org OrgManager`, which assigns the Org Manager role to
`huey@example.com` within the `example-org` org:
```
Assigning role OrgManager to user huey@example.com in org example-org as username@example.com...
OK
```

**Important**
If you are not an admin, you see this message when you try to run these commands: `error code: 10003, message: You
are not authorized to perform the requested action`

### Manage roles for users with identical usernames in multiple origins
If a username corresponds to multiple accounts from different user stores, such as both the internal UAA store and an external SAML or LDAP store, running
either `cf set-org-role` or `cf unset-org-role` returns an error similar to the following example:
```
The user exists in multiple origins. Specify an origin for the requested user from: ‘uaa’, ‘other’
```
To resolve this ambiguity, you can construct a `curl` command that uses the API to perform the desired role management function. For an example, see the
[Cloud Foundry API documentation](http://apidocs.cloudfoundry.org/280/organizations/associate_auditor_with_the_organization_by_username.html).

## Push an app
These sections describe how to use the `cf push` command to push a new app or sync changes to an existing app.
For more information about the `cf push` command, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/push.html).

### Push a new app or push changes to an app
To push an app:

1. In a terminal window, log in to the cf CLI by running:
```
cf login
```

2. Go to the directory of the app.

3. Push a new app or push changes to an app by running:
```
cf push APP-NAME
```
Where `APP-NAME` is the name of the app.

### Push an app using a manifest
You can provide a path to a manifest file when you push an app. The manifest file includes information such as the name of the app, disk limit, and number
of instances. You can use a manifest file rather than adding flags to the `cf push` command.
`cf push` locates the `manifest.yml` file in the current working directory by default. Alternatively, you can provide a path to the manifest with the `-f`
flag.
For more information about the `-f` flag, see the [Cloud Foundry CLI Reference Guide](http://cli.cloudfoundry.org/en-US/cf/push.html).

**Note**
When you provide an app name at the command line, the `cf push` command uses that app
name regardless of whether there is a different app name in the manifest. If the manifest configures multiple apps, you can push a
single app by providing thenname at the command line; the cf CLI does not push the others. Use these behaviors for testing.

### Push an app with a buildpack
You can specify a buildpack when you push an app with the `-b` flag. If you use the `-b` flag to specify a buildpack, the app remains permanently linked to
that buildpack. To use the app with a different buildpack, you must delete the app and then push it again.
For more information about available buildpacks, see the [Cloud Foundry documentation](https://docs.cloudfoundry.org/buildpacks/).
The following example shows the terminal output for `cf push awesome-app -b ruby_buildpack`, which pushes an app called `awesome-app` to the URL
`http://awesome-app.example.com` and specifies the Ruby buildpack with the `-b` flag:
```
Pushing app awesome-app to org example-org / space development as username@example.com...
...
Waiting for app awesome-app to start...
name: awesome-app
requested state: started
routes: awesome-app.example.com
last uploaded: Fri 16 Sep 01:54:16 UTC 2022
stack: cflinuxfs3
buildpacks:
name version detect output buildpack name
ruby_buildpack 1.8.58 ruby ruby
type: web
sidecars:
instances: 1/1
memory usage: 1024M
start command: bundle exec rackup config.ru -p $PORT -o 0.0.0.0
state since cpu memory disk logging details

#0 running 2022-09-16T01:54:29Z 0.0% 0 of 0 0 of 0 0/s of 0/s
```

**Important**
To avoid security exposure, verify that you migrate your apps and custom
buildpacks to use the `cflinuxfs4` stack based on Ubuntu 22.04 LTS (Jammy Jellyfish). The `cflinuxfs3` stack is
based on Ubuntu 18.04 (Bionic Beaver), which reaches end of standard support in April 2023.

### Map a route to an app
You can provide a hostname for your app when you push the app. If you do not provide a hostname, the `cf push` command routes your app to a URL of the form `APP-NAME.DOMAIN`, where `APP-NAME` is the name of your app and `DOMAIN` is your default domain. The route definition is included in the `manifest.yml` file.
For information about mapping a route to your app, see [Routes and domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html).
To map a route to the app:

1. In a terminal window, log in to the cf CLI by running:
```
cf login
```

2. Push and map a route by running:
```
cf push -f manifest.yml --var host=APP-HOSTNAME
```
Where:

* `APP-NAME` is the name of the app.

* `APP-DOMAIN` is the domain of the app.

* `APP-HOSTNAME` is the hostname of the app.

## Manage user-provided service instances
These sections describe how to create or update a service instance.

### Create a service instance
To create a new service instance, use the `cf create-user-provided-service` or `cf cups` commands. For more information about the
`cf create-user-provided-service` and `cf cups` commands, see the [Cloud Foundry CLI Reference
Guide](http://cli.cloudfoundry.org/en-US/cf/create-user-provided-service.html).
To create or update a user-provided service instance, you must supply basic parameters. For example, a database service might require a username, password,
host, port, and database name.
You can provide these parameters in the following ways:

* Interactively. For more information, see [Supply Parameters Interactively](https://docs.cloudfoundry.org/cf-cli/getting-started.html#interactive) below.

* Non-interactively. For more information, see [Supply Parameters Non-Interactively](https://docs.cloudfoundry.org/cf-cli/getting-started.html#non-interactive) below.

* With third-party log management software as described in RFC 6587. For more information, see [Supply Parameters Through a Third Party](https://docs.cloudfoundry.org/cf-cli/getting-started.html#third-party) below
and [RFC 6587](http://tools.ietf.org/html/rfc6587).
When used with third-party logging, data is sent formatted according to RFC 5424. For more information, see
[RFC 5424](http://tools.ietf.org/html/rfc5424).

#### Supply parameters interactively
To create a new service while supplying parameters interactively:

1. In a terminal window, log in to the cf CLI by running:
```
cf login
```

2. List parameters in a comma-separated list after the `-p` flag. Run:
```
cf cups SERVICE -p "PARAMETER, SECOND-PARAMETER, THIRD-PARAMETER"
```
Where:

* `SERVICE` is the name of the service you want to create.

* `PARAMETER`, `SECOND-PARAMETER`, and `THIRD-PARAMETER` are parameters such as username, password, host, port, and database name.

#### Supply parameters non-interactively
To create a new service while supplying parameters non-interactively:

1. In a terminal window, log in to the cf CLI by running:
```
cf login
```

2. Pass parameters and their values in as a JSON hash, bound by single quotes, after the `-p` tag. Run:
```
cf cups SERVICE -p '{"host":"HOSTNAME", "port":"PORT"}'
```
Where:

* `SERVICE` is the name of the service you want to create.

* `HOSTNAME` and `PORT` are service parameters.

#### Supply parameters through a third party
For specific log service instructions, see [Streaming app logs to third-party services](https://docs.cloudfoundry.org/devguide/services/log-management-thirdparty-svc.html).
To create a service instance that sends data to a third party:

1. Log in to the cf CLI:
```
cf login
```

2. Create a service instance that sends data to a third party by running:
```
cf cups SERVICE -l THIRD-PARTY-DESTINATION-URL
```
Where:

* `SERVICE` is the name of the service you want to create.

* `THIRD-PARTY-DESTINATION-URL` is the external URL of the third-party service.

### Bind and unbind service instances
After you create a user-provided service instance, you can:

* Bind the service to an app with `cf bind-service`. For more information, see the [Cloud Foundry CLI Reference
Guide](http://cli.cloudfoundry.org/en-US/cf/bind-service.html).

* Unbind the service with `cf unbind-service`. For more information, see the [Cloud Foundry CLI Reference
Guide](http://cli.cloudfoundry.org/en-US/cf/unbind-service.html).

* Rename the service with `cf rename-service`. For more information, see the [Cloud Foundry CLI Reference
Guide](http://cli.cloudfoundry.org/en-US/cf/rename-service.html).

* Delete the service with `cf delete-service`. For more information, see the [Cloud Foundry CLI Reference
Guide](http://cli.cloudfoundry.org/en-US/cf/delete-service.html).

### Update a service instance
To update one or more of the parameters for an existing user-provided service instance, use `cf update-user-provided-service` or `cf uups`.
For more information about the `cf update-user-provided-service` and `cf uups` commands, see the [Cloud Foundry CLI Reference
Guide](http://cli.cloudfoundry.org/en-US/cf/update-user-provided-service.html).
The `cf uups` command does not update any parameter values that you do not supply.

## Retrieve cf CLI return codes
The cf CLI uses exit codes, which help with scripting and confirming that a command has run successfully.
To view a cf CLI exit code:

1. In a terminal window, log in to the cf CLI by running:
```
cf login
```

2. To check that the login was successful, run one of these commands, depending on your OS:

* For Mac OS, run:
```
echo $?
```

* For Windows, run:
```
echo %ERRORLEVEL%
```
If the command succeeds, the exit code is `0`.

## View CLI help output
The `cf help` command lists the cf CLI commands and a brief description of each. For more information, see the [Cloud Foundry CLI Reference
Guide](http://cli.cloudfoundry.org/en-US/cf/help.html).
To list detailed help for any cf CLI command, add the `-h` flag to the command.
The example below shows detailed help output for the `cf delete` command:
```
NAME:
delete - Delete an app
USAGE:
cf delete APP_NAME [-f -r]
ALIAS:
d
OPTIONS:

-f Force deletion without confirmation

-r Delete any mapped routes (only deletes routes mapped to a single app)
```