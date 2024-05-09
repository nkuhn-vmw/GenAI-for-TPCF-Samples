# Backup and Restore for external blobstores
.note.warning {
background-color: #fdd;
border-color: #fbb;
&:before {
content: "\F071";
font-family: FontAwesome;
color: #b9b781;
font-size: 1.2em;
left: 0.6em;
position: absolute;
top: 0.75em;
}
}
This topic explains how to back up and restore external blobstores with BOSH Backup and Restore (BBR).
BBR supports Amazon S3 buckets, S3-compatible storage solutions, Azure storage containers, and Google Cloud Storage buckets.
The necessary configuration and supported restore scenarios differ depending on the type of blobstore you use. For details, see the sections below.

## S3-compatible unversioned blobstores
BBR backs up external blobstores by copying blobs from live buckets to specified backup buckets.
BBR uses the native copy functionality of your blobstore to transfer blobs between the live and backup buckets, without transferring the blobs to your BBR instance.
For resiliency and safety, store your backup buckets and live buckets in different regions.

### Enable backup and restore of your unversioned S3-compatible blobstore
To back up a Cloud Foundry deployment that uses an unversioned S3-compatible external blobstore,
you must co-locate the `s3-unversioned-blobstore-backup-restorer` job from the [backup-and-restore-sdk-release](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/tree/master) as part of your deployment.

1. Verify that your blobstore is either an Amazon S3 bucket or an S3-compatible bucket with support for AWS Signature Version 4.

