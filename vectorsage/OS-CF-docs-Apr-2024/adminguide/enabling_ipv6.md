# Enabling IPv6 for hosted apps on Cloud Foundry
You can enable IPv6 support for hosted apps on Cloud Foundry.
The following procedure allows apps deployed to Cloud Foundry to be reached
using IPv6 addresses.

**Important**
Amazon Web Services (AWS) EC2 instances do not support IPv6.
Cloud Foundry system components use a separate DNS subdomain from hosted apps. These
components support only IPv4 DNS resolved addresses. This means that although an IPv6 address can be
used for app domains, the system domain must resolve to an IPv4 address.

## Enable IPv6 Support for hosted pps
To enable support for IPv6 app domains:

1. Set up an external load balancer for your Cloud Foundry deployment.

2. Configure DNS to resolve app domains to an IPv6 address on your external load balancer.
Your IPv4 interface for the system domain and IPv6 interface for app domain can be
configured on the same or different load balancers.

3. Configure the external load balancer to route requests for an IPv6 address directly to the IPv4
addresses of the Gorouters.
The following diagram illustrates how a single load balancer can support traffic on both IPv4
and IPv6 addresses for a Cloud Foundry installation:
![IPv6 Application clients send IPv6 to the load balancer. The load balancer also takes in and puts out IPv4 to the CF components, which accept only IPv4.](https://docs.cloudfoundry.org/adminguide/images/cf_ipv4_ipv6.png)
For more information about domains in Cloud Foundry, see [Routes and
Domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html).