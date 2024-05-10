# Accessing services with SSH
You can gain direct command line access to your deployed service instance using SSH. This allows you to, for example, access your database to run raw SQL commands to edit the schema, import and export data, or debug app data issues.
To establish direct command line access to a service, you deploy a host app and use its SSH and port forwarding features to communicate with the service instance through the application container. The technique described here works with TCP services such as MySQL or Redis.

*This topic requires Cloud Foundry Command Line Interface (cf CLI) v6.15.0 or later, but at least v7 is recommended.*

**Note** If you have mutual TLS between the Gorouter and app containers, app containers accept incoming communication only from the Gorouter. This disables `cf ssh`. For more information, see the [TLS to Apps and Other Back End Services](https://docs.cloudfoundry.org/concepts/http-routing.html#tls-to-back-end) section of the *HTTP Routing* topic.

**Important**
The procedure in this topic requires use of a service key, and not all services support service keys. Some services support credentials through [app binding](https://docs.cloudfoundry.org/devguide/services/application-binding.html) only.

## Create a service instance

1. In your terminal window, log in to your deployment with `cf login`.

2. Run `cf marketplace` to list the marketplace services available.
```
$ cf marketplace
mysql 100mb MySQL databases on demand
```

3. Create your service instance. As part of the [create-service](http://cli.cloudfoundry.org/en-US/cf/create-service.html) command, indicate the service name, the service plan, and the name you choose for your service instance.
```
$ cf create-service MySQL 100mb MY-DB
```

## Push your host app
To push an app that acts as the host for the SSH tunnel, push any app that is deployed to Cloud Foundry.
Your app must be prepared before you push it. See [Pushing an app](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html) for details about preparing apps for pushing.

1. Push your app:
```
cf push YOUR-HOST-APP
```

2. Activate SSH for your app:
```
cf enable-ssh YOUR-HOST-APP
```
To activate SSH access to your app, SSH access must also be activated for both the space that contains the app and Cloud Foundry. For more information, see [App SSH Overview](https://docs.cloudfoundry.org/devguide/deploy-apps/app-ssh-overview.html).

## Create your service key
To establish SSH access to your service instance, you must create a service key that contains critical information for configuring your SSH tunnel.

1. Create a service key for your service instance using the [cf create-service-key](http://cli.cloudfoundry.org/en-US/cf/create-service-key.html) command.
```
cf create-service-key MY-DB EXTERNAL-ACCESS-KEY
```

2. Retrieve your new service key using the [cf service-key](http://cli.cloudfoundry.org/en-US/cf/service-key.html) command.
```
cf service-key MY-DB EXTERNAL-ACCESS-KEY
```
For example:
```
$ cf service-key MY-DB EXTERNAL-ACCESS-KEY
Getting key EXTERNAL-ACCESS-KEY for service instance MY-DB as user@example.com
{
"hostname": "us-cdbr-iron-east-01.mysql.net",
"jdbcUrl": "jdbc:mysql://us-cdbr-iron-east-03.mysql.net/ad\_b2fca6t49704585d?user=b5136e448be920\u0026password=231f435o05",
"name": "ad\_b2fca6t49704585d",
"password": "231f435o05",
"port": "3306",
"uri": "mysql://b5136e448be920:231f435o05@us-cdbr-iron-east-03.mysql.net:3306/ad\_b2fca6t49704585d?reconnect=true",
"username": "b5136e448be920"
}
```

## Configure your SSH tunnel
Configure an SSH tunnel to your service instance using [cf ssh](http://cli.cloudfoundry.org/en-US/cf/ssh.html). Tailor the following example command with information from your service key.
```
$ cf ssh -L 63306:us-cdbr-iron-east-01.mysql.net:3306 YOUR-HOST-APP
```

* You can use any available local port for port forwarding; for example, `63306`.

* `us-cdbr-iron-east-01.mysql.net` is the address provided under `hostname` in the service key retrieved earlier.

* `3306` is the port provided under `port`.

* `YOUR-HOST-APP` is the name of your host app.
After you enter the command, open another terminal and follow the steps in [Access your service instance](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-services.html#access-service).

## Access your service instance
To establish direct command line access to your service instance, use the relevant command line tool for that service. This example uses the MySQL command line client to access the MySQL service instance.
```
$ mysql -u b5136e448be920 -h 0 -p -D ad_b2fca6t49704585d -P 63306
```

* Replace `b5136e448be920` with the user name provided under `username` in your service key.

* `-h 0` instructs `mysql` to connect to your local machine (use `-h 127.0.0.1` for Windows).

* `-p` instructs `mysql` to prompt for a password. When prompted, use the password provided under `password` in your service key.

* Replace `ad_b2fca6t49704585d` with the database name provided under `name` in your service key.

* `-P 63306` instructs `mysql` to connect on port `63306`.