# Deploying PHP apps to Cloud Foundry
Learn about deploying your PHP apps to Cloud Foundry.
If you experience a problem deploying PHP apps, review the [Troubleshooting](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-usage.html#troubleshooting) section.

## Prerequisites

* Basic PHP knowledge

* [Cloud Foundry Command Line Interface (cf CLI)](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html) installed on your workstation

## A first PHP application
```
$ mkdir my-php-app
$ cd my-php-app
$ cat << EOF > index.php
<?php
phpinfo();
?>
EOF
$ cf push my-php-app -m 128M
```
Change “my-php-app” to a unique name or you may see an error and a failed push.
The previous example creates and pushes a test application to Cloud Foundry.
Here is a breakdown of what happens when you run the example:

* On your workstation…

+ It creates a new directory and one PHP file, which calls `phpinfo()`

+ Run `cf push` to push your application. This creates a new
application with a memory limit of 128M and uploads our test file.

* On Cloud Foundry…

+ The buildpack detects that your app is a php app

+ The buildpack is run.

- Application files are copied to the `htdocs` folder.

+ Apache HTTPD & PHP are downloaded, configured with the buildpack defaults, and run.

+ Your application is accessible at the default route. Run `cf app my-php-app` to view the url of your new app.

## Folder structure
The easiest way to use the buildpack is to put your assets and PHP files into a directory and push it to Cloud Foundry.
This way, the buildpack takes your files and moves them into the `WEBDIR` (defaults to `htdocs`) folder, which is the directory where your chosen web server looks for the files.

### URL rewriting
If you select Apache as your web server, you can include `.htaccess` files with your application.
Also, you can [provide your own Apache or Nginx configurations](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-config.html#engine-configurations).

### Prevent access to PHP files
The buildpack puts all of your files into a publicly accessible directory. In some cases, you might want to
have PHP files that are not publicly accessible but are on the [include\_path](http://us1.php.net/manual/en/ini.core.php#ini.include-path). To do that, create a `lib` directory in your project folder and place your protected files there.
For example:
```
$ ls -lRh
total 0

-rw-r--r-- 1 daniel staff 0B Feb 27 21:40 images

-rw-r--r-- 1 daniel staff 0B Feb 27 21:39 index.php
drwxr-xr-x 3 daniel staff 102B Feb 27 21:40 lib
./lib:
total 0

-rw-r--r-- 1 daniel staff 0B Feb 27 21:40 my.class.php <-- not public, http://app.cfapps.io/lib/my.class.php == 404
```
This comes with a catch. If your project legitimately has a `lib` directory, these files will not be publicly available because the buildpack does not copy a top-level `lib` directory into the `WEBDIR` folder. If your project has a `lib` directory that needs to be publicly available, then you have two options as follows:

#### Option #1
In your project folder, create an `htdocs` folder (or whatever you’ve set for `WEBDIR`). Then move any files that can be publicly accessible into this directory. In the following example, the `lib/controller.php` file is publicly accessible.
Example:
```
$ ls -lRh
total 0
drwxr-xr-x 7 daniel staff 238B Feb 27 21:48 htdocs
./htdocs: <-- create the htdocs directory and put your files there
total 0

-rw-r--r-- 1 daniel staff 0B Feb 27 21:40 images

-rw-r--r-- 1 daniel staff 0B Feb 27 21:39 index.php
drwxr-xr-x 3 daniel staff 102B Feb 27 21:48 lib
./htdocs/lib: <-- anything under htdocs is public, including a lib directory
total 0

-rw-r--r-- 1 daniel staff 0B Feb 27 21:48 controller.php
```
Given this setup, it is possible to have both a public `lib` directory and a protected `lib` directory. The following example demonstrates this setup:
Example:
```
$ ls -lRh
total 0
drwxr-xr-x 7 daniel staff 238B Feb 27 21:48 htdocs
drwxr-xr-x 3 daniel staff 102B Feb 27 21:51 lib
./htdocs:
total 0

-rw-r--r-- 1 daniel staff 0B Feb 27 21:40 images

-rw-r--r-- 1 daniel staff 0B Feb 27 21:39 index.php
drwxr-xr-x 3 daniel staff 102B Feb 27 21:48 lib
./htdocs/lib: <-- public lib directory
total 0

-rw-r--r-- 1 daniel staff 0B Feb 27 21:48 controller.php
./lib: <-- protected lib directory
total 0

-rw-r--r-- 1 daniel staff 0B Feb 27 21:51 my.class.php
```

#### Option #2
The second option is to pick a different name for the `LIBDIR`. This is a configuration option that you can set (it defaults to `lib`). Thus if you set it to something else such as `include`, your application’s `lib` directory would no longer be treated as a special directory and it would be placed into `WEBDIR` (i.e. become public).

#### Other folders
Beyond the `WEBDIR` and `LIBDIR` directories, the buildpack also supports a `.bp-config` directory and a `.extensions` directory.
The `.bp-config` directory exists at the root of your project directory and it is the location of application-specific configuration files. Application-specific configuration files override the default settings used by the buildpack. This link explains [application configuration files](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-config.html) in depth.
The `.extensions` directory also exists at the root of your project directory and it is the location of application-specific custom extensions. Application-specific custom extensions allow you, the developer, to override or enhance the behavior of the buildpack. See the [php-buildpack README](https://github.com/cloudfoundry/php-buildpack/blob/master/README.md) in GitHub for more information about extensions.

## Troubleshooting
To troubleshoot problems using the buildpack, you can do one of the following:

1. Review the output from the buildpack. The buildpack writes basic information to stdout, for example the files that it downloads. The buildpack also writes information in the form of stack traces when a process fails.

2. Review the logs from the buildpack. The buildpack writes logs to disk.
Follow these steps to access these logs:

1. SSH into the app container by running:
```
cf ssh APP-NAME
```
Where `APP-NAME` is the name of your app.

2. To view the logs, run:
```
cat app/.bp/logs/bp.log
```
By default, log files contain more detail than output to stdout. Set the `BP_DEBUG` environment variable to `true` for more verbose logging. This instructs the buildpack to set its log level to `DEBUG`, and to output logs to stdout. Follow [Environment Variables documentation](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#env-block) to set `BP_DEBUG`.

### Increasing log output with fpm.d
If you use [fpm.d](https://docs.cloudfoundry.org/buildpacks/php/gsg-php-config.html#fpm_d), follow these steps to configure `fpm` to redirect worker stdout and stderr into the logs:

1. Create a file in the `.bp-config/php/fpm.d/` directory of your app.

2. Add `catch_workers_output=yes` to the file you created.

3. Push your app.
For more information about allowed configuration settings in the `.bp-config/php/fpm.d` directory, see the [List of global php-fpm.conf directives](http://php.net/manual/en/install.fpm.configuration.php).
You can see an example [fmp fixture and configuration file](https://github.com/cloudfoundry/php-buildpack/blob/633bc6f0c078043186673a90d9727188501a866b/cf_spec/fixtures/php_71_with_fpm_d/.bp-config/php/fpm.d/output.conf) in the php-buildpack GitHub repository.