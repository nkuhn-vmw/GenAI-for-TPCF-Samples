# Cloud Foundry security
This topic provides you with an overview of Cloud Foundry security.
For an overview of container security, see [Container Security](https://docs.cloudfoundry.org/concepts/container-security.html).
Cloud Foundry implements the following measures to mitigate against security threats:

* Minimizes network surface area.

* Isolates customer apps and data in containers.

* Encrypts connections.

* Uses role-based access controls, applying and enforcing roles and permissions to ensure that users can only
view and affect the spaces for which they have been granted access.

* Ensures security of app bits in a multi-tenant environment.

* Prevents possible denial of service attacks through resource starvation.

## System boundaries and access
In a typical deployment of Cloud Foundry, the components run on virtual machines (VMs) that exist within a VLAN.
In this configuration, the only access points visible on a public network are a load balancer that maps to one or more Cloud Foundry routers and, optionally, a NAT VM and a jumpbox. Because of the limited number of contact points with the public internet, the surface area for possible security vulnerabilities is minimized.
As the following diagram shows the architecture of a typical deployment of Cloud Foundry:

**Important**
Cloud Foundry recommends that you also install a NAT VM for outbound requests and a
jumpbox to access the BOSH Director, though these access points are optional depending on your network
configuration.
![Full description of this diagram is in the text.](https://docs.cloudfoundry.org/concepts/images/security/sysbound1.png)
The diagram shows the following components:

* DMZ

+ Customer Load Balancers with SSL Termination

+ Outbound NAT

+ Jumpbox

* Private vLANs

+ Cloud Foundry vLAN

- Three Go Routers

- OAuth2 Server (UAA)

- Login Server

- Cloud Controller

- nsync

- Diego Brain

- Cell Reps

- Blob Store

- App Execution (Diego Cells) with Garden Containers

- Service Brokers

- BBS (HTTP/S)

- Consul

- NATS Message Bus

- Metrics Collector

- App Log Aggregator

+ BOSH vLAN

- BOSH Director

- Resurrector

- Workers

-Message Bus (NATS)

+ Services vLAN

- Brokers

- Services Nodes

* IaaS

+ Hypervisor
The preceding diagram shows the following communications:

* Customer Load Balancers send communication to the three Go Routers.

* Outbound NAT communicates with Hypervisor.

* BOSH Director communicates with the App Execution (Diego Cells).

* Service Brokers in Cloud Foundry vLAN communicates with Brokers in Services vLAN.

### Protocols
All traffic from the public internet to the Cloud Controller and UAA happens over HTTPS. Inside the boundary of the system, components communicate over a publish-subscribe (pub-sub) message bus NATS, HTTP, and SSL/TLS.

### BOSH
Operators deploy Cloud Foundry with BOSH. The BOSH Director is the core orchestrating component in BOSH: it controls VM creation and deployment, as well as other software and service lifecycle events. You use HTTPS to ensure secure communication to the BOSH Director.
Cloud Foundry recommends that you deploy the BOSH Director on a subnet that is not
publicly accessible, and access the BOSH Director from a jumpbox on the subnet or through VPN.
BOSH includes the following capability for security:

* Communicates with the VMs it runs through NATS. Because NATS cannot be accessed from outside Cloud Foundry, this ensures that published messages can only originate from a component within your deployment.

* Provides an audit trail through the `bosh tasks --all` and `bosh tasks --recent=VALUE` commands. `bosh tasks --all` returns a table that shows all BOSH actions taken by an operator or other running processes. `bosh tasks --recent=VALUE` returns a table of recent tasks, with `VALUE` being the number of recent tasks you want to view.

* Allows you to set up individual login accounts for each operator. BOSH operators have root access.

**Important**
BOSH does not encrypt data stored on BOSH VMs. Your IaaS might encrypt this data.

## Isolation segments
Isolation segments provide dedicated pools of resources to which apps can be deployed to isolate workloads. Using isolation segments separates app resources as completely as if they were in different Cloud Foundry deployments but avoids redundant management components and unneeded network complexity.
You can designate isolation segments for exclusive use by orgs and spaces within Cloud Foundry. This guarantees that apps within the org or space use resources that are not also used by other orgs or spaces. For more information, see [Orgs, Spaces, Roles, and Permissions](https://docs.cloudfoundry.org/concepts/roles.html).
Customers can use isolation segments for different reasons, including:

* To follow regulatory restrictions that require separation between different types of apps. For example, a health care company might not be able to host medical records and billing systems on the same machines.

* To dedicate specific hardware to different isolation segments. For example, to ensure that high-priority apps run on a cluster of high-performance hosts.

* To separate data on multiple clients, to strengthen a security story, or offer different hosting tiers.
In Cloud Foundry, the Cloud Controller database (CCDB) identifies isolation segments by name and GUID, for example `30dd879c-ee2f-11db-8314-0800200c9a66`. The isolation segment object has no internal structure beyond these two properties at the Cloud Foundry level, but BOSH associates the name of the isolation segment with Diego Cells, through their `placement_tag` property.
This diagram shows how isolation segments keep apps running on different pools of Diego Cells, and how the Diego Cells communicate with each other and with the management components:
![Description is in the text.](https://docs.cloudfoundry.org/concepts/images/security/isolation-segments.png)
For information about how to create and manage isolation segments in a Cloud Foundry deployment, see [Managing Isolation Segments](https://docs.cloudfoundry.org/adminguide/isolation-segments.html).
For API commands related to isolation segments, see [Isolation Segments](http://v3-apidocs.cloudfoundry.org/version/3.0.0/index.html#isolation-segments) in the Cloud Controller API (CAPI) Reference.

## Authentication and authorization
[User Account and Authentication](https://docs.cloudfoundry.org/concepts/architecture/uaa.html) (UAA) is the central identity management service for Cloud Foundry and its various components.
UAA acts as an [OAuth2](https://oauth.net/2/) Authorization Server and issues access tokens for apps that request platform resources.
The tokens are based on the [JSON Web Token](http://jwt.io/) and are digitally signed by UAA.
Operators can configure the identity store in UAA. If users register an account with the Cloud Foundry platform, UAA acts as the user store and stores user passwords in the UAA database using [bcrypt](http://en.wikipedia.org/wiki/Bcrypt). UAA also supports connecting to external user stores through LDAP and SAML. Once an operator has configured the external user store, such as a corporate Microsoft Active Directory, users can use their LDAP credentials to gain access to the Cloud Foundry platform instead of registering a separate account. Alternatively, operators can use SAML to connect to an external user store and enable single sign-on for users into the Cloud Foundry platform.
Standard Cloud Foundry deployments based on [cf-deployment](https://github.com/cloudfoundry/cf-deployment) provide a UAA client `cf` that can be used to create OAuth 2 tokens using the Password Grant Flow for Cloud Foundry users that are needed to access the CF API. This UAA client is also used by the CF CLI. The UAA client `cf` doesn’t require a `client_secret`.

### Managing user access with Role-Based Access Control
Apps that users deploy to Cloud Foundry exist within a space. Spaces exist within orgs. To view and access an org or a space, a user must be a member of it. Cloud Foundry uses role-based access control (RBAC), with each role granted permissions to either an org or a specified space. For more information about roles and permissions, see [Orgs, Spaces, Roles, and Permissions](https://docs.cloudfoundry.org/concepts/roles.html).

## Security for service broker integration
The Cloud Controller authenticates every request with the Service Broker API using HTTP or HTTPS, depending on which protocol that you specify during broker registration. The Cloud Controller rejects any broker registration that does not contain a username and password.
Service instances bound to an app contain credential data. Users specify the binding credentials for user-provided service instances, while third-party brokers specify the binding credentials for managed service instances. The VCAP\_SERVICES environment variable contains credential information for any service bound to an app. Cloud Foundry constructs this value from encrypted data that it stores in the CCDB. For more information about user-provided service instances, see [User-Provided Service Instances](https://docs.cloudfoundry.org/devguide/services/user-provided.html).
The selected third-party broker controls how securely to communicate managed service credentials.
A third-party broker might offer a dashboard client in its catalog. Dashboard clients require a text string defined as a `client_secret`. Cloud Foundry does not store this secret in the CCDB. Instead, Cloud Foundry passes the secret to the UAA component for verification using HTTP or HTTPS.

## Managing software vulnerabilities
Cloud Foundry manages software vulnerability using releases and BOSH stemcells. New Cloud Foundry releases are created with updates to address code issues, while new stemcells are created with patches for the latest security fixes to address any underlying operating system issues.

## Ensuring security for app artifacts
Cloud Foundry secures both the code and the configuration of an app using the following functions:

* App developers push their code using the Cloud Foundry API. Cloud Foundry secures each call to the Cloud Foundry API using the [UAA](https://docs.cloudfoundry.org/concepts/security.html#auth) and SSL.

* The Cloud Controller uses [RBAC](https://docs.cloudfoundry.org/concepts/security.html#rbac) to ensure that only authorized users can access a particular app.

* The Cloud Controller stores the configuration for an app in an encrypted database table. This configuration data includes user-specified environment variables and service credentials for any services bound to the app.

* Cloud Foundry runs the app inside a secure container. For more information, see [Container Security](https://docs.cloudfoundry.org/concepts/container-security.html).

* Cloud Foundry operators can configure network traffic rules to control inbound communication to and outbound communication from an app. For more information, see the [Network Traffic Rules](https://docs.cloudfoundry.org/concepts/container-security.html#config-traffic) section of the *Container Security* topic.

## Security event logging and auditing
For operators, Cloud Foundry provides an audit trail through the `bosh tasks` command. This command shows all actions that an operator has taken with the platform. Additionally, operators can redirect Cloud Foundry component logs to a standard syslog server using the `syslog_daemon_config` [property](http://docs.cloudfoundry.org/running/managing-cf/logging.html) in the `metron_agent` job of `cf-release`.
For users, Cloud Foundry records an audit trail of all relevant API invocations of an app. The Cloud Foundry Command Line Interface (cf CLI) command `cf events` returns this information.

## Recommendations for running a secure deployment
To help run a secure deployment, Cloud Foundry recommends:

* Configure UAA clients and users using a BOSH manifest. Limit and manage these clients and users as you would any other kind of privileged account.

* Deploy within a VLAN that limits network traffic to individual VMs. This reduces the possibility of unauthorized access to the VMs within your BOSH-managed cloud.

* Enable HTTPS for apps and SSL database connections to protect sensitive data transmitted to and from apps.

* Ensure that the jumpbox is secure, along with the load balancer and NAT VM.

* Encrypt stored files and data within databases to meet your data security requirements. Deploy using industry standard encryption and the best practices for your language or framework.

* Prohibit promiscuous network interfaces on the trusted network.

* Review and monitor data sharing and security practices with third party services that you use to provide additional function to your app.

* Store SSH keys securely to prevent disclosure, and promptly replace lost or compromised keys.

* Use Cloud Foundry’s RBAC model to restrict your users’ access to only what is necessary to complete their tasks.

* Use a strong passphrase for both your Cloud Foundry user account and SSH keys.

## Security for apps and services
This section links to topics that describe how Cloud Foundry and Cloud Foundry users manage security for apps and service instances.

* [App Security Groups](https://docs.cloudfoundry.org/concepts/asg.html): Describes how App Security Groups (ASGs) work and how to manage them in Cloud Foundry.

* [Trusted System Certificates](https://docs.cloudfoundry.org/devguide/deploy-apps/trusted-system-certificates.html): Explains where apps can find trusted system certificates.

* [Managing Access to Service Plans](https://docs.cloudfoundry.org/services/access-control.html): Describes how to activate or deactivate access to service plans for a subset of users.

* [Delivering Service Credentials to an App](https://docs.cloudfoundry.org/devguide/services/application-binding.html): Describes how to bind apps to service instances, which generate the credentials that enable the apps to use the service.

* [Managing Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html): Explains how to create and manage service keys that allow apps to use service instances.