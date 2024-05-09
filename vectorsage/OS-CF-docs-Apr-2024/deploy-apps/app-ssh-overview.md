# Configuring SSH access for your deployment
If you need to troubleshoot an instance of an application, you can gain SSH access to the app using the SSH proxy and daemon.
For example, one of the app instances might be unresponsive, or the log output from the app is inconsistent or incomplete. You can SSH into the individual VM to troubleshoot the problem instance.

**Note** If you have mutual TLS between the Gorouter and app containers, app containers accept incoming communication only from the Gorouter. This disables `cf ssh`. For more information, see the [TLS to Apps and Other Back End Services](https://docs.cloudfoundry.org/concepts/http-routing.html#tls-to-back-end) section of the *HTTP Routing* topic.

## About SSH access
The SSH system components include the SSH proxy and daemon, and the system also supports authentication and load balancing of incoming SSH traffic. For a conceptual overview, see [App SSH components and processes](https://docs.cloudfoundry.org/concepts/diego/ssh-conceptual.html).

## SSH access control hierarchy
Operators, space managers, and space developers can configure SSH access for Cloud Foundry,
for spaces, and for apps as described in the table:
| **User role** | **Scope of SSH permissions control** | **How they define SSH permissions** |
| --- | --- | --- |
| Operator | Entire deployment | Configure the deployment to allow or prohibit SSH access (one-time). For more information, see [Configuring SSH Access for Cloud Foundry](https://docs.cloudfoundry.org/running/config-ssh.html). |
| Space manager | Space | cf CLI [allow-space-ssh](http://cli.cloudfoundry.org/en-US/cf/allow-space-ssh.html) and [disallow-space-ssh](http://cli.cloudfoundry.org/en-US/cf/disallow-space-ssh.html) commands |
| Space developer | App | cf CLI [enable-ssh](http://cli.cloudfoundry.org/en-US/cf/enable-ssh.html) and [disable-ssh](http://cli.cloudfoundry.org/en-US/cf/disable-ssh.html) commands |
An app is SSH-accessible only if operators, space managers, and space developers all grant SSH access at their respective levels. For example, the following image shows a deployment in whi:

* An operator allowed SSH access at the deployment level.

* A space manager allowed SSH access for apps running in spaces “A” and “B,” but not “C”.

* A space developer activated SSH access for apps that include “Foo”, “Bar,” and “Baz”.
As a result, apps “Foo”, “Bar,” and “Baz” accept SSH requests.
![This diagram shows examples of successful and unsuccessful SSH Application Access Control in deployments.](https://docs.cloudfoundry.org/devguide/images/ssh-app-access.png)
Space A has SSH Access Enabled, indicated by a green check mark, for apps “Foo” and “Bar,” Space A does not have SSH Access allowed for the third app, indicated by a red X.
Space B has has SSH Access Enabled, indicated by a green check mark, for app “Baz”. Space B does not have SSH Access allowed for the other two apps, indicated by a red X.
Space C does not have SSH Access allowed for all three apps, indicated by a red X.

## SSH access for apps and spaces
Space managers and space developers can configure SSH access from the CLI. The Cloud Foundry Command Line Interface (cf CLI) also includes commands to return the value of the SSH access setting. To use and configure SSH at both the app level and the space level, see [Accessing apps with Diego SSH](https://docs.cloudfoundry.org/devguide/deploy-apps/ssh-apps.html).

## Configuring SSH access for Cloud Foundry
Cloud Foundry deployments control SSH access to apps at the Cloud Foundry level. Additionally, Cloud Foundry supports load balancing of SSH sessions. For more information about setting SSH access for your deployment, see [Configuring SSH Access](https://docs.cloudfoundry.org/running/config-ssh.html).