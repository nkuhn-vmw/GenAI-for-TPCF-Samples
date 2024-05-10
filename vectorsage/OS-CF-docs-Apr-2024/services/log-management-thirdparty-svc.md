# Streaming app logs to third-party services
Here are instructions for configuring some third-party log management services for your Cloud Foundry apps.
After you configure a service, see [Third-party log management services](https://docs.cloudfoundry.org/devguide/services/log-management.html) for instructions for binding your app to the service.

## Logit.io
From your Logit.io dashboard:

1. Identify the Logit ELK stack you want to use.

2. Click Logstash **Configuration**.

3. Note your Logstash **Endpoint**.

4. Note your TCP-SSL, TCP, or UDP **Port** (not the syslog port).

5. Create the log drain service in Cloud Foundry.
```
$ cf cups logit-ssl-drain -l syslog-tls://ENDPOINT:PORT
```
or
```
$ cf cups logit-drain -l syslog://ENDPOINT:PORT
```

6. Bind the service to an app.
```
$ cf bind-service YOUR-CF-APP-NAME logit-ssl-drain
```
or
```
$ cf bind-service YOUR-CF-APP-NAME logit-drain
```

7. Restage or push the app using one of these commands:
```
$ cf restage YOUR-CF-APP-NAME
```
```
$ cf push YOUR-CF-APP-NAME
```
After a short delay, logs begin to appear in Kibana.

## Papertrail
From your Papertrail account:

1. Click **Add System**. The Dashboard appears.

2. Click the **Other** link. The **Setup Systems** screen appears.

3. Click **I use Cloud Foundry**, enter a name, and click **Save**.
!["Choose your situation" pane.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/papertrail-04.png)

4. After the system is recorded, the URL, with the port, is displayed. Record the URL and port for later use.
![Message: CloudFoundry will log to "URL." Record the URL.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/papertrail-05.png)

5. Create the log drain service in Cloud Foundry.
```
$ cf cups my-logs -l syslog-tls://logs.papertrailapp.com:PORT
```

6. Bind the service to an app.
```
$ cf bind-service APPLICATION-NAME my-logs
```

7. Restage the app.
```
$ cf restage APPLICATION-NAME
```
After a short delay, logs begin to flow.

8. When Papertrail starts receiving log entries, the view changes to show the logs viewing page.
![Log viewer showing many log messages.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/papertrail-11.png)

## Splunk
See [Streaming app logs to splunk](https://docs.cloudfoundry.org/devguide/services/integrate-splunk.html) for details.

## Splunk Storm
From your Splunk Storm account:

1. Click **Add project**. On the dialog box that appears, enter the **Project name** and select the **Project time zone**. Click **Continue**.
![Add project page, with fields for Project name and Project time zone.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/splunkstorm-03.png)

2. In **Network data**, create a new input. Under **Network data**, click **Select**. Data is sent directly from your servers, and accepted data types include syslog, syslog-ng, snare, and netcat.
![Network data dialog box.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/splunkstorm-04.png)

3. Under **Add network data**, click **Authorize your IP address** and select **Manually**. Next, enter the external IP addresses your Cloud Foundry administrator assigns to outbound traffic.
![Add network data pane. The options are Automatically or Manually.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/splunkstorm-05.png)

4. Record the host and port provided for TCP input for later use.
![The Authorized network inputs pane shows the ports that data is sent to for this project only.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/splunkstorm-06.png)

5. Using the cf CLI, create the log drain service in Cloud Foundry using the TCP host and port you recorded. Then you bind the service to an app and restage the app using the syntax shown here. After a short delay, the logs begin to flow.
```
$ cf cups my-logs -l syslog://HOST:PORT
$ cf bind-service APPLICATION-NAME my-logs
$ cf restage APPLICATION-NAME
```

6. When events begin to appear, click **Data Summary**. The **Data Summary** button appears in the **What to Search** section.
![The What to Search section.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/splunkstorm-09.png)

7. In the **Data Summary** table, click the **loggregator** link to view all incoming log entries from Cloud Foundry.
![The Data Summary table has 3 tabs: Hosts, Sources, and Sourcetypes.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/splunkstorm-10.png)

## SumoLogic
SumoLogic uses HTTPS for communication. HTTPS is supported in Cloud Foundry v158 and later.
In your SumoLogic account:

1. Beside **Manage Collectors and Sources**, click the **Add Collector** link.
![The available actions are Upgrade Collectors, Add Collector, and Access Keys.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/sumologic-02.png)

2. Under **Add Collector**, select **Hosted Collector** and fill in the details.

1. In **Name**, enter `Cloud Foundry`.

2. In **Description**, enter the purpose of the new collector.

3. In **Category**, you can enter the source category, if you want. The collector sets the source category to this value unless it is overwritten by the source metadata.
![Add Collector screen.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/sumologic-03a.png)
![Inputs are Name, Description (optional) and Category (optional).](https://docs.cloudfoundry.org/devguide/images/third-party-logs/sumologic-03b.png)

3. Click **Save**.

4. In the **Manage Collectors and Sources** table, in the row for the new collector, click the **Add Source** link.
![The Manage Collectors and Sources table, you can filter the Collectors shown: All Collectors, Running Collectors, and Stopped Collectors.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/sumologic-04.png)

5. Under **Select a type of Source**, select **HTTP** and fill in the details. An HTTPS URL is provided.

1. In **Name**, leave the entry, `Cloud Foundry``.

2. In **Description**, enter a description of the source.

3. In **Source Host**, enter the host name for the system from which the log files are being collected.

4. In **Source Category**, enter the log category metadata. You can use this later in queries.![Source typo options are: Amazon S3 and HTTP.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/sumologic-05.png)

6. When the source is created, a URL is displayed. You can also view the URL by clicking the **Show URL** link beside the newly created source in the **Manage Collectors and Sources** table. Record the URL for the next step.
![Three options are available in the row: Show URL, Edit, Delete.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/sumologic-06a.png)

7. Using the cf CLI, create the log drain service in Cloud Foundry using the source URL you just recorded. Then you bind the service to an app and restage the app using the syntax shown here. After a short delay, the logs begin to flow.
```
$ cf cups my-logs -l HTTPS-SOURCE-URL
$ cf bind-service APPLICATION-NAME my-logs
$ cf restage APPLICATION-NAME
```

8. In the SumoLogic dashboard, click **Manage**, then click **Status** to see a view of the log entries.
![Status shows Total Message Volume](https://docs.cloudfoundry.org/devguide/images/third-party-logs/sumologic-09.png)

9. Click **Search**. Place the pointer in the search box, then click **Enter** to submit an empty search query.
![Search terms page.](https://docs.cloudfoundry.org/devguide/images/third-party-logs/sumologic-10.png)

## Logsene
Logsene uses HTTPS for communication. HTTPS is supported in Cloud Foundry v158 and later.
In your Sematext account:

1. Click the [Create App / Logsene App](https://apps.sematext.com/logsene-reports/registerApplication.do) menu item. Enter a name and click **Add Application** to create the Logsene App.

2. Using the cf CLI, create the log drain service using the source URL displayed. Then you bind the service to an app and restage the app using the syntax shown here. After a short delay, the logs begin to flow. The logs appear in the [Logsene UI](https://apps.sematext.com/users-web/services.do#logsene).
```
$ cf cups logsene-log-drain -l https://logsene-cf-receiver.sematext.com/YOUR_LOGSENE_TOKEN
$ cf bind-service YOUR-CF-APP-NAME logsene-log-drain
$ cf restage APPLICATION-NAME
```

## Logentries is not supported
Using Logentries is discouraged because it does not support multiple syslog sources. Cloud Foundry distributes log entries over multiple servers to handle the load.