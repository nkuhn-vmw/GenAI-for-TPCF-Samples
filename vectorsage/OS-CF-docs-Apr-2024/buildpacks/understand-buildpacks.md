# Working with buildpacks in Cloud Foundry
This topic tells you about how buildpacks are structured and detected in Cloud Foundry.

## Buildpack scripts
A buildpack repository might contain the following scripts in the `bin` directory:

* `bin/detect` determines whether or not to apply the buildpack to an app.

* `bin/supply` provides dependencies for an app.

* `bin/finalize` prepares the app for launch.

* `bin/release` provides feedback metadata to Cloud Foundry that indicates how you can run the app.

* `bin/compile` is a deprecated alternative to `bin/supply` and `bin/finalize`.
The `bin/supply` and `bin/finalize` scripts replace the deprecated `bin/compile` script. Older buildpacks might still use `bin/compile` with the latest version of Cloud Foundry. In this case, applying multiple buildpacks to a single app is not supported. Newer buildpacks might still provide `bin/compile` for compatibility with Heroku and older versions of Cloud Foundry.
The `bin/supply` script is required for non final buildpacks. The `bin/finalize` (or `bin/compile`) script is required for final buildpacks.
In this topic, the terms *non final buildpack* and *final buildpack*, or

*last buildpack*, are used to describe the process of applying
multiple buildpacks to an app.
For example:
```
<code>cf push APP-NAME -b FIRST-BUILDPACK -b SECOND-BUILDPACK -b FINAL-BUILDPACK</code>
```
If you use only one buildpack for your app, this buildpack behaves as a final, or last, buildpack.
When using multi buildpack support, the last buildpack in the order is the final buildpack, and
is able to make changes to the app and determine a start command. All other specified buildpacks are non
final and supply only the dependencies.

