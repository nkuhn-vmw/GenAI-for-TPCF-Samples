# Using PHP buildpack with runtimes
You can use the PHP buildpack with PHP or HHVM runtimes.

## Supported software and versions
The [release notes page](https://github.com/cloudfoundry/php-buildpack/releases) has a list of currently supported modules and packages.

* **PHP Runtimes**

+ php-cli

+ php-cgi

+ php-fpm

* **Third-Party Modules**

+ New Relic, in connected environments only.

## Push an app

### 30-second tutorial
With the [Cloud Foundry Command Line Interface](https://github.com/cloudfoundry/cli) installed, open a shell, change directories to the root of your PHP files and push your application using the argument `-b https://github.com/cloudfoundry/php-buildpack.git`.
Example:
```
$ mkdir my-php-app
$ cd my-php-app
$ cat << EOF > index.php
<?php
phpinfo();
?>
EOF
$ cf push -m 128M -b https://github.com/cloudfoundry/php-buildpack.git my-php-app
```
Change **my-php-app** in the above example to a unique name on your target Cloud Foundry instance to prevent a hostname conflict error and failed push.
The previous example creates and pushes a test application, **my-php-app**, to Cloud Foundry. The `-b` argument instructs CF to use this buildpack. The remainder of the options and arguments are not specific to the buildpack, for questions on those consult the output of `cf help push`.
Here’s a breakdown of what happens when you run the example:

* On your PC:

+ It creates a new directory and one PHP file, which just invokes `phpinfo()`

+ Run `cf` to push your application. This creates a new application with a memory limit of 128M (more than enough here) and upload our test file.

* Within Cloud Foundry:

+ The buildpack is run.

+ Application files are copied to the `htdocs` folder.

+ Apache HTTPD & PHP are downloaded, configured with the buildpack defaults and run.

+ Your application is accessible at the URL `http://my-php-app.example.com` (Replacing `example.com` with the domain of your public CF provider or private instance).

### More information about deployment
While the *30 Second Tutorial* shows how quick and easy it is to get started using the buildpack, it skips over quite a bit of what you can do to adjust, configure and extend the buildpack. The following sections and links provide a more in-depth look at the buildpack.

### Features
Here are some special features of the buildpack.

* Supports running commands or migration scripts prior to application startup.

* Supports an extension mechanism that allows the buildpack to provide additional functionality.

* Allows for application developers to provide custom extensions.

* Easy troubleshooting with the `BP_DEBUG` environment variable.

* Download location is configurable, allowing users to host binaries on the same network (i.e. run without an Internet connection)

* Smart session storage, defaults to file w/sticky sessions but can also use redis for storage.

### Examples
Here are some example applications that can be used with this buildpack.

* [php-info](https://github.com/cloudfoundry-samples/cf-ex-php-info) This app has a basic index page and shows the output of `phpinfo()`.

* [PHPMyAdmin](https://github.com/cloudfoundry-samples/cf-ex-phpmyadmin) A deployment of PHPMyAdmin that uses bound MySQL services.

* [PHPPgAdmin](https://github.com/cloudfoundry-samples/cf-ex-phppgadmin) A deployment of PHPPgAdmin that uses bound PostgreSQL services.

* [Drupal](https://github.com/cloudfoundry-samples/cf-ex-drupal) A deployment of Drupal that uses bound MySQL service.

* [CodeIgniter](https://github.com/cloudfoundry-samples/cf-ex-code-igniter) CodeIgniter tutorial application running on CF.

* [Stand Alone](https://github.com/cloudfoundry-samples/cf-ex-stand-alone) An example which runs a standalone PHP script.

* [pgbouncer](https://github.com/cloudfoundry-samples/cf-ex-pgbouncer) An example which runs the PgBouncer process in the container to pool database connections.

* [phalcon](https://github.com/cloudfoundry-samples/cf-ex-phalcon) An example which runs a Phalcon based application.

* [composer](https://github.com/cloudfoundry-samples/cf-ex-composer) An example which uses Composer.

### Advanced topics
See the following topics:

* [Tips for PHP developers](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-tips.html)

* [Getting started deploying PHP apps](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-usage.html)

* [PHP buildpack configuration](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-config.html)

* [Composer](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-composer.html)

* [Sessions](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-sessions.html)

* [New Relic](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-newrelic.html)
You can find the source for the buildpack on GitHub:
<https://github.com/cloudfoundry/php-buildpack>

## Proxy support
If you need to use a proxy to download dependencies during staging, you can set
the `http_proxy` and/or `https_proxy` environment variables. For more information, see
the [Proxy Usage Docs](https://docs.cloudfoundry.org/buildpacks/proxy-usage.html).

## BOSH configured custom trusted certificate support
For versions of PHP 5.6.0 and later, the default certificate location is `/usr/lib/ssl/certs`, which symlinks to `/etc/ssl/certs`.
Your platform operator can configure the platform to [add the custom certificates into the application container](https://docs.cloudfoundry.org/adminguide/trusted-system-certificates.html).

## Help and support
Join the #buildpacks channel in our [Slack community](http://slack.cloudfoundry.org/) if you need any further assistance.
For more information about using and extending the PHP buildpack in Cloud Foundry, see
the [php-buildpack GitHub repository](https://github.com/cloudfoundry/php-buildpack).
You can find current information about this buildpack on the PHP buildpack
[release page](https://github.com/cloudfoundry/php-buildpack/releases) in GitHub.

## License
The Cloud Foundry PHP Buildpack is released under v2.0 of the [Apache License](http://www.apache.org/licenses/LICENSE-2.0).