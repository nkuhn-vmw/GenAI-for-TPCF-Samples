# Loggregator guide for Cloud Foundry operators
Here you can view information for Cloud Foundry deployment operators about how to configure the
Loggregator system to avoid data loss with high volumes of logging and metrics data.
For more information about the Loggregator system, see [Loggregator Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html).

## Loggregator message throughput and reliability
You can measure both the message throughput and message reliability rates of your Loggregator system.

### Measuring message throughput
To measure the message throughput of the Loggregator system, you can monitor the total number of egress messages from all Loggregator Agents in your deployment using the `metron.egress` metric.
If you do not use a monitoring platform, you can measure the overall message throughput of your Loggregator system. To measure the overall message throughput:

1. Log in to the Cloud Foundry Command Line Interface (cf CLI) with your admin credentials by running:
```
cf login
```

2. Install the Cloud Foundry Firehose plug-in.
For more information, see [Install the plug-in](https://docs.cloudfoundry.org/loggregator/cli-plugin.html#add) in

*Installing the Loggregator Firehose Plug-in for cf CLI*.

3. Install Pipe Viewer by running:
```
apt-get install pv
```

4. Run:
```
cf nozzle -n | pv -l -i 10 -r > /dev/null
```

### Measuring message reliability
To measure the message reliability rate of your Loggregator system, you can run black-box tests.

## Scaling Loggregator
Most Loggregator configurations are set to use preferred resource defaults. If you want to customize these defaults or plan the capacity of your Loggregator system, see the following formulas:

### Doppler
Doppler resources can require scaling to accommodate your overall log and metric volume. The recommended formula for estimating the number of Doppler instances you need to achieve a loss rate of < 1% is:

**Note**
Number of Doppler instances = doppler.ingress / 16 000
where `doppler.ingress` represents the per-second rate of change of the `ingress` metric from the `doppler` source, summed over all VMs in your deployment.
Using maximum values over a two-week period is a recommended approach for ingress-based capacity planning.

### Traffic Controller
Traffic Controller resources are usually scaled in line with Doppler resources. The recommended formula for determining the number of Traffic Controller instances is:

**Note**
Number of Traffic Controller instances = Number of Doppler instances / 2
In addition, Traffic Controller resources can require scaling to accommodate the number of your log streams and Firehose subscriptions.

### Log Cache
Log Cache is an ephemeral in-memory store of logs and metrics. Operators scale Log Cache to make sure that at least 15 minutes of
logs and metrics are available at a time. Cloud Foundry recommends scaling Log Cache when the `log_cache_cache_period` metric drops under 900000 milliseconds.
For more information about scaling the Loggregator system,
see [Scaling Loggregator](https://docs.cloudfoundry.org/running/managing-cf/logging-config.html#scaling) in *Configuring System Logging*.

## Scaling nozzles
Nozzles are programs that consume data from the Loggregator Firehose. Nozzles can be configured to select, buffer, and transform data, and to forward it to other apps and services. You can scale a nozzle using the subscription ID specified when the nozzle connects to the Firehose. If you use the same subscription ID on each nozzle instance, the Firehose evenly distributes data across all instances of the nozzle.
For example, if you have two nozzle instances with the same subscription ID, the Firehose sends half of the data to one nozzle instance and half to the other. Similarly, if you have three nozzle instances with the same subscription ID, the Firehose sends one-third of the data to each instance.
If you want to scale a nozzle, the number of nozzle instances must match the number of Traffic Controller instances:
Note, the number of nozzle instances = Number of Traffic Controller instances.
Stateless nozzles handle scaling. If a nozzle buffers or caches the data, the nozzle author must test the results of scaling the number of nozzle instances up or down.
You can deactivate the Firehose. In place of the Firehose, you can configure an aggregate log and metric drain for your foundation.

## Slow nozzle alerts
The Traffic Controller alerts the nozzle programs if they consume events too slowly.
The following metrics can be used to identify slow consumers:

* For v1 consumers: `doppler_proxy.slow_consumer` is incremented as consumers are disconnected for being slow.

* For v2 consumers: `doppler.dropped{direction="egress"}` or `rlp.dropped{direction="egress"}` are incremented when a v2 consumer fails to keep up.
For more information about the Traffic Controller,
see [Loggregator Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html#loggregator-architecture) in *Loggregator Architecture*.

## Forwarding logs to an external service
You can configure Cloud Foundry to forward log data from apps to an external aggregator service. For information about how to bind apps to the external service and configure it to receive logs from Cloud Foundry, see [Streaming App Logs to Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html).

## Log message size constraints
When a Diego Cell emits app logs to Loggregator, Diego breaks up log messages greater than approximately 60 KiB into multiple envelopes.