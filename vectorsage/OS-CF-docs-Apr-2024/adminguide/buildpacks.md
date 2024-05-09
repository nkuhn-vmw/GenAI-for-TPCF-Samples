# Managing custom buildpacks in Cloud Foundry
You can manage additional buildpacks in Cloud Foundry by using the Cloud Foundry Command Line Interface
tool (cf CLI).
If your app uses a language
or framework that the Cloud Foundry
(Cloud Foundry) system buildpacks do not support, you can take one of the following
actions:

* Write your own buildpack. For more information, see [Creating custom buildpacks](https://docs.cloudfoundry.org/buildpacks/custom.html).

* Customize an existing buildpack.

* Use a [Cloud Foundry Community Buildpack](https://github.com/cloudfoundry-community/cf-docs-contrib/wiki/Buildpacks).

* Use a [Heroku Third-Party Buildpack](https://devcenter.heroku.com/articles/third-party-buildpacks).

## Add a buildpack
You must be a Cloud Foundry admin user to run the commands
discussed in this section.
To add a buildpack:

1. Run:
```
cf create-buildpack BUILDPACK PATH POSITION
```
Where:

* `BUILDPACK` specifies the buildpack name.

* `PATH` specifies the location of the buildpack. `PATH` can point to a ZIP file, the URL of a ZIP file, or a local
directory.

* `POSITION` specifies where to place the buildpack in the detection priority list.
For more information, see [create-buildpack](https://cli.cloudfoundry.org/en-US/cf/create-buildpack.html) in the

*Cloud Foundry CLI Reference Guide*.

2. To confirm that you have successfully added a buildpack, run:
```
cf buildpacks
```

## Rename a buildpack
To rename a buildpack:
Using cf CLI v7+ run:
```
cf update-buildpack --rename BUILDPACK-NAME NEW-BUILDPACK-NAME
```
Where:

* `BUILDPACK-NAME` is the original buildpack name.

* `NEW-BUILDPACK-NAME` is the new buildpack name.
For more information about renaming buildpacks, see
[rename-buildpack](https://cli.cloudfoundry.org/en-US/cf/rename-buildpack.html) in the

*Cloud Foundry CLI Reference Guide*.

## Update a buildpack
To update a buildpack, run:
```
cf update-buildpack BUILDPACK [-p PATH] [-i POSITION] [-s STACK][--enable|--disable] [--lock|--unlock] [--rename NEW_NAME]
```
Where:

* `BUILDPACK` is the buildpack name.

* `PATH` is the location of the buildpack.

* `POSITION` is where the buildpack is in the detection priority list.

* `STACK` is the stack that the buildpack uses.
If you are using cf CLI v6, use the `cf rename-buildpack` command instead of the
`--rename` flag.
For more information about updating buildpacks, see
[update buildpack](https://cli.cloudfoundry.org/en-US/cf/update-buildpack.html) in the

*Cloud Foundry CLI Reference Guide*.

## Delete a buildpack
To delete a buildpack, run:
```
cf delete-buildpack BUILDPACK [-s STACK] [-f]
```
Where:

* `BUILDPACK` is the buildpack name.

* `STACK` is the stack that the buildpack uses.
For more information about deleting buildpacks, see
[delete-buildpack](https://cli.cloudfoundry.org/en-US/cf/delete-buildpack.html) in the

*Cloud Foundry CLI Reference Guide*.

## Lock and unlock a buildpack
Every new version of Cloud Foundry ships with an updated buildpack. By default, your deployment applies
to the most recent
buildpack when you upgrade. In some cases, however, you might want to preserve an existing buildpack, rather than upgrade to the
latest version. For example, if an app you deploy depends on a specific component in Buildpack A that is not available in Buildpack B,
you might want to continue using Buildpack A.
The `--lock` flag lets you continue to use your existing buildpack even after you upgrade. Locked buildpacks are not updated when Cloud Foundry updates. You must manually unlock them to update them.
If you elect to use the `--unlock` flag, your deployment applies to the most recent buildpack when you upgrade Cloud Foundry.
```
cf update-buildpack BUILDPACK [-p PATH] [-i POSITION] [-s STACK] [--enable|--disable] [--lock|--unlock] [--rename NEW_NAME]
```

**Important**
If you are using cf CLI v6, the `--rename` flag is not supported. Use the
`cf rename-buildpack` instead.
This feature is also available through the API. See [Lock or unlock a Buildpack](https://apidocs.cloudfoundry.org/1.24.0/buildpacks/lock_or_unlock_a_buildpack.html) in the [Cloud Foundry API](https://apidocs.cloudfoundry.org/) documentation.

## Deactivate custom buildpacks
You can disable custom buildpacks for an entire deployment by adding `disable_custom_buildpacks: true` in your Cloud Foundry manifest under `properties.cc`.