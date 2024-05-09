# Streaming app logs with Fluentd
[Fluentd](http://www.fluentd.org) is an open source log collector that allows
you to implement unified logging layers. With Fluentd, you can stream app logs to different back ends or services like Elasticsearch, HDFS and
Amazon S3. This topic explains how to integrate Fluentd with Cloud Foundry apps.

## Step 1: Create a Cloud Foundry syslog drain for Fluentd

1. In Cloud Foundry, create a syslog drain user-provided service instance as
described in [Using third-party log management services](https://docs.cloudfoundry.org/devguide/services/log-management.html).

2. Choose one or more apps whose logs you want to drain to Fluentd
through the service.

3. Bind each app to the service instance, and restart the app.

4. Note the GUID for each app, the IP address of the Loggregator host, and the
port number for the service.

5. Locate the port number in the syslog URL.
For example:
`syslog://logs.example.com:5140`

## Step 2: Set up Fluentd for Cloud Foundry
To continue, you must have an active Fluentd instance running.
If you do not have an active Fluentd instance, see the
[Fluentd documentation](https://docs.fluentd.org/installation) for more details.
If you use cf to deploy your fluentd instances, you have to use
[tcp routing](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#create-route-w-port).
Fluentd comes with native support for syslog protocol.
To set up Fluentd for Cloud Foundry, configure the syslog input of Fluentd as follows.

1. In your main Fluentd configuration file, add the following `source` entry:
```
<source>
@type syslog
port 8080
bind 0.0.0.0
tag cf.app
message_length_limit 99990
frame_type octet_count
<transport tcp>
</transport>
<parse>
message_format rfc5424
</parse>
</source>
```

2. Restart the Fluentd service.

**Important**
The Fluentd syslog input plug-in supports `tls` and `tcp` options. You must use the same transport that Cloud Foundry is using.
Fluentd starts listening for syslog message on port 8080 and tagging the messages with `cf.app`, which can be used later for data routing. For more details about the full setup for the service, see [Config File](https://docs.fluentd.org/configuration/config-file).
To use an Elasticsearch or Amazon S3 back end, see the [Fluentd documentation](http://www.fluentd.org/guides/recipes/elasticsearch-and-s3).