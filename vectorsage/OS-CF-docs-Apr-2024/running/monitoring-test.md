# Monitoring and testing Diego components
You can use the Diego components described here to monitor and test runtime deployment of Cloud Foundry.

## Inigo
Inigo is an integration test suite that launches the Diego components through various test cases, including component failures and other exceptional scenarios. Inigo validates a given set of component versions to ensure mutual compatibility, robustness, and graceful performance degradation in failure conditions.
See the [Inigo repository](https://github.com/cloudfoundry-incubator/inigo) on GitHub for more information.

## Auction
The [auction package](https://github.com/cloudfoundry-incubator/auction) encodes behavioral details about Task and LRP allocation to cells during a Diego [Auction](https://docs.cloudfoundry.org/concepts/diego/diego-auction.html). It includes a simulation test suite that validates the optimal performance of the auction algorithm. You can run the simulation for different algorithm variants at various scales, and in the following ways:

* In-process, for short feedback loops

* Across multiple processes, to reveal the impact of communication in the auction

* Across multiple machines in a cloud-like infrastructure, to reveal the impact of latency on the auction
See the [Auction repository](https://github.com/cloudfoundry-incubator/auction) on GitHub for more information.

## cfdot CLI
The [CF Diego Operator Toolkit](https://github.com/cloudfoundry/cfdot/blob/master/README.md) (cfdot) is a Command Line Interface (CLI) tool
designed to interact with a Cloud Foundry Diego deployment. cfdot is included in Diego releases v0.1482.0 and later, but it can be built
from source for use with older Diego releases by following the instructions in the [cfdot repository](https://github.com/cloudfoundry/cfdot#building-from-source).
The cfdot commands perform the following Long-Running Process (LRP) operations:

* List actual LRP groups

* Retire actual LRPs by index and process `guid`

* List desired LRPs and their scheduling information

* Show a specified desired LRP

* Create and delete desired LRPs

* Update a desired LRP
The cfdot commands also perform the following operations:

* List domains

* Set domains

* Display tasks

* Delete tasks
For more information, see the [cfdot repository](https://github.com/cloudfoundry/cfdot) on GitHub.

## CF Acceptance Tests
CF Acceptance Tests (CATs) is a suite of acceptance-level tests that exercise a full Cloud Foundry deployment using the golang cf CLI and `curl`.
See the [CF Acceptance Tests repository](https://github.com/cloudfoundry/cf-acceptance-tests) on GitHub for more information.