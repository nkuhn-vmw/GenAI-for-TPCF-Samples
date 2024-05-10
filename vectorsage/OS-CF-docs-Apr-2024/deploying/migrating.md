# Migrating from cf-release to cf-deployment on AWS
This topic describes how to migrate your Cloud Foundry deployment
from `cf-release` to `cf-deployment` on AWS.
The procedures in this topic are specific to Amazon Web Services (AWS).

**IMPORTANT**: `cf-release` has been replaced by `cf-deployment` and moved to the [Cloud Foundry attic](https://github.com/cloudfoundry-attic/cf-release).
For more information, see [cf-release End of Life](https://docs.cloudfoundry.org/deploying/cf-release-eol.html).

## Migration Prerequisites
For a list of the current prerequisites, see [Migration Prerequisites](https://github.com/cloudfoundry/cf-deployment-transition/blob/master/README.md#prerequisites) in GitHub.

## Step 1: Configure the BOSH CLI v2+
Perform the following steps:

1. Set your BOSH Director address, username, and password as environment variables:
```
$ export BOSH_ENVIRONMENT=YOUR-DIRECTOR-ADDRESS
$ export BOSH_CLIENT=YOUR-DIRECTOR-USERNAME
$ export BOSH_CLIENT_SECRET=YOUR-DIRECTOR-PASSWORD
```

2. Confirm that your BOSH CLI is logged in and working:
```
$ bosh deployments
Using environment 'bosh.example.com' as client 'admin'
Name Release(s) Stemcell(s) Team(s) Cloud Config
cf cf/268 bosh-aws-xen-hvm-ubuntu-trusty-go_agent/3421.11 - none
cf-diego garden-runc/1.9.0 bosh-aws-xen-hvm-ubuntu-trusty-go_agent/3421.11 - none
grootfs/0.21.0
cf-networking/1.2.0
cflinuxfs3/1.138.0
diego/1.23.0
cf/268
```

3. Set your Cloud Foundry deployment name as an environment variable:
```
$ export BOSH_DEPLOYMENT=YOUR-CF-DEPLOYMENT-NAME
```

4. If your BOSH Director is configured with a self-signed certificate,
perform the following steps to provide that certificate to the BOSH CLI.

1. Extract the necessary certificate
from your BOSH Director deployment manifest:
```
$ bosh interpolate \

--path=/properties/director/ssl/cert PATH-TO-YOUR-BOSH-DIRECTOR-MANIFEST > /tmp/bosh-CA.crt
```

2. Configure the BOSH CLI to use the extracted certificate:
```
$ export BOSH_CA_CERT=/tmp/bosh-CA.crt
```

## Step 2: Build Variables Store File
You must build a variables store file from your Cloud Foundry and Diego manifests.
This file contains information that provides environment-specific or sensitive configuration
that the BOSH CLI reads and writes to. The operator uses this file when deploying Cloud Foundry
with `cf-deployment`.
Perform the following steps to build your variables store file:

1. Download your Cloud Foundry and Diego manifests from your existing `cf-release`-based deployments:
```
$ bosh download-manifest > /tmp/cf-manifest.yml
$ bosh download-manifest -d YOUR-DIEGO-DEPLOYMENT-NAME > /tmp/diego-manifest.yml
```

2. Visit the [cf-deployment-transition](https://github.com/cloudfoundry/cf-deployment-transition/blob/master/README.md) GitHub repository
and use the `extract-vars-store-from-manifests.sh` script
to generate `deployment-vars.yml`.

## Step 3: Write Scaling Ops File
To perform a successful migration, you must ensure that your `cf-deployment` manifest
deploys components at a scale equivalent to your existing Cloud Foundry and Diego deployments.

### Understand Name Changes
`cf-deployment` renames or combines some jobs in `cf-release`-based manifests.
`cf-release` had a copy of each job for each Availability Zone (AZ),
because historically,
BOSH was unaware of AZs.
`cf-deployment` no longer needs this workaround
thanks to first-class support of AZs in BOSH.
This means that several instance groups have been combined,
which has implications for scaling.
For instance, the `diego-cell` instance group replaces
both the `cell_z1` and the `cell_z2` instance groups
in your existing Diego deployment.
If you currently have 6 instances each of `cell_z1` and `cell_z2`,
you will need 12 instances of `diego-cell`,
which is configured to use both AZ1 and AZ2.
The BOSH Director will automatically
balance these instances between the AZs.
For a list of all job name changes from `cf-release`,
see the `cfr-to-cfd.yml` ops file
in the [cf-deployment-transition](https://github.com/cloudfoundry/cf-deployment-transition/blob/master/cfr-to-cfd.yml) GitHub repository.
This file does not list name changes from the Diego deployment.
However, the only job from the Diego deployment that you must scale is `diego-cells`.

### Write Ops File
To scale the components in `cf-deployment`, write an ops file.
An ops file is a YAML file that specifies operations to perform on the deployment manifest,
which you provide to the BOSH CLI when deploying Cloud Foundry in the following section.
The following example ops file scales to 12 instances of the `diego-cell`:
```

---

- type: replace
path: /instance\_groups/name=diego-cell/instances
value: 12
```

## Step 4: Write and Upload Cloud Config
You must write a cloud config to provide certain properties for `cf-deployment`, and upload it to your BOSH Director.
Perform the following steps:

1. Write a cloud config, drawing its values from your current Cloud Foundry and Diego manifests. Use the following example as the basis for your cloud config:
```
compilation:
az: z1
network: private
reuse\_compilation\_vms: true
vm\_extensions:

- 100GB\_ephemeral\_disk
vm\_type: c3.large
workers: 6
disk\_types:

- name: 5GB
cloud\_properties:
encrypted: true
type: gp2
disk\_size: 5120

- name: 10GB
cloud\_properties:
encrypted: true
type: gp2
disk\_size: 10240

- name: 100GB
cloud\_properties:
encrypted: true
type: gp2
disk\_size: 102400
vm\_types:

- name: t2.small
cloud\_properties:
ephemeral\_disk:
size: 10240
type: gp2
instance\_type: t2.small

- name: c3.large
cloud\_properties:
ephemeral\_disk:
size: 10240
type: gp2
instance\_type: c3.large

- name: m3.medium
cloud\_properties:
ephemeral\_disk:
size: 10240
type: gp2
instance\_type: m3.medium

- name: m3.large
cloud\_properties:
ephemeral\_disk:
size: 10240
type: gp2
instance\_type: m3.large

- name: r3.xlarge
cloud\_properties:
ephemeral\_disk:
size: 10240
type: gp2
instance\_type: r3.xlarge
vm\_extensions:

- name: 50GB\_ephemeral\_disk
cloud\_properties:
ephemeral\_disk:
size: 102400
type: gp2

- name: 100GB\_ephemeral\_disk
cloud\_properties:
ephemeral\_disk:
size: 512000
type: gp2

- name: cf-router-network-properties
cloud\_properties:
elbs:

- ELB-NAME-FROM-ROUTER-RESOURCE-POOL

- name: diego-ssh-proxy-network-properties
cloud\_properties:
elbs:

- ELB-NAME-FROM-DIEGO-MANIFEST-ACCESS-RESOURCE-POOL
azs:

- name: z1
cloud\_properties:
availability\_zone: AVAILABILITY-ZONE-FROM-LARGE-Z1-RESOURCE-POOL

- name: z1
cloud\_properties:
availability\_zone: AVAILABILITY-ZONE-FROM-LARGE-Z2-RESOURCE-POOL

- name: z3
cloud\_properties:
availability\_zone: AVAILABILITY-ZONE-FROM-LARGE-Z3-RESOURCE-POOL
networks:

- name: default
subnets:

- az: z1
cloud\_properties:
security\_groups:

- SECURITY-GROUP-FROM-AZ1-NETWORK
subnet: SUBNET-FROM-AZ1-NETWORK
gateway: GATEWAY-IP-FROM-AZ1-NETWORK
range: RANGE-FROM-AZ1-NETWORK
reserved:

- RESERVED-IPS-FROM-AZ1-NETWORK
static:

- STATIC-IPS-FROM-AZ1-NETWORK

- az: z2
cloud\_properties:
security\_groups:

- SECURITY-GROUP-FROM-AZ2-NETWORK
subnet: SUBNET-FROM-AZ2-NETWORK
gateway: GATEWAY-IP-FROM-AZ2-NETWORK
range: RANGE-FROM-AZ2-NETWORK
reserved:

- RESERVED-IPS-FROM-AZ2-NETWORK
static:

- STATIC-IPS-FROM-AZ2-NETWORK

- az: z3
cloud\_properties:
security\_groups:

- SECURITY-GROUP-FROM-AZ3-NETWORK
subnet: SUBNET-FROM-AZ3-NETWORK
gateway: GATEWAY-IP-FROM-AZ3-NETWORK
range: RANGE-FROM-AZ3-NETWORK
reserved:

- RESERVED-IPS-FROM-AZ3-NETWORK
static:

- STATIC-IPS-FROM-AZ3-NETWORK
type: manual
```
Keep in mind the following about the above example:

* Unless otherwise noted,
all values come from the Cloud Foundry manifest.

* You must include compilation configuration.

* You must include at least the VM types
and extensions from the example.

* You must have a network called `default`.

* You must configure AZs
`z1`, `z2`, and `z3`.

* This example assumes that your network setup
allows your Elastic Load Balancers (ELBs) to talk to your deployment
without additional security groups.
If not, you must add an array of `security_groups`
to the `cf-router-network-properties` and
`diego-ssh-proxy-network-properties`
`vm_extensions`.

2. Upload your cloud config to the BOSH Director:
```
$ bosh update-cloud-config PATH-TO-YOUR-CLOUD-CONFIG
```

## Step 5: Deploy Cloud Foundry
Perform all the steps in the [Deploying Cloud Foundry](https://docs.cloudfoundry.org/deploying/cf-deployment/deploy-cf.html) topic. Keep in mind the following when deploying Cloud Foundry in [Step 5: Deploy](https://docs.cloudfoundry.org/deploying/cf-deployment/deploy-cf.html#deploy):

* You must apply the ops file for scaling your components that you created in the previous step.

* You must apply the `cfr-to-cfd.yml` ops file.
Download this ops file from the [cf-deployment-transition](https://github.com/cloudfoundry/cf-deployment-transition/blob/master/cfr-to-cfd.yml) GitHub repository.
If you are disabling `cf-deployment` features to simplify the transition,
you must also apply the appropriate ops files from the transition repository.

* The `deployment-vars.yml` file you pass with the `--vars-store` flag must be the variables store file you created above.

## Step 6: Delete Old Diego Deployment
Delete your Diego deployment by running the following command:
```
$ bosh -d YOUR-DIEGO-DEPLOYMENT-NAME delete-deployment
```
This command may take several minutes, because each Diego cell must drain its contents to the new `cf-deployment` cells.

## Step 7: (Optional) Clean Up
To delete any unused releases and stemcells from your BOSH Director,
including `cf-release`, run the following command:
```
$ bosh clean-up --all
```