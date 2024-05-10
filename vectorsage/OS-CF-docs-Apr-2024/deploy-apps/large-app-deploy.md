# Deploying large apps
When you deploy apps larger than 750 MB to Cloud Foundry, you must observe additional constraints and recommended settings.

## Deployment considerations and limitations
Deployment involves uploading, staging, and starting the app. For more information about the default time limits for uploading, staging, and starting an app, see [Deployment](https://docs.cloudfoundry.org/devguide/deploy-apps/app-lifecycle.html#deployment) in *Application container life cycle*.
To deploy large apps to Cloud Foundry, ensure that:

* The total size of the files to upload for your app does not exceed the maximum app file size set in the `cc.packages.max_package_size` property in the manifest.

* Your network connection speed is sufficient to upload your app within the 15-minute limit. The minimum recommended speed is 874 KB per second. Cloud Foundry provides an authorization token that is valid for a minimum of 20 minutes.

* You allocate enough memory for all instances of your app. Use either the `-m` flag with `cf push` or set an app memory value in your `manifest.yml` file.

* You allocate enough disk space for all instances of your app. Use either the `-k` flag with `cf push` or set a disk space allocation value in your `manifest.yml` file.

* You allocate enough log quota for all instances of your app. Use either the `-l` flag with `cf push` or set a log rate limit in your `manifest.yml` file.

* If you use an app manifest file, `manifest.yml`, specify adequate values for your app for attributes such as app memory, app start timeout, and disk space allocation. For more information about using app manifests, see [Deploying with app manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html).

* The size of each environment variable for your app does not exceed 130 KB. This includes Cloud Foundry system environment variables such as `VCAP_SERVICES` and `VCAP_APPLICATION`. For more information, see [Cloud Foundry environment variables](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html).

* You push only the files that are necessary for your app. To meet this requirement, push only the directory for your app, and remove unneeded files or use the `.cfignore` file to specify excluded files. For more information about specifying excluded files, see [Ignore unnecessary files when pushing](https://docs.cloudfoundry.org/devguide/deploy-apps/prepare-to-deploy.html#exclude) in *Considerations for Designing and Running an App in the Cloud*.

* You configure Cloud Foundry Command Line Interface (cf CLI) staging, startup, and timeout settings to override settings in the manifest, as necessary:

+ `CF_STAGING_TIMEOUT`: The maximum time in minutes that the cf CLI waits for an app to stage after Cloud Foundry uploads and
packages the app.

+ `CF_STARTUP_TIMEOUT`: The maximum time in minutes that the cf CLI waits for an app to start

+ `cf push -t TIMEOUT`: The maximum time in seconds that Cloud Foundry allows to elapse between starting an app and the first healthy response from the app. When you use this flag, the cf CLI ignores any app start timeout value set in the manifest.
For more information about using the cf CLI to deploy apps, see [Push](https://docs.cloudfoundry.org/cf-cli/getting-started.html#push) in *Getting Started with the cf CLI*.

**Important**
Changing the timeout setting for the cf CLI does not change the timeout limit for Cloud Foundry
server-side jobs such as staging or starting apps. You must change server-side timeouts in the manifest. Because of the differences between the
Cloud Foundry and cf CLI timeout values, your app might start even though the cf CLI reports `App failed`. To review the status of your app, run `cf apps APP-NAME`, where `APP-NAME` is the name of your app.

## Default settings and limitations summary
The following table provides a summary of the constraints and default settings to consider when you deploy a large app to Cloud Foundry:
| Setting | Note |
| --- | --- |
| App package size | Maximum: Set in the `cc.packages.max_package_size` in the manifest |
| Authorization token grace period | Default: 20 minutes, minimum |
| `CF_STAGING_TIMEOUT` | cf CLI environment variable
Default: 15 minutes |
| `CF_STARTUP_TIMEOUT` | cf CLI environment variable
Default: 5 minutes |
| `cf push -t TIMEOUT` | App start timeout maximum
Default: 60 seconds |
| Disk space allocation | Default: 1024 MB |
| Internet connection speed | Recommended minimum: 874 KB per second |