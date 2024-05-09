# Accessing your apps with SSH
The Cloud Foundry Command Line Interface (cf CLI) lets you securely log in to remote host virtual machines (VMs) running Cloud Foundry (Cloud Foundry) app instances. The commands that activate SSH access to apps, and activate, deactivate, and verify permissions for such access are described here.

**Important**
The `cf ssh` command in cf CLI v7 and the `cf v3-ssh` command in cf CLI v6 include the `all_proxy` environment variable, which allows you to specify a proxy server to activate proxying for all requests. For more information, see [ssh](http://cli.cloudfoundry.org/en-US/v7/ssh.html) in the Cloud Foundry CLI Reference Guide and [Use SOCKS5 with cf v3-ssh](https://docs.cloudfoundry.org/cf-cli/http-proxy.html#v3-ssh-socks5) in *Using the cf CLI with a proxy server*.
The cf CLI looks up the `app_ssh_oauth_client` identifier in the Cloud Controller `/v2/info` endpoint, and uses this identifier to query the UAA server for an SSH authorization code. On the target VM side, the SSH proxy contacts the Cloud Controller through the `app_ssh_endpoint` listed in `/v2/info` to confirm permission for SSH access.

**Note** If you have mutual TLS between the Gorouter and app containers, app containers accept incoming communication only from the Gorouter. This disables `cf ssh`. For more information, see the [TLS to Apps and Other Back End Services](https://docs.cloudfoundry.org/concepts/http-routing.html#tls-to-back-end) section of the *HTTP Routing* topic.

## App SSH commands
| cf CLI command | Purpose |
| --- | --- |
| `cf enable-ssh`
`cf disable-ssh`
`cf allow-space-ssh`
`cf disallow-space-ssh` | [Activate and deactivate SSH access](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html#enable-disable-ssh) |
| `cf ssh-enabled`
`cf space-ssh-allowed` | [Verify SSH access permissions](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html#check-ssh-permissions) |
| `cf ssh` | [Log in to an application container with cf SSH](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html#ssh-command) |
| `cf ssh-code` | [App SSH access without cf CLI](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html#other-ssh-access) using non-`cf SSH` tools like `ssh`, `scp`, and `sftp` |

## Activate and deactivate SSH access
A cloud operator can deploy Cloud Foundry to either allow or prohibit app SSH across the entire deployment. For more information, see [Configuring SSH Access for Cloud Foundry](https://docs.cloudfoundry.org/running/config-ssh.html).
Within a deployment that permits SSH access to apps, Space Developers can activate or deactivate SSH access to individual apps, and Space Managers can activate or deactivate SSH access to all apps running within a space.
You must restart your app after enabling SSH access.

### Configuring SSH access at the app level
[cf enable-ssh](http://cli.cloudfoundry.org/en-US/cf/enable-ssh.html) activates SSH access to all instances of an app:
```
$ cf enable-ssh MY-AWESOME-APP
```
[cf disable-ssh](http://cli.cloudfoundry.org/en-US/cf/disable-ssh.html) deactivates SSH access to all instances of an app:
```
$ cf disable-ssh MY-AWESOME-APP
```

### Configuring SSH access at the space level
[cf allow-space-ssh](http://cli.cloudfoundry.org/en-US/cf/allow-space-ssh.html) allows SSH access into all apps in a space:
```
$ cf allow-space-ssh SPACE-NAME
```
[cf disallow-space-ssh](http://cli.cloudfoundry.org/en-US/cf/disallow-space-ssh.html) disallows SSH access into all apps in a space:
```
$ cf disallow-space-ssh SPACE-NAME
```

## Verify SSH permissions
[cf ssh-enabled](http://cli.cloudfoundry.org/en-US/cf/ssh-enabled.html) verifies whether an app is accessible with SSH:
```
$ cf ssh-enabled MY-AWESOME-APP
ssh support is disabled for 'MY-AWESOME-APP'
```
[cf space-ssh-allowed](http://cli.cloudfoundry.org/en-US/cf/space-ssh-allowed.html) verifies whether all apps running within a space are accessible with SSH:
```
$ cf space-ssh-allowed SPACE-NAME
ssh support is enabled in space 'SPACE-NAME'
```

## Log in to an application container with cf SSH
If SSH access is allowed at the deployment, space, and app level, you can run the `cf ssh APP-NAME` command to start an interactive SSH session with a VM hosting an app. By default, the command accesses the container running the first instance of the app, the instance with index **0**.
```
$ cf ssh MY-AWESOME-APP
```
When logged into a VM hosting an app, you can use tools like the Cloud Foundry Diego Operator Toolkit (cfdot) to run app status diagnostics. For more information, see the [cfdot](https://github.com/cloudfoundry/cfdot) repository on GitHub and the [cfdot CLI](https://docs.cloudfoundry.org/running/monitoring-test.html#cfdot) section of the *Monitoring and Testing Diego Components* topic.

### Common cf SSH flags
You can tailor [cf ssh](http://cli.cloudfoundry.org/en-US/cf/ssh.html) commands with the following flags, most of which mimic flags for the UNIX or Linux `ssh` command. Run the `cf ssh --help` command for more details.

* The `-i` flag targets a specific instance of an app. To log in to the VM container hosting the third instance, `index=2`, of MY-AWESOME-APP, run:
```
$ cf ssh MY-AWESOME-APP -i 2
```

* The `-L` flag activates local port forwarding, binding an output port on your machine to an input port on the app VM. Pass in a local port, and your app VM port and port number, all colon-separated. You can prepend your local network interface, or use the default `localhost`.
```
$ cf ssh MY-AWESOME-APP -L [LOCAL-NETWORK-INTERFACE:]LOCAL-PORT:REMOTE-HOST-NAME:REMOTE-HOST-PORT
```

* The `-N` flag skips returning a command prompt on the remote machine. This sets up local port forwarding if you do not need to run commands on the host VM.

* The `--process` flag in cf CLI v7 allows you to SSH into the container for a specific process running as part of your app.

* The `--request-pseudo-tty` and `--force-pseudo-tty` flags allow you run an SSH session in pseudo-tty mode rather than generate terminal line output.

## SSH session environment
To make the environment of your interactive SSH session match the environment of
your buildpack-based app, with the same environment variables and working directory, run
the following command after starting the session:
```
/tmp/lifecycle/shell
```
After running the previous command, the value of the `VCAP_APPLICATION` environment variable differs
slightly from its value in the environment of the app process, because it does not have the `host`,
`instance_id`, `instance_index`, or `port` fields set. These fields are available in other
environment variables, as described in
[VCAP\_APPLICATION](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#VCAP-APPLICATION) in

*Cloud Foundry Environment Variables*.

## App SSH access without cf CLI
In addition to `cf ssh`, you can use other SSH clients such as `ssh`, `scp`, or `sftp` to access
your app, if you have SSH permissions.
Follow one of these procedures to securely connect to an app instance by logging in with a
specially-formed user name that passes information to the SSH proxy running on the host VM. For the
password, use a one-time SSH authorization code generated by
[cf ssh-code](http://cli.cloudfoundry.org/en-US/cf/ssh-code.html).

* [Access app SSH using process GUID](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html#process-guid)

* [Access app sSH using app GUID](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html#app-guid)

### Access app SSH using process GUID

1. Query the `/v2/info` endpoint of the Cloud Controller in your deployment. Record the domain name
and port number of the `app_ssh_endpoint` field, and the `app_ssh_host_key_fingerprint` field. You
can compare the `app_ssh_host_key_fingerprint` with the fingerprint returned by the SSH proxy on
your target VM. For example:
```
$ cf curl /v2/info
{
...
"app_ssh_endpoint": "ssh.example.com:2222",
"app_ssh_host_key_fingerprint": "a6:14:c0:ea:42:07:b2:f7:53:2c:0b:60:e0:00:21:6c",
...
}
```
In this example:

* The domain name is `ssh.example.com`.

* The port number is `2222`.

* The fingerprint is `a6:14:c0:ea:42:07:b2:f7:53:2c:0b:60:e0:00:21:6c`.

2. Run:
```
ssh -p PORT-NUMBER cf:$(cf curl /v3/apps/$(cf app APP-NAME --guid)/processes | jq -r '.resources[] | select(.type=="web") | .guid')/0@SSH-ENDPOINT
```
Where:

* `PORT-NUMBER` is the port number of the `app_ssh_endpoint` field that you recorded in an earlier step.

* `APP-NAME` is the name of your target app.

* `SSH-ENDPOINT` is the domain name of the `app_ssh_endpoint` field that you recorded in an earlier step.
For example:
```
ssh -p 2222 cf:$(cf curl /v3/apps/$(cf app my-app --guid)/processes | jq -r '.resources[] | select(.type=="web") | .guid')/0@ssh.example.com
```

3. Run `cf ssh-code` to obtain a one-time authorization code that substitutes for an SSH password.
You can run `cf ssh-code | pbcopy` to copy the code to the clipboard. For example:
```
$ cf ssh-code
E1x89n
```

4. When the SSH proxy reports its RSA fingerprint, confirm that it matches the
`app_ssh_host_key_fingerprint` recorded previously. When prompted for a password, paste in the
authorization code returned by `cf ssh-code`. For example:
```
$ ssh -p 2222 cf:abcdefab-1234-5678-abcd-1234abcd1234/0@ssh.MY-DOMAIN.com
The authenticity of host '[ssh.example.com]:2222 ([203.0.113.5]:2222)' can't be established.
RSA key fingerprint is a6:14:c0:ea:42:07:b2:f7:53:2c:0b:60:e0:00:21:6c.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[ssh.example.com]:2222 [203.0.113.5]:2222' (RSA) to the list of known hosts.
cf:d0a2e11d-e6ca-4120-b32d-140@ssh.ketchup.cf-app.com's password:
vcap@ce4l5164kws:~$
```
You have now securely connected to the app instance.

### Access app SSH using app GUID

1. Display the GUID of your target app by running:
```
cf app APP-NAME --guid`
```
Where `APP-NAME` is the name of the app.
For example:
```
$ cf app my-app --guid
abcdefab-1234-5678-abcd-1234abcd1234
```

2. Query the `/v2/info` endpoint of the Cloud Controller in your deployment. Record the domain name
and port number of the `app_ssh_endpoint` field, and the `app_ssh_host_key_fingerprint` field. You can compare the `app_ssh_host_key_fingerprint` with the fingerprint returned by the SSH proxy on your target VM. For example:
```
$ cf curl /v2/info
{
...
"app_ssh_endpoint": "ssh.example.com:2222",
"app_ssh_host_key_fingerprint": "a6:14:c0:ea:42:07:b2:f7:53:2c:0b:60:e0:00:21:6c",
...
}
```
In this example:

* The domain name is `ssh.example.com`.

* The port number is `2222`.

* The fingerprint is `a6:14:c0:ea:42:07:b2:f7:53:2c:0b:60:e0:00:21:6c`.

3. Run `cf ssh-code` to obtain a one-time authorization code that substitutes for an SSH password. You can run `cf ssh-code | pbcopy` to copy the code to the clipboard. For example:
```
$ cf ssh-code
E1x89n
```

4. Run your `ssh` or other command to connect to the app instance.

* SSH into the container hosting the first instance of your app by running:
```
ssh -p `SSH-PORT` cf:APP-GUID/APP-INSTANCE-INDEX@SSH-ENDPOINT
```
Where:

+ `SSH-PORT` is the port number recorded in earlier steps.

+ `APP-GUID` comes from earlier steps.

+ `APP-INSTANCE-INDEX` is the index of the instance that you want to access.

+ `SSH-ENDPOINT` comes from the earlier steps and is in the form `ssh.MY-DOMAIN.com`.
For example:
```
$ ssh -p 2222 cf:abcdefab-1234-5678-abcd-1234abcd1234/0@ssh.example.com
```

* Or you can use `scp` to transfer files by running one of the following commands:
```
scp -P `SSH-PORT` -o User=cf:APP-GUID/APP-INSTANCE-INDEX ssh.MY-DOMAIN.com:REMOTE-FILE-TO-RETRIEVE LOCAL-FILE-DESTINATION
```
```
scp -P `SSH-PORT` -o User=cf:APP-GUID/APP-INSTANCE-INDEX LOCAL-FILE-TO-COPY ssh.MY-DOMAIN.com:REMOTE-FILE-DESTINATION
```

* Or you can use `ssh` piped with `cat` to transfer the file:
```
cat local_file_path | cf ssh MY-AWESOME-APP -c "cat > remote_file_path"
```

5. When the SSH proxy reports its RSA fingerprint, confirm that it matches the `app_ssh_host_key_fingerprint` recorded previously. When prompted for a password, paste in the authorization code returned by `cf ssh-code`, for example:
```
$ ssh -p 2222 cf:abcdefab-1234-5678-abcd-1234abcd1234/0@ssh.MY-DOMAIN.com
The authenticity of host '[ssh.MY-DOMAIN.com]:2222 ([203.0.113.5]:2222)' can't be established.
RSA key fingerprint is a6:14:c0:ea:42:07:b2:f7:53:2c:0b:60:e0:00:21:6c.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '[ssh.MY-DOMAIN.com]:2222 [203.0.113.5]:2222' (RSA) to the list of known hosts.
cf:d0a2e11d-e6ca-4120-b32d-140@ssh.ketchup.cf-app.com's password:
vcap@ce4l5164kws:~$
```
You have now securely connected to the app instance.

## SSH proxy security configuration
The SSH proxy has these SSH security configuration by default:
| Security parameter | Values |
| --- | --- |
| Ciphers | `chacha20-poly1305@openssh.com`
`aes128-gcm@openssh.com`
`aes256-ctr`
`aes192-ctr`
`aes128-ctr` |
| MACs | `hmac-sha2-256-etm@openssh.com`
`hmac-sha2-256` |
| Key exchanges | `curve25519-sha256@libssh.org` |
The `cf ssh` command is compatible with this security configuration. If you use a different SSH client to access apps over SSH, you can ensure that you configure your client to be compatible with these ciphers, MACs, and key exchanges. For more information about other SSH clients, see [App SSH access without cf CLI](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html#other-ssh-access).
Cloud Foundry deployment operators can also change these default values in the SSH proxy configuration. Changing these default values might require a change to the SSH client configuration.

## Proxy to container authentication
A second layer of SSH security runs within each container. When the SSH proxy attempts to handshake with the SSH daemon inside the target container, it uses the following fields associated with the `diego-ssh` key in its route to the app instance. This inner layer works invisibly and requires no user action, but is described here to complete the SSH security picture.

### CONTAINER\_PORT (required)
`container_port` indicates which port inside the container the SSH daemon is listening on. The proxy attempts to connect to host side mapping of this port after authenticating the client.

### HOST\_FINGERPRINT (optional)
When present, `host_fingerprint` declares the expected fingerprint of the SSH daemon’s host public key. When the fingerprint of the actual target’s host key does not match the expected fingerprint, the connection is stopped. The fingerprint must only contain the hex string generated by `ssh-keygen -l`.

### USER (optional)
`user` declares the user ID to use during authentication with the container’s SSH daemon. While this is not a required part of the routing data, it is required for password authentication and might be required for public key authentication.

### PASSWORD (optional)
`password` declares the password to use during password authentication with the container’s SSH daemon.

### PRIVATE\_KEY (optional)
`private_key` declares the private key to use when authenticating with the container’s SSH daemon. If present, the key must be a PEM encoded RSA or DSA public key.

#### Example app process
```
{
"process\_guid": "ssh-process-guid",
"domain": "ssh-experiments",
"rootfs": "preloaded:cflinuxfs3",
"instances": 1,
"start\_timeout": 30,
"setup": {
"download": {
"artifact": "diego-sshd",
"from": "http://file-server.service.cf.internal.example.com:8080/v1/static/diego-sshd/diego-sshd.tgz",
"to": "/tmp",
"cache\_key": "diego-sshd"
}
},
"action": {
"run": {
"path": "/tmp/diego-sshd",
"args": [
"-address=0.0.0.0:2222",
"-authorizedKey=ssh-rsa ..."
],
"env": [],
"resource\_limits": {}
}
},
"ports": [ 2222 ],
"routes": {
"diego-ssh": {
"container\_port": 2222,
"private\_key": "PEM encoded PKCS#1 private key"
}
}
}
```

**Important**
To avoid security exposure, migrate your apps and custom buildpacks to use the `cflinuxfs4` stack based on Ubuntu 22.04 LTS (Jammy Jellyfish). The `cflinuxfs3` stack is based on Ubuntu 18.04 (Bionic Beaver), which reaches end of standard support in April 2023.

### Daemon discovery
To be accessible through the SSH proxy, containers must host an SSH daemon, expose it through a mapped port, and advertise the port in a `diego-ssh` route. If a proxy cannot find the target process or a route, user authentication fails.
```
"routes": {
"diego-ssh": { "container_port": 2222 }
}
```
The Diego system generates the appropriate process definitions for Cloud Foundry apps to reflect the policies in effect.