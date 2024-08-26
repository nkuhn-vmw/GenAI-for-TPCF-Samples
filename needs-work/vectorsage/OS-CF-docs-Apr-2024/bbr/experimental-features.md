# Experimental features
This topic highlights features that are only recommended for advanced users of BBR.

## –unsafe-lock-free
As of v1.9.0, the BBR CLI has an `--unsafe-lock-free` flag.
This flag should only be used by expert users of BBR, for reasons that this topic highlights.
If you use this flag during a backup operation, BBR skips running the lock and unlock scripts in
your deployment.
In the case of backing up a Cloud Foundry deployment, this prevents Cloud Foundry API (CAPI)
downtime but might cause an inconsistent backup.
This topic covers covers:

* Why your backup might be inconsistent

* Inconsistencies that testers observed

* Inconsistencies that testers did not observe but might still be possible
This topic does not speculate about the consequences of using the `--unsafe-lock-free` flag for
backing up a deployment other than Cloud Foundry.

### Troubleshooting for observed –unsafe-lock-free issues
Cloud Foundry is a distributed system that relies on distributed state.
For example, consider a running app:

* The Cloud Controller stores the name of the app, the route it has claimed, and other similar data,
in the Cloud Controller database (CCDB).

* The binary bits that form the running app, known as the droplet, are stored in the blobstore.
If you back up Cloud Foundry while an app is being pushed, your backup of the CCDB might contain a
reference to this app, while your backup of the blobstore does not contain the app’s droplet.
If you attempt to restore this backup, the app fails to start.
To avoid this sort of problem, BBR locks Cloud Foundry before creating a backup and, as a side-effect,
the CAPI goes down during the critical phase of the backup.
The `--unsafe-lock-free` flag disables this safety feature.
If you use it you prevent CAPI downtime, but you lose protection from backup inconsistencies such as
the one described above.

### Missing blob

#### Symptom
After restoring an inconsistent backup, some apps fail to start.
Running `cf events APP-NAME` prints output similar to the below:
```
$ cf events my-app
time event actor description
2020-10-28T11:10:21.00+0000 app.crash APP-NAME index: 0, reason: CRASHED, cell_id: 03fdc92e-8d5e-447c-a894-52f62b5f9c8e, instance: 2e2ae69a-c750-4da6-7339-5240, exit_description: Downloading droplet failed
```
This suggests the app’s droplet is missing from the blobstore.

#### Explanation
Testers caused this issue by artificially delaying the blobstore backup part of the BBR backup
process while deleting an app.
This issue might also occur if a user creates an app at a critical point during the backup
process. In either case, only the newly deleted or created app is expected to be affected.

#### Solutions
If the app’s package is present in the blobstore, you can fix the issue by running
`cf restage APP-NAME`.
However, if the droplet is missing due to an inconsistent backup, the corresponding package is likely
also missing. In this case, the only way to recover is to re-push the app.
You can prevent this issue by doing any of the following:

* Using an external blobstore, such as Minio

* Using the native replication features of your external blobstore to keep your own backups separate
from BBR

* Setting a retention policy on your replica blobstore so that no files are truly deleted until they
are marked as deleted for a certain number of days.
Before you run `bbr restore`, restore your blobstore from your replica or swap out the live store for
the replica.
This gives you a certain period of time in which all your backups are valid.
If you restore a backup older than that period, you might still experience this issue.

### Unstarted app

#### Symptom
After restoring, some apps did not attempt to start.

#### Explanation
If an app is pushed at a critical point during the backup process, the app might be created before the
Cloud Controller database (CCDB) is backed up, but started after the CCDB is backed up.
The result is an app which is backed up in a stopped state.

#### Solution
Run `cf start APP-NAME`.
If this fails, check that you are not missing blobs.
For more information, see [Missing blob](https://docs.cloudfoundry.org/bbr/experimental-features.html#missing-blob) above.

### An incomplete user

#### Symptom
After restoring inconsistent backups, testers observed that:

* A Cloud Foundry user existed who had no name and no credentials

* A set of Cloud Foundry user credentials existed with no corresponding user

#### Explanation
Testers caused variants of this issue by creating or deleting a Cloud Foundry user at a critical
point during the backup process.
In one case, the backup took a snapshot of the Cloud Controller database (CCDB) in a state in which
the user structure was created, but no name was assigned.
No credentials were created for the user in the UAA Database (UAADB), so the user was not usable.
In another case, the backup took a snapshot of the CCDB after a user was deleted, and the UAADB
before the user was deleted.
This left a set of garbage credentials in the UAADB that were connected
to no users, and consequently did not have access to anything in the system.

#### Solutions
Delete the half-created user if possible.
You can avoid this issue by:

* Not creating or deleting users during the backup process.

* Using LDAP or similar, rather than managing users directly in Cloud Foundry.

## Theoretical –unsafe-lock-free issues
Testers did not observe the following issues during testing.
Consider these theoretical issues before relying on `--unsafe-lock-free` in production.

### An app exists in CCDB, but not in either the networking database or the routing database
An app appears to start successfully, but is not reachable from the outside world.
Alternatively, container-to-container networking routes are unavailable, preventing your microservices
from communicating with each other as expected.
Testers were unable to force this error case in the lab.
Apps in Cloud Foundry can register their own routes, so it is possible that the error briefly
occurred but self-corrected before the testers were able to observe it.

### A route exists with no app
A route is restored that now points to an app that no longer exists.
This is a security risk if the route points to a container that should not be exposed to the public
internet.
However, routes in Cloud Foundry are short-lived by design: they must be constantly renewed by the
app that claims them. So, even in the worst case scenario, this problem is expected to self-correct
shortly after the restore.

### An app has CredHub bindings which are not in CredHub database
An app tries to access a data service even though the relevant credentials no longer exist, causing
the app to fail to access the data service at runtime and possibly crash or behave unexpectedly.

### An app is missing an autoscaler entry
An app expected to autoscale fails to do so.
Testers did not investigate this issue because it is likely to be caused by a
locking-backup occurring slightly earlier than expected, not by the `--unsafe-lock-free` flag.

### An autoscaler entry is missing an app
The autoscaler attempts to scale an app that does not exist.
Testers did not investigate this issue.
Few Cloud Foundry users of `--unsafe-lock-free` are expected to also use autoscaler and, for any who
do, this issue is expected to be very low severity should it occur.

### A user who does not exist in UAADB owns a space in CCDB
A user who does not exist in UAADB owns a space in CCDB, making that Cloud Foundry space
inaccessible.
Testers were unable to force this error in the lab.
The order in which Cloud Controller manages user and space creation and deletion might make
this issue impossible or very unlikely to occur.

### Usage events might be missing for apps, spaces, or service instances
Usage Events is a messaging system, and this is a common issue when snapshotting messaging
systems. With or without locks, you might lose messages during a backup.
For more information about Usage Events, see
[Usage events and billing](https://docs.cloudfoundry.org/running/managing-cf/usage-events.html).

### Usage events might exist for apps, spaces, or service instances that are missing from the backup
A message fires just before the backup is created, and does not safely persist until afterward.
If this happens, the observed behavior of the system is exactly as if the message were fired just
after the backup was taken.
Testers did not test for this issue because it is low-severity and could happen with or without locks.