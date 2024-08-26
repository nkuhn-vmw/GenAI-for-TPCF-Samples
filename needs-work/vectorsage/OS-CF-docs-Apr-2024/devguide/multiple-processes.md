# Pushing an app with multiple processes
The Cloud Foundry API (CAPI) V3 supports using a single command to push apps that run multiple processes, such as a web app that has a UI process and a worker process. You can push an app with multiple processes using either a manifest or a Procfile.
For more information about processes, see the [CAPI V3 documentation](http://v3-apidocs.cloudfoundry.org/index.html#processes).

## Push an app with multiple processes using a manifest
To push an app with multiple processes using a manifest:

1. Create a file in YAML format that defines a manifest. Include each process with its start command.
This example manifest file defines the app `example-app` with two processes:
```
```yaml
version: 1

- name: example-app
processes:

- type: web
command: bundle exec rackup config.ru -p $PORT
instances: 3

- type: worker
command: bundle exec rake worker:start
health-check-type: process
instances: 2
```
```

1. Push the app with your manifest by running:
```
cf push -f MANIFEST.yml
```
Where `MANIFEST` is the filename of your manifest file.
For more information about defining processes with manifests, see [processes](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#processes) in *App Manifest Attribute Reference*.

## Push an app with multiple processes using a Procfile
Procfile support varies depending on the buildpack you use. For example, the Staticfile buildpack requires a Staticfile instead of a Procfile. For more information, see [Staticfile Buildpack](https://docs.cloudfoundry.org/buildpacks/staticfile/index.html)
To push an app with multiple processes using a Procfile:

1. Create a file named `Procfile` in the root of your app directory. For more information about Procfiles, see the
[CAPI V3 documentation](https://v3-apidocs.cloudfoundry.org/index.html#procfiles).

2. Add each process and its start command to the Procfile. For example:
```
web: bundle exec rackup config.ru -p $PORT
worker: bundle exec rake worker:start
```

3. Push the app by running:
```
cf push APP-NAME
```
Where `APP-NAME` is the name of your app.
By default, the web process has a route and one instance. Other processes have zero instances by default.

## Scale a process
To scale an app process:

1. Run:
```
cf scale APP-NAME --process PROCESS-NAME -i INSTANCE-COUNT
```
Where:

* `APP-NAME` is the name of your app.

* `PROCESS-NAME` is the name of the process you want to scale.

* `INSTANCE-COUNT` is the number of instances to which you want to scale the process.

## View processes
To view the processes running as part of an app:

1. Run:
```
cf app APP-NAME
```
Where `APP-NAME` is the name of your app.
The following example shows return output for an app that has a `web` and a `worker` process:
```
Showing health and status for app example-app in org test / space test as admin...
```
name: example-app
requested state: started
routes: example-app.cloudfoundry.example.com
last uploaded: Thu 15 Sep 02:34:18 UTC 2022
stack: cflinuxfs3
buildpacks:
name version detect output buildpack name
ruby\_buildpack 1.8.57 ruby ruby
type: web
sidecars:
instances: 1/1
memory usage: 1024M
state since cpu memory disk logging details

#0 running 2022-09-15T02:34:27Z 0.3% 36.3M of 1G 90.2M of 1G 0/s of unlimited
type: worker
sidecars:
instances: 2/2
memory usage: 1024M
state since cpu memory disk logging details

#0 running 2022-09-15T02:35:29Z 0.0% 36.1M of 1G 90.2M of 1G 15B/s of unlimited

#1 running 2022-09-15T02:35:29Z 0.0% 36.1M of 1G 90.2M of 1G 15B/s of unlimited

**Important**
To avoid security exposure, ensure that you migrated your apps and custom buildpacks to use the `cflinuxfs4` stack based on Ubuntu 22.04 LTS (Jammy Jellyfish). The `cflinuxfs3` stack is based on Ubuntu 18.04 (Bionic Beaver), which reaches end of standard support in April 2023.