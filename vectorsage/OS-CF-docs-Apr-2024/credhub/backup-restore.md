# Backing Up and Restoring CredHub Instances

* [Backing up the deployment manifest file](https://docs.cloudfoundry.org/credhub/backup-restore.html#deployment-manifest)

* [Backing up the encryption keys](https://docs.cloudfoundry.org/credhub/backup-restore.html#encryption-keys)

+ [Internal provider](https://docs.cloudfoundry.org/credhub/backup-restore.html#internal)

+ [Luna HSM](https://docs.cloudfoundry.org/credhub/backup-restore.html#luna-hsm)

+ [Encryption key back up frequency](https://docs.cloudfoundry.org/credhub/backup-restore.html#encryption-frequency)

* [Backing up the database](https://docs.cloudfoundry.org/credhub/backup-restore.html#database)

+ [Database backup frequency](https://docs.cloudfoundry.org/credhub/backup-restore.html#db-frequency)
You can back up and restore CredHub instances.
CredHub does not store any stateful data. However, CredHub relies on components that do store stateful data.
If you use CredHub in production or a similar environment that needs resiliency, you must create backups
regularly so you can recover the data in the event of a component failure.
The components that you can back up are:

* Your CredHub deployment manifest file. For more information, see [Backing up the deployment manifest file](https://docs.cloudfoundry.org/credhub/backup-restore.html#deployment-manifest).

* Your CredHub encryption keys. For more information, see [Backing up the encryption keys](https://docs.cloudfoundry.org/credhub/backup-restore.html#encryption-keys).

* The database you configured for CredHub. For more information, see [Backing up the database](https://docs.cloudfoundry.org/credhub/backup-restore.html#database).

## Backing up the Deployment Manifest file
Yopu can Back up the CredHub deployment manifest file every time you revise it.
You might want to keep the backups in a revision control system so you can manage them automatically.
To download the most recent version of your CredHub deployment manifest file, run:
```
bosh manifest -d DEPLOYMENT > MANIFEST.yml
```
Where:

* `DEPLOYMENT` is the name of your CredHub deployment.

* `MANIFEST` is the filename of your CredHub deployment manifest.

## Backing up the encryption keys
The process for backing up CredHub encryption keys can differ based on the encryption provider you use.
CredHub supports internal providers and Luna HSM.

### Internal provider
The internal provider performs encryption and decryption operations using a symmetrical AES key. This key is a hexadecimal value that is provided to the app during deployment.
Store the key in a secure place so you can use it in a future recovery deployment.

### Luna Hardware Security Modules
Luna Hardware Security Modules (HSMs) do not support traditional data export. HSMs are designed not to release key material once it’s placed on the device.
This does not mean that data lost from a Luna HSM is unrecoverable. You can configure your deployment to ensure that no data is lost if an HSM fails.
If you use a Luna HSM to store sensitive data, you can ensure data resiliency by:

* Setting up a redundant HSM configuration.
or

* Managing a Luna Backup HSM device.
For more information, see the [SafeNet Luna Network HSMs](https://safenet.gemalto.com/data-encryption/hardware-security-modules-hsms/safenet-network-hsm/) documentation.
CredHub supports management and integration with a high availability (HA) Luna HSM cluster. If you use this configuration, multiple HSMs use mirrored partitions to process incoming requests. Each HSM contains a copy of the encryption key; this provides redundancy, that ensures all but one of your HSMs can fail without the losing the availability of key material.
If you use a Luna HSM from Amazon Web Services (AWS), see [What Is AWS CloudHSM?](http://docs.aws.amazon.com/cloudhsm/latest/userguide/configuring-ha.html) in the AWS documentation.

### Encryption key back up frequency
Back up the encryption keys whenever you rotate them to ensure that you always have access to the latest value.
Keep an archive of the encryption key values for each CredHub database backup you make. For example, if you maintain backups of the five most recent versions of your CredHub database, also save the five most recent encryption keys so you can access each backup.

## Backing up the database
CredHub stores the majority of the stateful data in the configured database. This database is not deployed or managed by CredHub, so backup procedures can differ based on the database provider.
After you rotate the encryption key, test, verify a backup with the latest
encryption key. This testing ensures that you are not locked out of your backups in the event of a rollback or other data
loss.
For more information about database backups, see [Chapter 7 Backup and Recovery](http://dev.mysql.com/doc/refman/5.7/en/backup-and-recovery.html) in the MySQL documentation and [Chapter 24. Backup and Restore](https://www.postgresql.org/docs/9.5/static/backup.html) in the PostgreSQL documentation.

### Database backup frequency
Database best practices dictate that you do backups regularly, to avoid losing data if your database cluster fails. The right frequency varies based on the needs of your deployment.