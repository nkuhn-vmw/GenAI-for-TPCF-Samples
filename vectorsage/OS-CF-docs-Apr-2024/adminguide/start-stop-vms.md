# Stopping and starting virtual machines in Cloud Foundry
You can stop and start the component Cloud Foundry virtual machines that make up your deployment.
This article assumes you are using [BOSH CLI version 2](https://bosh.io/docs/cli-v2.html).
In some cases, you might want to stop all your VMs (for example, power down your deployment) or start all of your Cloud Foundry VMs (for example, recover from a power outage). You can stop or start all Cloud Foundry VMs with a single `bosh` command.
If you want to shut down or start up a single VM in your deployment, you can use the manual process described in [Stopping and Starting Individual Cloud Foundry VMs](https://docs.cloudfoundry.org/adminguide/start-stop-vms.html#manual).
This procedure uses the BOSH Command Line Interface (BOSH CLI).

## Stopping and starting all Cloud Foundry VMs
This section describes how to stop and start all the VMs in your deployment.

### Stopping all Cloud Foundry VMs
To shut down all the VMs in your deployment:

1. Scale down the following jobs to one instance:

* `consul_server`

* `mysql`

* `etcd_tls_server`

2. Run the following command for each of the deployments listed in the previous step:
```
bosh -e MY-ENV -d MY-DEPLOYMENT stop --hard
```
Where:

* `MY-ENV` is the alias you set for the BOSH Director.

* `MY-DEPLOYMENT` is the name of your deployment.
For example:
```
$ bosh -e prod -d mysql stop --hard
```
This command stops all VMs in the specified deployment. The `--hard` flag instructs BOSH to delete the VMs but retain any persistent disks.

### Starting all Cloud Foundry VMs
To start all the VMs in your deployment:

1. Select the product deployment for the VMs you want to shut down. You can run the following command to locate CF deployment manifests:
```
$ find /var/tempest/workspaces/default/deployments -name cf-*.yml
```

2. Run the following command:
```
bosh -e MY-ENV -d MY-DEPLOYMENT start
```
Where:

* `MY-ENV` is the alias you set for the BOSH Director.

* `MY-DEPLOYMENT` is the name of your deployment.
For example:
```
$ bosh -e prod -d mysql start
```
This command starts all VMs in the specified deployment.

3. If you require high availability in your deployment, scale up all instance groups to the original or desired counts.

## Stopping and starting individual Cloud Foundry VMs
This section describes how to stop and start individual VMs in your deployment.

### Find the names of your Cloud Foundry VMs
You need the full names of the VMs to stop and start them using the BOSH CLI. To find full names for the VMs running each component, run `bosh -e MY-ENV instances`, replacing `MY-ENV` with the alias you set for your BOSH Director. To filter the list of instances by deployment, run `bosh -e MY-ENV -d MY-DEPLOYMENT instances`.
For example:
```
$ bosh -e prod -d mysql instances
...
Deployment 'mysql'
Instance Process State AZ IPs
mysql/0123-abcd-4567ef89 running - 10.244.0.6
mysql/abcd-0123-ef4567ab running - 10.244.0.2
2 instances
...
```
You can see the full name of each VM in the `Instance` column of the terminal output. Each full name has:

* A prefix indicating the component function of the VM.

* An identifier string specific to the VM.
For any component, you can look for its prefix in the `bosh instances` output to find the full name of the VM or VMs that run it.

### Stopping an individual Cloud Foundry VM
To stop a job, run the following command for the component in your Cloud Foundry deployment, replacing `MY-ENV` with the alias you set for your BOSH Director and `MY-DEPLOYMENT` with the name of the deployment:
```
bosh -e MY-ENV -d MY-DEPLOYMENT stop VM-NAME
```
To delete the instance that contains the job, run the following command for the component in your Cloud Foundry deployment:
```
bosh -e MY-ENV -d MY-DEPLOYMENT stop VM-NAME --hard
```
Use the full name of the component VM as listed in your `bosh instances` terminal output without the unique identifier string.
For example, the following command stops the Loggregator Traffic Controller job:
```
$ bosh -e prod -d loggregator stop loggregator_trafficcontroller
```
To stop a specific instance of a job, include the identifier string at the end of its full name.
For example, the following command stops the Loggregator Traffic Controller job on only one Diego Cell instance:
```
$ bosh -e prod -d loggregator stop loggregator_trafficcontroller/0123-abcd-4567ef89
```
To delete the VM, include `--hard` at the end of the command. This command does not delete persistent disks.
For example, the following command deletes a specific Loggregator Traffic Controller instance:
```
$ bosh -e prod -d loggregator stop loggregator_trafficcontroller/0123-abcd-4567ef89 --hard
```

### Starting an individual Cloud Foundry VM
Run the following command for the component in your Cloud Foundry deployment you wish to start, replacing `MY-ENV` with the alias you set for your BOSH Director and `MY-DEPLOYMENT` with the name of the deployment. Use the full name of the component VM as listed in your `bosh vms` terminal output without the unique identifier string.
```
bosh -e MY-ENV -d MY-DEPLOYMENT start VM-NAME
```
The following example command starts the Loggregator Traffic Controller VM:
```
$ bosh -e prod -d loggregator start loggregator_trafficcontroller
```
To start a specific instance of a VM, include the identifier string at the end of its full name.
For example, the following command starts the Loggregator Traffic Controller job on one Diego Cell instance:
```
$ bosh -e prod -d loggregator start loggregator_trafficcontroller/0123-abcd-4567ef89
```