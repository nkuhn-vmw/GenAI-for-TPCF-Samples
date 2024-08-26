# Limiting your App Log Rate in Cloud Foundry
Here you can learn about limiting your app log rate for apps in Cloud Foundry.
Log rate limiting limits the number of logs that can be sent to an app.
App log rate limiting is deactivated by default. Cloud Foundry recommends activating this feature to prevent app instances from overloading the
Loggregator Agent with logs, so the Loggregator Agent does not drop logs for other app instances on the same Diego Cell.
Using app log rate limiting can also do the following:

* Prevent apps from reporting inaccurate app metrics in the Cloud Foundry Command Line Interface (cf CLI), which can happen if Log Cache evicts metrics from
its cache in order to store large volumes of logs.

* Limit the CPU usage of logging agents on the Diego Cell VM.
You can allow log rate limits on a per-app basis in bytes per second.

## App log rate limiting in bytes per second
In Cloud Foundry, you can limit the number of bytes each app instance can generate per second.
You can configure app log rate limiting in bytes per second on a per-app basis through either the app manifest or the cf CLI. Additionally, you can enforce
the log rate limit you configure for all apps that are deployed within a space or org by specifying the log rate limit in the quota plan for the space or org.
For more information, see [Creating and Modifying Quota Plans](https://docs.cloudfoundry.org/adminguide/quota-plans.html).

## Determining the ideal app log rate limit
The ideal app logging rate for a deployment depends on characteristics such as VM sizes and the number and type of apps in Cloud Foundry.
Cloud Foundry recommends using at minimum the default limit of `1k` bytes per second.
When you allow app log rate limiting, Diego applies the log rate limit to each app instance. For example, if there are five instances of an app running, Diego
does not sum the logging rates of all five instances when determining if the log rate limit has been exceeded. Instead, Diego evaluates the logging rate of
each individual app instance and only limits instances that exceed the log rate limit.

## What happens when app instances exceed the app log rate limit
When an app instance exceeds the log rate limit you configured, Diego drops the app logs that exceed that limit. When this happens, you see a message
indicating that Diego is dropping app logs.
For more information about how Diego rate-limits app logs, see the [Go documentation](https://godoc.org/golang.org/x/time/rate).

## How Diego Cells behave when an app instance exceeds the app log rate
When an app instance exceeds the log rate limit, the Diego Cell containing the app instance emits the `AppInstanceExceededLogRateLimitCount` counter metric,
similar to the following example:
```
origin:"rep" eventType:CounterEvent timestamp:1582582740243576212 deployment:"cf" job:"diego-cell" index:"0e98fd00-47b2-4589-94f0-385f78b3a04d" ip:"10.0.1.12" tags:<key:"instance_id" value:"0e98fd00-47b2-4589-94f0-385f78b3a04d" > tags:<key:"source_id" value:"rep" > counterEvent:<name:"AppInstanceExceededLogRateLimitCount" delta:1 total:206 >
```
Each Diego Cell in a deployment has a unique `AppInstanceExceededLogRateLimitCount` counter. The `total` value of the counter is the sum total of all app
instances on that Diego Cell that have exceeded the log rate limit since the creation of the Diego Cell. When there are no app instances exceeding the log
rate limit, Diego Cells do not emit the `AppInstanceExceededLogRateLimitCount` metric.
For example, `app-instanceA` and `app-instanceB` are running on one Diego Cell, `app-instanceC` and `app-instanceD` are running on a second Diego Cell, and
the current `total` for the `AppInstanceExceededLogRateLimitCount` is `125` on the first Diego Cell and `43` on the second Diego Cell. If `app-instanceD`
exceeds the log rate limit, the second Diego Cell emits the `AppInstanceExceededLogRateLimitCount` metric with a incremented `total` value of `44`. However,
the first Diego Cell does not emit the `AppInstanceExceededLogRateLimitCount` metric, and the `total` value for the `AppInstanceExceededLogRateLimitCount`
metric on the first Diego Cell is still `125`.
A Diego Cell emits the `AppInstanceExceededLogRateLimitCount` metric conditionally when an app instance on that Diego Cell begins to exceed the log rate
limit. For example, `app-instanceC` and `app-instanceD` are on the same Diego Cell. If `app-instanceC` exceeds the log rate limit continually over a
ten-minute period, and `app-instanceD` exceeds the log rate limit during the first three minutes of each five-minute interval within that ten-minute period
and then stops, the Diego Cell emits the `AppInstanceExceededLogRateLimitCount` metric three times within that ten-minute period.

## Configuring an alert for the AppInstanceExceededLogRateLimitCount metric
If you are using a third-party log management service, you can configure an alert for when the aggregated sum of the `AppInstanceExceededLogRateLimitCount`
metric across all the Diego Cells in Cloud Foundry has been incremented more than a certain number of times or over a certain percentage in the
last five or more minutes.
When you configure this alert, consider the number of app instances running on Cloud Foundry, the logging rate that you configured in
Cloud Foundry, your other Cloud Foundry configuration settings, and so on.
For more information about third-party log management services, see [Streaming App Logs to Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html).

## Identifying apps that exceed the app log rate limit
Diego also logs when a noisy app instance exceeds the log rate limit configured in Cloud Foundry. A log message similar to the following example:
appears in the log stream for the noisy app:
```
2022-08-22T12:42:18.90-0800 [APP/PROC/WEB/0] OUT app instance exceeded log rate limit (1024 bytes/sec)
```
To identify which app instances are exceeding the app log rate limit:
The Firehose and Log Cache plug-ins are developed by the open-source Cloud Foundry community and are not supported by
VMware.

1. In a terminal window, install the Firehose plug-in by running:
```
cf install-plugin 'Firehose Plugin'
```

2. Install the Log Cache plug-in by running:
```
cf install-plugin 'log-cache'
```

3. Filter your app log messages by running:
```
cf nozzle -f LogMessage | grep "app instance exceeded log rate limit"
```
This command returns all logs with log messages containing `"app instance exceeded log rate limit"`, similar to the following example:
```
origin:"rep" eventType:LogMessage timestamp:1583859621886751670 deployment:"warp-drive" job:"diego-cell" index:"3a574bde-91df-48b8-ae21-1d6913da0908" ip:"10.0.1.33" tags:<key:"app_id" value:"34bcfafc-402b-4bb4-84db-aea5401b79eb" > tags:<key:"app_name" value:"app-2" > tags:<key:"instance_id" value:"0" > tags:<key:"organization_id" value:"a30f39c2-4ff3-48a1-a869-a9ed21812a61" > tags:<key:"organization_name" value:"test" > tags:<key:"process_id" value:"34bcfafc-402b-4bb4-84db-aea5401b79eb" > tags:<key:"process_instance_id" value:"92e2ee78-3a1d-41a6-4933-e47b" > tags:<key:"process_type" value:"web" > tags:<key:"source_id" value:"34bcfafc-402b-4bb4-84db-aea5401b79eb" > tags:<key:"space_id" value:"0e2d2d58-3ef5-43f3-b880-c8a30903a96b" > tags:<key:"space_name" value:"test-2" > logMessage:<message:"app instance exceeded log rate limit (1024 bytes/sec)" message_type:OUT timestamp:1583859621886751670 app_id:"34bcfafc-402b-4bb4-84db-aea5401b79eb" source_type:"APP/PROC/WEB" source_instance:"0" >
```
You can inspect these logs to identify which app instances are exceeding the log rate limit.