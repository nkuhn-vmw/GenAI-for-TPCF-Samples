# CredHub
Learn about ther functionality of the CredHub component.
CredHub is a component designed for centralized credential management in Cloud Foundry. It’s
a single
component that can address several scenarios in the Cloud Foundry ecosystem. At the
highest level, CredHub
centralizes and secures credential generation, storage, lifecycle management, and access.

## Functions
CredHub performs a number of different functions to help generate and protect the credentials in your
Cloud Foundry deployment:

* Securing data for storage

* Authentication

* [Authorization and Permissions](https://github.com/cloudfoundry-incubator/credhub/blob/main/docs/authorization-and-permissions.md)

* Access and change logging

* Data typing

* Credential generation

* Credential metadata

* Credential versioning

## App architecture
CredHub consists of a REST API and a CLI. CredHub is an OAuth2
resource server that integrates with User Account Authentication (UAA) to provide core authentication and federation
capabilities.
![The CredHub CLI interacts with CredHub to export credentials to the Encryption Provider, Data Store, and Authentication Provider](https://docs.cloudfoundry.org/credhub/images/basic-architecture.png)

## Deployment architecture
The primary architectures for CredHub are either colocated on the BOSH Director VM or
deployed and managed independently as a service. You can choose your method depending on the needs of your
organization.

### Colocated deployment with BOSH Director
You can deploy CredHub on the same VM as the BOSH Director. If you need a
lightweight credential storage instance for the BOSH Director only, you might choose a colocated deployment.
This configuration does not provide high availability.
When you use a colocated deployment architecture, the BOSH Director, CredHub, UAA, and the BOSH Director database are all installed on a single BOSH VM, as shown in this diagram:
![The components colocated on the BOSH VM: BOSH Director, CredHub, UAA, and the BOSH Director database](https://docs.cloudfoundry.org/credhub/images/bosh-deployment.png)
For more information, see [Setting up and deploying CredHub with BOSH](https://docs.cloudfoundry.org/credhub/setup-credhub-bosh.html).

### Deploying as a service
You can deploy CredHub as an independent service on one or more VMs. If you need a highly available credential storage instance for multiple components in your deployment, you might choose to deploy CredHub as a service.
CredHub is a stateless app, so you can scale it to multiple instances that share a common
database cluster and encryption provider.
When you deploy CredHub as a service, the load balancer and external databases communicate
directly with the CredHub VMs, as shown in this diagram:
![Multiple CredHub VMs that connect to UAA, an HSM, an external database, and a load balancer. The load balancer connects to four consumer VMs.](https://docs.cloudfoundry.org/credhub/images/service-deployment.png)

## CredHub credential types
Credentials exist in multiple places.
Components use credentials to authenticate connections between components.
Installations often have hundreds of active credentials.
Leaked credentials are common causes of data and security breaches, so managing them securely is very important.
For more information, see [CredHub Credential Types](https://docs.cloudfoundry.org/credhub/credential-types.html).

## Backing up and restoring CredHub instances
CredHub does not hold state, but you must ensure its dependent components are backed up. Redundant backups can help
prevent data loss if an individual component fails.
For more information, see
[Backing Up and Restoring CredHub Instances](https://docs.cloudfoundry.org/credhub/backup-restore.html).