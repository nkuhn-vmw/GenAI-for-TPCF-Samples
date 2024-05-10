# Ruby buildpack
Cloud Foundry uses the Ruby buildpack if your app has a `Gemfile` and `Gemfile.lock` in the root directory.
The Ruby buildpack uses Bundler to install your dependencies.
If your Cloud Foundry deployment does not have the Ruby buildpack installed or the installed version is out of date,
push your app with the `-b` option to specify the buildpack:
```
$ cf push MY-APP -b https://github.com/cloudfoundry/ruby-buildpack.git
```
For more detailed information about deploying Ruby applications see the following topics:

* [Tips for Ruby developers](https://docs.cloudfoundry.org/buildpacks/ruby/ruby-tips.html)

* [Getting started deploying apps](https://docs.cloudfoundry.org/buildpacks/ruby/deploying-apps-index.html)

* [Configuring Rake Tasks for deployed apps](https://docs.cloudfoundry.org/buildpacks/ruby/rake-config.html)

* [Environment variables defined by the Ruby buildpack](https://docs.cloudfoundry.org/buildpacks/ruby/ruby-environment.html)

* [Configuring service connections for Ruby](https://docs.cloudfoundry.org/buildpacks/ruby/ruby-service-bindings.html)

* [Support for Windows Gemfiles](https://docs.cloudfoundry.org/buildpacks/ruby/windows.html)
See the source for the Ruby buildpack in the [Ruby buildpack repository](https://github.com/cloudfoundry/ruby-buildpack) on GitHub.

## Supported versions
See the supported Ruby versions in the [release notes for the Ruby buildpack](https://github.com/cloudfoundry/ruby-buildpack/releases) on GitHub.

## Specify a Ruby version
You can specify specific versions of the Ruby runtime in the `Gemfile` for your app as described in the following sections.
If you don’t specify a version of the Ruby runtime, the default Ruby version listed in the
[buildpack manifest.yml file](https://github.com/cloudfoundry/ruby-buildpack/blob/950b2337ff8a7ac0a68f7420f48ddc4ae4764977/manifest.yml#L3-L5) is used.

### MRI
For MRI, specify the version of Ruby in your `Gemfile` as follows:
```
ruby '~> 2.2.3'
```
With this example declaration in the `Gemfile`, if Ruby versions `2.2.4`, `2.2.5`, and `2.3.0` are present in the Ruby buildpack, the app uses Ruby version `2.2.5`.
For more information about the `ruby` directive for Bundler Gemfiles, see the [Bundler documentation](http://bundler.io/gemfile_ruby.html).
If you use v1.6.18 or earlier, you must specify an exact version, such as `ruby '2.2.3'`.
In [Ruby Buildpack v1.6.18](https://github.com/cloudfoundry/ruby-buildpack/releases/tag/v1.6.18) and earlier, Rubygems do not support version operators for the `ruby` directive.

### JRuby
For JRuby, specify the version of Ruby in your `Gemfile` based on the version of JRuby your app uses.
JRuby version `1.7.x` supports either `1.9` mode or `2.0` mode.

* For `1.9` mode, use:
```
ruby '1.9.3', :engine => 'jruby', :engine\_version => '1.7.25'
```

* For `2.0` mode, use:
```
ruby '2.0.0', :engine => 'jruby', :engine\_version => '1.7.25'
```
For Jruby version `>= 9.0`, use:
```
ruby '2.2.3', :engine => 'jruby', :engine\_version => '9.0.5.0'
```
The Ruby buildpack only supports the stable Ruby versions listed in the `manifest.yml` and [release notes for the Ruby buildpack](https://github.com/cloudfoundry/ruby-buildpack/releases) on GitHub.
If you try to use a binary that is not supported, staging your app fails with the following error message:
```
Could not get translated url, exited with: DEPENDENCY_MISSING_IN_MANIFEST: ...
!
! exit
!
Staging failed: Buildpack compilation step failed
```
The Ruby buildpack does not support the pessimistic version operator `~>` on the
Gemfile `ruby` directive for JRuby.

## Vendor app dependencies
As stated in the [Disconnected Environments documentation](https://github.com/cf-buildpacks/buildpack-packager/blob/master/doc/disconnected_environments.md), your application must ‘vendor’ its dependencies.
For the Ruby buildpack, use the `bundle package --all` command in Bundler to vendor the dependencies.
Example:
```
$ cd my-app-directory
bundle package --all
```
The `cf push` command uploads your vendored dependencies. The Ruby buildpack compiles any dependencies requiring compilation while staging your app.

## Buildpack logging and application logging
The Ruby buildpack only runs during staging, and only logs what is important to staging, such as what is being downloaded, what the configuration is, and work that the buildpack does on your application.
The buildpack stops logging when the staging is complete. The Loggregator handles application logging.
Your application must write to stdout or stderr for its logs to be included in the Loggregator stream. For more information, see [Application Logging in Cloud Foundry](https://docs.cloudfoundry.org/devguide/deploy-apps/streaming-logs.html).
If you are deploying a Rails application, the buildpack might not automatically install the necessary plug-in or gem for logging, depending on the Rails version of the application:

* Rails v2.x: The buildpack automatically installs the `rails_log_stdout` plugin into the application. For more information about the `rails_log_stdout` plugin, see the [GitHub README](https://github.com/ddollar/rails_log_stdout).

* Rails v3.x: The buildpack automatically installs the `rails_12factor` gem if it is not present and issues a warning message. You must add the `rails_12factor` gem to your `Gemfile` to quiet the warning message. For more information about the `rails_12factor` gem, see the [GitHub README](https://github.com/heroku/rails_12factor).

* Rails v4.x: The buildpack issues a warning message that the `rails_12factor` gem is not present, but does not install the gem. You must add the `rails_12factor` gem to your `Gemfile` to quiet the warning message. For more information about the `rails_12factor` gem, see the [GitHub README](https://github.com/heroku/rails_12factor).
For more information about the `rails_12factor` gem, see [GitHub README](https://github.com/heroku/rails_12factor).

## Proxy support
If you need to use a proxy to download dependencies during staging, set the `http_proxy` and `https_proxy` environment variables.
For more information, see [Using a Proxy](https://docs.cloudfoundry.org/buildpacks/proxy-usage.html).

## BOSH configured custom trusted certificate support
Ruby uses certificates stored in `/etc/ssl/certs`. Your platform operator can configure the platform to add the custom certificates into the application container.
For information about providing trusted certificates to applications running on Cloud Foundry, see [Configuring Trusted System Certificates for Applications](https://docs.cloudfoundry.org/running/trusted-system-certificates.html).

## Help and support
Join the #buildpacks channel in our [Slack community](http://slack.cloudfoundry.org/) if you need help.
For more information about using and extending the Ruby buildpack in Cloud Foundry, see the [Ruby buildpack repository](https://github.com/cloudfoundry/ruby-buildpack) on GitHub.
See the current information about the Ruby buildpack in the [release notes for the Ruby buildpack](https://github.com/cloudfoundry/ruby-buildpack/releases) on GitHub.