# Configuring Cloud Foundry for BOSH Backup and Restore
This topic describes the configuration you need for your Cloud Foundry (CF) deployment to work with BOSH Backup and Restore (BBR).
This topic assumes that you use
[cf-deployment](https://github.com/cloudfoundry/cf-deployment) with ops files
for your Cloud Foundry deployment.
If you do not use ops files for customization, you can still customize your
Cloud Foundry to use BBR. Examine the contents of the ops files on this page,
and use them as a guide to customize your deployment manifest directly.

**Caution**

* **Backup artifacts can contain secrets.** Secure backup artifacts with encryption or by other means.

* **The restore is a destructive operation.** BBR is designed to restore CF after a disaster.
If it fails, the environment could be left in an unusable state and require re-provisioning.
For the generic method of restoring a deployment, see [Restoring with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/restore.html).

* **Developers are unable to push apps for a few minutes during backup and restore.**
This is because the Cloud Foundry API (CAPI) stops sending and receiving calls
between the `pre-backup-lock` and `post-backup-unlock` stages of the process.

* **BBR does not back up any service data.**
Back up Service data, such as Redis or RabbitMQ data, separately.

## Supported Cloud Foundry configurations
To enable backup and restore for your `cf-deployment`, deploy it with the
[enable-backup-restore.yml](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/enable-backup-restore.yml) ops file. This
enables BBR backup and restore for default CF components, including the internal blobstore.
When using the default configuration, all apps return to a running state after a restore.
To enable BBR backup and restore for different configurations, you must also use the appropriate backup and restore ops files.
For information about the available backup and restore ops files, see the
[cf-deployment README file](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/README.md) in GitHub.

### Supported external databases
Cloud Foundry components use the backup and restore SDK to interface with databases for backup and restore.
For supported databases and versions, see
[backup-and-restore-sdk-release](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release#database-backup-and-restore)
in GitHub.

### Selective backup and restore configurations for blobstores
You can use an external blobstore instead
of the default internal blobstore. For more information about supported external
blobstores, see [Backup and restore for external blobstores](https://docs.cloudfoundry.org/bbr/external-blobstores.html).
When BBR backs up and restores your Cloud Foundry blobstore, it includes droplets, buildpacks, and packages
by default.
You can omit specific blobstore content from your backup and restore
using the following ops files:
| Selective backup ops file | Content included in backup |
| --- | --- |
| [`skip-backup-restore-droplets.yml`](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/skip-backup-restore-droplets.yml) | Buildpacks, Packages |
| [`skip-backup-restore-droplets-and-packages.yml`](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/skip-backup-restore-droplets-and-packages.yml) | Buildpacks |

**Caution**
Selective backups increase
your overall recovery time. When you use selective backup ops files, apps
require extra steps to return to a running state after a restore. For more
information, see the [Restoring apps when using selective backups](https://docs.cloudfoundry.org/bbr/cf-backup.html#selective-backup-restore-steps) section below.

#### Restoring apps when using selective backups
When using the `skip-backup-restore-droplets.yml` ops file, do the following to get your apps running after a restore:

1. For each user-pushed application, run `cf restage`.

2. For each application pushed using a BOSH errand, you can either run `cf restage` or re-run the BOSH errand.
When using the `skip-backup-restore-droplets-and-packages.yml` ops file, do the following to get your apps running after a restore:

1. For each user-pushed application, run `cf push`.

2. For each application pushed using a BOSH errand, re-run the BOSH errand.

### Applying ops files in the correct order
When enabling backup and restore for a `cf-deployment` component, you must apply
the component ops files first, then `enable-backup-restore.yml`, and then any
additional backup and restore ops files required by the components. See the
following sections for examples of applying ops files in the correct order.

**External database**
To configure `cf-deployment` to use an external database with backup and restore enabled, apply the ops files in the following order:

1. `use-external-db.yml`

2. `enable-backup-restore.yml`

**S3-compatible unversioned blobstore with selective backup and restore**
To configure `cf-deployment` to use an S3-compatible unversioned blobstore with selective backup and restore enabled, apply the ops files in the following order:

1. `use-external-blobstore.yml`

2. `use-s3-blobstore.yml`

3. `enable-backup-restore.yml`

4. `enable-backup-restore-s3-unversioned.yml`

5. `skip-backup-and-restore-droplets-and-packages.yml`

**Note**
You can apply other component ops files before the backup and restore ops files. For example, you can apply other component ops file between `use-s3-blobstore.yml` and `enable-backup-restore.yml`.

## Next steps
After you have configured Cloud Foundry to be compatible with BBR, you can back up and restore Cloud Foundry.
Follow the procedures in the [Back up a BOSH deployment](https://docs.cloudfoundry.org/bbr/backup.html#back-up-deployment) section
of *Backing up with BOSH Backup and Restore* and the [Restore a BOSH deployment](https://docs.cloudfoundry.org/bbr/restore.html#restore-deployment) section
of *Restoring with BOSH Backup and Restore*.
At minimum, run the pre-backup check against your Cloud Foundry deployment by following
the first two steps of the [Back up a BOSH deployment](https://docs.cloudfoundry.org/bbr/backup.html#back-up-deployment) section
of *Backing up with BOSH Backup*.
This lists the scripts that run during a backup and the order in which they are applied.