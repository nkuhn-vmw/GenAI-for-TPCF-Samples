# Staging your apps in Cloud Foundry
This topic tells you how Diego stages buildpack apps and Docker images
in Cloud Foundry.
Cloud Foundry uses Diego to manage app containers. It is a self-healing system that attempts to keep the correct number of instances running in Diego Cells to avoid network failures and crashes. For more information about Diego, see [Diego Components and Architecture](https://docs.cloudfoundry.org/concepts/diego/diego-architecture.html).
Learn about tasks and long-running processes (LRPs).
For more information about these, see the [Tasks and Long-Running Processes](https://docs.cloudfoundry.org/concepts/diego/diego-auction.html#processes) section of the *How Diego Balances App Processes* topic.
To better understand the flow and caching of source bits during staging, see the [How Staging Uses the Blobstore](https://docs.cloudfoundry.org/concepts/cc-blobstore.html#stage-blobstore) section of the *Cloud Controller blobstore* topic.

## How Diego stages buildpack apps
Learn how Diego stages buildpack apps.
The following diagram illustrates the steps and components involved in the process of staging a buildpack app.
The staging process for buildpack apps includes a developer and the following components: CF Command Line, Cloud Controller (CCNG), CCNG Blobstore, CCDB, Diego Cell (Staging), and Diego Cell (Running).\

* Step 1: cf push from Developer to CF Command Line.

* Step 2: Create App from CF Command Line to Cloud Controller (CCNG).

* Step 3: Stores App Metadata from CCNG to the CCDB.

* Step 4: Upload App Files from the CF Command Line to CCNG.

* Step 5: Store App Files from CCNG to CCNG Blobstore.

* Step 6: App Start from CF Command Line to CCNG.

* Step 7: Stage App from CCNG to Diego Cell (Staging).

* Step 8: Stream Staging Output from Diego Cell (Staging) to the Developer.

* Step 9: Store App Droplet from Diego Cell (Staging) to CCNG Blobstore.

* Step 10: Report Staging Complete from Diego Cell (Staging) to CCNG.

* Step 11: Start Staged App from CCNG to Diego Cell (Running).

* Step 12: Report App Status from Diego Cell (Running) to CCNG.
![Full description of this diagram is in the text.](https://docs.cloudfoundry.org/concepts/images/app_push_flow_diagram_diego.png)
The following steps describe the process of staging a buildpack app:

1. A developer runs `cf push`.

2. Cloud Foundry Command Line Interface (cf CLI) tells the Cloud Controller to create a record for the app. For more information about the Cloud Controller, see [Cloud Controller](https://docs.cloudfoundry.org/concepts/architecture/cloud-controller.html).

3. Cloud Controller stores the app metadata. App metadata can include the app name, number of instances, buildpack, and other information about the app.

4. This step includes:

1. The cf CLI requests a resource match from the Cloud Controller.

2. The cf CLI uploads the app source files, omitting any app files that already exist in the resource cache.

3. The Cloud Controller combines the uploaded app files with files from the resource cache to create the app package.

5. Cloud Controller stores the app package in the blobstore. For more information, see the [Blobstore](https://docs.cloudfoundry.org/concepts/architecture/#blob) section of the *Cloud Foundry Components* topic.

6. The cf CLI issues a request to start the app.

7. This step includes:

1. The Cloud Controller issues a staging request to Diego.

2. Diego schedules a Diego Cell to run the staging task.

3. The task downloads buildpacks and the app buildpack cache, if present.

4. The task uses the buildpack to compile and stage the app.

8. Diego Cell streams the output of the staging process. You might need to view the output to troubleshoot staging problems.

9. This step includes:

1. The task creates a tarball, or droplet, with the compiled and staged app.

2. The Diego Cell stores the droplet in the blobstore.

3. The task uploads the buildpack cache to the blobstore for use the next time the app is staged.

10. Diego Bulletin Board System (BBS) reports to the Cloud Controller that staging is complete. If staging does not complete within 15 minutes, it fails.

11. Diego schedules the app as a LRP on one or more Diego Cells.

12. Diego Cells report the status of the app to the Cloud Controller.

## How Diego stages Docker images
This section describes how Diego stages Docker images.
The following diagram illustrates the steps and components involved in the process of staging a Docker image.
The staging process for Docker images includes a developer and the following components: CF Command Line, Cloud Controller (CCNG), CCDB, Diego Cell (Staging), and Diego Cell (Running).

* Step 1: CF Push from Developer to CF Command Line.

* Step 2: Create Record from CF Command Line to CCNG.

* Step 3: Stage Image from CCNG to CCDB.

* Step 4: Stream Staging Output from Diego Cell (Staging) to Developer.

* Step 5: Fetch Metadata from Diego Cell (Staging) to CCNG.

* Step 6: Store Metadata from CCNG to CCDB.

* Step 7: Submit LRP an Run Start Command from CCNG to Diego Cell (Running).
![Full description of this diagram is in the text.](https://docs.cloudfoundry.org/concepts/images/docker_push_flow_diagram_diego.png)
The following describe each step in the process of staging a Docker image:

1. A developer runs `cf push` and includes the name of a Docker image in an accessible Docker Registry.

2. The cf CLI tells the Cloud Controller to create a record for the Docker image.

3. This step includes:

1. The Cloud Controller issues a staging request to Diego.

2. Diego schedules a Diego Cell to run the task.

4. Diego Cell streams the output of the staging process. You might need to view the output to troubleshoot staging problems.

5. The task fetches the metadata associated with the Docker image and returns a portion of it to the Cloud Controller.

6. Cloud Controller stores the metadata in the Cloud Controller database.

7. This step includes:

1. Cloud Controller uses the Docker image metadata to construct a LRP that runs the start command specified in the Dockerfile.

2. Cloud Controller submits the LRP to Diego.

3. Diego schedules the LRP on one or more Diego Cells.

4. Cloud Controller instructs Diego and the Gorouter to route traffic to the Docker image.
Cloud Controller takes into account any user-specified overrides specified in the Dockerfile, such as
environment variables.