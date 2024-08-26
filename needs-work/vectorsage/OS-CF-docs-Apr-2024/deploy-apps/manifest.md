# Deploying with app manifests
App manifests provide consistency and reproducibility, and can help you automate deploying apps. This topic provides basic procedures and guidance for deploying apps with a manifest file to Cloud Foundry.
Both manifests and command line options allow you to override the default attribute values of `cf push`. These attributes include the number of app instances, disk space limit, memory limit, and log rate limit.
`cf push` follows rules of precedence when setting attribute values:

* Manifests override most recent values, including defaults and values set by commands such as `cf scale`.

* Command line options override manifests.
For a full list of attributes you can specify in an app manifest, see [App manifest attribute reference](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html).

## Deploy an app with a manifest
To deploy an app with a manifest:

1. Create a `manifest.yml` file in the root directory of your app. By default, the `cf push` command uses the `manifest.yml` file in the app directory. To specify a different location for the manifest, pass its local path to the `-f` flag when you run `cf push`.

2. Add the following content to the file:
```

---
applications:

- name: APP-NAME
```
Where `APP-NAME` is the name of your app.

3. Run:
```
cf push
```
If you specify any values with command-line flags, they override the values specified in the manifest. For more information, see [Deploy multiple apps with one manifest](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#multi-apps).
For more information about manifest format and attributes, see [App manifest attribute reference](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html).

## Deploy multiple apps with one manifest
This section describes how to deploy multiple apps with a minimal manifest. For more information about manifest format and attributes, see [App manifest attribute reference](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html).

### General rules
Follow these general rules when deploying multiple apps with one manifest:

* Use a `no-route` line in the description of any app that provides background services to another app.

* You cannot use any command line options with `cf push` except for `-f` and `--no-start`.

+ If your manifest is not named `manifest.yml` or not in the current working directory, use the `-f` command line option.

* To push a single app rather than all of the apps described in the manifest, provide the app name by running `cf push APP-NAME`, where `APP-NAME` is the name of your app.

* Each app must be in a subdirectory under the same parent directory.

### Procedure
To deploy multiple apps with a manifest:

1. Create a `manifest.yml` file in the directory that contains the apps.

2. Add each app and its directory to the file. Cloud Foundry pushes the apps in the order specified in the manifest. If you push multiple apps using a manifest and one fails to deploy, Cloud Foundry does not attempt to push apps specified after the app that failed.
```

---
applications:

- name: APP-ONE
path: ./APP-ONE-DIRECTORY

- name: APP-TWO
path: ./APP-TWO-DIRECTORY
```
Where:

* `APP-ONE` is the name of the first app you want Cloud Foundry to push.

* `APP-ONE-DIRECTORY` is the directory containing the first app.

* `APP-TWO` is the name of the second app you want Cloud Foundry to push.

* `APP-TWO-DIRECTORY` is the directory containing the second app.

3. From the directory that contains the apps and the manifest, run:
```
cf push
```