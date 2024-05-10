# Managing service keys
Here are instructions for managing service instance credentials (binding credentials) with service keys.
Service keys generate credentials for manually configuring consumers of Marketplace services. After you configure them for your service, local clients, apps in other spaces, or entities outside your deployment can access your service with these keys.

**Important**
Some service brokers do not support service keys. To build a service broker that supports service keys, see [Services](https://docs.cloudfoundry.org/services/index.html). To use a service broker that does not support service keys, see [Delivering service credentials to an app](https://docs.cloudfoundry.org/devguide/services/application-binding.html).

## Create a service key
To generate credentials for a service instance, use the `cf create-service-key` command:
```
$ cf create-service-key MY-SERVICE MY-KEY
Creating service key MY-KEY for service instance MY-SERVICE as me@example.com...
OK
```
Use the `-c` flag to provide service-specific configuration parameters in a valid JSON object, either in-line or in a file.
To provide the JSON object in-line, use the following format:
```
$ cf create-service-key MY-SERVICE MY-KEY -c '{"read-only":true}'
Creating service key MY-KEY for service instance MY-SERVICE as me@example.com...
OK
```
To provide the JSON object as a file, give the absolute or relative path to your JSON file:
```
$ cf create-service-key MY-SERVICE MY-KEY -c PATH-TO-JSON-FILE
Creating service key MY-KEY for service instance MY-SERVICE as me@example.com...
OK
```

## List service keys for a service instance
To list service keys for a service instance, use the `cf service-keys` command:
```
$ cf service-keys MY-SERVICE
Getting service keys for service instance MY-SERVICE as me@example.com...
name
mykey1
mykey2
```

## Get credentials for a service key
To retrieve credentials for a service key, use the `cf service-key` command:
```
$ cf service-key MY-SERVICE MY-KEY
Getting key MY-KEY for service instance MY-SERVICE as me@example.com...
{
uri: foo://user2:pass2@example.com/mydb,
servicename: mydb
}
```
Use the `--guid` flag to display the API GUID for the service key:
```
$ cf service-key --guid MY-SERVICE MY-KEY
Getting key MY-KEY for service instance MY-SERVICE as me@example.com...
e3696fcb-7a8f-437f-8692-436558e45c7b
OK
```

## Configure credentials for a service key
After obtaining these credentials, you can use a local CLI or utility to connect to the service instance, configure an app running outside the platform to connect to the service instance, or create a user-provided service instance so that apps in another space can connect to the service instance. How you configure these credentials depends on what local client, app, or entity is used to access your service instance.
For more information about configuring credentials with a user-provided service instance, see [User-provided service instances](http://docs.cloudfoundry.org/devguide/services/user-provided.html).

## Delete a service key
To delete a service key, use the `cf delete-service-key` command:
```
$ cf delete-service-key MY-SERVICE MY-KEY
Are you sure you want to delete the service key MY-KEY ? y
Deleting service key MY-KEY for service instance MY-SERVICE as me@example.com...
OK
```
Add option `-f` to force deletion without confirmation.
```
$ cf delete-service-key -f MY-SERVICE MY-KEY
Deleting service key MY-KEY for service instance MY-SERVICE as me@example.com...
OK
```