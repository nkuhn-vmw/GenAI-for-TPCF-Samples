# Delivering service credentials to an app
You can bind your apps to service instances for the purpose of generating credentials and delivering them to apps. For an overview of services, and documentation about other service management operations, see [Using services](https://docs.cloudfoundry.org/). If you are interested in building services for Cloud Foundry and making them available to end users, see [Services](http://docs.cloudfoundry.org/services/index.html).

## Bind a service instance
Binding a service instance to your app triggers credentials to be provisioned for the service instance and delivered to the app runtime in the [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html) environment variable. For details about consuming these credentials with your app, see [Using bound service instances](https://docs.cloudfoundry.org/devguide/services/application-binding.html#use).
Not all services support binding, as some services deliver value to users directly without integration with an app. In many cases, binding credentials are unique to an app, and another app bound to the same service instance receives different credentials, but this depends on the service.
```
$ cf bind-service my-app mydb
Binding service mydb to my-app in org my-org / space test as me@example.com...
OK
TIP: Use 'cf push' to ensure your env variable changes take effect
$ cf restart my-app
```

**Important**
You must restart or in some cases re-push your app for changes to be applied to the [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html) environment variable and for the app to recognize these changes.

### Arbitrary parameters
Some services support additional configuration parameters with the bind request. These parameters are passed in a valid JSON object containing service-specific configuration parameters, provided either in-line or in a file. For a list of supported configuration parameters, see documentation for the particular service offering.
See the following examples:
```
$ cf bind-service rails-sample my-db -c '{"role":"read-only"}'
Binding service my-db to app rails-sample in org console / space development as user@example.com...
OK
```
```
$ cf bind-service rails-sample my-db -c /tmp/config.json
Binding service my-db to app rails-sample in org console / space development as user@example.com... OK
```

### Binding with app manifest
As an alternative to binding a service instance after pushing an app, you can use the app manifest to bind the service instance during `cf push`.
The following excerpt from an app manifest binds a service instance called `test-mysql-01` to the app on push.
```
services:

- test-mysql-01
```
The following excerpt from an app manifest binds a service instance called `db-test` with arbitrary parameters to the app on push. Arbitrary parameters used in this example are available in cf CLI 7.0 and later.
```
services:

- name: db-test
parameters:
schema: customschema
```
The following excerpt from the `cf push` command and response demonstrates that the cf CLI reads the manifest and binds the service instance to an app called `test-msg-app`.
```
$ cf push
Using manifest file /Users/Bob/test-apps/test-msg-app/manifest.yml
...
Binding service test-mysql-01 to test-msg-app in org My-Org / space development as Bob@shared-domain.example.com
OK
```
For more information about app manifests, see [Deploying with app manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#services-block).

### Named service bindings
Service offering and service instance names vary across environments. App authors can discover the service instances their apps require, without having to know environment-specific service names. Developers can specify a service binding name to include in [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html).
To specify the service binding name, provide the `--binding-name` flag when binding an app to a service instance:
```
$ cf bind-service my-app my-service --binding-name postgres-database
OK
```
The provided name is available in the `name` and `binding_name` properties in the [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html) environment variable:
```
"VCAP_SERVICES": {
"service-name": [
{
"name": "postgres-database",
"binding_name": "postgres-database",
...
}
]
}
```

### Using bound service instances
After your service instance is created and bound to your app, you must configure the app to dynamically fetch the credentials for your service instance. The [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#VCAP-SERVICES) environment variable contains credentials and additional metadata for all bound service instances. There are two methods developers can use to have their apps consume binding credentials.

* **Parse the JSON yourself:** See the documentation for [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#VCAP-SERVICES). Helper libraries are available for some frameworks.

* **Auto-configuration:** Some buildpacks create a service connection for you by creating additional environment variables, updating config files, or passing system parameters to the JVM.
For details about consuming credentials specific to your development framework, see the Service Binding section in the documentation for your framework’s [buildpack](https://docs.cloudfoundry.org/buildpacks/).

## Update service credentials
This section describes how to update service instance credentials.
When updating the credentials, you can restage the app immediately and experience app downtime.
If your app uses blue-green deployment, you can update service instance credentials with no downtime.
For more information about user-provided services, see [Update a user-provided service instance](https://docs.cloudfoundry.org/devguide/services/user-provided.html#update) in *User-Provided Service Instances*.

### With downtime
To update your service credentials:

1. [Unbind the service instance](https://docs.cloudfoundry.org/devguide/services/application-binding.html#unbind) using the credentials you are updating by running:
```
$ cf unbind-service YOUR-APP YOUR-SERVICE-INSTANCE
```

2. [Bind the service instance](https://docs.cloudfoundry.org/devguide/services/application-binding.html#bind). This command adds your credentials to the [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html) environment variable.
```
$ cf bind-service YOUR-APP YOUR-SERVICE-INSTANCE
```

3. Restart or re-push the app bound to the service instance so that the app recognizes your environment variable updates.

### Without downtime
To update your service credentials without experiencing app downtime:

1. Start a blue-green update of the app. For more information, see [Using blue-green deployment to reduce downtime and risk](https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html). Push the “Green” version of the app with the `--no-start` parameter to prevent the app from starting right away:
```
$ cf push YOUR-APP --no-start
```

2. Bind the service instances to the newly-deployed “Green” app by running:
```
$ cf bind-service YOUR-APP YOUR-SERVICE-INSTANCE
```

3. Start the “Green” app with `cf start`:
```
$ cf start YOUR-APP
```

4. Unbind the service instances from the `Blue` app:
```
$ cf unbind-service YOUR-APP YOUR-SERVICE-INSTANCE
```

## Unbind a service instance
Unbinding a service removes the credentials created for your app from the [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html) environment variable.
```
$ cf unbind-service my-app mydb
Unbinding app my-app from service mydb in org my-org / space test as me@example.com...
OK
```

**Important**
You must restart or in some cases re-push your app for changes to be applied to the [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html) environment variable and for the app to recognize these changes.