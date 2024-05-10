# Streaming app logs to Azure OMS Log Analytics
Here are instructions for integrating your Cloud Foundry apps with OMS Log Analytics in the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/log-analytics/).
Operations Management Suite (OMS) Log Analytics is a monitoring service for Microsoft Azure. The OMS Log Analytics Firehose Nozzle is a Cloud Foundry component that forwards metrics from the Loggregator Firehose to OMS Log Analytics.
This topic assumes you are using the latest version of the Cloud Foundry Command Line Interface (cf CLI) and a working Cloud Foundry deployment on Azure.

## Step 1: Create an OMS workspace in Azure
To create an OMS workspace, see the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-get-started) in the Microsoft Azure documentation.

## Step 2: Deploy the nozzle to Cloud Foundry
To deploy the OMS Log Analytics Firehose nozzle to Cloud Foundry:

1. Authenticate to your Cloud Foundry instance. For more information, see [Creating and Managing Users with the UAA CLI (UAAC)](https://docs.cloudfoundry.org/uaa/uaa-user-management.html) and [Orgs, Spaces, Roles, and Permissions](https://docs.cloudfoundry.org/concepts/roles.html). Run:
```
cf login -a https://api.YOUR-DOMAIN -u YOUR-USERNAME --skip-ssl-validation
```
Where:

* `YOUR-DOMAIN` is your domain.

* `YOUR-USERNAME` is your Cloud Foundry user name.

2. To create a new Cloud Foundry user and grant it access to the Loggregator Firehose using the UAA CLI (UAAC):

1. Target your UAA server by running:
```
uaac target uaa.YOUR-DOMAIN --skip-ssl-validation
```
Where `YOUR-DOMAIN` is your domain.

2. Obtain an access token for the admin client by running:
```
uaac token client get admin
```

3. Create a new user by running:
```
uaac user add USERNAME -p PASSWORD --email EMAIL
```
Where:

* `USERNAME` is a new user name.

* `PASSWORD` is a password.

* `EMAIL` is an email address.

4. Grant the new user admin permissions by running:
```
uaac member add cloud_controller.admin USERNAME
```
Where `USERNAME` is the user name you set in an earlier step.

5. Grant the new user permission to read logs from the Loggregator Firehose endpoint by running:
```
uaac member add doppler.firehose USERNAME
```
Where `USERNAME` is the user name you set.

3. Download the [OMS Log Analytics Firehose Nozzle BOSH release](https://github.com/Azure/oms-log-analytics-firehose-nozzle) from GitHub. Clone the repository and navigate to the `oms-log-analytics-firehose-nozzle` directory by running:
```
git clone https://github.com/Azure/oms-log-analytics-firehose-nozzle.git
cd oms-log-analytics-firehose-nozzle
```

4. Set the environment variables in the [OMS Log Analytics Firehose Nozzle manifest](https://github.com/Azure/oms-log-analytics-firehose-nozzle/blob/master/manifest.yml):
| Environment variable | Description |
| --- | --- |
|
```
applications:
```
|

* name: oms\_nozzle
...
env:
OMS\_WORKSPACE: YOUR-WORKSPACE-ID
OMS\_KEY: YOUR-OMS-KEY
Enter the ID and key value for your OMS workspace. || `OMS_POST_TIMEOUT: 10s` | (Optional) Set the HTTP post timeout for sending events to OMS LogmAnalytics. The default value is 10 seconds. |
| `OMS_BATCH_TIME: 10s` | (Optional) Set the interval for posting a batch to OMS. The default value is 10 seconds.
For more information, see [Configure Additional Logging](https://docs.cloudfoundry.org/devguide/services/oms-nozzle.html#events). |
| `OMS_MAX_MSG_NUM_PER_BATCH: 1000` | (Optional) Set the maximum number of messages to include in an OMS batch. The default amount is 1000.
For more information, see [Configure Additional Logging](https://docs.cloudfoundry.org/devguide/services/oms-nozzle.html#events). |
|
```
FIREHOSE_USER: YOUR-FIREHOSE-USER
FIREHOSE_USER_PASSWORD: YOUR-FIREHOSE-PASSWORD
```
| Enter the user name and password for the Firehose user you created in Step 2c. |
| `API_ADDR: <https://api.YOUR-DOMAIN>` | Enter the URL of your API endpoint. |
| `DOPPLER_ADDR: wss://doppler.YOUR-DOMAIN:443` | Enter the URL of your Loggregator Traffic Controller endpoint. |
| `EVENT_FILTER: YOUR-LIST` | (Optional) Enter the event types you want to filter out in a comma-separated list. The valid event types are `METRIC`, `LOG`, and `HTTP`. |
| `IDLE_TIMEOUT: 60s` | (Optional) Set the duration for the Firehose keep-alive connection. The default time is 60 seconds. |
| `SKIP_SSL_VALIDATION: TRUE-OR-FALSE` | Set this value to `TRUE` to allow insecure connections to the UAA and the Traffic Controller. To block insecure connections to the UAA and Traffic Controller, set this value to `FALSE`. |
| `LOG_LEVEL: INFO` | (Optional) Change this value to increase or decrease the amount of logs. Valid log levels in increasing order include `INFO`, `ERROR`, and `DEBUG`. The default value is `INFO`. |
| `LOG_EVENT_COUNT: TRUE-OR-FALSE` | Set this value to `TRUE` to log the total count of events that the nozzle has sent, received, and lost. OMS logs this value as `CounterEvents`.
For more information, see [Configure Additional Logging](https://docs.cloudfoundry.org/devguide/services/oms-nozzle.html#events). |
| `LOG_EVENT_COUNT_INTERVAL: 60s` | (Optional) Set the time interval for logging the event count to OMS. The default interval is 60 seconds.
For more information, see [Configure Additional Logging](https://docs.cloudfoundry.org/devguide/services/oms-nozzle.html#events). |

5. Push the app by running:
```
cf push
```

## Step 3: View logs in OMS Portal
Import the Cloud Foundry OMS view to your OMS Portal to view visualized logs and metrics. You can also create alert rules for specific events.
The OMS view of Cloud Foundry is not available in the OMS Solutions Gallery. You can add it manually to view your logs in OMS Portal.

### Import the OMS view
To import the OMS view:

1. From the main OMS Overview page, go to **View Designer**.

2. Click **Import**.

3. Click **Browse**.

4. Select the **Cloud Foundry (Preview).omsview** file.

5. Save the view. The main OMS Overview page displays the **Tile**.

6. Click the **Tile** to view visualized metrics.
For more information, see the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-view-designer) in the Azure documentation.

### Create alert rules
For more information about OMS Log Analytics alerts, see the [Microsoft documentation](https://docs.microsoft.com/en-us/azure/log-analytics/log-analytics-alerts) in the Azure documentation.

### Set alert queries
This section includes example queries that operators can set in the OMS Portal.

* This query alerts the operator when the nozzle sends a `slowConsumerAlert` to OMS:
```
Type=CF_ValueMetric_CL Name_s=slowConsumerAlert
```

* This query alerts the operator when Loggregator sends an `LGR` to indicate problems with logging:
```
Type=CF_LogMessage_CL SourceType_s=LGR MessageType_s=ERR
```

* This query alerts the operator when the number of lost events reaches a certain threshold, specified in the OMS Portal:
```
Type=CF_CounterEvent_CL Job_s=nozzle Name_s=eventsLost
```

* This query alerts the operator when the nozzle receives the `TruncatingBuffer.DroppedMessages` **CounterEvent**:
```
Type=CF_CounterEvent_CL Name_s="TruncatingBuffer.DroppedMessages"
```

## Step 4: Configure additional logging (optional)
OMS Log Analytics Firehose Nozzle forwards metrics from the Loggregator Firehose to OMS with minimal processing, but the nozzle can push additional metrics to OMS.

### Logs sent and received, events lost
If you set the `LOG_EVENT_COUNT` environment variable to `TRUE` in the [manifest](https://docs.cloudfoundry.org/devguide/services/oms-nozzle.html#deploy), the nozzle periodically sends the count of sent, received, and lost events to OMS. The value you set for the `LOG_EVENT_COUNT_INTERVAL` specifies how frequently the nozzle sends the count.
The nozzle does not count CounterEvents in the sent, received, or lost event count.
The nozzle sends the count as a **CounterEvent** with one of these values for **CounterKey**:
| CounterEvent | CounterKey |
| --- | --- |
| nozzle.stats.eventsReceived | The number of events the Firehose has received during the interval |
| nozzle.stats.eventsSent | The number of events the nozzle has sent to OMS during the interval |
| nozzle.stats.eventsLost | The number of events the nozzle has tried to send to OMS during the interval, but failed to send after 4 attempts |
In most cases, the total count of `eventsSent` plus `eventsLost` is less than the total `eventsReceived` at the same time. The nozzle buffers some messages and posts them in a batch to OMS. Operators can adjust the buffer size by adjusting the `OMS_BATCH_TIME` and `OMS_MAX_MSG_NUM_PER_BATCH` environment variables in the manifest.

### Log slow consumer alerts
Loggregator sends the nozzle a `slowConsumerAlert` when:

* WebSocket sends the error code `ClosePolicyViolation (1008)`.

* The nozzle receives a **CounterEvent** with the value `TruncatingBuffer.DroppedMessages`.
In either case, the nozzle sends the `slowConsumerAlert` event to OMS as the following **ValueMetric**:
| ValueMetric | MetricKey |
| --- | --- |
| nozzle.alert.slowConsumerAlert | 1 |
The nozzle does not count ValueMetrics in the sent, received, or lost event count.
For more information, see the [Slow Nozzle Alerts](https://docs.cloudfoundry.org/loggregator/log-ops-guide.html#slow-noz) section of the *Loggregator Guide for Cloud Foundry Operators* topic.

## Step 5: Scale the deployment (optional)

### Scale the nozzle
If the nozzle is unable to keep up with processing logs from the Firehose, Loggregator alerts the nozzle. When the nozzle receives the alert, it sends a `slowConsumerAlert` to OMS. If this happens, scaling up the nozzle minimizes data loss.
If an operator scales up their deployment, the Firehose evenly distributes events across all instances of the nozzle. For more information, see the [Scaling Nozzles](https://docs.cloudfoundry.org/loggregator/log-ops-guide.html#scaling-nozzles) section of the *Loggregator Guide for Cloud Foundry Operators* topic.
Operators can create an alert rule for the `slowConsumerAlert` message. For more information, see [Create alert rules](https://docs.cloudfoundry.org/devguide/services/oms-nozzle.html#alert).

### Scale Loggregator
Loggregator sends `LGR` log entries to indicate problems with logging. For more information, see [Scaling Loggregator](https://docs.cloudfoundry.org/loggregator/log-ops-guide.html#scaling) in *Loggregator Guide for Cloud Foundry Operators*.
Operators can create an alert rule for the `LGR` message. For more information, see [Create alert rules](https://docs.cloudfoundry.org/devguide/services/oms-nozzle.html#alert).