**Note**
If your S3-compatible blobstore uses a custom CA certificate, see [Configuring trusted certificates](https://bosh.io/docs/trusted-certs.html) in the [BOSH documentation](https://bosh.io/docs).
BBR automatically makes use of your configured trusted certificates.

2. Create backup buckets for droplets, packages, and buildpacks. Cloud Foundry recommends that either the backup buckets or copies of them be in a different region than the live buckets.

3. Include the `enable-backup-restore-s3-unversioned.yml` ops file in your deployment. The `enable-backup-restore-s3-unversioned.yml` file is in the [cf-deployment](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/enable-backup-restore-s3-unversioned.yml) GitHub repository.
See [vars-enable-backup-restore-s3-unversioned.yml](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/example-vars-files/vars-enable-backup-restore-s3-unversioned.yml) in GitHub for information about how to configure the variables for your backup bucket locations.

**Note**
Apply `enable-backup-restore.yml` and `use-s3-blobstore.yml`
before `enable-backup-restore-s3-unversioned.yml`.
See [Apply ops files in the correct order](https://docs.cloudfoundry.org/bbr/cf-backup.html#order).
If you do not use [cf-deployment](https://github.com/cloudfoundry/cf-deployment) and ops files, you can still back up and restore external blobstores with BBR.
See the contents of the `enable-backup-restore-s3-unversioned.yml` ops file as an example and review the [backup-and-restore-sdk-release](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/blob/master/docs/blobstore-backup-restore.md#s3-compatible-unversioned-blobstores) documentation in GitHub for further information.

**Caution**
To minimize storage costs, Cloud Foundry recommends creating a lifecycle policy for your backup buckets that permanently expires your older backups. For more information, see the [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-lifecycle.html).

### Supported restore scenarios for your unversioned S3-compatible blobstore
The restore process copies blobs from a directory in the backup bucket to the live buckets in use by the CF deployment you are restoring into.
If your original backup buckets are lost but you are restoring from copies of those original backup buckets, ensure that the variables listed in [vars-enable-backup-restore-s3-unversioned.yml](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/example-vars-files/vars-enable-backup-restore-s3-unversioned.yml) reference those copies.

**Caution**
Restoring to an unversioned bucket overwrites blobs with the backed up copies of those blobs.
BBR only modifies the blobs that were copied to the backup bucket. Other blobs are not changed during this process.

## S3-compatible versioned blobstores
BBR supports S3-compatible buckets that are versioned and support AWS Signature Version 4.
For more details about enabling versioning on your blobstore,
see [Enable Versioning on your S3-compatible blobstore](https://docs.cloudfoundry.org/bbr/external-blobstores.html#enable-s3-versioning) below.
External blobstores are backed up by storing the current version of each blob, not the actual files. Those versions are set to be the current versions at restore time.

**Caution**
Storing the current version of each blob makes backing up and restoring faster. However, this means that you can only restore if the original bucket still exists. If the original bucket is deleted, all of that bucket’s related versions are also deleted. If the original bucket is deleted, you can only restore from a replica. For more information, see [Restore from replicas](https://docs.cloudfoundry.org/bbr/external-blobstores.html#s3-versioned-restore-from-replicas).

**Caution**
The `s3-versioned-blobstore-backup-restorer` in
[backup-and-restore-sdk](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/releases)
v1.5.1 and earlier does not support the backup and restore of an Amazon S3 blobstore with individual blobs greater than 5 GB.

### Enable backup and restore of your versioned S3-compatible blobstore
To back up a Cloud Foundry deployment that uses an external blobstore,
you must co-locate the `s3-versioned-blobstore-backup-restorer` job from [`backup-and-restore-sdk-release`](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/tree/master) as part of your deployment.

1. Verify that your blobstore is either an Amazon S3 bucket with versioning enabled or an S3-compatible bucket with versioning enabled and support for AWS Signature Version 4.

**Note**
If your S3-compatible blobstore uses a custom CA certificate, see [Configuring trusted certificates](https://bosh.io/docs/trusted-certs.html) in the [BOSH documentation](https://bosh.io/docs). BBR automatically makes use of your configured trusted certificates.

2. Include the `enable-backup-restore-s3-versioned.yml` ops file in your deployment. The `enable-backup-restore-s3-unversioned.yml` file is in the [cf-deployment](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/enable-backup-restore-s3-unversioned.yml) GitHub repository.

**Note**
Apply `enable-backup-restore.yml` and `use-s3-blobstore.yml`
before `enable-backup-restore-s3-versioned.yml`.
See [Apply ops files in the correct order](https://docs.cloudfoundry.org/bbr/cf-backup.html#order).
If you do not use [cf-deployment](https://github.com/cloudfoundry/cf-deployment) and ops files, you can still back up and restore external blobstores with BBR.
See the contents of the `enable-backup-restore-s3-versioned.yml` ops file as an example and see the [S3-compatible Versioned Blobstores](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/blob/master/docs/blobstore-backup-restore.md#s3-compatible-versioned-blobstores) in the Blobstore Backup and Restore documentation in GitHub.

### Enable versioning on your S3-compatible blobstore
BBR only supports the backup and restore of blobstores stored in versioned Amazon S3 buckets
and in S3-compatible buckets that are versioned and support AWS Signature Version 4.
Three Cloud Foundry buckets are backed up by BBR, so you only need to enable versioning of:

* `droplets`

* `packages`

* `buildpacks`
Enabling versioning of the `resource_pool` bucket is not required.
To enable versioning of Amazon S3 buckets, see [How Do I Enable or Suspend Versioning for an S3 Bucket?](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/enable-versioning.html) in the Amazon Simple Storage Service documentation.
If you prefer to use the [AWS CLI](https://aws.amazon.com/cli/), use the `put-bucket-versioning` command. For more information, see [put-bucket-versioning](https://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-versioning.html) in the AWS CLI Command Reference.

1. If your blobstore buckets are not empty, run the following command on each one of them, using the AWS CLI:
```
aws s3 cp s3://BUCKET-NAME/ s3://BUCKET-NAME/ --recursive --metadata bump=true
```
Where `BUCKET-NAME` is the name of your bucket.
For example:
```
$ aws s3 cp s3://my-bucket/ s3://my-bucket/ --recursive --metadata bump=true
```
This ensures that each file in your buckets has a valid version ID.

2. After enabling versioning, you have a current version and zero or more non-current versions for each object.

**Note**
Cloud Foundry recommends setting an expiration policy on your buckets to delete old non-current versions and minimize storage costs. For more information, see the [AWS documentation](https://docs.aws.amazon.com/AmazonS3/latest/dev/lifecycle-configuration-examples.html#lifecycle-config-conceptual-ex6) in the Amazon Simple Storage Service documentation.

**Note**
If your blobstore uses S3-compatible buckets that are not from Amazon,
see the documentation for your storage provider regarding enabling versioning and setting an expiration policy.

### Enable replication on your versioned S3-compatible blobstore
BBR does not download your blobs to the backup artifact when performing a backup. Instead, BBR notes the current version identifier of each blob and stores the identifiers in the artifact.
When restoring, BBR reverts your blobs to the original versions using the version identifiers. Because the backup artifact contains only identifiers, not blobs, BBR can only restore the blobs if the original bucket containing the blob versions still exists.
If a bucket is deleted, all of that bucket’s versions are also deleted and you cannot restore using that bucket. To prevent this from happening, set up [Cross-Region Replication](https://docs.aws.amazon.com/AmazonS3/latest/dev/crr.html). See the [`put-bucket-replication` command](https://docs.aws.amazon.com/cli/latest/reference/s3api/put-bucket-replication.html) if you prefer to use the AWS CLI.
If your original buckets are lost, you can restore from a replica. Replication results in buckets that are identical to the original buckets, including the original version identifiers. To restore from a replica, see [Restore from Replicas](https://docs.cloudfoundry.org/bbr/external-blobstores.html#s3-versioned-restore-from-replicas) below.

### Supported restore scenarios for your versioned S3-compatible blobstore
Determine which of the following scenarios applies to your deployment before restoring:

* [In-place restore](https://docs.cloudfoundry.org/bbr/external-blobstores.html#s3-versioned-in-place-restore)

* [Restore to new buckets](https://docs.cloudfoundry.org/bbr/external-blobstores.html#s3-versioned-restore-to-new-buckets)

* [Restore from replicas](https://docs.cloudfoundry.org/bbr/external-blobstores.html#s3-versioned-restore-from-replicas)

**Note**
When restoring to a bucket, BBR only modifies blobs that are recorded in the backup artifact. Other blobs are not affected.

#### In-place sestore
When backing up an
external blobstore, the backup consists of a snapshot of the objects’ IDs and versions.
If you are doing an in-place restore and your destination Cloud Foundry for that restore uses the original buckets of the backed-up Cloud Foundry, those versions are retrieved and set to be the current versions in the buckets.

#### Restore to new buckets
If your destination Cloud Foundry for a restore uses different buckets,
then you can also restore into those new buckets, if the original buckets still exist.
During restore, the original versions are copied from the original buckets to the destination buckets.
In order to restore to new buckets, those new buckets must be versioned.
For more information about versioning an Amazon S3 blobstore, see [Enable versioning on your S3-compatible blobstore](https://docs.cloudfoundry.org/bbr/external-blobstores.html#enable-s3-versioning) above.
Before restoring, ensure that the `s3-versioned-blobstore-backup-restorer` job in the `backup-and-restore-sdk` is configured to point to the
destination buckets.

#### Restore from replicas
To protect yourself from losing your blobstore buckets, you should [enable replication](https://docs.cloudfoundry.org/bbr/external-blobstores.html#enable-s3-versioned-replication), as described below. This allows you to perform restores from the replicas, in case your original buckets are lost.
To restore from replicas, you must modify the backup artifacts to point to the replicas
before beginning a restore.
To modify the backup artifacts:

1. In your terminal, change into the directory for your backup artifact.

2. Extract the blobstore backup archive by running:
```
tar xvf BLOBSTORE-ARTIFACT.tar
```
Where `BLOBSTORE-ARTIFACT` is the name of your blobstore artifact.
For example:
```
$ tar xvf backup-restore-0-s3-versioned-blobstore-backup-restorer.tar
```

3. Modify the `blobstore.json` to point to the replicated buckets.

4. Recalculate the shasum of `blobstore.json` by running:
```
shasum -a 256 blobstore.json
```

5. Update the metadata file entry for that `blobstore.json` with the new checksum.

6. Re-create the archive by running:
```
tar cvf BLOBSTORE-ARTIFACT.tar ./blobstore.json
```
Where `BLOBSTORE-ARTIFACT` is the name of your blobstore artifact.
For example:
```
$ tar cvf backup-restore-0-s3-versioned-blobstore-backup-restorer.tar ./blobstore.json
```
The backup artifact is now ready to be restored from the replicated buckets.

## Azure blobstores
BBR backs up Azure storage containers by storing the ETags of each blob, not the actual blobs, which makes backups and restores faster. However, this means that restores work only if the original containers still exist.

### Enable soft delete in your Azure storage account
BBR requires that you enable soft delete in your Azure storage account. With soft delete, you can recover your data when blobs or blob snapshots are deleted.
To enable soft delete in your Azure storage account, follow the instructions in the [Azure documentation](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blob-soft-delete#quickstart).
You should set a reasonable retention policy to minimize storage costs.

### Enable replication for your Azure blobstore
BBR does not download your blobs to the backup artifact when it performs a backup. Instead, BBR records the current ETag of each blob and stores the identifiers in the artifact.
When restoring, BBR reverts your blobs to the original versions using the ETags.
Because the backup artifact stores identifiers, not blobs, BBR can restore the blobs only if the original container with the blob versions still exists.
An Azure data center failure can render your original container unavailable. To mitigate this threat, configure replication for your container. For more information, see [Azure Storage replication](https://docs.microsoft.com/en-us/azure/storage/common/storage-redundancy) in the Azure documentation.

### Enable backup and restore of your Azure blobstore
To back up a Cloud Foundry deployment that uses an Azure external blobstore, you must include the `enable-backup-restore-azure.yml` ops file in your deployment.
This co-locates the `azure-blobstore-backup-restorer` job from [backup-and-restore-sdk-release](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/tree/master) as part of your deployment.

**Note**
Apply `enable-backup-restore.yml` and `use-azure-storage-blobstore.yml`
before `enable-backup-restore-azure.yml`.
For more information, see [Apply ops files in the correct order](https://docs.cloudfoundry.org/bbr/cf-backup.html#order).
If you do not use [cf-deployment](https://github.com/cloudfoundry/cf-deployment) and ops files,
you can still back up and restore external blobstores with BBR.
See the contents of the `enable-backup-restore-azure.yml` ops file as an example and see the [backup-and-restore-sdk-release](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/blob/master/docs/blobstore-backup-restore.md#azure-blobstores) documentation in GitHub for details.

### Supported restore scenarios for your Azure blobstore
Determine which of the following scenarios applies to your deployment before restoring it:

* [In-place restore](https://docs.cloudfoundry.org/bbr/external-blobstores.html#azure-in-place-restore)

* [Restore to a new container in the same storage account](https://docs.cloudfoundry.org/bbr/external-blobstores.html#azure-restore-to-new-containers)

* [Restore to a new container in a different storage account](https://docs.cloudfoundry.org/bbr/external-blobstores.html#azure-restore-to-different-storage-account)

**Note**
When restoring to a container, BBR modifies only blobs that are recorded in the backup artifact. Other blobs are not affected.

#### In-place restore
When BBR backs up an Azure blobstore, the backup consists of a snapshot with the IDs and ETags of the objects.
In an in-place restore, you reuse the same containers.
BBR replaces the current blob versions in the container with those corresponding to the ETags recorded in the backup artifact.

#### Restore to a new container in the same storage account
When you restore to different containers, BBR copies the versions recorded in the backup artifact from the backed-up containers to the new containers.
In this scenario, the backed-up containers must exist during the restore.

#### Restore to a new container in a different storage account
You can restore blobs to a container in a different Azure storage account from the original.
In this scenario, BBR copies the blobs from the backed-up containers in the source Azure storage account to the new containers in the storage account used for restore.
You must use the `enable-restore-azure-clone.yml` ops file in your deployment.

**Note**
Apply `enable-backup-restore.yml` and `use-azure-storage-blobstore.yml`
before `enable-restore-azure-clone.yml`.
For more information, see [Apply ops files in the correct order](https://docs.cloudfoundry.org/bbr/cf-backup.html#order)
in *Configuring Cloud Foundry for BOSH Backup and Restore*.
After restoring, replace the `enable-restore-azure-clone.yml` ops file in your deployment with the `enable-backup-restore-azure.yml` ops file and redeploy.

## Google Cloud Storage (GCS) blobstores
BBR backs up GCS blobstores by copying blobs from live buckets to specified backup buckets.
BBR uses the native copy functionality of your blobstore to transfer blobs between the live and
backup buckets, without transferring the blobs to your BBR instance.

### Enable backup and restore of your GCS blobstore
To back up a Cloud Foundry deployment that uses a GCS external blobstore,
you must co-locate the `gcs-blobstore-backup-restorer` job from the [backup-and-restore-sdk-release](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/tree/master) as part of your deployment.

1. Create backup buckets for droplets, packages, and buildpacks. Cloud Foundry recommends that either the backup buckets or copies of them be in a different region than the live buckets.

2. Include the `enable-backup-restore-gcs.yml` ops file in your deployment. The `enable-backup-restore-gcs.yml` file is in the [cf-deployment](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/enable-backup-restore-gcs.yml) GitHub repository.
See [vars-enable-backup-restore-gcs.yml](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/example-vars-files/vars-enable-backup-restore-gcs.yml) for information about how to configure the variables for your backup bucket locations.

**Note**
Apply `enable-backup-restore.yml` and `use-gcs-blobstore-service-account.yml`
before `enable-backup-restore-gcs.yml`.
See [Apply ops files in the correct order](https://docs.cloudfoundry.org/bbr/cf-backup.html#order) in

*Configuring Cloud Foundry for BOSH Backup and Restore*.
If you do not use [cf-deployment](https://github.com/cloudfoundry/cf-deployment) and ops files, you can still back up and restore external blobstores with BBR.
See the contents of the `enable-backup-restore-gcs.yml` ops file as an example and review the [backup-and-restore-sdk-release](https://github.com/cloudfoundry-incubator/backup-and-restore-sdk-release/blob/master/docs/blobstore-backup-restore.md#google-cloud-storage-blobstores) documentation in GitHub for further information.

**Caution**
To minimize storage costs, Cloud Foundry recommends creating a lifecycle policy for your backup buckets that permanently expires your older backups. For more information, see the [GCP documentation](https://cloud.google.com/storage/docs/lifecycle).

### Supported restore scenarios for your GCS blobstore
The restore process copies blobs from a directory in the backup bucket to the live buckets in use by the CF deployment you are restoring into.
If your original backup buckets are lost but you are restoring from copies of those original backup buckets, ensure that the variables listed in [vars-enable-backup-restore-gcs.yml](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/backup-and-restore/example-vars-files/vars-enable-backup-restore-gcs.yml) reference those copies.

**Caution**
Restoring to a GCS bucket overwrites blobs with the backed up copies of those blobs.
BBR only modifies the blobs that were copied to the backup bucket. Other blobs are not changed during this process.