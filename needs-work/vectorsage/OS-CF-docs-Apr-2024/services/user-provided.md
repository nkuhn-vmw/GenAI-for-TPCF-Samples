# User-provided service instances
User-provided service instances allow you to use services that are not available in the Marketplace with their apps running on Cloud Foundry.
You can use user-provided service instances to deliver service credentials to an app, or to trigger streaming of app logs to a syslog-compatible consumer. These two functions can be used individually or both at the same time.
After creation, user-provided service instances behave like service instances created through the Marketplace. See [Managing service instances](https://docs.cloudfoundry.org/devguide/services/managing-services.html) and [App binding](https://docs.cloudfoundry.org/devguide/services/application-binding.html) for details about listing, renaming, deleting, binding, and unbinding service instances.

## Create a user-provided service instance
The alias for [cf create-user-provided-service](http://cli.cloudfoundry.org/en-US/cf/create-user-provided-service.html) is `cf cups`.

### Deliver service credentials to an app
Suppose a developer obtains a URL, port, user name, and password for communicating with an Oracle database managed outside of Cloud Foundry. The developer can manually create custom environment variables to configure their app with these credentials (of course you never hard code these credentials in your app!).
User-provided service instances allow developers to configure their apps with these using the familiar [App binding](https://docs.cloudfoundry.org/devguide/services/application-binding.html) operation and the same app runtime environment variable used by Cloud Foundry to deliver credentials for Marketplace services ([VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#VCAP-SERVICES)).
```
cf cups SERVICE_INSTANCE -p '{"username":"admin","password":"pa55woRD"}'
```
To create a service instance in interactive mode, use the `-p` option with a comma-separated list of parameter names. The Cloud Foundry Command Line Interface (cf CLI) prompts you for each parameter value.
```
$ cf cups my-user-provided-route-service -p "host, port"
host> rdb.local
port> 5432
Creating user provided service my-user-provided-route-service in org my-org / space my-space as user@example.com...
OK
```
After creating the user-provided service instance, to deliver the credentials to one or more apps, see [App binding](https://docs.cloudfoundry.org/devguide/services/application-binding.html).

### Stream app logs to a service
User-provided service instances allow developers to stream app logs to a syslog compatible aggregation or analytics service that isn’t available in the Marketplace. For more information about the syslog protocol see [RFC 5424](http://tools.ietf.org/html/rfc5424) and [RFC 6587](http://tools.ietf.org/html/rfc6587).
Create the user-provided service instance, specifying the URL of the service with the `-l` option.
```
cf cups SERVICE_INSTANCE -l syslog-tls://example.log-aggregator.com:6514
```
To stream app logs to the service, bind the user-provided service instance to your app.

### Proxy app requests to a route service
User-provided service instances allow developers to proxy app requests to [route services](https://docs.cloudfoundry.org/devguide/services/#route-services) for preprocessing. To create a user-provided service instance for a route service, specify the URL for the route service using the `-r` option.
```
$ cf create-user-provided-service my-user-provided-route-service -r https://my-route-service.example.com
Creating user provided service my-user-provided-route-service in org my-org / space my-space as user@example.com...
OK
```

**Important**
When creating the user-provided service, the route service URL you specify must be “https.”
To proxy requests to the user-provided route service, you must bind the service instance to the route.
For more information, see [Managing app requests with route services](https://docs.cloudfoundry.org/devguide/services/route-binding.html).

## Update a user-provided service instance
You can use [cf update-user-provided-service](http://cli.cloudfoundry.org/en-US/cf/update-user-provided-service.html) to update the attributes of an instance of a user-provided service. New credentials overwrite old credentials, and parameters that are not provided are deleted.
The alias for `update-user-provided-service` is `uups`. Bound apps can access the new configuration after restart.
You can use rolling restarts to avoid any app downtime.
For more information, see [Restart an app](https://docs.cloudfoundry.org/devguide/deploy-apps/rolling-deploy.html#restart) in *Rolling App Deployments*.

**Caution**
If you are rotating credentials, the old credentials must be active until the restart is finished.