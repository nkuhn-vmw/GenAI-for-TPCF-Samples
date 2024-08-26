# Pushing apps with sidecar processes
You can run additional processes in the same container as your app. These additional processes
are called sidecar processes, or sidecars. An example of a sidecar is an Application Performance
Monitoring (APM) tool.

**Important**
The cf CLI v6 commands described in this topic are unsupported, but are supported in cf CLI v7. The latest supported cf CLI release is cf CLI v8. To upgrade to cf CLI v7, see [Upgrading to cf CLI v7](https://docs.cloudfoundry.org/cf-cli/v7.html). To upgrade to cf CLI v8, see [Upgrading to cf CLI v8](https://docs.cloudfoundry.org/cf-cli/v8.html).

**Note** This feature requires that your Cloud Foundry deployment uses capi-release 1.790 or later.

## About sidecars
When you provide a sidecar for your app,
Cloud Foundry packages the required code and
configuration needed to run the sidecar and app in the same droplet. It deploys this droplet in a
single container on Diego. Both processes within the container undergo health checks independently.
You can push sidecar processes with your app by using one of two methods:

* Using an app manifest. For instructions, see [Push an app with a sidecar Using an app manifest](https://docs.cloudfoundry.org/devguide/sidecars.html#create).

* With a custom buildpack. For instructions, see [Sidecar buildpacks](https://docs.cloudfoundry.org/buildpacks/sidecar-buildpacks.html).
For additional information about sidecars, see [Sidecars](http://v3-apidocs.cloudfoundry.org/version/release-candidate/#sidecars) in the
Cloud Foundry API (CAPI) documentation.
For sample apps that use sidecars, see the
[capi-sidecar-samples](https://github.com/cloudfoundry-samples/capi-sidecar-samples) repository on
GitHub. These sample apps use an app manifest.

## Use cases
You can use sidecars for processes that depend on each other or must run in the same container.
For example, you can use sidecars for processes that must:

* Communicate over a UNIX socket or through localhost

* Share the same file system

* Be scaled and placed together

* Have fast interprocess communication

## Limitations
Sidecars have these limitations:

* The start and stop order of app processes and their sidecars is undefined.

* App processes and sidecars are codependent. If either fails or exits, the other does also.

* Sidecars are not independently scalable. Sidecars share resources with the main app process and other sidecars within the container.

* Sidecars only support PID-based health checks. HTTP health checks for sidecars are not supported.

## Requirements for Java apps
These sections describe several requirements that are specific to pushing sidecars with Java apps.

### Reserving memory
You must allocate memory to the sidecar. If you do not, the Java buildpack allocates all of the
available memory to the app. As a result, the sidecar does not have enough memory and the app fails
to start.
To allocate memory to the sidecar, use the `memory` property in the app manifest. For example:
```
sidecars:

- name: SIDECAR-NAME
process_types: [ 'PROCESS-TYPES' ]
command: START-COMMAND
memory: 256MB
```
Where:

* `SIDECAR-NAME` is a name you give your sidecar.

* `PROCESS-TYPES` is a list of app processes for the sidecar to attach to, such as `web` or `worker`. You can attach multiple sidecars to each process type your app uses.

* `START-COMMAND` is the command used to start the sidecar. For example, `./binary` or `java -jar java-file.jar`.
You must also allocate memory to sidecars that you push with a custom buildpack.
For more information, see [Sidecar buildpacks](https://docs.cloudfoundry.org/buildpacks/sidecar-buildpacks.html).

### Packaging binaries
If your sidecar is a binary file rather than a set of buildable source files, then you must package the binary file with your Java app.
In some cases, the Java buildpack requires you to push a `.jar` file. If this is the case with your app, you must include the sidecar binary in the `.jar` file.
To package the sidecar binary with the `.jar` file, run:
```
zip JAR -u SIDECAR-BINARY
```
Where:

* `JAR` is your `.jar` file.

* `SIDECAR-BINARY` is your sidecar binary.
For more information about packaging assets with your Java app, see [Cloud Foundry documentation](https://docs.cloudfoundry.org/buildpacks/java/java-tips.html).

## Push an app with a sidecar using an app manifest
These sections explain how to push an app with a sidecar using an app manifest. For an example that you can try yourself, see [Sidecar tutorial](https://docs.cloudfoundry.org/devguide/sidecars.html#tutorial).
When pushing a Java app, follow the requirements listed in [Requirements for Java Apps](https://docs.cloudfoundry.org/devguide/sidecars.html#java).

### Prerequisites
Before you can push an app with a sidecar with an app manifest, you must have:

* An app that is running or ready to be pushed.

* A file that Cloud Foundry can run inside the application container as a sidecar process. For example, an executable binary, a Java .jar file, or Ruby scripts.

### Procedure
To push an app with a sidecar:

1. Create an app or use an existing app. To create an app:

* If you are using cf CLI v7, run:
```
cf create-app APP-NAME
```
Where `APP-NAME` is the name you give your app.

* If you are using cf CLI v6, run:
```
cf v3-create-app APP-NAME
```
Where `APP-NAME` is the name you give your app.

2. Create a manifest file in the root directory of your app, such as `manifest.yml`. Otherwise, use an existing manifest file for your app. For more information, see [Deploying with app manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html).

3. Add the following values to your app manifest file under the `applications` key:
```
sidecars:

- name: SIDECAR-NAME
process_types: [ 'PROCESS-TYPES' ]
command: START-COMMAND
```
Where:

* `SIDECAR-NAME` is a name you give your sidecar.

* `PROCESS-TYPES` is a list of app processes for the sidecar to attach to, such as `web` or `worker`. You can attach multiple sidecars to each process type your app uses.

* `START-COMMAND` is the command used to start the sidecar. For example, `./binary` or `java -jar java-file.jar`.
This example manifest file includes multiple sidecars:
```

---
applications:

- name: my-app
sidecars:

- name: authenticator
process_types: [ 'web', 'worker' ]
command: bundle exec run-authenticator

- name: performance monitor
process_types: [ 'web' ]
command: bundle exec run-performance-monitor
```

4. To apply the manifest file to your app:

* If you are using cf CLI v7, run:
```
cf apply-manifest -f PATH-TO-MANIFEST
```
Where `PATH-TO-MANIFEST` is the path to your manifest file.

* If you are using cf CLI v6, run:
```
cf v3-apply-manifest -f PATH-TO-MANIFEST
```
Where `PATH-TO-MANIFEST` is the path to your manifest file.

5. To push your app:

* If you are using cf CLI v7, run:
```
cf push APP-NAME
```
Where `APP-NAME` is the name of your app.

* If you are using cf CLI v6, run:
```
cf v3-push APP-NAME
```
Where `APP-NAME` is the name of your app.

## Sidecar tutorial
You can explore sidecars using the app in the [capi-sidecar-samples](https://github.com/cloudfoundry-samples/capi-sidecar-samples) repository on GitHub. The following sections describe the app, how to build and push the app, and some ways to observe the app and its processes after pushing.

**Important**
In this tutorial, you are pushing the Ruby sample app. You can also follow this tutorial for a Java app using the `sidecar-dependent-java-app` and `push_java_app_with_binary_sidecar.sh` in the samples repository. When pushing a Java app, follow the requirements listed in [Requirements for Java apps](https://docs.cloudfoundry.org/devguide/sidecars.html#java).

### About the sample app
The [capi-sidecar-samples](https://github.com/cloudfoundry-samples/capi-sidecar-samples) repository contains:

* **A simple Ruby app**: This app is named `sidecar-dependent-app`. It includes a `/config` endpoint that calls to the sidecar and prints the response, as shown in this code snippet:
```
get '/config' do
puts "Sending a request to the config-server sidecar at localhost:#{ENV['CONFIG_SERVER_PORT']}/config/"
response = Typhoeus.get("localhost:#{ENV['CONFIG_SERVER_PORT']}/config/")
puts "Received #{response.body} from the config-server sidecar"
response.body
end
```

* **A Golang sidecar**: The `config-server-sidecar` produces a `config-server` binary. It provides apps with their required configuration over its `/config` endpoint. It also accepts connections only over localhost on the `CONFIG_SERVER_PORT` port. This means the sidecar must be co-located in the same container as the app, so that it shares the same network namespace as the main app.
The following diagram illustrates the app architecture:
![App Process and Sidecar Process are inside an App Container, which is inside a Diego cell.](https://docs.cloudfoundry.org/devguide/images/sidecar-diagram.png)

### Push the app and sidecar
If you do not have Go installed, download the `config-server_linux_x86-64` binary from [CAPI Sidecar sample releases](https://github.com/cloudfoundry-samples/capi-sidecar-samples/releases) in the `capi-sidecar-samples` repository in GitHub.
To push the app and sidecar:

1. In a terminal window, clone the Git repository to your workspace by running:
```
git clone https://github.com/cloudfoundry-samples/capi-sidecar-samples.git
```

2. Go to the `config-server-sidecar` directory.

3. Build the binary for the sidecar by running:
```
GOOS=linux GOARCH=amd64 go build -o config-server .
```

4. To create the app:

* If you are using cf CLI v7, run:
```
cf create-app sidecar-dependent-app
```

* If you are using cf CLI v6, run:
```
cf v3-create-app sidecar-dependent-app
```

5. Go to the `sidecar-dependent-app` directory.

6. Open and review the `manifest.yml` file. Under `sidecars`, the sidecar is specified with a name, process type, and start command. Under `env`, an environment variable defines the port on which the app and sidecar communicate.

7. To apply the manifest to the app:

* If you are using cf CLI v7, run:
```
cf apply-manifest
```

* If you are using cf CLI v6, run:
```
cf v3-apply-manifest
```

8. To push the app:

* If you are using cf CLI v7, run:
```
cf push sidecar-dependent-app
```

* If you are using cf CLI v6, run:
```
cf v3-push sidecar-dependent-app
```
After you push the app, you can further explore it in [View the processes running in the container](https://docs.cloudfoundry.org/devguide/sidecars.html#view-processes) and [View the web URL and app logs](https://docs.cloudfoundry.org/devguide/sidecars.html#view-logs).

### View the processes running in the container
To view the app and sidecar process running in the container:

1. SSH into the application container by running:
```
cf ssh sidecar-dependent-app
```

2. To see both the `rackup` process for the main app and `config-server` process for the sidecar, run:
```
ps aux
```
The output you might see resembles this example output:
```
vcap@f00949bd-6601-4731-6f7e-e859:~$ ps aux
USER PID %CPU %MEM VSZ RSS TTY STAT START TIME COMMAND
root 1 0.0 0.0 1120 0 ? S 22:17 0:00 /tmp/garden-init
vcap 7 0.0 0.0 106716 4508 ? S 22:17 0:00 ./config-server
vcap 13 0.0 0.1 519688 35412 ? S 22:17 0:00 /home/vcap/deps/0/vendor_bundle/ruby/2.4.0/bin/rackup config.ru -p 8080
vcap 24 0.0 0.0 116344 10792 ? S 22:17 0:00 /tmp/lifecycle/diego-sshd --allowedKeyExchanges= --address=0.0.0.0:2222 --allowUnauthenticatedClients=false --inhe
root 82 0.0 0.0 108012 4548 ? S 22:17 0:00 /etc/cf-assets/healthcheck/healthcheck -port=8080 -timeout=1000ms -liveness-interval=30s
vcap 215 0.3 0.0 70376 3756 pts/0 S 23:12 0:00 /bin/bash
vcap 227 0.0 0.0 86268 3116 pts/0 R 23:12 0:00 ps aux
```

3. To see that the sidecar is listening on the port specified by `CONFIG_SERVER_PORT` and that the main `ruby` process is connected to it, run:
```
lsof -i | grep $CONFIG_SERVER_PORT
```
The output you see might resemble this example output:
```
vcap@f00949bd-6601-4731-6f7e-e859:~$ lsof -i | grep $CONFIG_SERVER_PORT
config-se 7 vcap 3u IPv4 17265901 0t0 TCP *:8082 (LISTEN)
config-se 7 vcap 5u IPv4 17265992 0t0 TCP localhost:8082->localhost:42266 (ESTABLISHED)
ruby 13 vcap 11u IPv4 17274965 0t0 TCP localhost:42266->localhost:8082 (ESTABLISHED)
```

### View the web URL and app logs
To view the web URL and logs for the app:

1. In a browser, go to the `config` endpoint of the `sidecar-dependent-app`. For example: `https://sidecar-dependent-app.example.com/config`.

2. See that the browser displays `Scope` and `Password` information. This is the configuration that the app fetches from the `config-server` sidecar.

3. Begin streaming logs for the app by running:
```
cf logs sidecar-dependent-app
```

4. In your browser, refresh the `/config` endpoint page and observe that the log stream in your terminal displays logs for both the sidecar and the main app process.

5. In a separate terminal from your log stream, SSH into the application container by running:
```
cf ssh sidecar-dependent-app
```

6. Stop the sidecar process by running:
```
kill -9 $(pgrep config-server)
```

7. View the output in the terminal where you are streaming the app logs. The app logs indicate that the sidecar process failed and that Diego restarted the application container. For example:
```
2019-04-17T16:48:55.41-0700 [API/0] OUT App instance exited with guid
21df1eb8-f25d-43b2-990b-c1a417310553 payload:
{"instance"=>"a8db0eed-7371-4805-5ad3-4596", "index"=>0,
"cell_id"=>"86808ce7-afc2-47da-9e79-522a62a48cff", "reason"=>"CRASHED",
"exit_description"=>"APP/PROC/WEB/SIDECAR/CONFIG-SERVER: Exited with status 137",
"crash_count"=>1, "crash_timestamp"=>1555544935367052708,
"version"=>"50892dcb-274d-4cf6-b944-3eda1e000283"}
```