# Releasing a new Cloud Foundry buildpack version
You can update and release a new version of a Cloud Foundry (CF) buildpack through the
CF Buildpacks Team Concourse [pipeline](https://buildpacks.ci.cf-app.com/). Concourse is a continuous
integration (CI) tool for software development teams. This process is used by the CF Buildpacks Team and
other CF buildpack development teams. You can use this process as a model for using Concourse to build and
release new versions of your own buildpacks.
The Concourse pipelines for Cloud Foundry buildpacks are located in the [buildpacks-ci](http://github.com/cloudfoundry/buildpacks-ci) GitHub repository.

## Releasing a new buildpack version
To release a new buildpack version, do the following:

1. Download the `buildpacks-ci` repository:
```
$ git clone https://github.com/cloudfoundry/buildpacks-ci.git
```

2. From the buildpack directory, check out the `develop` branch of the buildpack:
```
$ cd /system/path/to/buildpack
$ git checkout develop
```

3. Make sure you have the most current version of the repository:
```
$ git pull -r
```

4. Run `bump` to update the version in the buildpack repository:
```
$ /system/path/to/buildpacks-ci/scripts/bump
```

5. Modify the `CHANGELOG` file manually to condense recent commits
into relevant changes. For more information, see [Modify Changelogs](https://docs.cloudfoundry.org/buildpacks/releasing_a_new_buildpack_version.html#changelogs).

6. Add and commit your changes:
```
$ git add VERSION CHANGELOG
$ git commit -m "Bump version to $(cat VERSION) [{insert story #}]"
```

7. Push your changes to the `develop` branch:
```
$ git push origin develop
```

## Concourse buildpack workflow
If `buildpacks-ci` is not deployed to Concourse, manually add
a Git tag to the buildpack, and mark the tag as a release on GitHub.
If `buildpacks-ci` is deployed to Concourse, the buildpack update passes through the following life cycle:

1. Concourse starts the `buildpack-to-master` job in the pipeline for the updated buildpack. This job merges into the master or main branch of the buildpack.

2. The `detect-new-buildpack-and-upload-artifacts` job starts in the pipeline for the updated buildpack. This job creates a cached and uncached buildpack, and uploads them to an AWS S3 bucket.

3. The `specs-lts-master` and `specs-edge-master` jobs start and
run the buildpack test suite, and the buildpack-specific tests of the [Buildpack Runtime Acceptance Tests (BRATS)](https://github.com/cloudfoundry/brats).

4. If you use [Pivotal Tracker](https://www.pivotaltracker.com), paste the links for
the `specs-edge-master` and `specs-lts-master` builds in the related buildpack release story,
and deliver the story.

5. Your project manager can manually start the `buildpack-to-github` job on Concourse as part
of the acceptance process. This releases the buildpack to GitHub.

6. After the buildpack has been released to GitHub, the `cf-release` pipeline is started using the manual initiation of
the `recreate-bosh-lite` job in that pipeline. If the new buildpack has been released to GitHub, the CF that
is deployed for testing in the `cf-release` pipeline is tested against that new buildpack.

7. After the `cats` job has successfully completed, your project manager can include the new buildpacks in the `cf-release` repository and create the new buildpack BOSH release by manually starting the `ship-it` job.
If errors occur during this workflow, you might need to remove unwanted tags. For more information, see [Handle Unwanted Tags](https://docs.cloudfoundry.org/buildpacks/releasing_a_new_buildpack_version.html#dealing-with-unwanted-tags).

## Modifying changelogs
The [Ruby buildpack changelog](https://github.com/cloudfoundry/ruby-buildpack/blob/master/CHANGELOG) shows an example
layout, and content of a changelog. In general, changelogs follow these conventions:

* Reference public tracker stories whenever possible.

* Exclude unnecessary files.

* Combine and condense commit statements into individual stories containing valuable changes.

## Handling unwanted tags
If you encounter problems with the commit that contains the new version, change the target of the release tag by performing the following:

1. Verify that the repository is in a valid state and is building successfully.

2. Remove the tag from your local repository and from GitHub.

3. Start a build. The pipeline build script tags the build again if it is successful.