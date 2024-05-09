# Using the CPU entitlement plug-in in Cloud Foundry
You can use the CPU entitlement plug-in to help manage your CPU resources in Cloud Foundry.

## CPU entitlement
To watch an overview of the topic, see [CPU Entitlements in Cloud
Foundry](https://www.youtube.com/watch?v=vV87xmxKLeA) on YouTube.
CPU entitlement describes the percentage of host CPU a particular app instance
is *entitled* to use. The CPU entitlement plug-in shows that apps have a CPU
performance of 100% when they are using exactly the CPU they are entitled. Apps
have a CPU performance of less than 100% when their usage is less than their
entitlement and greater than 100% when they are above their entitlement.
In Cloud Foundry, apps have CPU entitlements that are
proportional to their allocated memory by default. For example, an app with
access to 256MB of memory on a 512MB machine has access to half of the
memory on the machine and is also entitled to half of the CPU of that machine.
You can change the exact mapping of memory to CPU when you configure the `experimental_cpu_entitlement_per_share_in_percent`Garden BOSH release property. This property changes the CPU percentage that is entitled to a container per CPU share. For example, a value of `0.3` means that each app has access to 0.3% of the total CPU per share.
By default, the total shares available on a host is equal to the amount of memory on the host. The optimal value for the `experimental_cpu_entitlement_per_share_in_percent` property is 100% divided by the amount of total memory on the host. For example, a host with 1024 MB of memory can have an optimal value of `100 / 1024`, which is 0.0977% per share. An 256 MB app has access to 76.8% of the total CPU. In this case, if there is only a single core machine, you have over committed the amount of CPU available.
The way you configure the `experimental_cpu_entitlement_per_share_in_percent` property can create three possible states for the apps in your Cloud Foundry deployment:

* Undercommitted - The apps’ CPU entitlements are guaranteed minimums, but some CPU host might not be used.

* Optimal - The apps’ CPU entitlements are guaranteed minimums.

* Overcommitted - The apps are not guaranteed to have access to their entitlement.
The following table contains examples of optimal values for machines with different total memory and number of CPU cores:
| | 256M | 1024M | 8192M |
| --- | --- | --- | --- |
| 1 core | 0.39 | 0.098 | 0.012 |
| 4 cores | 1.563 | 0.39 | 0.049 |
| 8 cores | 3.125 | 0.781 | 0.098 |

## CPU entitlement plug-in
The metric `absolute_entitlement` shows an app’s CPU usage relative to its
entitlement.
To retrieve `absolute_entitlement` metrics for all instances of an app:

1. Install the CPU Entitlement Plug-in from the
[cpu-entitlement-plug-in](https://github.com/cloudfoundry/cpu-entitlement-plugin)
repository on GitHub.

2. Run:
```
cf cpu-entitlement APP-NAME
```
Where `APP-NAME` is the name of the app.
This command returns `absolute_entitlement` metrics for all instances of the app, similar to the following example:
```
Showing CPU usage against entitlement for app dora-example in org example-org / space example-org-staging as [dora@example.com](mailto:dora@example.com) ...
​
avg usage curr usage

#0 1.62% 1.66%

#1 2.93% 3.09%

#2 2.51% 2.62%
```
After you run the `cf cpu-entitlement` command, you see the following values:
\* `avg usage`
\* `curr usage`.
The average usage is used to split the app into two groups,
good and bad. Good apps have an average CPU usage that is below 100% of their
CPU entitlements, and bad apps have an average CPU usage that is over 100% of
their CPU entitlements. In the preceding example, all values for the average CPU
usage are under 100% of their CPU entitlements.
This partial is used for both VMware Tanzu Application Service for VMs and Cloud Foundry docs.
Don’t reference VMware Tanzu Application Service for VMs or BOSH configurations here.

## Spare CPU resources and throttling
If there are three cores on the Diego Cell to which your app is deployed, 300%
CPU can be distributed between all the apps on the Diego Cell. This is the
percentage that the `cf app` command displays. The metrics depend on factors
such as the capacity of the Diego Cell and the total number of apps on it that
are not visible to the user. This can make it difficult for users and operators
to balance CPU resources.
An app always receives 100% of its CPU entitlement, no matter what other apps
are on the Diego Cell. If there are spare resources on the machine, an app can
consume over 100% CPU.
Spare resources are distributed on the Diego Cell when the `experimental_cpu_throttling` property is set to `false`. If an app consumes less than the entitlement, and needs CPU resources over its entitlement, it receives the maximum amount of CPU resources from the spare CPU. Without CPU entitlement it depends on the other apps that run on the same Diego Cell. If the other apps constantly use high CPU, they restrict other apps from using more CPU when needed even though the other apps on the same Diego Cell use much more than their CPU entitlements. When an app that usually consumes less than its CPU entitlement needs extra CPU, the spare capacity is distributed evenly between the app that consumes less and all the other apps. When this occurs, the app can never spike over a certain amount of CPU. To provide bandwidth, you might over provision resources for Diego Cells.
When the `experimental_cpu_throttling` property is set to `false`, apps are allowed to temporarily exceed their entitlement, but apps that have been using less than their entitlement over a longer period of time are prioritized. Apps are never forced to use less than their entitlement.
Good and bad apps always get their entitlement. If you use the CPU Entitlement plug-in, the difference is in how the spare CPU gets distributed between the apps. All spare CPU is given to the good app that needs it, and then the bad apps are throttled to only have the amount of CPU to which they are entitled.
If the CPU spike of a good app happens for a long period of time, it eventually becomes a bad app, and is throttled to 100% if a different good app needs the CPU. Resources are then distributed more fairly between the apps.