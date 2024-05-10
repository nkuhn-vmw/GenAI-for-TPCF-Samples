# Configuring New Relic for the PHP buildpack
[New Relic](http://newrelic.com/) collects analytics about your application and client side performance.

## Configuration
You can configure New Relic for the PHP buildpack in one of two ways:

* License key

* Cloud Foundry service

### With a license key
Use this method if you already have a New Relic account. Use these steps:

1. In a web browser. go to the New Relic website to find your [license key](https://docs.newrelic.com/docs/accounts-partnerships/accounts/account-setup/license-key).

2. Set the value of the environment variable `NEWRELIC_LICENSE` to your New Relic license key, either through the [manifest.yml file](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#env-block) or by running the `cf set-env` command.
For more information, see
<https://github.com/cloudfoundry/php-buildpack#supported-software>

### With a Cloud Foundry service
To configure New Relic for the PHP buildpack with a Cloud Foundry service, bind a New Relic service to the app.
The buildpack automatically detects and configures New Relic.
Your `VCAP_SERVICES` environment variable must contain a service named `newrelic`, the `newrelic` service must contain a key named `credentials`, and the `credentials` key must contain named `licenseKey`.

**Important**
You cannot configure New Relic for the PHP buildpack with user provided services.