### bin/detect
The `detect` script determines whether or not to apply the buildpack to an app. The script is called with one argument, the `build` directory for the app. The `build` directory contains the app files uploaded when you run `cf push`.
The `detect` script returns an exit code of `0` if the buildpack is compatible with the app. In the case of system buildpacks, the script prints the buildpack name, version, and other information to `STDOUT`.
The following is an example `detect` script that checks for a Ruby app that is based on the existence of a `Gemfile`:
```

#!/usr/bin/env ruby
gemfile_path = File.join ARGV[0], "Gemfile"
if File.exist?(gemfile_path)
puts "Ruby"
exit 0
else
exit 1
end
```
The buildpack `detect` script output provides additional details by the buildpack developer. This includes buildpack version information and a list of configured frameworks and their associated versions.
The following is an example of the detailed information returned by the Java buildpack:
```
java-buildpack=v3.0-https://github.com/cloudfoundry/java-buildpack.git#3bd15e1 open-jdk-jre=1.8.0_45 spring-auto-reconfiguration=1.7.0_RELEASE tomcat-access-logging-support=2.4.0_RELEASE tomcat-instance=8.0.21 tomcat-lifecycle-support=2.4.0_RELEASE ...
```
By default, Cloud Foundry detects only one buildpack. When you want to detect multiple
buildpacks, you must explicitly specify them.
For more information, see [Buildpack detection](https://docs.cloudfoundry.org/buildpacks/understand-buildpacks.html#buildpack-detection).

### bin/supply
The `supply` script provides dependencies for the app and runs for all buildpacks. All output is sent to `STDOUT` and is relayed to the user through the Cloud Foundry Command Line Interface (cf CLI).
The script is run with four arguments:

* The `build` directory for the app.

* The `cache` directory, which is a location the buildpack can use to store assets during the build process.

* The `deps` directory, which is where dependencies provided by all buildpacks are installed.

* The `index`, which is a number that represents the ordinal position of the buildpack.
The `supply` script stores dependencies in the `deps`/`index` directory. It might also look in other directories in `deps` to find dependencies supplied by other buildpacks.
The `supply` script must not modify anything outside of the `deps`/`index` directory. Staging might fail if such modification is detected.
The `cache` directory is provided to the `supply` script for the final buildpack and is preserved even when the buildpack is upgraded or changes. The `finalize` script also has access to this cache directory.
The `cache` directories provided to the `supply` scripts of non final buildpacks are cleared if those buildpacks are upgraded or changed.
The following is an example of a simple `supply` script:
```

#!/usr/bin/env ruby

#sync output
$stdout.sync = true
build_path = ARGV[0]
cache_path = ARGV[1]
deps_path = ARGV[2]
index = ARGV[3]
install_ruby
private
def install_ruby
puts "Installing Ruby"

# !!! build tasks go here !!!

# download ruby

# install ruby
end
```

### bin/finalize
The `finalize` script prepares the app for launch and runs only for the last buildpack. All output is sent to `STDOUT` and is relayed to the user through the cf CLI.
The script is run with four arguments:

* The `build` directory for the app.

* The `cache` directory, which is a location the buildpack can use to store assets during the build process.

* The `deps` directory, which is where dependencies provided by all buildpacks are installed.

* The `index`, which is a number that represents the ordinal position of the buildpack.
The `finalize` script might find dependencies installed by the `supply` script of the same buildpack in `deps`/`index` directory. It might also look in other directories in `deps` to find dependencies that are supplied by other buildpacks.
The `cache` directory provided to the `finalize` script is preserved even when the buildpack is upgraded or otherwise changes. The `supply` script of the same buildpack also has access to this cache directory.
The following example shows a simple `finalize` script:
```

#!/usr/bin/env ruby

#sync output
$stdout.sync = true
build_path = ARGV[0]
cache_path = ARGV[1]
deps_path = ARGV[2]
index = ARGV[3]
setup_ruby
private
def setup_ruby
puts "Configuring your app to use Ruby"

# !!! build tasks go here !!!

# setup ruby
end
```

### Deprecated bin/compile
The `compile` script is deprecated. It encompasses the behavior of the `supply` and `finalize` scripts for single buildpack apps by using the `build` directory to store dependencies.
The script is run with two arguments:

* The `build` directory for the app.

* The `cache` directory, which is a location the buildpack can use to store assets during the build process.
During the running of the `compile` script, all output is sent to `STDOUT` and relayed to the user through the cf CLI.

### bin/release
The `release` script provides feedback metadata to Cloud Foundry that indicates how you run the app. The script is run with one argument, the `build` directory. The script must generate a YAML file in the following format:
```
default\_process\_types:
web: start\_command.filetype
```
The `default_process_types` line indicates the type of app being run and the command used to start it. This start command is used if a start command is not specified in the `cf push` or in a Procfile.
At this time, only the `web` type of apps is supported.
To define environment variables for your buildpack, add a Bash script to the `.profile.d`
directory in the root folder of your app.
The following example shows what a `release` script for a Rack app might return:
```
default_process_types:
web: bundle exec rackup config.ru -p $PORT
```
The `web` command runs as `bash -c COMMAND` when Cloud Foundry starts your app.

## Droplet filesystem
The buildpack staging process extracts the droplet into the `/home/vcap` directory inside the instance container and creates the following filesystem tree:
```
app/
deps/
logs/
tmp/
staging_info.yml
```
The `app` directory includes the contents of the `build` directory, and the `staging_info.yml` file contains the staging metadata saved in the droplet.

## Buildpack detection
When you push an app, Cloud Foundry uses a detection process to determine a single buildpack to use. For general information about this process, see [How Diego Stages Buildpack Apps](https://docs.cloudfoundry.org/concepts/how-applications-are-staged.html#stage-buildpack) section of the *How Apps Are Staged* topic.
During staging, each buildpack has a position in a priority list. You can retrieve this position by running the `cf buildpacks`.
Cloud Foundry checks if the buildpack in position 1 is a compatible buildpack. If the position 1 buildpack is not compatible, Cloud Foundry moves on to the buildpack in position 2. Cloud Foundry continues this process until the correct buildpack is found.
If no buildpack is compatible, the `cf push` command fails with the following error:
```
None of the buildpacks detected a compatible application
Exit status 222
Staging failed: Exited with status 222
FAILED
NoAppDetectedError
```
For a more detailed account of how Cloud Foundry interacts with the buildpack, see [Sequence of interactions](https://docs.cloudfoundry.org/buildpacks/understand-buildpacks.html#interactions).

## Sequence of interactions
This section describes the sequence of interactions between the Cloud Foundry platform and the buildpack. The sequence of interactions differs depending on whether the platform skips or performs buildpack detection.

### No buildpack detection
Cloud Foundry skips buildpack detection if the developer specifies one or more buildpacks in the app manifest or in the `cf push APP-NAME -b BUILDPACK-NAME` cf CLI command.
If you explicitly specify buildpacks, Cloud Foundry performs the following interactions:

1. For each buildpack except the last buildpack, the platform:

2. Creates the `deps`/`index` directory.

3. Runs `/bin/supply` with the `build`, `cache`, and `deps` directories and the buildpack `index`.

4. Accepts any modification of the `deps`/`index` directory.

5. Accepts any modification of the `cache` directory.

6. Might disallow modification of any other directories.

7. For the last buildpack, the platform:

8. If `/bin/finalize` is present:

9. Creates the `deps`/`index` directory if it does not exist.

10. If `/bin/supply` is present, runs `/bin/supply` with the `build`, `cache`, and `deps` directories and the buildpack `index`.

11. Accepts any modification of the `deps`/`index` directory.

12. Might disallow modification of the `build` directory.

13. Runs `/bin/finalize` with the `build`, `cache`, and `deps` directories and the buildpack `index`.

14. Accepts any modification of the `build` directory.

15. If `/bin/finalize` is not present:

16. Runs `/bin/compile` with the `build` and `cache` directories.

17. Accepts any modification of the `build` directory.

18. Runs `/bin/release` to determine staging information.
At the end of this process, the `deps` directory is included at the root of the droplet, adjacent to the `app` directory.

### Buildpack detection
Cloud Foundry does buildpack detection if you do not specify one or more buildpacks in the app manifest or in the `cf push APP-NAME -b BUILDPACK-NAME` cf CLI command.
Cloud Foundry detects only one buildpack to use with the app.
If the platform performs detection, it:

1. Runs `/bin/detect` for each buildpack.

2. Selects the first buildpack with a `/bin/detect` script that returns a zero exit status.

3. If `/bin/finalize` is present:

4. Creates the `deps`/`index` directory if it does not exist.

5. If `/bin/supply` is present, runs `/bin/supply` with the `build`, `cache`, and `deps` directories and the buildpack `index`.

6. Accepts any modification of the `deps`/`index` directory.

7. Might disallow modification of the `build` directory.

8. Runs `/bin/finalize` on the `build`, `cache`, and `deps` directories.

9. Accepts any modification of the `build` directory.

10. If `/bin/finalize` is not present:

11. Runs `/bin/compile` on the `build` and `cache` directories.

12. Accepts any modification of the `build` directory.

13. Runs `/bin/release` to determine staging information.
At the end of this process, the `deps` directory is included at the root of the droplet, adjacent to the `app` directory.