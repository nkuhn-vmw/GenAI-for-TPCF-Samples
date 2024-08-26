# Customizing and developing buildpacks in Cloud Foundry
Buildpacks enable you to package frameworks and runtime support for your application.
Cloud Foundry provides system buildpacks and an interface for customizing existing buildpacks and
developing new buildpacks.

## Customizing and creating buildpacks
If your application uses a language or framework that the Cloud Foundry system buildpacks do not support, do one of the following:

* Use a [Cloud Foundry Community Buildpack](https://github.com/cloudfoundry-community/cf-docs-contrib/wiki/Buildpacks).

* Use a [Heroku Third-Party Buildpack](https://devcenter.heroku.com/articles/third-party-buildpacks).

* Customize an existing buildpack or create your own [custom buildpack](https://docs.cloudfoundry.org/buildpacks/custom.html).
A common development practice for custom buildpacks is to fork existing buildpacks and sync subsequent patches from upstream.
For information about customizing an existing buildpack or creating your own, see the following:
```

+ <a href="./custom.html" class="subnav">Creating Custom Buildpacks</a>

+ <a href="./depend-pkg-offline.html" class="subnav">Packaging Dependencies for Offline Buildpacks</a>
```

## Maintaining buildpacks
After you have modified an existing buildpack or created your own, it is necessary to maintain it.
See the following topics to maintain your own buildpacks:

* [Merging with upstream buildpacks](https://docs.cloudfoundry.org/buildpacks/merging_upstream.html)

* [Upgrading dependency versions](https://docs.cloudfoundry.org/buildpacks/upgrading_dependency_versions.html)
To configure a production server for your web app,
see [Configuring a production server](https://docs.cloudfoundry.org/buildpacks/prod-server.html).

## Using CI for buildpacks
For information about updating and releasing a new version of a Cloud Foundry buildpack through
the Cloud Foundry Buildpacks Team Concourse pipeline, see [Using CI for buildpacks](https://docs.cloudfoundry.org/buildpacks/buildpack-ci-index.html).
You can use this as a model when working with Concourse to build and release new versions of your own buildpacks.