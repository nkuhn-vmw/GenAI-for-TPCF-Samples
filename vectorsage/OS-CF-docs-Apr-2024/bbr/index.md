# BOSH Backup and Restore (BBR)
This guide documents BOSH Backup and Restore (BBR), a framework for backing up and restoring BOSH
deployments and BOSH Directors.
BBR orchestrates triggering the backup or restore process on the BOSH deployment or BOSH Director,
and transfers the backup artifacts to and from the BOSH deployment or BOSH Director.
Cloud Foundry recommends that you frequently back up your deployment using BBR, especially before
upgrading a deployment.
For more information about installing and using BBR, see the
[Installing BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/installing.html),
[Backing up with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/backup.html),
and [Restoring with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/restore.html) topics.
Information for release authors and developers is also available in the
[BOSH Backup and Restore Developer’s Guide](https://docs.cloudfoundry.org/bbr/bbr-devguide.html).
For more information about backing up and restoring cf-deployment with BBR, see
[Configuring Cloud Foundry for BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/cf-backup.html).

## Supported components
BBR is a binary that can back up and restore BOSH deployments and BOSH Directors.
BBR requires that the backup targets supply scripts that implement the backup and restore functions.
BBR is not dependent on a particular version of BOSH.
However, a BOSH deployment must have its backup and restore [scripts](https://docs.cloudfoundry.org/bbr/index.html#contract) packaged in the
releases to be backed up and restored with BBR. For more information, consult the documentation for
the deployment.

**You can currently back up and restore the following BOSH deployments with BBR:**

1. The BOSH Director, including CredHub, with either Basic Auth or Client/Client-Secret UAA
authentication

2. Cloud Foundry with specific [configuration](https://docs.cloudfoundry.org/bbr/cf-backup.html)

## Contract
BBR sets out a contract with BOSH release authors to call designated backup and restore scripts in a
specific order.
This approach has the following advantages:

* The deployment itself encapsulates the knowledge of how to back up and restore the deployment.

* Because the release author is responsible for writing and maintaining scripts, scripts
can change as the deployment changes and do not get out of sync.

### Backup scripts

1. **pre-backup-lock**: The pre-backup lock script locks the job so backups are consistent across the
cluster.

2. **backup**: The backup script backs up the release.

3. **post-backup-unlock**: The post-backup unlock script unlocks the job after the backup is complete.

### Restore scripts

1. **pre-restore-lock**: The pre-restore-lock script locks the job so the restore is consistent
across the cluster.

2. **restore**: The restore script restores the release.

3. **post-restore-unlock**: The post-restore-unlock script unlocks the job after the restore is
complete.

## What happens when you run a BBR backup?

**Prerequisite:** The operator has [installed BBR](https://docs.cloudfoundry.org/bbr/installing.html).
When a BBR `backup` command is run the following things happen:
BBR connects to instances in the deployment/director that was specified in the BBR command invocation.
Using these connections, BBR gathers information about which scripts it should run for each stage in
the backup.
BBR then runs the `pre-backup-lock`, `backup`, and `post-backup-unlock` scripts in stages.
Scripts in the same stage all finish before the next stage starts.
For instance, BBR triggers and waits for completion of all `pre-backup-lock` scripts before it
triggers any `backup` scripts.
Scripts within the `backup` stage can happen in any order.
A release author can configure ordering for scripts in in the `locking` and `unlocking` stages, but
any scripts that are unconstrained by that ordering can also happen in any order within their stage.
BBR drains and tars the backup artifacts to the jumpbox from where the operator can transfer the
resulting artifact to storage and use it to restore the BOSH deployment or BOSH Director.
The following diagram shows a sample backup flow.
![This diagram is described in the steps immediately below.](https://docs.cloudfoundry.org/bbr/images/backup-flow.png)
In the diagram above:

1. An operator runs `bbr backup pcf-deployment` on the jumpbox.

2. BBR calls the following backup scripts on the deployment:

* `backup-lock`

* `backup`

* `backup-unlock`

3. BBR transfers the backup artifacts from the deployment to the jumpbox.

4. BBR transfers the backup artifacts from the jumpbox to a secondary backup store that is outside of
the network or availability zone (AZ).

## What happens when you run a BBR restore?

*Prerequisite:* You have available on the jumpbox an artifact produced by a BBR `backup` of your
deployment or director.
When a BBR `restore` command is run for that artifact the following things happen:
BBR connects to instances in the deployment/director that was specified in the command invocation.
Using these connections, BBR gathers information about which scripts it should run for each stage in
the restore.
BBR uploads the each part of the artifact to the instance it belongs to.
BBR then runs the `pre-restore-lock`, `restore`, and `post-restore-unlock` scripts in stages.
Scripts in the same stage all finish before the next stage starts.
For instance, BBR triggers and waits for completion of all `pre-restore-lock` scripts before it
triggers any `restore` scripts.
Scripts within the `restore` stage can happen in any order.
A release author can configure ordering for scripts in in the `locking` and `unlocking` stages, but
any scripts that are unconstrained by that ordering can also happen in any order within their stage.

## Syntax
This section provides syntax information for the BBR binary.
For detailed procedures on how to use BBR to back up and restore a BOSH Director or BOSH deployment,
see the [Backing up with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/backup.html) and
[Restoring with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/restore.html) topics.
The syntax for the BBR binary is:
```
bbr [command] [arguments...] [subcommand]
```
The options for `[command]` are:

* `deployment`: Specifies that the target of BBR is a BOSH deployment

* `director`: Specifies that the target of BBR is a BOSH Director

* `help`: Prints help text

* `version`: Prints the version of the `bbr` binary
The `[arguments]` are specific to the command.

### BOSH Director
The arguments to specify when running BBR for a BOSH Director are:
```
$ bbr director \

--debug (OPTIONAL) \

--private-key-path PATH_TO_PRIVATE_KEY \

--username USER_NAME \

--host HOST \
SUB-COMMAND [--artifact-path PATH_TO_ARTIFACT]
```
The parameters are:

* `--debug`: This is an optional flag to display debug output.

* `--private-key-path`: This is the path to the SSH private key used to connect to the BOSH Director.

* `--username`: This is the SSH username of the BOSH Director.

* `--host`: This is the address of the BOSH Director with an optional port that defaults to 22.
If the BOSH Director is public, this is a URL, such as `https://my-bosh.xxx.cf-app.com`.
Otherwise, this is the BOSH Director IP address.

* `--artifact-path`: This is the path to the BOSH Director backup artifact you want to backup to or
restore from.

### BOSH deployment
The arguments to specify when running BBR for a BOSH deployment are:
```
$ BOSH\_CLIENT\_SECRET=BOSH_CLIENT_SECRET \
bbr deployment \

--debug (OPTIONAL)

--target BOSH_TARGET \

--username BOSH_CLIENT \

--deployment DEPLOYMENT_NAME \

--ca-cert PATH_TO_BOSH_CA_CERTIFICATE \
SUB-COMMAND [--artifact-path PATH_TO_ARTIFACT]
```
The arguments are:

* `--debug`: This is an optional flag to display debug output.

* `BOSH_CLIENT`, `BOSH_CLIENT_SECRET`: If you have a BOSH Director with User Account and
Authentication (UAA) as the authentication provider, use a UAA client as the username and a UAA
client secret as the password.
If you have a BOSH Director with basic authentication configured, use your username and password.

* `--target`: This is the FQDN or IP address of your BOSH Director.

* `--deployment`: This is the name of the deployment you want to back up. For a list of deployments,
run `bosh deployments`.

* `--ca-cert`: This is the path to the BOSH Director’s Certificate Authority (CA) certificate if the
certificate is not verifiable by the local machine’s certificate chain.

* `--artifact-path`: This is the path to the BOSH deployment backup artifact you want to backup to or
restore from.

### Subcommands
BBR supports five subcommands:

* `backup`

* `restore`

* `pre-backup-check`

* `backup-cleanup`

* `restore-cleanup`