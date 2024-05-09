# Overview of Deploying Cloud Foundry
Cloud Foundry is designed to be configured, deployed, managed, scaled, and
upgraded on any cloud IaaS provider. Cloud Foundry achieves this by leveraging
[BOSH](https://bosh.io/), an open source tool for release engineering,
deployment, lifecycle management, and distributed systems monitoring.
If installing Cloud Foundry for the first time, [deploy](https://docs.cloudfoundry.org/deploying/cf-deployment/) with `cf-deployment`.
If you have an existing Cloud Foundry deployment that uses `cf-release`, [migrate](https://docs.cloudfoundry.org/deploying/migrating.html) your deployment to `cf-deployment`.

* [Deploying Cloud Foundry with cf-deployment](https://docs.cloudfoundry.org/deploying/cf-deployment/)

* [Migrating from cf-release to cf-deployment](https://docs.cloudfoundry.org/deploying/migrating.html)

**Note**: To deploy a local Cloud Foundry environment for experimentation or debugging purposes, you can use CF Dev. For more information, see [CF Dev](https://github.com/cloudfoundry-incubator/cfdev).