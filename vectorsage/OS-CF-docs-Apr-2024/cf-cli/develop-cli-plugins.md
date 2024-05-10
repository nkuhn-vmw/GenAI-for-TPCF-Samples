# Developing cf CLI plug-ins
You can create and install cf CLI plug-ins to provide custom commands. You can submit and share these plug-ins to the [CF Community repository](https://plugins.cloudfoundry.org/).

## Prerequisite
To use plug-ins, you must use cf CLI v7 or later. For information about downloading, installing, and uninstalling tcf CLI commands, see [Installing the Cloud Foundry Command Line Interface](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html).

## Creating a plug-in
To prepare to create a plug-in:

1. Implement the predefined plug-in interface from [plugin.go](https://github.com/cloudfoundry/cli/blob/master/plugin/plugin.go) in the Cloud Foundry CLI repository on GitHub.

2. Clone the [Cloud Foundry CLI repository](https://github.com/cloudfoundry/cli) from GitHub. To create a plug-in, you need the [basic GO plugin](https://github.com/cloudfoundry/cli/blob/master/plugin/plugin_examples/basic_plugin.go).

## Initializing the plug-in
To initialize a plug-in:

1. From within the `main()` method of your plug-in, call:
```
plugin.Start(new(MyPluginStruct))
```
The `plugin.Start(...)` function requires a new reference to the `struct` that implements the defined interface.

## Invoking cf CLI commands
To invoke cf CLI commands,

1. From within the `Run(...)` method of your plug-in, call:
```
cliConnection.CliCommand([]args)
```
The `Run(...)` method receives the `cliConnection` as its first argument. The `cliConnection.CliCommand([]args)` returns the output printed by the command and an error.
The output is returned as a slice of strings. The error occurs if the call to the cf CLI command fails.
For more information, see [Plug-in API](https://github.com/cloudfoundry/cli/blob/master/plugin/plugin_examples/DOC.md) in the Cloud Foundry CLI repository on GitHub.

## Installing a plug-in
To install a plug-in:

1. Run:
```
cf install-plugin PATH-TO-PLUGIN-BINARY
```
Where `PATH-TO-PLUGIN-BINARY` is the path to your plug-in binary.
For more information about developing plug-ins, see [plugin\_examples](https://github.com/cloudfoundry/cli/tree/master/plugin/plugin_examples) in the Cloud Foundry CLI repository on GitHub.