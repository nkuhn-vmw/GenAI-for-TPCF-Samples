# Configuring Diego Cell disk cleanup scheduling
This topic describes how to configure disk cleanup scheduling on Diego Cells in Cloud Foundry (CF).
CF isolates app instances from each other using containers that run inside Diego Cells. Containers enforce a set of isolation layers including file system isolation. A CF container file system can either be a CF stack or the result of pulling a Docker image.
For performance reasons, the Diego Cells cache the Docker image layers and the CF stacks that running app instances use. When CF destroys an app instance or when CF reschedules an app instance to a different Diego Cell, there is a chance that certain Docker image layers or an old CF stack becomes unused. If CF does not clean these unused layers, the Diego Cell ephemeral disk slowly fills.
Disk cleanup is the process of removing unused layers from the Diego Cell disk. The disk cleanup process removes all unused Docker image layers and old CF stacks, regardless of their size or age.

## Options for disk cleanup
CF provides the following options for scheduling the disk cleanup process on Diego Cells:

* **Never clean up Diego Cell disk space**: Cloud Foundry does not recommend using this option for production environments.

* **outinely clean up Diego Cell disk space**: This option makes the Diego Cell schedule a disk cleanup every time a container gets created. Running the disk cleanup process so frequently may have a negative impact on the Diego Cell performance.

* **CClean up disk space once usage fills disk**: Choosing this option makes the Diego Cell schedule the disk cleanup process only when a configurable disk space threshold is reached or exceeded.
For more information about these options, see [Configure disk cleanup scheduling](https://docs.cloudfoundry.org/running/config-cell-cleanup.html#applying-configuration).

### Recommendations
Choosing the best option for disk cleanup depends on the workload that the Diego Cells run: Docker images or Cloud Foundry buildpack-based apps.
For CF installations that mainly run **buildpack-based apps**, Cloud Foundry recommends using the **Routinely clean up Diego Cell disk space** option. The **Routinely clean up Diego Cell disk space** option ensures that when a new stack becomes available on a Diego Cell, the old stack is dropped immediately from the cache.
For CF installations that mainly run **Docker images**, or both Docker images and buildpack-based apps, Cloud Foundry recommends using the **Clean up disk space once usage fills disk** option along with a reasonable threshold. For more information about choosing a threshold, see [Choosing a threshold](https://docs.cloudfoundry.org/running/config-cell-cleanup.html#choosing-a-threshold).

### Choosing a threshold
To choose a realistic value when configuring the disk cleanup threshold, you must identify some of the most frequently used Docker images in your CF installation. Docker images tend to be constructed by creating layers over existing, base, images. In some cases, you may find it easier to identify which base Docker images are most frequently used.
To configure the disk cleanup threshold:

1. Identify the most frequently used Docker images or base Docker images. For example, the most frequently used images in a test deployment are `openjdk:7`, `nginx:1.13`, and `php:7-apache`.

2. Using the Docker CLI, measure the size of those images. For example:
```

# Pull identified images locally
$> docker pull openjdk:7
$> docker pull nginx:1.13
$> docker pull php:7-apache
```

# Measure their sizes
$> docker images
REPOSITORY TAG IMAGE ID CREATED SIZE
php 7-apache 2720c02fc079 2 days ago 391 MB
openjdk 7 f45207c01009 5 days ago 586 MB
nginx 1.13 3448f27c273f 5 days ago 109 MB
...

3. Calculate the threshold as the sum of the frequently used image sizes plus a reasonable buffer such as 15-20%. For example, using the output above, the sample threshold calculation is `(&nbsp;391&nbsp;MB&nbsp;+&nbsp;586&nbsp;MB&nbsp;+&nbsp;109&nbsp;MB&nbsp;)&nbsp;*&nbsp;1.2&nbsp;=&nbsp;1303.2&nbsp;MB`

## Configure disk cleanup scheduling
To control how Diego Cells schedule their disk cleanup, set the BOSH property `garden.graph_cleanup_threshold_in_mb` to one of the following options:

* **0**: The Diego Cell runs disk cleanup whenever it creates a new container.

* **A positive integer**: the Diego Cell runs disk cleanup whenever its total disk usage exceeds the number in MB. The number acts as the threshold. For example, as calculated in the previous step, you would set the BOSH property to **1303**.
If you are deploying CF with GrootFS, configure the `grootfs.graph_cleanup_threshold_in_mb` option instead.