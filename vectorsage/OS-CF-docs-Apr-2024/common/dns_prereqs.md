# Setting Up DNS for Your Environment
This topic describes how to set up DNS for your Cloud Foundry environment.

## Domains
You must create several wildcard DNS records to point to your load balancers and routers. Consult the table below for details about these wildcard DNS records.
Cloud Foundry gives each application its own hostname in your app domain. With a wildcard DNS record, every hostname in your domain resolves to the IP address of your router or load balancer, and you do not need to configure an A record for each app hostname. For example, if you create a DNS record for a system domain `*.example.com` pointing to your router, every application deployed to the `example.com` domain resolves to the IP address of your router.
| Domain | Example | Notes |
| --- | --- | --- |
| TCP | \*.tcp.example.com | This handles TCP traffic destined for the TCP Router. |
| HTTP | \*.sys.example.com | This is the system domain that handles HTTP traffic for system components destined for the Gorouter. |
| HTTP | \*.example.com | This is the app domain that handles HTTP traffic for applications destined for the Gorouter. |
| WebSockets | \*.ws.example.com | This is an optional domain that handles WebSocket traffic destined for the Gorouter. |
| SSH | \*.ssh.example.com | This is an optional domain that provides SSH access to application containers. |

## Example Topologies
Your exact configuration may vary significantly depending on your IaaS and your load balancing configuration. Below are the following example topologies.

* [An Amazon Web Services](https://docs.cloudfoundry.org/deploying/common/dns_prereqs.html#aws) (AWS) deployment using Elastic Load Balancer (ELBs)

* A deployment that uses [HAProxy](https://docs.cloudfoundry.org/deploying/common/dns_prereqs.html#haproxy) for load balancing
The diagrams below show which particular jobs will have traffic routed to them by load balancers. The instance groups may have different names. Run the `bosh instances` command to see the instance groups.
For example, in a default [cf-deployment](https://github.com/cloudfoundry/cf-deployment), the `ssh_proxy` job is deployed to an instance group name `scheduler`. Your load balancers must route traffic to that VM.

### AWS
This topology has DNS configured to point five domains to four ELBs:
![Aws dns prereq](https://docs.cloudfoundry.org/deploying/common/images/aws-dns-prereq.png)

### HAProxy
This topology has DNS configured to point five domains to one HAProxy:
![Haproxy dns prereq](https://docs.cloudfoundry.org/deploying/common/images/haproxy-dns-prereq.png)