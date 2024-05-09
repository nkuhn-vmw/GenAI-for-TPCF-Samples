# Cloud Controller
Cloud Controller in Cloud Foundry provides you with REST API endpoints to access the
system.
Cloud Controller maintains a database with tables for orgs, spaces,
services, user roles, and more.
Refer to the following diagram for information about internal and external communications of the Cloud Controller.
![Internal and external Cloud Controller communications](https://docs.cloudfoundry.org/concepts/images/cc-communications-map.png)
View a [larger version](https://docs.cloudfoundry.org/concepts/images/cc-communications-map.png) of this image.

## Diego Auction
The Cloud Controller uses the [Diego Auction](https://docs.cloudfoundry.org/concepts/diego/diego-auction.html) to balance application
processes over the [Diego Cells](https://docs.cloudfoundry.org/concepts/architecture/#diego-cell) in a Cloud Foundry installation.

## Database (CC\_DB)
The Cloud Controller database has been tested with Postgres and MySQL.

## Blobstore
To stage and run apps, Cloud Foundry manages and stores the following types of
binary large object (blob) files:
| Blob Type | Description | Location in Blobstore |
| --- | --- | --- |
| App Packages | Full contents of app directories, including source code and resource files, zipped into single blob files. | `/cc-packages` |
| Buildpacks | Buildpack directories, which Diego cells download to compile and stage apps with. | `/cc-buildpacks` |
| Resource Cache | Large files from app packages that the Cloud Controller stores with a SHA for later re-use. To save bandwidth, the Cloud Foundry Command Line Interface (cf CLI) only uploads large application files that the Cloud Controller has not already stored in the resource cache. | `/cc-resources` |
| Buildpack Cache | Large files that buildpacks generate during staging, stored for later re-use. This cache lets buildpacks run more quickly when staging apps that have been staged previously. | `cc-droplets/buildpack_cache` |
| Droplets | Staged apps packaged with everything needed to run in a container. | `/cc-droplets` |
Cloud Foundry blobstores use the [Fog](http://fog.io/) Ruby gem to store blobs in
services like Amazon S3, WebDAV, or the NFS filesystem. The file system location of an internal blobstore is `/var/vcap/store/shared`.
A single blobstore typically stores all five types of blobs, but you can configure the Cloud Controller to use separate blobstores for each type.

### Automatic blob cleanup
After a blob deletion fails silently or something else goes wrong, the blobstore might contain blobs that the Cloud Controller no longer needs or lists in its database. These are called orphan blobs, and they waste blobstore capacity.
Cloud Controller detects and removes orphan blobs by scanning part of the blobstore daily and checking for any blobs that its database does not account for. The process scans through the entire blobstore every week, and only removes blobs that show as orphans for three consecutive days.
Cloud Controller performs this automatic cleanup when the `cloud_controller_worker` job property `cc.perform_blob_cleanup` is set to `true`.

### Manual blob cleanup
Cloud Controller does not track resource cache and buildpack cache [blob types](https://docs.cloudfoundry.org/concepts/architecture/cloud-controller.html#blob-types) in its database, so it does not [clean them up automatically](https://docs.cloudfoundry.org/concepts/architecture/cloud-controller.html#automatic-clean) as it does with app package, buildpack, and droplet type blobs.
To clean up the buildpack cache, admin users can run `cf curl -X DELETE /v2/blobstores/buildpack_cache`. This empties the buildpack cache completely, which is a safe operation.
To clean up the resource cache, delete it as follows:

* **Internal blobstore**: Run `bosh ssh` to connect to the blobstore VM (NFS or WebDav) and `rm *` the contents of the `/var/vcap/store/shared/cc-resources` directory.

* **External blobstore**: Use the file store’s API to delete the contents of the `resources` bucket.
Do not manually delete app package, buildpack, or droplet blobs from the blobstore. To free up resources from those locations, run `cf delete-buildpack` for buildpacks or `cf delete` for app packages and droplets.

## Testing
By default `rspec` runs a test suite with the SQLite in-memory database.
Specify a connection string using the `DB_CONNECTION` environment variable to
test against Postgres and MySQL. For example:
```
DB_CONNECTION="postgres://postgres@localhost:5432/ccng" rspec
DB_CONNECTION="mysql2://root:password@localhost:3306/ccng" rspec
```
Travis currently runs two build jobs against Postgres and MySQL.
For more information about how Cloud Foundry aggregates and streams logs and metrics, see [Overview of Logging and Metrics](https://docs.cloudfoundry.org/loggregator/data-sources.html).