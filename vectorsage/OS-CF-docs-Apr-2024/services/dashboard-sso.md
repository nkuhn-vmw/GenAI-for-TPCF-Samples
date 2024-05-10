# Dashboard Single Sign-on
Single sign-on (SSO) allows Cloud Foundry you to authenticate with third party service
dashboards
using your Cloud Foundry credentials.
Service dashboards are web interfaces which allow you to interact with some or all of the features the
service offers.
SSO provides a streamlined experience that limits repeated logins and multiple accounts across managed services.
Your credentials are never directly transmitted to the service because the OAuth protocol handles authentication.
Dashboard SSO was introduced in [cf-release v169](https://github.com/cloudfoundry/cf-release/tree/v169) so
this or a newer version is required to support the feature.

## Enabling SSO
To activate the SSO feature, Cloud Controller requires a UAA client with sufficient permissions to
create and delete clients for the service brokers that request them.
You can configure the client by including the following snippet in the cf-release manifest:
```
properties:
uaa:
clients:
cc-service-dashboards:
secret: cc-broker-secret
scope: openid,cloud_controller_service_permissions.read
authorities: clients.read,clients.write,clients.admin
authorized-grant-types: authorization_code,client_credentials
```
When this client is not present in the cf-release manifest, Cloud Controller cannot manage UAA clients
and you receive a warning when creating or updating service brokers that advertise the `dashboard_client`
properties.

## Service Broker responsibilities

### Registering the dashboard client

1. A service broker must include the `dashboard_client` line in the JSON response from
its [catalog endpoint](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#catalog-management) for each service that implements this feature. A valid response appears:
```
{
"services": [
{
"id": "44b26033-1f54-4087-b7bc-da9652c2a539",
...
"dashboard\_client": {
"id": "p-mysql-client",
"secret": "p-mysql-secret",
"redirect\_uri": "http://p-mysql.example.com"
}
}
]
}
```
The `dashboard_client` line is a hash containing three lines:

* `id` is the unique identifier for the OAuth client that creates your service dashboard on the token server (UAA), and is used by your dashboard to authenticate with the token server (UAA). If the client id is already taken, Cloud Foundry returns an error when registering or updating the broker.

* `secret` is the shared secret your dashboard uses to authenticate with the token server (UAA).

* `redirect_uri` is used by the token server as an additional security precaution. UAA does not provide a token if the callback URL declared by the service dashboard does not match the domain name in `redirect_uri`. The token server matches on the domain name. Any paths also match. For example, a service dashboard requesting a token and declaring a callback URL of `http://p-mysql.example.com/manage/auth` is approved if `redirect_uri` for its client is `http://p-mysql.example.com/`.

2. When a service broker advertises the `dashboard_client` property for any of its services is [added or updated](https://docs.cloudfoundry.org/services/managing-service-brokers.html), Cloud Controller creates or update UAA clients as necessary. This client is used by the service dashboard to authenticate users.

### Dashboard URL
A service broker must return a URL for `dashboard_url` in response to a [provision request](https://github.com/openservicebrokerapi/servicebroker/blob/v2.13/spec.md#provisioning). Cloud Controller clients exposes this URL to users. `dashboard_url` can be found in the response from Cloud Controller to create a service instance, enumerate service instances, space summary, and other endpoints.
You can go to the service dashboard at the URL provided by `dashboard_url`, initiating the OAuth login flow.

## Service dashboard responsibilities

### OAuth flow
When you go to the URL from `dashboard_url`, the service dashboard initiates the OAuth login flow. A summary of the flow can be found in [section 1.2 of the OAuth RFC](http://tools.ietf.org/html/rfc6749#section-1.2). OAuth expects the presence of an [Authorization Endpoint](http://tools.ietf.org/html/rfc6749#section-3.1) and a [Token Endpoint](http://tools.ietf.org/html/rfc6749#section-3.2). In Cloud Foundry these endpoints are provided by the UAA. Clients can discover the location of UAA from Cloud Controller’s info endpoint; in the response the location can be found in the `token_endpoint` field.
```
$ curl api.example.com/info
{"name":"vcap","build":"2222","support":"http://support.example.com","version
":2,"description":"Cloud Foundry sponsored by Example Company","authorization_endpoint":
"https://login.example.com","token_endpoint":"https://uaa.example.com",
"allow_debug":true}
```
To activate service dashboards to support SSO for service instances created from different Cloud Foundry instances, the /v2/info url is sent to service brokers in the `X-Api-Info-Location` header of every API call.
A service dashboard can discover this URL from the broker, which activates the dashboard
to contact the appropriate UAA for a particular service instance. Although the Cloud Foundry API (CAPI) V2 is now deprecated, the Cloud Controller still communicates its /v2/info URL through this header. /v2/info is the sole CAPI V2 endpoint that continues to be served even where a Cloud Controller has been configured, through the CAPI bosh release, to deactivate the V2 API
A service dashboard must implement the OAuth Authorization Code Grant type [UAA documentation](https://github.com/cloudfoundry/uaa/blob/master/docs/UAA-APIs.rst#authorization-code-grant), [RFC documentation](http://tools.ietf.org/html/rfc6749#section-4.1).

1. When you visit the service dashboard at the value of `dashboard_url`, the dashboard redirects you to a browser for the Authorization Endpoint and includes `client_id`, a `redirect_uri` (callback URL with domain matching the value of `dashboard_client.redirect_uri`), and a list of requested scopes.
Scopes are permissions that are included in the token for a dashboard client that are received from UAA, and which Cloud Controller uses to enforce access. A client must request the minimum scopes it requires. The minimum scopes required for this workflow are:
`cloud_controller_service_permissions.read` and `openid`.
For an explanation of the scopes available to dashboard clients, see [On Scopes](https://docs.cloudfoundry.org/services/dashboard-sso.html#on-scopes).

2. You are authenticated by UAA and redirected to the Login Server, where you approve or deny the scopes requested by the service dashboard. You are presented with a description for permissions that represent each scope. After authentication, your browser is redirected back to the Authorization endpoint on UAA with an authentication cookie for the UAA.

3. Assuming you grant access, UAA redirects your browser back to the value of `redirect_uri` that the dashboard provided in the request for the Authorization Endpoint. The `Location` header in the response includes an authorization code:
```
HTTP/1.1 302 Found
Location: https://p-mysql.example.com/manage/auth?code=F45jH
```

4. The dashboard UI then requests an access token from the Token Endpoint by including the authorization code that you received in the previous step. When you make the request, the dashboard must authenticate with UAA by passing the client `id` and `secret` lines in a basic auth header. UAA verifies that the client id matches the client that issued the code. The dashboard also includes the `redirect_uri` used to obtain the authorization code for verification.

5. UAA authenticates the dashboard client, validates the authorization code, and makes sure that the redirect URI that was received matches the URI used to redirect the client. If valid, UAA responds back with an access token and a refresh token.

### Checking user permissions
UAA is responsible for your authentication and provides the service with an access token with the requested permissions. However, after you have been logged in, it is the responsibility of the service dashboard to verify that you make the request to manage an instance and have access to that service instance.
The service uses a GET to the `/v3/service_instances/:guid/permissions` endpoint on the Cloud Controller. The request must include a token for an authenticated user and the service instance GUID. The token is the same one obtained from the UAA in response to a request to the Token Endpoint described earlier.

#### Request example
```
curl -H 'Content-Type: application/json' \

-H 'Authorization: bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoid' \
http://api.cloudfoundry.com/v3/service\_instances/44b26033-1f54-4087-b7bc-da9652c2a539/permissions
```

#### Response
```
{
"manage": true,
"read": true
}
```
The response includes the following strings which indicate the your various permissions for a given service instance:

* `manage`: if `true`, you have sufficient permissions to make changes and update the service instance.`false` indicates insufficient permissions.

* `read`: if `true`, you have permission to access read-only diagnostic and monitoring information for a given service instance.For example, permission to view a read-only dashboard. `false` indicates insufficient permissions.
Since administrators might change the permissions of users at any time, the service checks this endpoint whenever a user uses the SSO flow to access the service UI.

### Scopes
With scopes you can specify exactly what type of access you need. Scopes limit access for OAuth tokens. They do not grant any additional permission beyond what you already have.

#### Minimum scopes
The following scopes are necessary to implement the integration. Most dashboards might not need more permissions than to have the scopes activated.
| Scope | Permissions |
| --- | --- |
| `openid` | Allows access to basic data, for example, email addresses |
| `cloud_controller_service_permissions.read` | Allows access to the CC endpoint that specifies whether you can manage a given service instance |

#### Additional scopes
Dashboards with extended capabilities might need to request the following additional scopes:
| Scope | Permissions |
| --- | --- |
| `cloud_controller.read` | Allows read access to all resources you are authorized to read |
| `cloud_controller.write` | Allows write access to all resources you are authorized to update / create / delete |

## Reference implementation
The [MySQL Service Broker](https://github.com/cloudfoundry/cf-mysql-broker) is an example of a broker that implements a SSO dashboard.
The login flow is implemented using the [OmniAuth library](https://github.com/intridea/omniauth) and a custom [UAA OmniAuth Strategy](https://github.com/cloudfoundry/omniauth-uaa-oauth2).
See the [OmniAuth wiki page](https://github.com/intridea/omniauth/wiki/Strategy-Contribution-Guide) for instructions on how to create your own strategy.
The UAA OmniAuth strategy is used to get an authorization code.
For more information on authorization codes, see [this section](https://github.com/cloudfoundry/uaa/blob/master/docs/UAA-APIs.rst#authorization-code-grant) of the UAA documentation.
You are redirected back to the service (as specified by the `callback_path` option or the default `auth/cloudfoundry/callback` path) with the authorization code. Before the application action is dispatched, the OmniAuth strategy uses the authorization code to [get a token](https://github.com/cloudfoundry/uaa/blob/master/docs/UAA-APIs.rst#client-obtains-token-post-oauth-token) and uses the token to request information from UAA to fill the `omniauth.auth` environment variable. When OmniAuth returns control to the application, the `omniauth.auth` environment variable hash is filled with the token and user information obtained from UAA.
For more information, see [Auth Controller](https://github.com/cloudfoundry/cf-mysql-broker/blob/master/app/controllers/manage/auth_controller.rb).

## Restrictions

* UAA clients are scoped to services. There must be a `dashboard_client` entry for each service that uses SSO integration.

* Each `dashboard_client id` must be unique across the Cloud Foundry deployment.

## Resources

* [OAuth](http://oauth.net/2/)

* [Example broker with SSO implementation](https://github.com/cloudfoundry/cf-mysql-broker)

* [Cloud Controller API docs](https://v3-apidocs.cloudfoundry.org/version/3.147.0/#introduction)

* [User Account and Authentication (UAA) Service APIs](https://github.com/cloudfoundry/uaa/blob/master/docs/UAA-APIs.rst)

* [MySQL Service Broker / example-broker](https://github.com/cloudfoundry/cf-mysql-broker)