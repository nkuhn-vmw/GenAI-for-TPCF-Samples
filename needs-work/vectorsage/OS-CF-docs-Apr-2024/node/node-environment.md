# Environment variables in Node buildpack
Cloud Foundry provides configuration information to apps through environment variables.
You can also use the additional environment variables provided by the Node buildpack.
For more information about the standard environment variables provided, see [Cloud Foundry Environment Variables](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html).

## Node buildpack environment Variables
The following table describes the environment variables provided by the Node buildpack:
| Environment Variable | Description |
| --- | --- |
| `BUILD_DIR` | The directory where Node.js is copied each time a Node.js app runs. |
| `CACHE_DIR` | The directory Node.js uses for caching. |
| `PATH` | The system path used by Node.js:`PATH=/home/vcap/app/bin:/home/vcap/app/node_modules/.bin:/bin:/usr/bin` |