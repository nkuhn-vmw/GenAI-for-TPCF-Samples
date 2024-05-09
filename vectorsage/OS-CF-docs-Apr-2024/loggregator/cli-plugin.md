# Installing the Loggregator Firehose Plug-in for cf CLI
You can use the Loggregator Firehose Plug-in for the Cloud Foundry Command Line Interface (cf CLI).
The Loggregator Firehose plug-in for the cf CLI allows Cloud Foundry admins to access the output of the Loggregator Firehose. The output of the Firehose includes logs and metrics from apps deployed on Cloud Foundry as well as metrics from Cloud Foundry platform components. For more information about the Firehose, see the [Loggregator Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html#loggregator-architecture) section of the *Loggregator Architecture* topic.
For more information about using plug-ins with the cf CLI, see [Using cf CLI plug-ins](https://docs.cloudfoundry.org/cf-cli/use-cli-plugins.html).
You can deactivate the Firehose. In place of the Firehose, you can configure an aggregate log and metric drain for your foundation:

## Prerequisites
Before you install the Loggregator Firehose plug-in, you need the following prerequisites:

* Admin access to the Cloud Foundry deployment that you want to monitor

* Cloud Foundry Command Line Interface (cf CLI) v6.12.2 or later
For information about downloading, installing, and uninstalling the cf CLI, see [Installing the cf CLI](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html).

## Installing the plug-in
To install the Loggregator Firehose plug-in:

1. Add the CF Community plug-in repository to your cf CLI plug-ins by running:
“`
cf add-plugin-repo CF-Community <https://plugins.cloudfoundry.org>

1. Install the Firehose plug-in from the CF Community plug-in repository by running:
```
cf install-plugin -r CF-Community "Firehose Plugin"
```

## Viewing the Firehose
To view the streaming output of the Firehose, which includes logging events and metrics from Cloud Foundry system components, run:
```
cf nozzle --debug
```
You must be logged in as a Cloud Foundry admin to access the Firehose.
For more information about logging and metrics in Cloud Foundry, see [Loggregator Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html).

## Uninstalling the plug-in
To uninstall the Loggregator Firehose plug-in:

1. Run `cf plugins` to see a list of installed plug-ins.
```
$ cf plugins
Listing Installed Plugins...
OK
Plugin Name Version Command Name Command Help
FirehosePlugin 0.6.0 nozzle Command to print out messages from the firehose
```

2. To uninstall the plug-in, run:
```
cf uninstall-plugin FirehosePlugin
```