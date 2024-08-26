# Using Docker in Cloud Foundry
You can activate Docker support so Cloud Foundry can deploy and manage apps running in Docker containers.
For information about Diego, the Cloud Foundry component that manages app containers, see
[Diego Components and Architecture](https://docs.cloudfoundry.org/concepts/diego/diego-architecture.html). For information about how Cloud Foundry developers push apps with Docker images, see [Deploying an App with Docker](https://docs.cloudfoundry.org/devguide/deploy-apps/push-docker.html).

## Activate Docker
By default, apps deployed with the `cf push` command run in standard Cloud Foundry Linux containers. With Docker
support activated, Cloud Foundry can also deploy and manage apps running in Docker containers.
To deploy apps to Docker, developers run `cf push` with the `--docker-image` option and the location of a Docker image to create the containers from. For information about how Cloud Foundry developers push apps with Docker images, see [Push a Docker Image](https://docs.cloudfoundry.org/devguide/deploy-apps/push-docker.html).
To activate Docker support on a Cloud Foundry deployment, you must:

* Activate the `diego_docker` feature flag.

* Configure access to any Docker registries that you want to use images from.

### Enable and deactivate the diego\_docker feature flag
The `diego_docker` feature flag governs whether a Cloud Foundry deployment supports Docker containers.
To activate Docker support, run:
```
cf enable-feature-flag diego_docker
```
To deactivate Docker support, run:
```
cf disable-feature-flag diego_docker
```
Deactivating the `diego_docker` feature flag stops
all Docker based apps in your deployment within a few convergence cycles, on the order of a one minute.

### Configure Docker registry access
To support Docker, Cloud Foundry needs the ability to access Docker registries
using either a Certificate Authority or an IP address allow list. For information about
configuring this access, see [Installing Certificates on VMs](https://bosh.io/docs/trusted-certs/).

## Docker image contents
A Docker image consists of a collection of layers. Each layer consists of one or both of the following:

* Raw bits to download and mount. These bits form the file system.

* Metadata that describes commands, users, and environment for the layer. This metadata includes the `ENTRYPOINT` and `CMD` directives, and is specified in the Dockerfile.

## How Garden-runC creates containers
Diego currently uses Garden-runC to construct Linux containers.
Both Docker and Garden-runC use libraries from the [Open Container Initiative (OCI)](https://www.opencontainers.org/) to build Linux containers. After creation, these containers use name space isolation, or *namespaces*, and control groups, or *cgroups*, to isolate processes in containers and limit resource usage. These are common kernel resource isolation features used by all Linux containers.
Before Garden-runC creates a Linux container, it creates a file system that is mounted as the root file system of the container. Garden-runC supports mounting Docker images as the root file systems for the containers it creates.
When creating a container, both Docker and Garden-runC:

* Fetch and cache the individual layers associated with a Docker image.

* Combine and mount the layers as the root file system.
These actions produce a container whose contents exactly match the contents of the associated Docker image.
For earlier versions of Diego used Garden-Linux, see [Garden](https://docs.cloudfoundry.org/concepts/architecture/garden.html).

## How Diego runs and monitors processes
After Garden-runC creates a container, Diego runs and monitors the processes inside of it.
To determine which processes to run, the Cloud Controller fetches and stores the metadata associated with the
Docker image. The Cloud Controller uses this metadata to:

* Run the start command as the user specified in the Docker image.

* Instruct Diego and the Gorouter to route traffic to the lowest-numbered port exposed in the Docker image, or port 8080 if the Dockerfile does not explicitly expose a listen port.
For more information about Cloud Controller, see [Cloud Controller](https://docs.cloudfoundry.org/concepts/architecture/cloud-controller.html).
For more information about Gorouter and the routing tier, see [Cloud Foundry Routing Architecture](https://docs.cloudfoundry.org/concepts/cf-routing-architecture.html).
For more information about exposed ports in Docker images, see the [Expose](https://docs.docker.com/engine/reference/builder/#expose) section of the *Dockerfile reference* topic in the
Docker documentation.
When you launch an app on Diego, the Cloud Controller honors any user specified overrides. For example, a
custom start command or custom environment variables.

## Docker security concerns in a multi-tenant environment
The attack surface area for a Docker based container that runs on Diego remains somewhat higher than that of a buildpack app
because Docker allows you to fully specify the contents of your root file systems. A buildpack app runs on a trusted root filesystem.
Garden-runC provides features that allow the platform to run Docker images more securely in a multitenant context. In
particular, Cloud Foundry uses the `user-namespacing` feature found on modern Linux kernels to ensure that users
cannot gain escalated privileges on the host even if they escalate privileges within a container.
The Cloud Controller always runs Docker containers on Diego with user namespaces enabled. This security restriction
prevents certain features, for example, the ability to mount FuseFS devices, from working in Docker containers. Docker apps can use
fuse mounts through volume services, but they cannot directly mount fuse devices from within the container.
For more information about volume services, see [Using an External File System (Volume Services)](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html).
To mitigate security concerns, Cloud Foundry run only trusted Docker containers on the platform. By default,
the Cloud Controller does not allow Docker based apps to run on the platform.