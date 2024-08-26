# Using a cf CLI plug-in
The Cloud Foundry CLI (cf CLI) includes plug-in capability. The plug-in allows you to add custom commands to the cf CLI.
You can install and use the plug-in that Cloud Foundry developers and third-party developers create. For a current list of community-supported plug-ins, see the [Cloud Foundry Community CLI Plug-in page](https://plugins.cloudfoundry.org). For information about submitting your own plug-in, see the [Cloud Foundry CLI Plugin Repository (CLIPR)](https://github.com/cloudfoundry-incubator/cli-plugin-repo) repository on GitHub.

**Important**
Plug-ins are not vetted, including for security or function. Use plug-ins at your own risk.
The cf CLI identifies a plug-in by binary filename, its developer defined plug-in name, and the commands that the plug-in provides. Use the binary filename only to install a plug-in. You use the plug-in name or a command for any other action.
The cf CLI uses case sensitive commands, but plug in management commands accept plug-in and repository names
irrespective of their casing.

## Changing the plug-in directory
By default, the cf CLI stores plug-ins on your workstation in `$CF_HOME/.cf/plugins`, which defaults to `$HOME/.cf/plugins`.
To change the root directory of this path from `$CF_HOME`, you must set the `CF_PLUGIN_HOME` environment variable.
The cf CLI appends `.cf/plugins` to the `CF_PLUGIN_HOME` path that you specify and stores plug ins in that location. For example, if you set `CF_PLUGIN_HOME` to `/my-folder`, cf CLI stores plug-ins in `/my-folder/.cf/plugins`.

## Installing a plug-in
To install a plug-in:

1. Download a binary or the source code for a plug-in from a trusted provider.
The cf CLI requires a binary file compiled from source code written in Go. If you download source code, you must compile the code to create a binary.

1. Run:
```
cf install-plugin BINARY-FILENAME
```
Where `BINARY-FILENAME` is the path to and name of your binary file.
You cannot install a plug in that has the same name or that uses the same command as an existing plugin. If you attempt to do so, you are prompted to uninstall the existing plugin.
The cf CLI prohibits you from implementing any plug-in that uses a native cf CLI command name or alias. For example, if you attempt to install a third-party plugin that includes the `cf push` command, the cf CLI halts the installation.
For more information, see [install-plugin](http://cli.cloudfoundry.org/en-US/cf/install-plugin.html) in the *Cloud Foundry CLI Reference Guide*.

## Managing plug-ins and running plug-in commands
Use the contents of the `cf help` **CLI plug-in management** and **Commands offered by installed plug-ins** sections to manage plug-ins and run plug-in commands.
To manage plug-ins and run plug-in commands:

1. List all installed plug-ins and all commands that the plug-ins provide by running:
```
cf plugins
```

2. Run a plug-in command:
```
cf PLUGIN-COMMAND
```
Where `PLUGIN-COMMAND` is the plug-in command you ran.

## Checking for plug-in updates
To check all registered plug-in repositories for newer versions of currently installed plug-ins:

1. Run:
```
cf plugins --outdated
```

2. See the output of the previous command, in this example:
```
$ cf plugins --outdated
Searching CF-Community, company-repo for newer versions of installed plugins...
plugin version latest version
coffeemaker 1.1.2 1.2.0
Use 'cf install-plugin' to update a plugin to the latest version.
```
For more information about the `cf plugins` command, see [cf plugins](http://cli.cloudfoundry.org/en-US/cf/plugins.html) in the *Cloud Foundry CLI Reference Guide*.

## Uninstalling a plug-in
To uninstall a plug-in:

1. To view the names of all installed plug-ins, run:
```
cf plugins
```

2. Run:
```
cf uninstall-plugin PLUGIN-NAME
```
Where `PLUGIN-NAME` is the name of the plug-in you want to uninstall.
You must use the name of the plug-in to uninstall it, not the binary filename.
For more information, see [uninstall-plugin](http://cli.cloudfoundry.org/en-US/cf/uninstall-plugin.html) in the *Cloud Foundry CLI Reference Guide*.

## Adding a plug-in repository
To add a plug-in repository:

1. Run:
```
cf add-plugin-repo REPOSITORY-NAME-URL
```
Where `REPOSITORY-NAME-URL` is the URL of the plug-in repository you want to add.
For more information, see [add-plugin-repo](http://cli.cloudfoundry.org/en-US/cf/add-plugin-repo.html) in the *Cloud Foundry CLI Reference Guide*.

## Viewing available plug-in repositories
To view your available plug-in repositories:

1. Run:
```
cf list-plugin-repos
```
For more information, see [list-plugin-repos](http://cli.cloudfoundry.org/en-US/cf/list-plugin-repos.html) in the *Cloud Foundry CLI Reference Guide*.

## Listing all plug-ins by repository
To show all plug-ins from all available repositories:

1. Run:
```
cf repo-plugins
```
For more information, see [repo-plugins](http://cli.cloudfoundry.org/en-US/cf/repo-plugins.html) in the *Cloud Foundry CLI Reference Guide*.

## Troubleshooting
The cf CLI provides the following error messages to help you troubleshoot installation and usage issues. Third party plug-ins provide their own error messages.

### Permission denied
If you receive a `permission denied` error message, you lack required permissions to the plug-in. You must have `read` and `execute` permissions to the plug-in binary file.

### Plug-in command collision
Plug-in names and commands must be unique. The CLI displays an error message if you attempt to install a plug-in with a non unique name or command.
If the plug-in has the same name or command as a currently installed plug-in, you must uninstall the existing plug-in to install the new plug-in.
If the plug-in has a command with the same name as a native cf CLI command or alias, you cannot install the plug-in.