# Rate limit information returned by the Cloud Controller API
This topic describes rate limit information that is returned by the Cloud Controller API (CAPI).
For information about how to configure rate limits, see [Setting the rate limit for the Cloud Controller API](https://docs.cloudfoundry.org/running/setting-rate-limit-cloud-api.html).
Note that the Cloud Controller offers several, distinct rate limiters to serve different purposes. Where multiple rate limiters are enabled, information about each will be shared in its own HTTP response header.

## Rate limit responses: General
CAPI includes rate limit information in the HTTP header. Each header includes:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 56
X-RateLimit-Reset: 1372700873
```
Use this table to understand the rate limit header.
| Field Value | Description |
| --- | --- |
| X-RateLimit-Limit | The maximum number of attempts per [User Account and Authentication (UAA)](https://docs.cloudfoundry.org/concepts/architecture/uaa.html) user, if a user is authenticated. The maximum number of attempts per IP address, if no user is authenticated. |
| X-RateLimit-Remaining | The estimated number of attempts remaining. |
| X-RateLimit-Reset | The time when the rate limit counter resets, in UTC [epoch seconds](https://en.wikipedia.org/wiki/Unix_time). |
Requests are counted separately in each Cloud Controller instance and each produces an estimate for the total number of remaining requests.
The estimate is based on the fraction remaining on the Cloud Controller instance, rounded down to the nearest 10%, multiplied by the global maximum number of attempts.
This might result in inconsistent values for the `X-RateLimit-Remaining` header when running multiple instances of CAPI, such as some requests still being allowed when the header value is `0`.
When requests exceed the maximum rate limit value, CAPI returns a `429: Too Many Requests` error code.

## Rate limit responses: V2 API
Operators can limit the number of V2 API requests. This includes all `v2/*` requests except `v2/info`. Each HTTP header includes the following information:
```
X-Ratelimit-Limit-V2-Api: 60
X-Ratelimit-Remaining-V2-Api: 56
X-Ratelimit-Reset-V2-Api: 1643767322
```
The way V2 API requests are counted is the same as for the general rate limiter, and headers contain the same information. See the table for more details.
When the maximum rate limit value is exceeded, CAPI returns `429 Too Many Requests` with the body `CF-RateLimitV2APIExceeded`.
Operators can configure CAPI to exempt users and clients with the UAA scope cloud\_controller.v2\_api\_rate\_limit\_exempt from the V2 API rate limit.

## Rate limit responses: Service Brokers
Operators can limit the number of concurrent requests per user, for each Cloud Controller instance, for operations related to service brokers that can be made to CAPI endpoints for the following resource types:

* [`v3/service_instances`](https://v3-apidocs.cloudfoundry.org/index.html#service-instances)

* [`v3/service_credential_bindings`](https://v3-apidocs.cloudfoundry.org/index.html#service-credential-binding)

* [`v3/service_route_binding`](https://v3-apidocs.cloudfoundry.org/index.html#service-route-binding)

* [`v2/service_instances`](https://apidocs.cloudfoundry.org/#service-instances)

* [`v2/service_bindings`](https://apidocs.cloudfoundry.org/#service-bindings)

* [`v2/service_keys`](https://apidocs.cloudfoundry.org/#service-keys)
Important
Unlike the CAPI rate limit, which caps the requests a user can make across the whole Cloud Foundry platform, service broker rate limits apply per CAPI instance. For example, if the limit is 3 and there are 2 instances, the maximum number of concurrent requests a user can make is 6.
A request finishes when CAPI sends a response. This occurs even if that response is `202 Accepted`, indicating that an asynchronous operation is to be performed, such as a service broker creating a service instance.
For more information, see [Asynchronous Operations](https://v3-apidocs.cloudfoundry.org/index.html#asynchronous-operations) in the CAPI V3 documentation.
This rate limit does not cap the number of asynchronous operations that can be in progress at any one time for any of the above service-related endpoints.
Any requests that breach the concurrency are rate limited, and receive a `429 Too Many Requests` response with the body `CF-ServiceBrokerRateLimitExceeded (10016)` and a Retry-After header.
The header gives an absolute time suggesting when the client should attempt to make their request again.
This is the current time plus a random number of seconds between 0.5x and 1.5x of the configured value for `cc.broker_client_timeout_seconds`.
If this property is not set, it defaults to 60 seconds, and the header suggests a random retry time between 30 and 90 seconds in the future.