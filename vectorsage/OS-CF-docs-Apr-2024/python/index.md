# Python buildpack
You can push your Python app to Cloud Foundry and configure your Python app to use the Python buildpack.

## Push an app
Cloud Foundry automatically uses this buildpack if it detects a `requirements.txt` or `setup.py` file in the root directory of your project.
If your Cloud Foundry deployment does not have the Python Buildpack installed, or the installed version is out of date, you can use the latest version by specifying it with the `-b` option when you push your app. For example:
```
$ cf push my_app -b https://github.com/cloudfoundry/python-buildpack.git
```

## Supported versions
You can find the list of supported Python versions in the [Python buildpack release notes](https://github.com/cloudfoundry/python-buildpack/releases).

## Specify a Python version
You can specify a version of the Python runtime by including it within a `runtime.txt` file. For example:
```
$ cat runtime.txt
python-3.5.2
```
The buildpack only supports the stable Python versions, which are listed in the `manifest.yml` and [Python buildpack release notes](https://github.com/cloudfoundry/python-buildpack/releases).
To request the latest Python version in a patch line, replace the patch version with `x`: `3.6.x`. To request the latest version in a minor line, replace the minor version: `3.x`.
If you try to use a binary that is not currently supported, staging your app fails and you see the following error message:
```
Could not get translated url, exited with: DEPENDENCY_MISSING_IN_MANIFEST: ...
!
! exit
!
Staging failed: Buildpack compilation step failed
```

## Specify a PIP version
The Python buildpack supports dependency installation using PIP when a `requirements.txt` file is included at the top level of your app’s directory.
By default, the PIP module built into Python is used when staging your app.
The version of PIP used in this case depends on which version of Python is being used.
To use the latest version of PIP, set the `BP_PIP_VERSION` environment variable to `latest` before staging your app by doing either of the following:

* Use `cf set-env`. See [set-env](https://cli.cloudfoundry.org/en-US/v6/set-env.html) in the Cloud Foundry CLI Reference Guide.

* Set the PIP version in the app manifest. See *Environment Variables* in [App Manifest Attribute Reference](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html#env-block).
Currently, only `latest` is supported when setting `BP_PIP_VERSION`. The buildpack
does not provide multiple versions of its independent PIP dependency. You can inspect the buildpack’s
releases to determine which version of PIP is currently provided. See [Python buildpack releases](https://github.com/cloudfoundry/python-buildpack/releases) on GitHub.

## Specify a start command
The Python buildpack does not generate a [default start command](https://docs.cloudfoundry.org/devguide/deploy-apps/start-restart-restage.html#first-time) for your apps.
To stage with the Python buildpack and start an app, do one of the following:

* **[Required](https://www.pivotaltracker.com/n/projects/966314/stories/132190561) for Cloud Foundry v245 only:** Supply a Procfile. For more information about Procfiles, see the [Configuring a Production Server](https://docs.cloudfoundry.org/buildpacks/prod-server.html) topic. The following example Procfile specifies `gunicorn` as the start command for a web app running on Gunicorn:
```
web: gunicorn SERVER-NAME:APP-NAME
```

* Specify a start command with `-c`. The following example specifies `waitress-serve` as the start command for a web app running on Waitress:
```
$ cf push python-app -c "waitress-serve --port=$PORT DJANGO-WEB-APP.wsgi:MY-APP"
```

* Specify a start command in the application manifest by setting the `command` attribute. For more information, see the [Deploying with App Manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#start-commands) topic.

## Run the web server
The Python buildpack expects the Python app to listen to port 8080. You can use the exposed `PORT` variable to start the web server on the port that Cloud Foundry expects on all network interfaces.
For example, you can do the following using Flask:
```
if \_\_name\_\_ == "\_\_main\_\_":
port = int(os.getenv("PORT", 8080))
app.run(host='0.0.0.0', port=port)
```
The `PORT` variable is not visible in the GUI or the `cf env MY-APP` command.

## Vendor app dependencies
If you are deploying in an environment that is disconnected from the Internet, your application must vendor its dependencies. For more information, see [Disconnected environments](https://github.com/cf-buildpacks/buildpack-packager/blob/master/doc/disconnected_environments.md) in the `cloudfoundry/buildpack-packager` GitHub repository.
For the Python buildpack, use `pip`:
```
$ cd YOUR-APP-DIR
$ mkdir -p vendor

# vendors pip *.whl into vendor/
$ pip download -r requirements.txt --no-binary=:none: -d vendor
```
`cf push` uploads your vendored dependencies. The buildpack installs them directly from the `vendor/` directory.
To ensure proper installation of dependencies, Cloud Foundry recommends binary vendored
dependencies (wheels). The preceding `pip download` command achieves this.

## Private dependency repository
To deploy apps in an environment that needs to use a private dependency repository, you have the following options:

* [PIP](https://docs.cloudfoundry.org/buildpacks/python/index.html#private-repos-pip)

* [Conda](https://docs.cloudfoundry.org/buildpacks/python/index.html#private-repos-conda)

### PIP
To install dependencies using PIP, add the URL of the repository to the `requirements.txt` file in the following format:
```

--index-url=https://example.com/api/pypi/ext_pypi/simple
fixtures==2.0.0
```
If the private repository uses a custom SSL certificate that is installed on the platform, you may see an error similar to the following:
```
Could not fetch URL https://example.com/api/pypi/ext_pypi/simple/fixtures/:
There was a problem confirming the ssl certificate:
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:777) - skipping
```
This error occurs because `pip` does not use system certificates by default. To resolve this issue, set the `PIP_CERT` environment variable in the `manifest.yml` file to point to the system certificate store.
For example:
```

---
env:
PIP_CERT: /etc/ssl/certs/ca-certificates.crt
```

### Conda
To install dependencies using Conda, add a `channels` block to the `environment.yml` file.
In the `channels` block, list custom channels and add `nodefaults`. Specifying `nodefaults` tells Conda to only use the channels in the channels block.
For example:
```
channels:

- https://conda.example.com/repo

- nodefaults
```
If the private repository uses a custom SSL certificate that is installed on the platform, you may see an error similar to the following:
```
Error: Connection error: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed (_ssl.c:581):
```
This error occurs because `conda` does not use system certificates by default. To resolve this issue, set the `CONDA_SSL_VERIFY` environment variable in the `manifest.yml` file to point to the system certificate store.
For example:
```

---
env:
CONDA_SSL_VERIFY: /etc/ssl/certs/ca-certificates.crt
```

## Parse environment variables
The `cfenv` package provides access to Cloud Foundry application environment settings by parsing all the relevant environment variables. The settings are returned as a class instance. See <https://github.com/jmcarp/py-cfenv>
for more information.

## Miniconda support(starting in buildpack version1.5.6)
To use miniconda instead of pip for installing dependencies, place an `environment.yml` file in the root directory.

## Pipenv support(starting in buildpack version1.5.19)
To use [Pipenv](https://docs.pipenv.org) instead of pip (directly) for installing dependencies, place a `Pipfile` in the root directory. Easiest to let Pipenv generate this for you.

## NLTK support
To use NLTK corpora in your app, you can include an `nltk.txt` file in the root of your application. Each line in the file specifies one dataset to download. The full list of data sets available this way can be found [on the NLTK website](http://www.nltk.org/nltk_data/). The `id` listed for the corpora on that page is the string you must include in your app’s `nltk.txt`.
Example `nltk.txt`:
```
brown
wordnet
```
Having an `nltk.txt` file only causes the buildpack to download the corpora. You still must specify NLTK as a dependency of your app if you want to use it to process the corpora files.

## Proxy support
If you need to use a proxy to download dependencies during staging, you can set the `http_proxy` and `https_proxy` environment variables. For more information, see [Using a Proxy](https://docs.cloudfoundry.org/buildpacks/proxy-usage.html).

## BOSH configured custom trusted certificate support
Versions of Python 2.7.9 and later use certificates stored in `/etc/ssl/certs`. Your platform operator can configure the platform to [add the custom certificates into the application container](https://docs.cloudfoundry.org/adminguide/trusted-system-certificates.html).
To configure your Python applications to make HTTP requests with this custom certificate, set the environment variable `REQUESTS_CA_BUNDLE="/etc/ssl/certs/ca-certificates.crt"`.

## Help and support
Join the #buildpacks channel in our [Slack community](http://slack.cloudfoundry.org/) if you need any further assistance.
For more information about using and extending the Python buildpack in Cloud Foundry, see [Python buildpack](https://docs.cloudfoundry.org/buildpacks/python/index.html).
You can find current information about this buildpack on the [Python buildpack release page](https://github.com/cloudfoundry/python-buildpack/releases) in GitHub.