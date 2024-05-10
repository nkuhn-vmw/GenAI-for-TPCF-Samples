# Backing up with BOSH Backup and Restore
This topic describes how to use BOSH Backup and Restore (BBR) to back up a BOSH deployment or BOSH Director.
Follow the steps below to back up a BOSH Director, a BOSH deployment, or both.
To perform a restore, see [Restoring with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/restore.html).

## Prerequisites
Before using the result of the backup to restore to a destination environment,
verify that the current environment and the destination environment are compatible.
For information, see [Compatibility of restore](https://docs.cloudfoundry.org/bbr/restore.html#compatibility).

## Connect to your jumpbox
To back up a BOSH Director or BOSH deployment using BBR, you need to establish a
connection to your jumpbox in one of the ways below:

* [Option 1: Connect with SSH](https://docs.cloudfoundry.org/bbr/backup.html#ssh)

* [Option 2: Connect with BOSH\_ALL\_PROXY](https://docs.cloudfoundry.org/bbr/backup.html#bosh-all-proxy)
For more information about the jumpbox, see [Installing BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/installing.html).

### Option 1: Connect with SSH
To connect to your jumpbox using the command line interface (CLI), run:
```
ssh -i PATH-TO-KEY JUMPBOX-USERNAME@JUMPBOX-ADDRESS
```
Where:

* `PATH-TO-KEY` is the local path to your private key file for the jumpbox host.

* `JUMPBOX-USERNAME` is your jumpbox username.

* `JUMPBOX-ADDRESS` is the IP address or hostname of the jumpbox.

**Note**
If you connect to your jumpbox with SSH, you must run the BBR commands in this topic from inside your jumpbox.

### Option 2: Connect with BOSH\_ALL\_PROXY
You can use the environment variable `BOSH_ALL_PROXY` to open an SSH tunnel with
SOCKS5 to the jumpbox.
This tunnel enables you to forward requests from your local machine to the BOSH
Director through the jumpbox.
When `BOSH_ALL_PROXY` is set, the BBR CLI uses its value to forward
requests to the BOSH Director.

**Note**
For the following procedures to work, ensure the SOCKS port is not already in use by a different tunnel or process.
To connect with `BOSH_ALL_PROXY`, follow one of the below procedures:

* **To establish the tunnel separate from the BOSH CLI:**

1. Establish the tunnel and make it available on a local port by running:
`ssh -4 -D SOCKS-PORT -fNC JUMPBOX-USERNAME@JUMPBOX-ADDRESS -i JUMPBOX-KEY-FILE -o ServerAliveInterval=60`
Where:

+ `SOCKS-PORT` is the local SOCKS port.

+ `JUMPBOX-USERNAME` is your jumpbox username.

+ `JUMPBOX-ADDRESS` is the IP address or hostname of the jumpbox.

+ `JUMPBOX-KEY-FILE` is the local SSH private key for accessing the jumpbox.

2. Provide the BOSH CLI with access to the tunnel using the `BOSH_ALL_PROXY` environment variable
by running:
`export BOSH_ALL_PROXY=socks5://localhost:SOCKS-PORT`
Where `SOCKS-PORT` is your local SOCKS port.

* **To establish the tunnel using the BOSH CLI:**
Provide the BOSH CLI with the necessary SSH credentials to create the tunnel by
running:
```
export BOSH_ALL_PROXY=ssh+socks5://JUMPBOX-USERNAME@JUMPBOX-ADDRESS:SOCKS-PORT?private-key=JUMPBOX-KEY-FILE
```
Where:

+ `JUMPBOX-USERNAME` is your jumpbox username.

+ `JUMPBOX-ADDRESS` is the IP address or hostname of the jumpbox.

+ `SOCKS-PORT` is the local SOCKS port.

+ `JUMPBOX-KEY-FILE` is the local SSH private key for accessing the jumpbox.

**Note**
Using `BOSH_ALL_PROXY` can result in longer backup and restore
times due to network performance degradation.
All operations must pass through the proxy, which can make moving backup artifacts significantly
slower.

**Caution**
In the BBR v1.5.0 and earlier, the tunnel created by the BOSH CLI does
not include the `ServerAliveInterval` flag.
This might cause your SSH connection to timeout when transferring large artifacts.
In BBR v1.5.1, the `ServerAliveInterval` flag is included.
For more information, see
[bosh-backup-and-restore](https://github.com/cloudfoundry-incubator/bosh-backup-and-restore/releases/tag/v1.5.1)
on GitHub.

## Back up a BOSH Director

1. Run the BBR pre-backup check to confirm that your BOSH Director is reachable, and can therefore be backed up with BBR.
```
bbr director \

--private-key-path PATH-TO-PRIVATE-KEY \

--username USER-NAME \

--host BOSH-DIRECTOR-IP \
pre-backup-check
```
Where:

* `PATH-TO-PRIVATE-KEY` is the path to the SSH private key used to connect to the BOSH Director.

* `USER-NAME` is the SSH username of the BOSH Director.

* `BOSH-DIRECTOR-IP` is the internal (or public) IP address of your BOSH Director.
If the BOSH Director is public, this could be a public IP address or a domain, such as `my-bosh.xxx.cf-app.com`.For example:
```
$ bbr director \

--private-key-path bosh.pem \

--username bosh \

--host bosh.example.com \
pre-backup-check
```

**Note**
The pre-backup check cannot check for available disk space, ongoing network connections (for example, to databases), correctly configured credentials, or other circumstances that might impede a successful backup. It only checks that we can connect to the director.

1. If the pre-check command fails:

* Run the command again adding the `--debug` flag to enable debug logs.
For more information, see [BBR logging](https://docs.cloudfoundry.org/bbr/logging.html).

* Make the fix suggested in the output and run the pre-backup check again.
For example, the command fails if the BOSH Director selected did not have the correct backup scripts or if the connection to the BOSH Director failed.

2. If you are using BOSH v270.0 or later, you can prune the BOSH blobstore by running:
```
bosh clean-up --all
```
This command removes all unused resources, including packages complied against older
stemcells. If a lot of unused resources have accumulated over time, this clean-up causes a
smaller, faster backup of BOSH Director.
For more information, see [Clean-up](https://bosh.io/docs/cli-v2/#clean-up) in the BOSH
documentation.

**Caution**
This command is destructive and can remove resources that are
unused but necessary. For example, if an on-demand service broker is deployed and no service
instances have been created, the releases needed to create a service instance are categorized
as unused and are removed.

3. Run the BBR backup command to back up your BOSH Director:
```
bbr director \

--private-key-path PATH-TO-PRIVATE-KEY \

--username USER-NAME \

--host BOSH-DIRECTOR-IP \
backup
```
Where:

* `PATH-TO-PRIVATE-KEY` is the path to the SSH private key used to connect to the BOSH Director.

* `USER-NAME` is the SSH username of the BOSH Director.

* `BOSH-DIRECTOR-IP` is the internal (or public) IP address of your BOSH Director.
If the BOSH Director is public, this could be a public IP address or a domain, such as `my-bosh.xxx.cf-app.com`.For example:
```
$ bbr director \

--private-key-path bosh.pem \

--username bosh \

--host bosh.example.com \
backup
```

4. If the backup command completes successfully, follow the steps in [Manage your backup artifact](https://docs.cloudfoundry.org/bbr/backup.html#good-practices) below.

5. If the backup command fails:

* Run the command again adding the `--debug` flag to enable debug logs.
For more information, see [BBR logging](https://docs.cloudfoundry.org/bbr/logging.html).

* Follow the steps in [Recover from a failing command](https://docs.cloudfoundry.org/bbr/backup.html#recovering-from-failing-command).

## Back up a BOSH deployment

1. Run the BBR pre-backup check to confirm that your BOSH Director is reachable and has a deployment
that you can back up with BBR:
```
BOSH_CLIENT_SECRET=BOSH-CLIENT-SECRET \
bbr deployment \

--target BOSH-TARGET \

--username BOSH-CLIENT \

--deployment BOSH-DEPLOYMENT \

--ca-cert PATH-TO-BOSH-SERVER-CERTIFICATE \
pre-backup-check
```
Replace the placeholder text as follows:

* `BOSH-CLIENT-SECRET`: If you have a BOSH Director with User Account and Authentication (UAA)
as the authentication provider, this is a UAA client secret as the password.
If you have a BOSH Director with basic authentication configured, this is your password.

* `BOSH-TARGET`: The FQDN or IP address of your BOSH Director.

* `BOSH-CLIENT`: If you have a BOSH Director with User Account and Authentication (UAA) as the
authentication provider, this is a UAA client as the username.
If you have a BOSH Director with basic authentication configured, this is your username.

* `BOSH-DEPLOYMENT`: The name of the deployment you want to back up. For a list of deployments,
run `bosh deployments`.

* `PATH-TO-BOSH-CA-CERTIFICATE`: The path to the BOSH Director’s Certificate Authority (CA)
certificate, if the certificate is not verifiable by the local machine’s certificate chain. If you manually deployed,
then the certificate might be stored in a `secrets.yml` or similar file.For example:
```
$ BOSH_CLIENT_SECRET=p455w0rd \
bbr deployment \

--target bosh.example.com \

--username jumpbox \

--deployment cf-acceptance-0 \

--ca-cert bosh.ca.cert \
pre-backup-check
```

**Note**
The pre-backup check cannot check for available disk space, ongoing network connections (for example, to databases), correctly configured credentials, or other circumstances that might impede a successful backup. It only checks that we can connect to the director, and the VMs of our deployment.

1. If the pre-backup check command fails:

* Run the command again adding the `--debug` flag to enable debug logs.
For more information, see [BBR logging](https://docs.cloudfoundry.org/bbr/logging.html).

* Make the fix suggested in the output and run the pre-backup check again.
For example, the deployment you selected might not have the correct backup scripts,
or the connection to the BOSH Director failed.

2. If the pre-backup check succeeds, run the BBR backup command to back up your BOSH deployment:
```
BOSH_CLIENT_SECRET=BOSH-CLIENT-SECRET \
nohup bbr deployment \

--target BOSH-TARGET \

--username BOSH-CLIENT \

--deployment BOSH-DEPLOYMENT \

--ca-cert PATH-TO-BOSH-SERVER-CERTIFICATE \
backup
```
Replace the placeholder text as follows. These are the same values as used in the with the
previous command.

* `BOSH-CLIENT-SECRET`: If you have a BOSH Director with User Account and Authentication (UAA)
as the authentication provider, this is a UAA client secret as the password.
If you have a BOSH Director with basic authentication configured, this is your password.

* `BOSH-TARGET`: The FQDN or IP address of your BOSH Director.

* `BOSH-CLIENT`: If you have a BOSH Director with User Account and Authentication (UAA) as the
authentication provider, this is a UAA client as the username.
If you have a BOSH Director with basic authentication configured, this is your username.

* `BOSH-DEPLOYMENT`: The name of the deployment you want to back up. For a list of deployments,
run `bosh deployments`.

* `PATH-TO-BOSH-CA-CERTIFICATE`: The path to the BOSH Director’s Certificate Authority (CA)
certificate, if the certificate is not verifiable by the local machine’s certificate chain.
If you manually deployed, then the certificate might be stored in a `secrets.yml` or similar file.

**Note**
To include the manifest in the backup artifact, add the
`--with-manifest` flag. However, be aware that doing so causes the backup artifact
to include credentials that you need to keep secret.

**Caution**
The `--unsafe-lock-free` flag should only be used by advanced
users because it can result in inconsistent backups. For more information about this
feature, see [Experimental features](https://docs.cloudfoundry.org/bbr/experimental-features.html).
For example:
```
$ BOSH_CLIENT_SECRET=p455w0rd \
nohup bbr deployment \

--target bosh.example.com \

--username jumpbox \

--deployment cf-acceptance-0 \

--ca-cert bosh.ca.cert \
backup
```

**Note**
The BBR backup command can take a long time to complete.
You can run it independently of the SSH session so that the process can continue running even
if your connection to the jumpbox fails. The command above uses `nohup`, but you can
run the command in a `screen` or `tmux` session instead.

3. If the command completes successfully, follow the steps in [What to do with your backup artifact](https://docs.cloudfoundry.org/bbr/backup.html#what-to-do-with-artifact) below.

4. If the backup command fails:

* Run the command again adding the `--debug` flag to enable debug logs.
For more information, see [BBR logging](https://docs.cloudfoundry.org/bbr/logging.html).

* Follow the steps in [Recover from a failing command](https://docs.cloudfoundry.org/bbr/backup.html#recovering-from-failing-command).

## Recover from a failing command
If the backup fails for the BOSH Director or deployment:

1. Ensure that you set all the parameters in the command.

2. Ensure the BOSH Director credentials are valid.

3. If you are backing up a deployment, ensure the deployment you specify in the BBR command exists.

4. Ensure that the jumpbox can reach the BOSH Director.

5. See [BBR logging](https://docs.cloudfoundry.org/bbr/logging.html).

6. If you see the error message `Directory /var/vcap/store/bbr-backup already exists on instance`,
run the appropriate cleanup command. See [Clean up after a failed backup](https://docs.cloudfoundry.org/bbr/backup.html#manual-clean) below.

7. If the backup artifact is corrupted, discard the failing artifacts and rerun the backup.

## Cancel a backup
Backups can take a long time.
You might want to cancel a backup, for example, if you learn that the backup is going to fail
or that your developers urgently need to push an app.
To cancel a backup:

1. Terminate the BBR process by pressing Ctrl-C and typing `yes` to confirm.

**Caution**
Cancelling a backup can leave the system in an unusable state and prevent
additional backups. Follow the steps in [Clean up after a failed backup](https://docs.cloudfoundry.org/bbr/backup.html#manual-clean)
below to fix these issues.

## Clean up after a failed backup
If your backup process fails, it might leave the BBR backup directory on the instance, causing any
subsequent attempts to backup to fail. In addition, BBR might not have run the post-backup scripts, leaving the instance in a locked state.
Follow the steps below to use the BBR cleanup script after a failed backup attempt.

1. If the BOSH Director backup failed, run:
```
bbr director \

--private-key-path PATH-TO-PRIVATE-KEY \

--username USER-NAME \

--host BOSH-DIRECTOR-IP \
backup-cleanup
```
For example:
```
$ bbr director \

--private-key-path bosh.pem \

--username bosh \

--host bosh.example.com \
backup-cleanup
```

2. If the BOSH deployment backup failed, run:
```
BOSH_CLIENT_SECRET=BOSH-CLIENT-SECRET \
bbr deployment \

--target BOSH-TARGET \

--username BOSH-CLIENT \

--deployment BOSH-DEPLOYMENT \

--ca-cert PATH-TO-BOSH-CA-CERTIFICATE \
backup-cleanup
```
For example:
```
$ BOSH_CLIENT_SECRET=p455w0rd \
bbr deployment \

--target bosh.example.com \

--username jumpbox \

--deployment cf-acceptance-0 \

--ca-cert bosh.ca.crt \
backup-cleanup
```

## Manage your backup artifact
To keep your backup artifact safe:

1. Move the backup artifact off the jumpbox to your storage space. BBR stores each backup in a
subdirectory named `DEPLOYMENT-TIMESTAMP` within the current working directory.
The backup created by BBR consists of a directory with the backup artifacts and metadata files.

2. Compress and encrypt the backup artifacts when storing them.

3. Make redundant copies of your backup and store them in multiple locations.
This minimizes the risk of losing your backups in the event of a disaster.

4. Each time you redeploy Cloud Foundry, test your backup artifact by following the procedures in
[Restoring with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/restore.html).

**Note**
Backup artifacts might contain data covered by the European Union’s
General Data Protection Regulation (GDPR), includingS contain personal data.
For example, a backup of a BOSH deployment could contain user email addresses.
As such, backup artifacts should be handled in accordance with organizational policies and
applicable laws as they pertain to security, confidentiality, and privacy.