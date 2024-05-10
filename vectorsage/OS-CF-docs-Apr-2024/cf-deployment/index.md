# Deploying Cloud Foundry with cf-deployment
This topic describes how to deploy Cloud Foundry using `cf-deployment`.
For more information about `cf-deployment`, see the
[cf-deployment repository](https://github.com/cloudfoundry/cf-deployment) on
GitHub.
`cf-deployment` relies on individual component releases and prioritizes the
following:

* Readability for a human operator: `cf-deployment` includes only necessary
configuration

* Security and production-readiness by default

* Native use of [Diego](https://docs.cloudfoundry.org/concepts/diego/diego-architecture.html) and lack
of support for [Droplet Execution Agents](https://docs.cloudfoundry.org/concepts/architecture/execution-agent.html)

## Prepare Your Environment
Before deploying Cloud Foundry with `cf-deployment`, you must prepare your
environment and deploy a BOSH Director. The procedures to do this vary
depending on your IaaS.
Select the topic specific to your IaaS:

* [Deploying BOSH on AWS](https://docs.cloudfoundry.org/deploying/common/aws.html)

* [Deploying BOSH on GCP](https://docs.cloudfoundry.org/deploying/cf-deployment/gcp.html)

* [Deploying BOSH on Azure](https://docs.cloudfoundry.org/deploying/cf-deployment/azure.html)

* [Deploying BOSH on vSphere](https://github.com/cloudfoundry/bosh-bootloader/blob/master/docs/getting-started-vsphere.md)

* [Deploying BOSH on OpenStack](https://github.com/cloudfoundry/bosh-bootloader/blob/master/docs/getting-started-openstack.md)

**Note**: The topics for preparing your
environment use the `bosh-bootloader` tool. `bosh-bootloader` is currently compatible with GCP, AWS, Microsoft Azure, VMware vSphere and OpenStack.

## Deploy Cloud Foundry
After preparing your environment and deploying a BOSH Director, continue to the
[Deploying Cloud Foundry](https://docs.cloudfoundry.org/deploying/cf-deployment/deploy-cf.html) topic.

## Other IaaS Support
You can deploy Cloud Foundry using `cf-deployment` to an IaaS not listed above.
The Cloud Foundry community tested and found Cloud Foundry compatible with the
following:

* [AWS](https://docs.cloudfoundry.org/deploying/common/aws.html)

* [BOSH-Lite](https://github.com/cloudfoundry/cf-deployment/tree/master/iaas-support/bosh-lite)

* [GCP](https://docs.cloudfoundry.org/deploying/cf-deployment/gcp.html)

* [OpenStack](https://github.com/cloudfoundry/cf-deployment/tree/master/iaas-support/openstack)

* [vSphere](https://github.com/cloudfoundry/cf-deployment/tree/master/iaas-support/vsphere)

* [AliCloud](https://github.com/cloudfoundry/cf-deployment/tree/master/iaas-support/alicloud)

* [Softlayer](https://github.com/cloudfoundry/cf-deployment/tree/master/iaas-support/softlayer)

**Note**: Any IaaS not listed have not been tested
with Cloud Foundry. Attempts to deploy Cloud Foundry on an untested IaaS may
fail.