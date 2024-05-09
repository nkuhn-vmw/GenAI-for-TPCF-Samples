# App developer guide
This guide provides instructions for deploying, running, and managing apps and services with Cloud Foundry.

## Overview
Developing, running, and managing apps on Cloud Foundry might include:

* Deploying and scaling apps with diverse languages, frameworks, and dependencies

* Finding software services in the services Marketplace, such as databases, email, or message servers

* Creating your own Cloud Foundry service based on an external server

* Creating service instances and binding them to your apps

* Streaming app logs to an external log management service

* Troubleshooting app deployment and health
If you do these things, you are a Cloud Foundry **developer**, and the contents of this guide are for you.

## Contents

* [Considerations for designing and running an app in the cloud](https://docs.cloudfoundry.org/devguide/deploy-apps/prepare-to-deploy.html)

* **cf push:** How to use `cf push` and troubleshoot when running `cf push`.

+ [Pushing your app using Cloud Foundry CLI (cf push)](https://docs.cloudfoundry.org/devguide/deploy-apps/deploy-app.html)

+ [Deploying with app manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html)

+ [App manifest attribute reference](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest-attributes.html)

+ [Deploying your app with Docker](https://docs.cloudfoundry.org/devguide/deploy-apps/push-docker.html)

+ [Deploying your large apps](https://docs.cloudfoundry.org/devguide/deploy-apps/large-app-deploy.html)

+ [Starting, restarting, and restaging apps](https://docs.cloudfoundry.org/devguide/deploy-apps/start-restart-restage.html)

+ [Pushing an app with multiple processes](https://docs.cloudfoundry.org/devguide/multiple-processes.html)

+ [Running cf push sub-step commands](https://docs.cloudfoundry.org/devguide/push-sub-commands.html)

+ [Rolling app deployments](https://docs.cloudfoundry.org/devguide/deploy-apps/rolling-deploy.html)

+ [Pushing apps with sidecar processes](https://docs.cloudfoundry.org/devguide/sidecars.html)

+ [Using blue-green deployment to reduce downtime and risk](https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html)

+ [Troubleshooting app deployment and health](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html)

* **Routes and Domains:** How to configure routes and domains.

+ [Configuring routes and domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html)

+ [Configuring Cloud Foundry to route traffic to apps on custom ports](https://docs.cloudfoundry.org/devguide/custom-ports.html)

+ [Routing HTTP/2 and gRPC traffic to apps](https://docs.cloudfoundry.org/devguide/http2-protocol.html)

* **Managing Apps with the cf CLI:** How to manage apps through the Cloud Foundry Command Line Interface (cf CLI).

+ [Running tasks in your apps](https://docs.cloudfoundry.org/devguide/using-tasks.html)

+ [Scaling an app Using cf scale](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-scale.html)

+ [Using app health checks](https://docs.cloudfoundry.org/devguide/deploy-apps/healthchecks.html)

+ [Cloud Foundry API app revisions](https://docs.cloudfoundry.org/devguide/revisions.html)

+ [Configuring container-to-container networking](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html)

* **Managing Services:** How to use software services from your apps.

+ [Services overview](https://docs.cloudfoundry.org/services/)

+ [Managing service instances with the cf CLI](https://docs.cloudfoundry.org/devguide/services/managing-services.html)

+ [Sharing service instances](https://docs.cloudfoundry.org/devguide/services/sharing-instances.html)

+ [Delivering service credentials to an app](https://docs.cloudfoundry.org/devguide/services/application-binding.html)

+ [Managing service keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html)

+ [Managing app requests with route services](https://docs.cloudfoundry.org/devguide/services/route-binding.html)

+ [Configuring Play Framework service connections](https://docs.cloudfoundry.org/devguide/services/play-service-bindings.html)

+ [Using an external file system (volume services)](https://docs.cloudfoundry.org/devguide/services/using-vol-services.html)

+ [User-provided service instances](https://docs.cloudfoundry.org/devguide/services/user-provided.html)

* **Streaming App Logs:** How to stream app logs to third-party log management services.

+ [Streaming app logs to log management services](https://docs.cloudfoundry.org/devguide/services/log-management.html)

+ [Service-specific instructions for streaming app logs](https://docs.cloudfoundry.org/devguide/services/log-management-thirdparty-svc.html)

+ [Streaming app logs to Splunk](https://docs.cloudfoundry.org/devguide/services/integrate-splunk.html)

+ [Streaming app logs with Fluentd](https://docs.cloudfoundry.org/devguide/services/fluentd.html)

+ [Streaming app logs to Azure OMS Log Analytics](https://docs.cloudfoundry.org/devguide/services/oms-nozzle.html)

* **SSH for Apps and Services:** How to configure and use SSH access to apps and services.

+ [App SSH overview](https://docs.cloudfoundry.org/devguide/deploy-apps/app-ssh-overview.html)

+ [Accessing apps with SSH](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html)

+ [Accessing services with SSH](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-services.html)

* [Cloud Foundry environment variables](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html): The environment variables that the Cloud Foundry runtime and buildpacks set for a deployed app.

* [Cloud Controller API client libraries](https://docs.cloudfoundry.org/devguide/capi/client-libraries.html): Libraries for calling the Cloud Controller, the executive component of Cloud Foundry, programmatically.