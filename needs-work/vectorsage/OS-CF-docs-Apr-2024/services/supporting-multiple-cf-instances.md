# Supporting multiple instances
You can register your service broker with multiple Cloud Foundry instances.
It might be necessary for the broker to know which Cloud Foundry instance is making a given request. For example, when using [Dashboard Single Sign-On](https://docs.cloudfoundry.org/services/dashboard-sso.html), the broker is expected to interact with the authorization and token endpoints for a given Cloud Foundry instance.
There are two strategies that can be used to discover which Cloud Foundry instance is making a given request.

## Routing and authentication
The broker can use unique credentials, a unique URL, or both for each Cloud Foundry instance. When registering the broker, you can configure different Cloud Foundry instances to use different base URLs that include a unique ID. For example:

* On Cloud Foundry instance 1, the service broker is registered with the URL `broker.example.com/123`.

* On Cloud Foundry instance 2, the service broker is registered with the URL `broker.example.com/456`.

## X-Api-Info-Location header
All calls to the broker from Cloud Foundry include an `X-Api-Info-Location` header containing the `/v2/info` URL for that instance. The `/v2/info` endpoint returns further information, including the location of that Cloud Foundry instance’s UAA.
Support for this header was introduced in cf-release v212.