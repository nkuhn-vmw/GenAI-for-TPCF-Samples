# Using an external file system (volume services)
Here are instructions to help you read and write to a mounted file system from your apps.
In Cloud Foundry, a volume service provides a volume so your app can read
or write to a reliable, persistent file system.

**Note** NFS and SMB volume services are available for Linux cells only. These services are not available for Windows cells.

## Prerequisite
Before you can use a volume service with your app, find out if any volume services are available for your app.

1. Log in to the Cloud Foundry Command Line Interface (cf CLI). Run:
```
cf login
```

2. List available NFS volume services. Run:
```
cf marketplace
```
See the following example output of the NFS volume service:
```
cf marketplace
service plans description
nfs Existing Service for connecting to NFS volumes
```

3. Do one of the following:

* **If no NFS volume service exists**: If no volume service that fits your requirements exists, contact your Cloud Foundry administrator. For more information, see [Adding Volume Services to your Deployment](https://docs.cloudfoundry.org/running/deploy-vol-services.html).

* **If an NFS volume service exists**: Continue to [Mount an external file system](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html#mount-external-filesystem).

## Mount an external file system
The following sections describe how to mount an external file system to your app.

### Create and bind a service instance
To use a volume service deployed by your Cloud Foundry administrator, you must first create an instance of the specific volume service that you need.

**Note**
You can also bind volume services using an app manifest. However, app manifests do not support bind configuration. To bind a volume service using an app manifest, you must specify bind configuration when you create the service instance. The releases that support this are `nfs-volume` v1.3.1 and later and `smb-volume` v1.0.0 and later. For more information, see [Services](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#services-block) in *Deploying with App Manifests*.
To create and bind an instance for the volume service:

1. Create a service instance:

* **NFS**: See [Create an NFS volume service](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html#create-nfs).

* **SMB**: See [Create an SMB volume service](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html#create-smb).

1. Bind your service instance to an app:

* **NFS-only**: Bind an NFS service instance to an app. Run:
```
cf bind-service YOUR-APP SERVICE-NAME -c '{"mount":"OPTIONAL-MOUNT-PATH","readonly":true}'
```
The app file operations use the UID of the running app process. For buildpack apps, this UID is always `2000`. For Docker apps, the effective UID is the same as the UID of the process inside the Docker container, except for `root`, which is mapped to `4294967294` outside the Docker container.
Or to use UID/GID mapping:
`cf bind-service YOUR-APP SERVICE-NAME -c '{"uid":"UID","gid":"GID","mount":"OPTIONAL-MOUNT-PATH","readonly":true}'`
Where:

+ `YOUR-APP` is the name of the app for which you want to use the volume service.

+ `SERVICE-NAME` is the name of the volume service instance you created in an earlier step.

+ (Optional) `UID` and `GID` are the UID and GID to use when mounting the share to the app.
The `GID` and `UID` must be positive integer values greater than `0`.
Provide the UID and GID as a JSON string in-line or in a file.
If you omit `uid` and `gid`, the driver skips `mapfs` mounting and performs
only the normal kernel mount of the NFS file system without the performance overhead associated with FUSE mounts.
The key advantage of specifying `UID` and `GID` is that you can specify different values for different apps, so
file permissions can be granted at the app level. If this is not needed, the you can eliminate the performance overhead of `mapfs` by managing permissions on the NFS server.
The user specified by `uid` must have access to the files on the share. When `uid` and `gid` are omitted, the app file operations use the UID of the running app process. For buildpack apps, this UID is always `2000`. For Docker apps, the effective UID is the same as the UID of the process inside the Docker container, except for `root`, which is mapped to `4294967294` outside the Docker container.

**Caution**
Specifying UID and GID values affects performance because the FUSE file system mapfs is used to translate UID and GID values.

+ (Optional) `OPTIONAL-MOUNT-PATH` is a JSON string that indicates that the volume must be mounted to a particular path in your app rather than the default path. Choose a path with a root-level directory that already exists in the container, such as `/home`, `/usr`, or `/var`.

**Important**
Do not specify a `MOUNT-PATH` in the `/app` directory, which is where Cloud Foundry unpacks the droplet. For more information, see [Mount a shared volume in the /app directory](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html#mount-path).

+ (Optional) `"readonly":true` is a JSON string that creates a read-only mount. By default, Volume Services mounts a read-write file system. For read-only mounts, the driver activates attribute caching. This results in fewer attribute RPCs and better performance.
The following example shows binding `my-app` to the `nfs_service_instance` and specifying a read-only volume to be mounted to `/var/volume1`, passing an in-line JSON string:
```
cf bind-service my-app nfs_service_instance -c '{"uid":"1000","gid":"1000","mount":"/var/volume1","readonly":true}'
```

+ **LDAP-only**: Bind an LDAP service to an app. Run:
```
cf bind-service YOUR-APP SERVICE-NAME -c '{"username":"USERNAME","password":"PASSWORD","mount":"OPTIONAL-MOUNT-PATH","readonly":true}'
```
Where:

- `YOUR-APP` is the name of the app for which you want to use the volume service.

- `SERVICE-NAME` is the name of the volume service instance you created in an earlier step.

- `USERNAME` and `PASSWORD` are the user name and password for the LDAP server. If you omit `username` and `password`, the driver skips `mapfs` mounting and performs only the normal kernel mount of the NFS file system without the overhead associated with FUSE mounts.

- (Optional) `OPTIONAL-MOUNT-PATH` is a JSON string that indicates the volume must be mounted to a particular path within your app rather than the default path. Choose a path with a root-level directory that already exists in the container, such as `/home`, `/usr`, or `/var`.

**Important**
Do not specify a `MOUNT-PATH` within the `/app` directory, which is where Cloud Foundry unpacks the droplet. For more information, see [Mount a shared volume in the /app directory](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html#mount-path).

- (Optional) `"readonly":true` is a JSON string that creates a read-only mount. By default, Volume Services mounts a read write file system. For read-only mounts, the driver activates attribute caching. This results in fewer attribute RPCs and better performance.

1. Restage your app. Run:
```
cf restage YOUR-APP
```
Where `YOUR-APP` is the name of the app.

### Access the volume service from your app
To access the volume service from your app, you must know which file path to use in your code.
You can view the file path in the details of the service binding, which are available from the `VCAP_SERVICES` environment variable. See [VCAP\_SERVICES](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#view-env).
To access the volume service from your app:

1. View environment variables for your app. Run:
```
cf env YOUR-APP
```
Where `YOUR-APP` is the name of your app.
The following is example output of the `cf env` command:
```
$ cf env YOUR-APP
"VCAP_SERVICES": {
"nfs": [
{
"credentials": {},
"label": "nfs",
"name": "nfs_service_instance",
"plan": "Existing",
"provider": null,
"syslog_drain_url": null,
"tags": [
"nfs"
],
"volume_mounts": [
{
"container_dir": "/var/vcap/data/153e3c4b-1151-4cf7-b311-948dd77fce64",
"device_type": "shared",
"mode": "rw"
}
]
}
]
}
```

2. Use the properties under `volume_mounts` for any information your app needs.
|
Property
|
Description
|
| --- | --- |
| `container_dir` | String containing the path to the mounted volume that you bound to your app. |
| `device_type` | The NFS volume release. This only supports `shared` devices. A `shared` device represents a distributed file system that can mount on all app instances simultaneously. |
| `mode` | String that informs what type of access your app has to NFS, either read-only, `ro`, or read and write, `rw`.
|

### Mount a shared volume in the /app directory
If you specify a mount inside the `/app` directory, the app might fail to start and parts of the app droplet can be written to the remote file share. This is because Cloud Foundry mounts the volume before moving your compiled app into the droplet.
If your app requires the shared volume to be placed within the `/app` directory, you can use a symbolic link at app startup.
To mount a volume in the `/app` directory:

1. Specify a mount volume in a location outside of the `/app` directory.

2. Create a symbolic link at app startup time, prior to launching the app. For example, run:
```
cf push YOUR-APP -c "ln -s /var/volume1 /app/volume1 && \$HOME/boot.sh"
```
Where `YOUR-APP` is the name of the app.

## Create and use NFS volume services
This section describes how to use the NFS volume service.
Cloud Foundry offers two NFS volume services:

* `nfs`: This volume service provides support for NFS volumes using both v3 and v4.x protocols.

* `nfs-legacy` (deprecated): Although it is deprecated, this volume service is still available due to the difficulty of retiring services. If you use this service, it performs exactly the same mount as the `nfs` service. For information about migrating to `nfs`, see [Migrate `nfs-legacy` Services to `nfs`](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html#migrate).
Both services offer a single plan called `Existing`.

**Note**
NFS is not available on Windows systems.

### Create an NFS volume service
To create an NFS volume service using the `Existing` plan of the `nfs` service:

1. Create an NFS volume service. Run:
```
cf create-service nfs Existing SERVICE-INSTANCE-NAME -c '{"share":"SERVER/SHARE", "version":"NFS-PROTOCOL"}'
```
Where:

* `SERVICE-INSTANCE-NAME` is a name you provide for this NFS volume service instance.

* `SERVER/SHARE` is the NFS address of your server and share.

**Important**
Omit the `:` that usually follows the server name in the address.

* (Optional) `NFS-PROTOCOL` is the NFS protocol you want to use. For example, to use NFSv4, set the version to `4.1`. Valid values are `3`, `4.0`, `4.1` or `4.2`. If you do not specify a `version`, the protocol version used is negotiated between client and server at mount time. This usually causes the latest available version to be used.

**Important**
nfs-volume versions `v7.1.45 - v7.1.47` ship with a recent version of nfs-utils (a dependency of nfs-volume-service). Recent versions of nfs-utils have stricter option parsing. This leads to an issue with environments that configured the `vers=3.0` mount option.
NFSv3 does not utilize a MINOR version, but NFSv4 introduced MINOR versions that can be specified.
This has been mitigated by adding auto-correction logic to the nfsdriver process available with nfs-volume `>= v7.1.48`.

2. Confirm that the NFS volume service appears in your list of services. Run:
```
cf services
```

### Migrate nfs-legacy services to nfs
With the release of NFS Volume Service v1.5.4, the original fuse-based NFS service is deprecated in favor of the later kernel mount-based NFS service. Existing NFS volume service bindings are listed as `nfs-legacy`.
To migrate from `nfs-legacy` to the later `nfs` service,
Cloud Foundry recommends that you recreate and re-bind your `nfs` service instances.
With the release of NFS Volume Service v2.0.0, the `nfs-legacy` service uses the `nfs` service. To avoid being affected when the `nfs-legacy` service is retired, recreate and re-bind your service instances using the `nfs` service.

### Deploy and bind a sample app
This section describes how to deploy a sample app and bind it to the NFS volume service.
To deploy and bind a sample app:

1. Clone the GitHub repository for the sample app into your workspace by running these commands:
```
cd ~/workspace
```
```
git clone https://github.com/cloudfoundry/persi-acceptance-tests.git
```

2. Change into the `persi-acceptance-tests/assets/pora/` directory:
```
cd ~/workspace/persi-acceptance-tests/assets/pora
```

3. Push the `pora` test app by running:
```
cf push pora --no-start
```

4. Bind the service to your app. Run:
```
cf bind-service pora SERVICE-INSTANCE-NAME -c '{"uid":"UID","gid":"GID"}'
```
Where:

* `SERVICE-INSTANCE-NAME`: The name of the volume service instance you created previously.

* `UID` and `GID`: The `UID` and `GID` to use when mounting the share to the app. The NFS driver uses these values in the following ways:

+ When sending traffic to the NFS server, the NFS driver translates the app user ID
and group ID to the `UID` and `GID` values.

+ When returning attributes from the NFS server, the NFS driver translates the
`UID` and `GID` back to the running user UID and default GID.
This allows you to interact with your NFS server as a specific user
while allowing Cloud Foundry to run your app as an arbitrary user.
`UID` and `GID` must be positive integer values.

**Important**
In NFS v2.0.0 and later, `uid` and `gid` values of `0` are no longer permissible because of security concerns.

* (Optional) `mount`: Use this option to specify the path at which volumes mount to the application container.
The default is an arbitrarily-named directory in `/var/vcap/data`.
You can edit this value if your app has specific requirements. For example:
```
cf bind-service pora myVolume -c '{"mount":"/var/path"}'
```

* (Optional) `readonly`: When you run the `cf bind-service` command, Volume Services mounts a read-write file system by default.
You can specify a read-only mount by adding `"readonly":true` to the bind configuration JSON string.

* (Optional) `cache`: When you run the `cf bind-service` command,
Volume Services mounts the remote file system with attribute caching deactivated by default.
You can activate attribute caching using default values by adding `"cache":true`
to the bind configuration JSON string.

5. Start the app. Run:
```
cf start pora
```

6. Confirm the app is running. Run:
```
curl http://pora.YOUR-CF-DOMAIN.com
```
The command returns an instance index for your app.

7. Confirm the app can access the shared volume. Run:
```
curl http://pora.YOUR-CF-DOMAIN.com/write
```
The command writes a file to the share and then reads it back out again.

### Use NFS volume service
This section describes using the NFS volume service.

#### Configure LDAP credentials with service instance creation
If your Cloud Foundry deployment has LDAP activated, you can configure LDAP credentials for your NFS Volume Service instance.
To configure LDAP credentials while creating your NFS Volume Service instance:

1. Specify values for `username` and `password` in the JSON string for your `cf create-service` command:
```
cf create-service nfs PLAN SERVICE-INSTANCE-NAME -c '{"share":"SERVER/SHARE", "username":"USERNAME", "password":"PASSWORD"}'
```
Where:

* `PLAN` is the name of the service plan.

* `SERVICE-INSTANCE-NAME` is a name you provide for this NFS Volume Service instance.

* `SERVER/SHARE` is the NFS address of your server and share.

* `USERNAME` is a user name you provide for this NFS Volume Service instance.

* `PASSWORD` is a password you provide for this NFS Volume Service instance.

#### Specify bind parameters during service instance creation
As of `nfs-volume-release` v1.3.1, you can specify bind parameters in advance, when you create a service instance. Use this option if you bind the service to your app in an app manifest, where bind configuration is not supported.

#### File locking with flock() and lockf()/fcntl()
Apps that use file locking through UNIX system calls such as `flock()` and `fcntl()` or script commands such as `flock` to use the `nfs` service. The `nfs-legacy` service uses a fuse mounting process that does not enforce locks across Diego Cells.

#### Hard links in the NFS service
The mapfs UID mapping layer used by the NFS service does not support hard link operations.
You get a `Function not implemented` error if you try to create a hard link in an NFS share
when `uid` or `username` is specified for the service.
Workarounds for this issue:

* Use symbolic links, `ln -s`, instead of hard links.

* Omit the `uid` and `gid` or the `username` and `password` parameters to mount the share without UID mapping.
For this workaround, the app user must have access to the files on the share.

## Create and use SMB volume services
This section describes how to use a Server Message Block (SMB) volume service. For more information about SMB volume services, see the [Microsoft documentation](https://docs.microsoft.com/en-us/windows/desktop/fileio/microsoft-smb-protocol-and-cifs-protocol-overview) in the Microsoft documentation.

### Create an SMB volume service
Cloud Foundry offers an `smb` volume service.
This volume service provides support for existing SMB shares.
The service offers a single plan called `Existing`.
To create an SMB volume service:

1. Create the service by running:
```
cf create-service smb Existing SERVICE-INSTANCE-NAME -c '{"share":"//SERVER/SHARE", "version":"SMB-VERSION"}'
```
Where:

* `SERVICE-INSTANCE-NAME` is a name you provide for this SMB volume service instance.

* `//SERVER/SHARE` is the SMB address of your server and share.

* (Optional) `SMB-VERSION` is the SMB protocol version you want to use. For example, to use SMB 2.1, set the version to `2.1`. Valid values are `1.0`, `2.0`, `2.1`, or `3.0`. If you do not specify a `version`, the client and server negotiate a protocol version at mount time. The client and server usually select the latest available version.

2. Confirm that the SMB volume service appears in your list of services. Run:
```
cf services
```

### Deploy and bind a sample app
This section describes how to deploy a sample app and bind it to the SMB volume service.
To deploy and bind a sample app:

1. Clone the GitHub repository for the sample app into your workspace. Run:
```
cd ~/workspace
```
```
git clone https://github.com/cloudfoundry/persi-acceptance-tests.git
```

2. Change into the `persi-acceptance-tests/assets/pora/` directory:
```
cd ~/workspace/persi-acceptance-tests/assets/pora
```

3. Push the `pora` test app. Run:
```
cf push pora --no-start
```

4. Bind the service to your app. Run:
```
cf bind-service pora SERVICE-INSTANCE-NAME -c '{"username":"USERNAME","password":"PASSWORD"}'
```
Where:

* `SERVICE-INSTANCE-NAME`: The name of the volume service instance you created previously.

* `USERNAME` and `PASSWORD`: The user name and password to use when mounting the share to the app. This allows you to interact with your SMB server as a specific user while allowing Cloud Foundry to run your app as an arbitrary user.

* (Optional) `mount`: Use this option to specify the path at which volumes mount to the application container. The default is an arbitrarily-named directory in `/var/vcap/data`. You can edit this value if your app has specific requirements. For example, run:
```
cf bind-service pora myVolume -c '{"username":"some-user","password":"some-password","mount":"/var/path"}'
```

* (Optional) `readonly`: When you run the `cf bind-service` command, Volume Services mounts a read-write file system by default. You can specify a read-only mount by adding `"readonly":true` to the bind configuration JSON string.

* (Optional) `domain`: If you use a Windows domain, you can specify a `domain` parameter.

5. Start the app. Run:
```
cf start pora
```

6. Confirm the app is running. Run:
```
curl http://pora.YOUR-CF-DOMAIN.com
```
The command returns an instance index for your app.

7. Confirm the app can access the shared volume. Run:
```
curl http://pora.YOUR-CF-DOMAIN.com/write
```
The command writes a file to the share and then reads it back out again.