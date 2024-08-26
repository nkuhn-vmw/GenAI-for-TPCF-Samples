# Restoring with BOSH Backup and Restore
This topic describes how to use BOSH Backup and Restore (BBR) to restore a BOSH deployment or BOSH Director.
To back up a BOSH deployment or BOSH Director with BBR, see the [Backing up with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/backup.html) topic.
The steps in this topic allow you to restore a BOSH Director, a BOSH deployment, or both.

## Compatibility of restore
This section describes the restrictions for a backup artifact to be restorable to another environment.
This section is for guidance only, and Cloud Foundry recommends that operators validate their backups
by using the backup artifacts in a restore.
The restrictions for a backup artifact to be restorable are:

* **Topology**: BBR requires the BOSH topology of a deployment to be the same in the restore
environment as it was in the backup environment.

* **Naming of instance groups and jobs**: For any deployment that implements the backup and restore
scripts, the instance groups and jobs must have the same names.

* **Number of instance groups and jobs**: For instance groups and jobs that have backup and restore
scripts, there must be the same number of instances.

* **Limited validation**: BBR puts the backed up data into the corresponding instance groups and
jobs in the restored environment, but cannot validate the restore beyond that.
For example, if the MySQL encryption key is different in the restore environment, the BBR restore
might succeed although the restored MySQL database is unusable.

**Note**
A change in VM size or underlying hardware should not affect
BBR’s ability to restore data, as long as there is adequate storage space to restore the data.

## Step 1: Re-create VMs
Before restoring a BOSH deployment or Director, you must create the VMs that constitute that
deployment or Director.
In a disaster recovery scenario, you can re-create the deployment with your BOSH deployment
manifest.
If you used the `--with-manifest` flag when running the BBR backup command, your backup artifact
includes a copy of your manifest.
Alternatively, if you are restoring a deployment and you have already restored the Director that
contains knowledge of this deployment, the Director brings back your VMs for the deployment if
the BOSH Resurrector is enabled.
For more information about the BOSH Resurrector, see [Auto-healing Capabilities] in the BOSH documentation.

## Step 2: Transfer artifacts to jumpbox
Move your BBR backup artifact from your safe storage location to the jumpbox.
For instance, to SCP the backup artifact to your jumpbox you could run:
```
scp LOCAL-PATH-TO-BACKUP-ARTIFACT JUMPBOX-USER/JUMPBOX-ADDRESS
```
If this artifact is encrypted, you must decrypt it.

## Step 3: Restore

**Note**
The BBR restore command can take a long time to complete.
You can run it independently of the SSH session so that the process can continue running even if
your connection to the jumpbox fails. The command above uses `nohup`, but you run
the command in a `screen` or `tmux` session instead.
Use the optional `--debug` flag to enable debug logs. For more information, see [BBR logging](https://docs.cloudfoundry.org/bbr/logging.html).

#### Restore a BOSH Director
To restore a BOSH Director:

1. Ensure the BOSH Director backup artifact is in the directory from which you run BBR.

2. Run the BBR restore command from your jumpbox to restore the BOSH Director:
```
nohup bbr director \

--private-key-path PATH-TO-PRIVATE-KEY \

--username USER-NAME \

--host HOST \
restore \

--artifact-path PATH-TO-DIRECTOR-BACKUP
```
Replace the placeholder values as follows:

* `PATH-TO-PRIVATE-KEY`: This is the path to the SSH private key used to connect to the BOSH Director.

* `USER-NAME`: This is the SSH username of the BOSH Director.

* `HOST`: This is the address of the BOSH Director with an optional port that defaults to 22. If the BOSH Director is public, this is a URL, such as `https://my-bosh.xxx.cf-app.com`. Otherwise, this is the BOSH Director IP address.

+ `PATH-TO-DIRECTOR-BACKUP`: This is the path to the BOSH Director backup you want to restore.
If the command fails, follow the steps in [Recover from a failing command](https://docs.cloudfoundry.org/bbr/restore.html#recover-from-failing-command) below.

#### Restore a BOSH deployment
To restore a BOSH deployment:

1. Ensure the BOSH deployment backup artifact is in the directory from which you run BBR.

2. Run the BBR restore:
```
BOSH_CLIENT_SECRET=BOSH-CLIENT-SECRET \
nohup bbr deployment \

--target BOSH-TARGET \

--username BOSH-CLIENT \

--deployment DEPLOYMENT \

--ca-cert PATH-TO-BOSH-SERVER-CERTIFICATE \
restore \

--artifact-path PATH-TO-DEPLOYMENT-BACKUP
```
Replace the placeholder values as follows:

* `BOSH-CLIENT`, `BOSH-CLIENT-SECRET`: If you have a BOSH Director with User Account and Authentication (UAA) as the authentication provider, use a UAA client as the username and a UAA client secret as the password. If you have a BOSH Director with basic authentication configured, use your username and password.

* `BOSH-TARGET`: This is the FQDN or IP address of your BOSH Director.

* `DEPLOYMENT-NAME`: This is the name of the deployment you want to restore.

* `PATH-TO-BOSH-CA-CERTIFICATE`: This is the path to the BOSH Director’s Certificate Authority (CA) certificate if the certificate is not verifiable by the local machine’s certificate chain.

+ `PATH-TO-DEPLOYMENT-BACKUP`: This is the path to the BOSH deployment backup you want to restore.
If the command fails, follow the steps in [Recover from a failing command](https://docs.cloudfoundry.org/bbr/restore.html#recover-from-failing-command) below.

## Recover from a failing command

1. Ensure all the parameters in the command are set.

2. Ensure the BOSH Director credentials are valid.

3. Ensure the specified BOSH deployment exists.

4. Ensure that the jumpbox can reach the BOSH Director.

5. Ensure the source BOSH deployment is compatible with the target BOSH deployment.

6. If you see the error message `Directory /var/vcap/store/bbr-backup already exists on instance`, follow the
steps in [Clean up after failed restore](https://docs.cloudfoundry.org/bbr/restore.html#manual-clean) below.

## Cancel a restore
To cancel a restore, you must terminate the BBR process.

1. Press Ctrl-C.

2. Type `yes` at the prompt to confirm.
Stopping a restore can leave the system in an unusable state and prevent future restores.
Perform the procedures in the [Clean up after failed restore](https://docs.cloudfoundry.org/bbr/restore.html#manual-clean) section to ensure you can
perform future restores.

## Clean up after failed restore
If your restore process fails, then the process might leave the BBR restore directory on the instance.
As a result, any subsequent restore attempts might fail.
In addition, BBR might not have run the post-restore scripts, which can leave the instance in a locked state.
To resolve these issues, run the BBR cleanup script.
To clean up after a failed BOSH Director restore, run:
```
bbr director \

--private-key-path PATH-TO-PRIVATE-KEY \

--username USER-NAME \

--host HOST
restore-cleanup
```
To clean up after a failed BOSH deployment restore, run:
```
BOSH_CLIENT_SECRET=BOSH-CLIENT-SECRET \
bbr deployment \

--target BOSH-TARGET \

--username BOSH-CLIENT \

--deployment DEPLOYMENT-NAME \

--ca-cert PATH-TO-BOSH-CA-CERTIFICATE \
restore-cleanup
```