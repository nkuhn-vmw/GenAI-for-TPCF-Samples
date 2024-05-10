# Deploying your app with docker
You can use the [Cloud Foundry Command Line Interface (cf CLI)](https://docs.cloudfoundry.org/cf-cli/install-go-cli.html) to push an app with a new or updated Docker image. Cloud Foundry then uses the Docker image to create containers for the app.
For an explanation of how Docker works in Cloud Foundry, see [Using Docker in Cloud Foundry](https://docs.cloudfoundry.org/adminguide/docker.html).

## Requirements
To push apps with Docker, you need:

* A Cloud Foundry deployment with Docker support activated. To enable Docker support, see the [Enable Docker](https://docs.cloudfoundry.org/adminguide/docker.html#enable) section of the *Using Docker in Cloud Foundry* topic.

* A Docker image that meets the following requirements:

+ The Docker image must contain an `/etc/passwd` file with an entry for the `root` user. In addition, the home directory and the shell for that `root` user must be present in the image file system.

+ The total size of the Docker image file system layers must not exceed the disk quota for the app. The maximum disk allocation for apps is set by the Cloud Controller. The default maximum disk quota is 2048 MB per app.

**Important**
If the total size of the Docker image file system layers exceeds the disk quota, the app instances do not start.

* The location of the Docker image on Docker Hub or another Docker registry.

* A registry that supports the Docker Registry HTTP API V2 and presents a valid certificate for HTTPS traffic. For more information, see the [Docker Registry HTTP API V2](https://docs.docker.com/registry/spec/api/) spec in the Docker documentation.

### Requirement for cf ssh support
To log in to your application container using the `cf ssh` command, you must make a shell such as `sh` or `bash` available in the container.
The SSH server in the container looks for the following executables in absolute locations or the `PATH` environment variable:

* `/bin/bash`

* `/usr/local/bin/bash`

* `/bin/sh`

* `bash`

* `sh`

## Benefits of specifying tags
To make your application container consistent after platform updates and code changes, specify a tag when you push your Docker image. Otherwise, the platform applies the `latest` tag without respecting changes to `PORT` or `ENTRYPOINT`.
If you push your Docker image without specifying a tag, you must run `cf restage` for the changes to take effect.

## Port configuration
By default, apps listen for connections on the port specified in the `PORT` environment variable for the app. Cloud Foundry allocates this value dynamically.
When configuring a Docker image for Cloud Foundry, you can control the exposed port and the corresponding value of `PORT` by specifying the `EXPOSE` directive in the image Dockerfile. If you specify the `EXPOSE` directive, then the corresponding app pushed to Cloud Foundry listens on that exposed port. For example, if you set `EXPOSE` to `7070`, then the app listens for connections on port 7070.
If you do not specify a port in the `EXPOSE` directive, then the app listens on the value of the `PORT` environment variable as determined by Cloud Foundry.
If you set the `PORT` environment variable via an `ENV` directive in a Dockerfile, Cloud Foundry overrides the value with the system-determined value.
Cloud Foundry supports only one exposed port on the image.
For more information about the `PORT` environment variable, see the [PORT](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#PORT) section of *Cloud Foundry Environment variables*. For more information about the `EXPOSE` directive, see the [EXPOSE](https://docs.docker.com/engine/reference/builder/#expose) in the Docker documentation.

## Start command
By default, Docker uses the start command specified in the Docker image. You can override the start command either by using a command-line parameter or by specifying it in a manifest file.
For more information about command-line parameters for `docker start`, see [docker start](https://docs.docker.com/engine/reference/commandline/start/) in the Docker Documentation.

## Push a Docker image from a registry
Cloud Foundry supports pushing apps from container registries such as Docker Hub, Google Container Registry (GCR), and Amazon Elastic Container Registry (ECR).
How you run `cf push` with apps stored in container registries depends on which registry you use and how it authenticates requests for the container image.
The following sections explain how to push apps under different container registry scenarios.

### Docker Hub
To deploy a Docker image from a Docker Hub repository, run:
```
cf push APP-NAME --docker-image REPO/IMAGE:TAG
```
Where:

* `APP-NAME` is the name to give the pushed app on Cloud Foundry.

* `REPO` is the name of the repository where the image is stored.

* `IMAGE` is the name of the app image on Docker Hub.

* (Optional, but recommended) `TAG` is the tag or version for the image.
For example, the following command pushes the `your-image` image from Docker Hub to a Cloud Foundry app:
```
cf push your-app --docker-image cloudfoundry/your-image
```

### Private container registry without authentication
As an alternative to Docker Hub, you can use any Docker image registry that presents a valid certificate for HTTPS traffic, such as a company-internal Docker registry.
To push an app as a Docker image using a specified Docker registry, run:
```
cf push APP-NAME --docker-image YOUR-PRIVATE-REGISTRY.DOMAIN:PORT/REPO/IMAGE:TAG
```
Where:

* `APP-NAME` is the name to give the pushed app on Cloud Foundry.

* `YOUR-PRIVATE-REGISTRY.DOMAIN` is the path to the Docker registry.

* `PORT` is the port where the registry serves traffic.

* `REPO` is the name of the repository where the image is stored.

* `IMAGE` is the name of the app image being pushed.

* (Optional, but recommended) `TAG` is the tag or version for the image.
For example, the following command pushes the `v2` version of the `your-image` image from the `your-repo` repository of the `internal-registry.example.com` registry on port `5000`:
```
cf push your-app --docker-image internal-registry.example.com:5000/your-repo/your-image:v2
```

### Private container registry with basic authentication
Many Docker registries control access to Docker images by authenticating with a user name and password.
To push an app as a Docker image from a registry that uses basic user name and password authentication, run:
```
CF_DOCKER_PASSWORD=YOUR-PASSWORD cf push APP-NAME --docker-image REPO/IMAGE:TAG --docker-username USER
```
Where:

* `YOUR-PASSWORD` is the password to use for authentication with the Docker registry.

+ Setting `CF_DOCKER_PASSWORD` prepended to the `cf push --docker-image` makes the value temporary, which is more secure than setting the environment variable indefinitely with `export`.

* `APP-NAME` is the name to give the pushed app on Cloud Foundry.

* `REPO` is the repository where the image is stored.

+ For Docker Hub, this is just the repository name.

+ For a private registry, this includes the registry address and port, as described in [Push a Docker image from a private registry](https://docs.cloudfoundry.org/devguide/deploy-apps/push-docker.html#private), in the format `YOUR-PRIVATE-REGISTRY.DOMAIN:PORT/REPO`.

* `IMAGE` is the name of the app image being pushed.

* (Optional, but recommended) `TAG` is the tag or version for the image.

* `USER` is the user name to use for authentication with the registry.
If container registry credentials change, you have two options for an update: either you push the app with the new credentials or you update the latest package with the new credentials using [PATCH /v3/packages](https://v3-apidocs.cloudfoundry.org/version/3.150.0/index.html#update-a-package) and then restage your app.
Apps require access to the container registry when starting.
If you do not update the app with the new credentials, Cloud Foundry fails to start the app.
When you rotate container credentials, Cloud Foundry recommends using a set of two credentials, where the `old` credentials can be deactivated after all apps are pushed with the `new` credentials.

### Amazon Elastic Container Registry (ECR)
Cloud Foundry supports pushing apps from images hosted on Amazon Web Services ECR, which authenticates with temporary password tokens.
To push an app as a Docker image from ECR, run:
```
CF_DOCKER_PASSWORD=AWS-SECRET-ACCESS-KEY cf push APP-NAME --docker-image REPO/IMAGE:TAG --docker-username AWS-ACCESS-KEY-ID
```
Where:

* `AWS-SECRET-ACCESS-KEY` is the AWS Secret Access Key for the IAM user accessing the ECR registry.

+ Setting `CF_DOCKER_PASSWORD` prepended to the `cf push --docker-image` makes the value temporary, which is more secure than setting the environment variable indefinitely with `export`.

* `APP-NAME` is the name to give the pushed app on Cloud Foundry.

* `REPO` is the ECR repository containing the image being pushed.

* `IMAGE` is the name of the app image being pushed.

* (Optional, but recommended) `TAG` is the tag or version for the image.

* `AWS-ACCESS-KEY-ID` is the AWS Access Key ID for the IAM user accessing the ECR registry.
Running `cf push` with an ECR registry triggers Cloud Foundry to:

1. Use the AWS Secret Access Key and Access Key ID to retrieve the temporary ECR user name and password.

2. Use the temporary tokens to retrieve the image.

### Google Container Registry (GCR)
Cloud Foundry supports pushing apps from images hosted on Google Container Registry (GCR) service.
This feature requires that you use JSON key-based authentication.
For more information about JSON key authentication,
see the [Google Cloud documentation](https://cloud.google.com/container-registry/docs/advanced-authentication#json_key).

#### Step 1: Authenticate with GCR
To authenticate with GCR, you must create a JSON key file and associate it with your project.
To create a JSON key file and associate it with your project:

1. Create a GCP service account. To create a GCP service account,
see the [Google Cloud documentation](https://cloud.google.com/compute/docs/access/create-enable-service-accounts-for-instances).
Run:
```
gcloud iam service-accounts create YOUR-ACCOUNT --display-name "YOUR-DISPLAY-NAME"
```
Where:

* `YOUR-ACCOUNT` is the name of your service account.

* `YOUR-DISPLAY-NAME` is the display name of your service account.

2. Set your project ID by running:
```
gcloud config set project YOUR-PROJECT-ID
```
Where `YOUR-PROJECT-ID` is your project ID.

3. Create a JSON key file and associate it with the service account by running:
```
gcloud iam service-accounts keys create key.json --iam-account=YOUR-ACCOUNT@YOUR-PROJECT-ID.iam.gserviceaccount.com
```
Where:

* `YOUR-ACCOUNT` is the name of your service account.

* `YOUR-PROJECT-ID` is your project ID.

4. Add the IAM policy binding for your project and service account by running:
```
gcloud projects add-iam-policy-binding YOUR-PROJECT --member serviceAccount:YOUR-ACCOUNT@YOUR-PROJECT-ID.iam.gserviceaccount.com --role roles/storage.objectViewer
```
Where:

* `YOUR-PROJECT` is the name of your project.

* `YOUR-ACCOUNT` is the name of your service account.

* `YOUR-PROJECT-ID` is your project ID.

#### Step 2: Deploy the GCP image
To deploy your GCR image using the cf CLI, run:
```
CF_DOCKER_PASSWORD="$(cat key.json)" cf push APP-NAME --docker-image docker://YOUR-REGISTRY-URL/YOUR-PROJECT/YOUR-IMAGE-NAME --docker-username _json_key`
```
Where:

* `APP-NAME` is the name of the app being pushed.

* `YOUR-REGISTRY-URL` is the URL of your registry.

* `YOUR-PROJECT` is the name of your project.

* `YOUR-IMAGE-NAME` is the name of your image.

* The `key.json` file must point to the file you created earlier.

**Note**
For information about specifying `YOUR-REGISTRY-URL`, see [Pushing and Pulling Images](https://cloud.google.com/container-registry/docs/pushing-and-pulling) in the Google Cloud documentation.

## Docker volume support
You can use volume services with Docker apps. For more information about enabling volume support, see [Using an external file system (volume services)](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html).