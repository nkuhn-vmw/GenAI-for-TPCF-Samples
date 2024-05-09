# Configuring the production server for Cloud Foundry apps
You can configure a production server for your apps in Cloud Foundry.
When you deploy an app, Cloud Foundry determines the command that is used to start the app through the following process:

1. If you use the command `cf push -c COMMAND`, then Cloud Foundry uses `COMMAND` to start the app.

2. If you create a file called a Procfile, Cloud Foundry uses Procfile to configure the command that launches the app.
See [About Procfiles](https://docs.cloudfoundry.org/buildpacks/prod-server.html#procfile).

3. If you do not use `cf push -c COMMAND` and do not create a Procfile, then Cloud Foundry does one of the following,
depending on the buildpack:

* Uses a default start command.

* Fails to start the app and shows a warning that the app is missing a Procfile.

## Procfiles
Use a Procfile to specify a start command for buildpacks when a default start command is not provided.
Some buildpacks use Python to work on a variety of frameworks and do not attempt to provide a default start command.
Another reason to use a Procfile is to configure a production server for web apps.
When you use a Procfile, you declare required runtime processes, and called process types, for your web app.
Process managers in a server use the process type to run and manage the workload.
In a Procfile, you declare one process type per line and use the following syntax:
```
PROCESS-TYPE: COMMAND
```
Where:

* `PROCESS-TYPE` is `web`. A `web` process handles HTTP traffic.

* `COMMAND` is the command line to launch the process.
For example, a Procfile with the following content starts the launch script created by the build process for a Java app:
```
web: build/install/MY-PROJECT-NAME/bin/MY-PROJECT-NAME
```
Procfile support is integrated into the [buildpack lifecycle](https://github.com/cloudfoundry/buildpackapplifecycle).
However, due to differing behavior of buildpacks, it might not be suitable with all buildpacks.
Procfiles can be used with the
following buildpacks:

* [Binary buildpack](https://docs.cloudfoundry.org/buildpacks/binary/)

* [.NET Core buildpack](https://docs.cloudfoundry.org/buildpacks/dotnet-core/)

* [Go buildpack](https://docs.cloudfoundry.org/buildpacks/go/)

* [NGINX buildpack](https://docs.cloudfoundry.org/buildpacks/nginx/)

* [Node.js buildpack](https://docs.cloudfoundry.org/buildpacks/node/)

* [Python buildpack](https://docs.cloudfoundry.org/buildpacks/python/)

* [R buildpack](https://docs.cloudfoundry.org/buildpacks/r/)

* [Ruby buildpack](https://docs.cloudfoundry.org/buildpacks/ruby/)

## Specifying a web server
Follow these steps to specify a web server using a Procfile.
For more information about configuring a web server for Rails apps, see [Configuring a Ruby web server](https://docs.cloudfoundry.org/buildpacks/prod-server.html#config-ruby).

1. Create a blank file with a command line for a `web` process type.

2. Save it as a file named `Procfile` with no extension in the root directory of your app.

3. Push your app.

## Configuring a Ruby web server
Cloud Foundry uses the default standard Ruby web server library WEBrick for Ruby and Ruby on Rails apps.
However, Cloud Foundry can support a more robust production web server. For example, Phusion Passenger, Puma, Thin, or Unicorn.
To instruct Cloud Foundry to use a web server other than WEBrick, use the following steps:

1. Add the gem for the web server to your Gemfile.

2. In the `config` directory of your app, create a new configuration file or modify an existing file.
See your web server documentation for how to configure this file.
The following example uses the Puma web server:
```

# config/puma.rb
threads 8,32
workers 3
on_worker_boot do

# things workers do
end
```

3. In the root directory of your app, create a Procfile and add a command line for a `web` process type that points to your web server.
For information about configuring the specific command for a process type, see your web server documentation.
The following example shows a command that starts a Puma web server and specifies the app runtime environment, TCP port, paths to the server state information, and configuration files:
```
web: bundle exec puma -e $RAILS_ENV -p 1234 -S ~/puma -C config/puma.rb
```