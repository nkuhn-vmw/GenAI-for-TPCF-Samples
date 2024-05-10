# Deploying a Nozzle to your Cloud Foundry Loggregator Firehose
You can deploy a nozzle app to the Cloud Foundry Loggregator Firehose.
For more information about nozzles and the Loggregator Firehose, see
[Loggregator Architecture](https://docs.cloudfoundry.org/loggregator/architecture.html). The Cloud Foundry Loggregator team created an example
nozzle app for use with this tutorial.
The following procedure deploys an example nozzle to the Firehose of a Cloud Foundry
installation deployed locally with BOSH Lite v2. For more information about BOSH Lite v2, see
[VirtualBox BOSH Lite v2](https://bosh.io/docs/bosh-lite/) in the BOSH documentation.
To reduce the load on custom nozzles that you develop, you can request Firehose subscriptions that emit only
metrics on an allow list. For examples, see `rlpreader` and `rlptypereader` in the
[Loggregator Tools](https://github.com/cloudfoundry-incubator/loggregator-tools) repository and
[V2 Subscriptions](https://github.com/cloudfoundry/loggregator-release/blob/main/docs/v2-subscriptions.md) in the
Loggregator Release repository in GitHub.
You can deactivate the Firehose. In place of the Firehose, you can configure an
aggregate log and metric drain for your foundation.

## Prerequisites
Before you deploy a nozzle to the Loggregator Firehose, you must have:

* BOSH CLI installed locally. For more information, see [BOSH CLI](https://bosh.io/docs/bosh-cli.html) in the BOSH
documentation.

* Spiff installed locally and added to the load path of your shell. For more information, see the
[Spiff](https://github.com/cloudfoundry-incubator/spiff) repository on GitHub.

* BOSH Lite v2 deployed locally using VirtualBox. For more information about BOSH Lite v2, see
[VirtualBox BOSH Lite v2](https://bosh.io/docs/bosh-lite/) in the BOSH documentation.

* A working Cloud Foundry deployment, including Loggregator, deployed with your local BOSH Lite v2. This
deployment serves as the source of data. Use the `provision_cf` script included in the BOSH Lite v2 release.

**Important**
Deploying Cloud Foundry can take several hours depending on your
internet bandwith, even when using the automated `provision_cf` script.

## Step 1: Downloading Cloud Foundry BOSH manifest
To download the BOSH manifest:

1. Identify the names of all deployments in the environment that you specify by running:
```
bosh -e BOSH-ENVIRONMENT deployments
```
Where `BOSH-ENVIRONMENT` is the alias that you set for your BOSH Director. For example:
```
$ bosh -e dev deployments
Using environment '192.168.15.4' as client 'admin'
Name Release(s) Stemcell(s) Team(s) Cloud Config
cf-example binary-buildpack/1.0.9 bosh-warden-boshlite-ubuntu-trusty-go_agent/3363.9 - latest
capi/1.21.0
cf-mysql/34
cf-smoke-tests/11
cflinuxfs3-rootfs/1.52.0
consul/155
diego/1.8.1
etcd/94
garden-runc/1.2.0
loggregator/78
nats/15
routing/0.145.0
statsd-injector/1.0.20
uaa/25
service-instance_0d4140a0-42b7-... mysql/0.6.0 bosh-warden-boshlite-ubuntu-trusty-go_agent/3363.9 - latest
2 deployments
Succeeded
```

2. Download and save the current BOSH deployment manifest by running:
```
bosh -e BOSH-ENVIRONMENT -d BOSH-DEPLOYMENT manifest > PATH-TO-MANIFEST.yml
```
Where:

* `BOSH-ENVIRONMENT` is your BOSH Director alias.

* `BOSH-DEPLOYMENT` is the deployment name from the output of the previous step.

* `PATH-TO-MANIFEST.yml` is a name that you choose for the saved manifest file. Use this manifest to locate
information about your databases.For example:
```
$ bosh -e dev -d cf-example manifest > cf.yml
```

## Step 2: Adding UAA client
You must authorize the example nozzle as a UAA client for your Cloud Foundry deployment. To do this, add
an entry for the example nozzle as a `client` for `uaa` under the `properties` key in your Cloud Foundry
deployment manifest YAML file. You must enter the example nozzle object in the correct location in the manifest, and
with the correct indentation.
To add the nozzle as a UAA client for your deployment:

1. Open the deployment manifest in a text editor.

2. Locate the left-aligned `properties` key.

3. Under the `properties` key, locate `uaa` at the next level of indentation.

4. Under the `uaa` key, locate the `clients` key at the next level of indentation.

5. Enter properties for the `example-nozzle` at the next level of indentation, exactly as shown. The `...` in the
text indicates other properties that might populate the manifest at each level in the hierarchy.
```
properties:
...
uaa:
...
clients:
...
example-nozzle:
access-token-validity: 1209600
authorized-grant-types: client_credentials
override: true
secret: example-nozzle
authorities: oauth.login,doppler.firehose
```

6. Save the deployment manifest file.

## Step 3: Redeploying Cloud Foundry
To redeploy Cloud Foundry with BOSH, run:
```
bosh -e BOSH-ENVIRONMENT deploy
```
Where `BOSH-ENVIRONMENT` is the alias that you set for your BOSH Director.
For example:
```
$ bosh -e dev deploy
Acting as user 'admin' on deployment 'cf-warden' on 'Bosh Lite Director'
Getting deployment properties from director...
Detecting deployment changes

----------------------------
Releases
No changes
Compilation
No changes
Update
No changes
Resource pools
No changes
Disk pools
No changes
Networks
No changes
Jobs
No changes
Properties
uaa
clients
example-nozzle

+ access-token-validity: 1209600

+ authorized-grant-types: authorization_code,client_credentials,refresh_token

+ override: true

+ secret: example-nozzle

+ scope: openid,oauth.approvals,doppler.firehose

+ authorities: oauth.login,doppler.firehose
Meta
No changes
Please review all changes carefully
Deploying

---------
Are you sure you want to deploy? (type 'yes' to continue):yes
```

## Step 4: Cloning an example release
The Cloud Foundry Loggregator team created an example nozzle app for use with this tutorial.
To clone the example nozzle release:

1. Clone the main release repository from the example-nozzle-release repository on GitHub by running:
```
git clone https://github.com/cloudfoundry-incubator/example-nozzle-release.git
```

2. Go to the `example-nozzle-release` directory by running:
```
cd example-nozzle-release
```

3. Update all of the included submodules by running:
```
git submodule update --init --recursive
```
For example:
```
$ git submodule update --init --recursive
Submodule 'src/github.com/cloudfoundry-incubator/example-nozzle' (git@github.com:cloudfoundry-incubator/example-nozzle.git) registered for path 'src/github.com/cloudfoundry-incubator/example-nozzle'
Submodule 'src/github.com/cloudfoundry-incubator/uaago' (git@github.com:cloudfoundry-incubator/uaago.git) registered for path 'src/github.com/cloudfoundry-incubator/uaago'
...
Cloning into 'src/github.com/cloudfoundry-incubator/example-nozzle'...
...
```

## Step 5: Preparing nozzle manifest
To prepare the nozzle deployment manifest:

1. In the `example-nozzle-release` directory, navigate to the `templates` directory by running:
```
cd templates
```
Within this directory, examine the two YAML files. `bosh-lite-stub.yml` contains the values used to populate the
missing information in `template.yml`. By combining these two files, you can create a deployment manifest for the
nozzle.

2. Create a `tmp` directory for the compiled manifest.

3. Use Spiff to compile a deployment manifest from the template and stub by running:
```
spiff merge templates/template.yml templates/bosh-lite-stub.yml > tmp/manifest_bosh_lite.yml
```
Save this manifest.

4. To identify the names of all deployments in the environment that you specify, run:
```
bosh -e BOSH-ENVIRONMENT deployments
```
Where `BOSH-ENVIRONMENT` is the alias that you set for your BOSH Director.

5. To obtain your BOSH Director UUID, run:
```
bosh -e BOSH-ENVIRONMENT env --column=uuid
```
Where `BOSH-ENVIRONMENT` is the alias that you set for your BOSH Director. For example:
```
$ bosh -e dev env --column=uuid
```

6. In the compiled nozzle deployment manifest, locate the `director_uuid` property. Replace `PLACEHOLDER-DIRECTOR-UUID`
with your BOSH Director UUID.
```
compilation:
cloud_properties:
name: default
network: example-nozzle-net
reuse_compilation_vms: true
workers: 1
director_uuid: PLACEHOLDER-DIRECTOR-UUID
```
If you do not want to see the complete deployment procedure, run
`scripts/make_manifest_spiff_bosh_lite` to prepare the manifest.

## Step 6: Creating nozzle BOSH release
To create a nozzle BOSH release, run:
```
bosh -e BOSH-ENVIRONMENT create-release --name RELEASE-NAME
```
Where:

* `BOSH-ENVIRONMENT` is the alias that you set for your BOSH Director.

* `RELEASE-NAME` is `example-nozzle` to match the UAA client that you created in the Cloud Foundry
deployment manifest.
For example:
```
$ bosh -e dev create-release --name example-nozzle
Syncing blobs...
...
```

## Step 7: Uploading nozzle BOSH release
Upload the nozzle BOSH release that you created in [Step 6: Create nozzle BOSH release](https://docs.cloudfoundry.org/loggregator/nozzle-tutorial.html#create-nozzle-bosh-release).
To upload the BOSH release, run:
```
bosh -e BOSH-ENVIRONMENT upload-release
```
Where `BOSH-ENVIRONMENT` is the alias that you set for your BOSH Director.
For example:
```
$ bosh -e dev upload-release
Acting as user 'admin' on 'Bosh Lite Director'
Copying packages

----------------
example-nozzle
golang1.7
Copying jobs

------------
example-nozzle
Generated /var/folders/4n/qs1rjbmd1c5gfb78m3_06j6r0000gn/T/d20151009-71219-17a5m49/d20151009-71219-rts928/release.tgz
Release size: 59.2M
Verifying release...
...
Release info

------------
Name: nozzle-test
Version: 0+dev.2
Packages

- example-nozzle (b0944f95eb5a332e9be2adfb4db1bc88f9755894)

- golang1.7 (b68dc9557ef296cb21e577c31ba97e2584a5154b)
Jobs

- example-nozzle (112e01c6ee91e8b268a42239e58e8e18e0360f58)
License

- none
Uploading release
```

## Step 8: Deploying nozzle
To deploy the nozzle, run:
```
bosh -e BOSH-ENVIRONMENT deploy
```
Where `BOSH-ENVIRONMENT` is the alias that you set for your BOSH Director.
For example:
```
$ bosh -e dev deploy
Acting as user 'admin' on deployment 'example-nozzle-lite' on 'Bosh Lite Director'
Getting deployment properties from director...
Unable to get properties list from director, trying without it...
Cannot get current deployment information from director, possibly a new deployment
Please review all changes carefully
Deploying

---------
Are you sure you want to deploy? (type 'yes' to continue):yes
```

## Step 9: Viewing nozzle output
The example nozzle outputs all of the data originating coming from the Firehose to its log files. To view this data,
SSH into the `example-nozzle` VM and examine the logs.
To view nozzle output:

1. Access the nozzle VM at the IP address configured in the nozzle manifest template stub,
`./templates/bosh-lite-stub.yml`, by running:
```
bosh -e BOSH-ENVIRONMENT ssh
```
Where `BOSH-ENVIRONMENT` is the alias that you set for your BOSH Director.
For example:
```
$ bosh -e dev ssh example-nozzle
Welcome to Ubuntu 14.04.1 LTS (GNU/Linux 3.19.0-25-generic x86_64)
Documentation: https://help.ubuntu.com/
Last login: Wed Sep 23 21:29:50 2015 from 192.0.2.1
```

2. Use the `cat` command to output the `stdout` log file.
```
$ cat /var/vcap/sys/log/example-nozzle/example-nozzle.stdout.log
===== Streaming Firehose (will only succeed if you have admin credentials)
origin:"bosh-system-metrics-forwarder" eventType:ValueMetric timestamp:1541091851000000000 deployment:"cf-c42ae2c4dfb6f67b6c27" job:"loggregator_trafficcontroller" index:"d1dffe15-5894-44de-b7f0-ad43161a0a7b" ip:"" tags:>key:"id" value:"d1dffe15-5894-44de-b7f0-ad43161a0a7b" > tags:>key:"source_id" value:"bosh-system-metrics-forwarder" > valueMetric:>"system.swap.percent" value:0 unit:"Percent" >
origin:"bosh-system-metrics-forwarder" eventType:ValueMetric timestamp:1541091851000000000 deployment:"cf-c42ae2c4dfb6f67b6c27" job:"loggregator_trafficcontroller" index:"d1dffe15-5894-44de-b7f0-ad43161a0a7b" ip:"" tags:>key:"id" value:"d1dffe15-5894-44de-b7f0-ad43161a0a7b" > tags:>key:"source_id" value:"bosh-system-metrics-forwarder" > valueMetric:>"system.swap.kb" value:0 unit:"Kb" >
origin:"bosh-system-metrics-forwarder" eventType:ValueMetric timestamp:1541091851000000000 deployment:"cf-c42ae2c4dfb6f67b6c27" job:"loggregator_trafficcontroller" index:"d1dffe15-5894-44de-b7f0-ad43161a0a7b" ip:"" tags:>key:"id" value:"d1dffe15-5894-44de-b7f0-ad43161a0a7b" > tags:>key:"source_id" value:"bosh-system-metrics-forwarder" > valueMetric:>"system.disk.ephemeral.percent" value:3 unit:"Percent" >
origin:"bosh-system-metrics-forwarder" eventType:ValueMetric timestamp:1541091851000000000 deployment:"cf-c42ae2c4dfb6f67b6c27" job:"loggregator_trafficcontroller" index:"d1dffe15-5894-44de-b7f0-ad43161a0a7b" ip:"" tags:>key:"id" value:"d1dffe15-5894-44de-b7f0-ad43161a0a7b" > tags:>key:"source_id" value:"bosh-system-metrics-forwarder" > valueMetric:>"system.healthy" value:1 unit:"b" >
origin:"gorouter" eventType:ValueMetric timestamp:1541091851218590916 deployment:"cf-c56ab7c4dfb6f67b6c28" job:"router" index:"d5d1b5a4-2497-4679-8d3b-66ffc978d829" ip:"10.0.4.13" tags:>key:"source_id" value:"gorouter" > valueMetric:>"uptime" value:3.273478e+06 unit:"seconds" >
origin:"netmon" eventType:ValueMetric timestamp:1541091851234217334 deployment:"cf-c56ab7c4dfb6f67b6c28" job:"diego_cell" index:"8007afda-3bff-4856-857f-a47a43cbf994" ip:"10.0.4.18" tags:>key:"source_id" value:"netmon" > valueMetric:>name:"numGoRoutines" value:13 unit:"count" >
origin:"netmon" eventType:ValueMetric timestamp:1541091851234129669 deployment:"cf-c56ab7c4dfb6f67b6c28" job:"diego_cell" index:"8007afda-3bff-4856-857f-a47a43cbf994" ip:"10.0.4.18" tags:>key:"source_id" value:"netmon" > valueMetric:>"numCPUS" value:2 unit:"count" >
origin:"netmon" eventType:ValueMetric timestamp:1541091851234292367 deployment:"cf-c56ab7c4dfb6f67b6c28" job:"diego_cell" index:"8007afda-3bff-4856-857f-a47a43cbf994" ip:"10.0.4.18" tags:>key:"source_id" value:"netmon" > valueMetric:>"memoryStats.numBytesAllocated" value:542328 unit:"count" >
origin:"netmon" eventType:ValueMetric timestamp:1541091851234279470 deployment:"cf-c56ab7c4dfb6f67b6c28" job:"diego_cell" index:"8007afda-3bff-4856-857f-a47a43cbf994" ip:"10.0.4.18" tags:>key:"source_id" value:"netmon" > valueMetric:>"memoryStats.numBytesAllocatedStack" value:655360 unit:"count" >
...
```