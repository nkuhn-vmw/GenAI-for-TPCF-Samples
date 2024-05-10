# Configuring routes and domains
Developers and administrators can configure routes and domains for their apps using the Cloud Foundry Command Line Interface (cf CLI).
This topic describes how routes and domains work in Cloud Foundry (Cloud Foundry).
For more information about routing capabilities in Cloud Foundry, see [HTTP routing](https://docs.cloudfoundry.org/concepts/http-routing.html).

## Routes
The Cloud Foundry Gorouter routes requests to apps by associating an app with an address, known as a route. This is known as a *mapping*. Use
the cf CLI [cf map-route](https://cli.cloudfoundry.org/en-US/cf/map-route.html) command to associate an app and route.
The routing tier compares each request with a list of all the routes mapped to apps and attempts to find the best match. For example, the Gorouter makes the following matches for the two routes `example-app.shared-domain.example.com` and `example-app.shared-domain.example.com/products`:
| Request | Matched Route |
| --- | --- |
| `http://example-app.shared-domain.example.com` | `example-app.shared-domain.example.com` |
| `http://example-app.shared-domain.example.com/contact` | `example-app.shared-domain.example.com` |
| `http://example-app.shared-domain.example.com/products` | `example-app.shared-domain.example.com/products` |
| `http://example-app.shared-domain.example.com/products/123` | `example-app.shared-domain.example.com/products` |
| `http://products.shared-domain.example.com` | No match; `404` |
The Gorouter does not use a route to match requests until the route is mapped to an app. In the example, `products.shared-domain.example.com` might have been created as a route in Cloud Foundry, but until it is mapped to an app, requests for the route receive a `404` error.
The routing tier knows the location of instances for apps mapped to routes. After the routing tier calculates a route as the best match for a request, it makes a load-balancing calculation using the configured balancing algorithm (by default, this is [round-robin](https://docs.cloudfoundry.org/concepts/http-routing.html#round-robin)), and forwards the request to an instance of the mapped app.
Developers can map many apps to a single route, resulting in load-balanced requests for the route across all instances of all mapped apps. This approach activates the blue/green rolling deployment strategy. Developers can also map an individual app to multiple routes, enabling access to the app from many URLs.
The number of routes that can be mapped to each app is approximately 1000 (128 KB).
Routes belong to a space, and developers can only map apps to a route created in or shared with the same space. For more information about sharing routes across spaces, see [Share a route with another space](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#share-route) .
Routes are globally unique. Developers in one space cannot create a route with the same URL as developers in another space, regardless of which orgs control these spaces.

### HTTP versus TCP routes
By default, Cloud Foundry only supports routing of HTTP requests to apps.
Routes are considered HTTP if they are created from HTTP domains, and TCP if they are created from TCP domains. For more information, see [HTTP versus TCP shared domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#http-vs-tcp-shared-domains).
HTTP routes include a domain, a host name (optional), and a context path (optional). `shared-domain.example.com`, `example-app.shared-domain.example.com`, and `example-app.shared-domain.example.com/products` are all examples of HTTP routes. Apps listen to the `localhost` port defined by the `$PORT` environment variable, which is `8080` on Diego. For example, requests to `example-app.shared-domain.example.com` are routed to the application container at `localhost:8080`.
Requests to HTTP routes must be sent to ports `80` or `443`. Ports cannot be reserved for HTTP routes. You can update the ports on which an app can receive requests through the Cloud Controller API. For more information, see [Configuring apps to listen on custom ports (Beta)](https://docs.cloudfoundry.org/devguide/custom-ports.html).
TCP routes include a domain and a route port. A route port is the port clients make requests to. This is not the same port as what an app pushed to Cloud Foundry listens on. `tcp.shared-domain.example.com:60000` is an example of a TCP route. Just as for HTTP routes, apps listen to the `localhost` port defined by the `$PORT` environment variable, which is `8080` on Diego. For example, requests to `tcp.shared-domain.example.com:60000` are routed to the application container at `localhost:8080`.
When a port is reserved for a route, it cannot be reserved for another route. Host name and path are not supported for TCP routes.

### Internal container-to-container routes
Cloud Foundry apps can communicate with each other securely and directly over internal routes that never leave the platform.
Apps running on Windows cells cannot use internal, container-to-container routes.
To create an internal route:

1. Use the [cf map-route](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#map-internal-route) command with an [internal domain](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#internal-domains). For example:
```
$ cf map-route app apps.internal --hostname app
```

* After an internal route is mapped to an app, the route resolves to IP addresses of the app instances. The IP addresses are visible in the application container:
```
$ cf ssh app
vcap@1234:~$ host app.apps.internal
app.apps.internal has address 10.255.169.200
app.apps.internal has address 10.255.49.7
app.apps.internal has address 10.255.49.77
```

* To resolve individual instances, prepend the index to the internal route.
```
vcap@1234:~$ host 1.app.apps.internal

1.app.apps.internal has address 10.255.49.7
```

2. Create a network policy that allows your apps to communicate with each other. By default, apps cannot communicate over the container network. For more
information, see [Configuring container-to-container networking](https://docs.cloudfoundry.org/devguide/deploy-apps/cf-networking.html) and the [Cloud Foundry CLI reference guide](https://cli.cloudfoundry.org/en-US/cf/add-network-policy.html).

### Create a route
When a developer creates a route using the cf CLI, Cloud Foundry determines whether the route is an HTTP or a TCP route based on the domain. To create a HTTP route, a developer must choose an HTTP domain. To create a TCP route, a developer must choose a TCP domain.
Domains in Cloud Foundry provide a namespace from which to create routes. To list available domains for a targeted organization, use the [cf domains](https://cli.cloudfoundry.org/en-US/cf/domains.html) command. For more information about domains, see [Domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#domains).
The following sections describe how developers can create HTTP and TCP routes for different use cases.

#### Create an HTTP route with host name
In Cloud Foundry, a host name is the label that indicates a subdomain of the domain associated with the route. Given a domain
`shared-domain.example.com`, a developer can create the route `example-app.shared-domain.example.com` by specifying the host name `example-app` with the
[cf create-route](https://cli.cloudfoundry.org/en-US/cf/create-route.html) command as shown in this example:

* **cf CLI v7**
```
$ cf create-route shared-domain.example.com --hostname example-app
Creating route example-app.shared-domain.example.com for org example-org / space example-space as username@example.com...
OK
```

**Important**
The cf CLI v7 `create-route` command does not require the space as an argument. It uses the space you are targeting.

* **cf CLI v6**
```
$ cf create-route example-space shared-domain.example.com --hostname example-app
Creating route example-app.shared-domain.example.com for org example-org / space example-space as username@example.com...
OK
```
This command instructs Cloud Foundry to only route requests to apps mapped to this route for these URLs:

* `http://example-app.shared-domain.example.com`

* `https://example-app.shared-domain.example.com`

* Any path under either of the these URLs, such as `http://example-app.shared-domain.example.com/bar`

#### Create an HTTP route without host name
This approach creates a route with the same address as the domain itself and is permitted for private domains only. For more information, see [Private
Domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#private-domains) .
A developer can create a route from the domain `private-domain.example.com` with no host name with the
[cf create-route](https://cli.cloudfoundry.org/en-US/cf/create-route.html) command:

* **cf CLI v7**
```
$ cf create-route private-domain.example.com
Creating route private-domain.example.com for org example-org / space example-space as username@example.com...
OK
```

* **cf CLI v6**
```
$ cf create-route example-space private-domain.example.com
Creating route private-domain.example.com for org example-org / space example-space as username@example.com...
OK
```
If DNS is configured correctly, this command instructs Cloud Foundry to route requests to apps mapped to this route from these URLs:

* `http://private-domain.example.com`

* `https://private-domain.example.com`

* Any path under either of these URLs, such as `http://private-domain.example.com/foo`
If there are no other routes for the domain, requests to any subdomain, such as `http://foo.private-domain.example.com`, fail.
A developer can also create routes for subdomains with no host names. The following command creates a route from the subdomain
`foo.private-domain.example.com`:

* **cf CLI v7**
```
$ cf create-route foo.private-domain.example.com
Creating route foo.private-domain.example.com for org example-org / space example-space as username@example.com...
OK
```

* **cf CLI v6**
```
$ cf create-route example-space foo.private-domain.example.com
Creating route foo.private-domain.example.com for org example-org / space example-space as username@example.com...
OK
```
If DNS is configured for this subdomain, this command instructs Cloud Foundry to route requests to apps mapped to this route from these URLs:

* `http://foo.private-domain.example.com`

* `https://foo.private-domain.example.com`

* Any path under either of these URLs, such as `http://foo.private-domain.example.com/foo`

#### Create an HTTP route with wildcard host name
An app mapped to a wildcard route acts as a fallback app for route requests if the requested route does not exist. To create a wildcard route, use an asterisk for the host name.
A developer can create a wildcard route from the domain `foo.shared-domain.example.com` by running:

* **cf CLI v7**
```
$ cf create-route foo.shared-domain.example.com --hostname '*'
Creating route *.foo.shared-domain.example.com for org example-org / space example-space as username@example.com...
OK
```

* **cf CLI v6**
```
$ cf create-route example-space foo.shared-domain.example.com --hostname '*'
Creating route *.foo.shared-domain.example.com for org example-org / space example-space as username@example.com...
OK
```
If a client sends a request to `http://app.foo.shared-domain.example.com` by accident, attempting to reach `example-app.foo.shared-domain.example.com`,
Cloud Foundry routes the request to the app mapped to the route `*.foo.shared-domain.example.com`.

#### Create an HTTP route with a path
Developers can use paths to route requests for the same host name and domain to different apps.
A developer can create three routes using the same host name and domain in the space `example-space` by running:

* **cf CLI v7**
```
$ cf create-route shared-domain.example.com --hostname store --path products
Creating route store.shared-domain.example.com/products for org example-org / space example-space as username@example.com...
OK
```
```
$ cf create-route shared-domain.example.com --hostname store --path orders
Creating route store.shared-domain.example.com/orders for org example-org / space example-space as username@example.com...
OK
```
```
$ cf create-route shared-domain.example.com --hostname store
Creating route store.shared-domain.example.com for org example-org / space example-space as username@example.com...
OK
```

* **cf CLI v6**

**Important**
To create a route without a path using cf CLI v6, you must run the commands in this order: Create the route without a path, and then create any routes with a path. If you do not need a route without a path, then this sequence is not required.
```
$ cf create-route example-space shared-domain.example.com --hostname store
Creating route store.shared-domain.example.com for org example-org / space example-space as username@example.com...
OK
```
```
$ cf create-route example-space shared-domain.example.com --hostname store --path products
Creating route store.shared-domain.example.com/products for org example-org / space example-space as username@example.com...
OK
```
```
$ cf create-route example-space shared-domain.example.com --hostname store --path orders
Creating route store.shared-domain.example.com/orders for org example-org / space example-space as username@example.com...
OK
```
The developer can then map the new routes to different apps by following the procedure in [Map a route to your app](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#map-route).
If the developer maps the first route with path `products` to the `products` app, the second route with path `orders` to the `orders` app, and the last route to the `storefront` app. After this:

* Cloud Foundry routes requests to `http://store.shared-domain.example.com/products` to the `products` app.

* Cloud Foundry routes requests to `http://store.shared-domain.example.com/orders` to the `orders` app.

* Cloud Foundry routes requests to `http://store.shared-domain.example.com` to the `storefront` app.
Cloud Foundry attempts to match routes with a path, and then attempts to match host and domain.

**Important**

* Routes with the same domain and host name but different paths can only be created in the same space. Private domains do not have this limitation.

* Cloud Foundry does not route requests for context paths to the root context of an app. Apps must serve requests on the context path.

#### Create a TCP route with a port
A developer can create a TCP route for `tcp-domain.example.com` on an arbitrary port. This is the default in the v7 version of the cf CLI.

* **cf CLI v6** - To get an arbitrary (random) port, you must use the `--random port` flag.
```
$ cf create-route example-space tcp-domain.example.com --random-port
Creating route tcp-domain.example.com for org example-org / space example-space as [user@example.com](mailto:user@example.com)...
OK
Route tcp-domain.example.com:60034 has been created
```

* **cf CLI v7** - An arbitrary (random) port is the default. The `--random port` flag is not supported.
```
$ cf create-route example-space tcp-domain.example.com --random-port
Creating route tcp-domain.example.com for org example-org / space example-space as [user@example.com](mailto:user@example.com)...
OK
Route tcp-domain.example.com:60034 has been created
```
In this example, Cloud Foundry routes requests to `tcp-domain.example.com:60034` to apps mapped to this route.
To request a specific port, a developer can use the `--port` flag, so long as the port is not reserved for another space. To create a TCP route for
`tcp-domain.example.com` on port 60035, run:
```
$ cf create-route example-space tcp-domain.example.com --port 60035
Creating route tcp-domain.example.com:60035 for org example-org / space example-space as user@example.com...
OK
```

### List routes
Developers can list routes for the current space with the [cf routes](https://cli.cloudfoundry.org/en-US/cf/routes.html) command. A route is uniquely identified by the combination of host name, domain, port, and path.
```
$ cf routes
Getting routes as user@private-domain.example.com ...
space host domain port path type apps
example-space example-app shared-domain.example.com example-app
example-space example-app private-domain.example.com example-app
example-space store shared-domain.example.com /products products
example-space store shared-domain.example.com /orders orders
example-space store shared-domain.example.com storefront
example-space shared-domain.example.com 60000 tcp tcp-app
```
Developers can only see routes in spaces where they are a member.
Note that cf CLI v7 removes the `port` and `path` columns from the output.

### View a route
Developers can view a route and its destinations within the current space with the `cf route` command. A route is uniquely identified by the combination of a host name, domain, port, and path.
Note that the `cf route` command is available in cf CLI v8 only.
```
$ cf route shared-domain.example.com --hostname example-app
Showing route example-app.shared-domain.example.com in org o / space example-space as admin...
domain: shared-domain.example.com
host: example-app
port:
path:
protocol: http
Destinations:
app process port protocol
mystore web 8080 http1
```
Developers can only view a route within a space where they are a member.

### Check routes
Developers cannot create a route that is already taken. To find out if a route is available, developers can use the [cf
check-route](https://cli.cloudfoundry.org/en-US/cf/check-route.html) command.
To find out if a route with the host name `store` and the domain `shared-domain.example.com` and the path `products` exists, run:

* **cf CLI v7**:
```
$ cf check-route shared-domain.example.com --hostname store --path /products
Checking for route...
OK
Route store.shared-domain.example.com/products does exist
```

* **cf CLI v6**:
```
$ cf check-route store shared-domain.example.com --path /products
Checking for route...
OK
Route store.shared-domain.example.com/products does exist
```

### Map a route to your app
For an app to receive requests to a route, developers must map the route to the app with the [cf map-route](https://cli.cloudfoundry.org/en-US/cf/map-route.html) command. If the route does not already exist, this command creates it.
Any app that is not routed to port `80` or port `443` must be explicitly mapped using the `cf map-route` command. Otherwise, the route is mapped to port `443`.
You can create and reserve routes for later use by following the procedure in [Manually map a route](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#map-route-manually). You can also map routes to their app immediately as part of a push. See [Map a route with app push](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#map-route-on-push).
Changes to route mappings are run asynchronously. On startup, an app becomes accessible at its route within a few seconds. Similarly, upon mapping a new route to a running app, the app becomes accessible at this route within a few seconds of the CLI exiting.

#### Manually map a route
For these routes and apps:
| Route | Apps |
| --- | --- |
| store.shared-domain.example.com/products | products |
| store.shared-domain.example.com/orders | orders |
| store.shared-domain.example.com | storefront |
| tcp-domain.example.com:60000 | tcp-app |
The following commands map the routes in the table to their respective apps. Developers use host name, domain, and path to uniquely identify a route to which to map their apps.
```
$ cf map-route products shared-domain.example.com --hostname store --path products
$ cf map-route orders shared-domain.example.com --hostname store --path orders
$ cf map-route storefront shared-domain.example.com --hostname store
$ cf map-route tcp-app tcp-domain.example.com --port 60000
```
The following command maps the wildcard route `*.foo.shared-domain.example.com` to the app `myfallbackapp`.
```
$ cf map-route myfallbackapp foo.shared-domain.example.com --hostname '*'
```
In cf CLI v8, the following command maps the route `h2app.shared-domain.example.com` as an HTTP/2 route to the HTTP/2 app `h2app`.
```
$ cf map-route h2app shared-domain.example.com --hostname h2app --destination-protocol http2
```

#### Map a route with app push
Developers can map a route to their app with the `cf push` command.
As of cf CLI v7, the best way to do this is by using the `routes` property in the manifest. The `-d` flag is no longer supported.

**For cf CLI v6 only:**
If a domain or host name is not specified, then a route is created using the app name and the default shared domain. For more information, see [Shared domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#shared-domains). The following command pushes the app `example-app`, creating the route `example-app.shared-domain.example.com` from the default shared domain `shared-domain.example.com`. If the route has not already been created in another space, this command also maps it to the app.
```
$ cf push example-app
```
To customize the route during `push`, specify the domain using the `-d` flag and the host name with the `--hostname` flag. The following command creates the `foo.private-domain.example.com` route for `example-app`:
```
$ cf push example-app -d private-domain.example.com --hostname foo
```
To map a TCP route during `push`, specify a TCP domain and request a random port using `--random-route`. To specify a port, push the app without a route, then create and map the route manually by following the procedure in [Create a TCP route with a port](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#create-route-w-port).
```
$ cf push tcp-app -d tcp-domain.example.com --random-route
```

#### Map a route using app manifest
Developers can map a route to their app with a manifest by editing the `route` attribute to specify the host, domain, port, and path components of the route. For more information, see [Deploying with app manifests](https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html#routes).

#### Map a route to multiple apps
Cloud Foundry allows multiple apps, or versions of the same app, to be mapped to the same route. This feature activates blue-green deployment. For more information see [Using blue-green deployment to reduce downtime and risk](https://docs.cloudfoundry.org/devguide/deploy-apps/blue-green.html).
Routing multiple apps to the same route might cause undesirable behavior in some situations by routing incoming requests randomly to one of the apps on the shared route.
For more information about troubleshooting this problem, see [Routing conflict](https://docs.cloudfoundry.org/devguide/deploy-apps/troubleshoot-app-health.html#routing-conflict) in *Troubleshooting app deployment and health*.

#### Map multiple routes to one app
You can have multiple routes to an app, but those routes cannot have different context paths.
These routes are valid for a single app:
| Route 1 | Route 2 |
| --- | --- |
| `example-app.example.com` | `example-app.apps.cf.example.com` |
| `example-app.example.com/foo` | `example-app.apps.cf.example.com/foo` |
These routes are *not* valid for a single app:
| Route 1 | Route 2 |
| --- | --- |
| `example-app.example.com/foo` | `example-app.apps.cf.example.com/bar` |
| `example-app.apps.cf.example.com/foo` | `example-app.example.com/bar` |

#### Map an internal route to an app
You can map an internal route to any app. This internal route allows your app to communicate with other apps without leaving the platform. After it is mapped, this route becomes available to all other apps on the platform.
This example creates a `foo.apps.internal` internal route for `example-app`:
```
$ cf map-route example-app apps.internal --hostname foo
```

### Unmap a route
Developers can remove a route from an app using the `cf unmap-route` command. The route remains reserved for later use in the space where it was created until the route is deleted.
To unmap an HTTP route from an app, identify the route using the host name, domain, and path:
```
$ cf unmap-route tcp-app private-domain.example.com --hostname example-app --path mypath
```
To unmap a TCP route from an app, identify the route using the domain and port:
```
$ cf unmap-route tcp-app tcp-domain.example.com --port 60000
```

### Share a route with another space
To follow the procedure in this section, you must use cf CLI v8.5.0 or later. To download cf CLI v8.5.0 or later, see the [Cloud Foundry CLI repository](https://github.com/cloudfoundry/cli/releases/tag/v8.5.0) on GitHub.
You can share a route with another space using the `cf share-route` command. To move an app to another space, you can share routes with that space to prevent downtime during the transition. Rather than deleting the route in the original space and re-creating the route in the new space, you can share the route with the new space and map it to the app running in that space.
To share a route with another space:

1. In a terminal window, allow route sharing by running:
```
cf enable-feature-flag route_sharing
```

2. Run:
```
cf share-route DOMAIN --hostname HOSTNAME --path PATH -s SPACE -o ORG
```
Where:

* `DOMAIN` is the domain in the route for your app.

* `HOSTNAME` is the host name in the route for your app.

* `PATH` is the path in the route for your app.

* `SPACE` is the space with which you want to share the route for your app.

* `ORG` is the org containing space with which you want to share the route for your app. If the space with which you want to share the route is within the same org as the space that contains the route, do not include the `-o` flag.The following example command shares the route `example-app.example.com/example-path` with the `other-space` space in the `other-org` org:
```
cf share-route example.com --hostname example-app --path example-path -s other-space -o other-org
```

### Transfer ownership of a route to another space

**Important**
To follow the procedure in this section, you must use cf CLI v8.5.0 or later. To download cf CLI v8.5.0 or later, see the [Cloud Foundry CLI repository](https://github.com/cloudfoundry/cli/releases/tag/v8.5.0) on GitHub.
After sharing a route with another space, you can transfer ownership of the route to that space using the `cf move-route` command. You can use this command if you are unable to maintain or delete a shared route within the space with which it was shared. For information about sharing routes across spaces, see [Share a route with another space](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#share-route).
To move a route:

1. In a terminal window, target the space from which the route was originally shared by running:
“`
cf target -s SPACE -o ORG
”`
Where:

* `SPACE` is the space from which the route was originally shared.

* `ORG` is the org containing space from which the route was originally shared. If the space from which the route was originally shared is within the same
org as the space with which the route was shared, do not include the `-o` flag.

2. Run:
“`
cf move-route DOMAIN –hostname HOSTNAME –path PATH -s SPACE -o ORG
”`
Where:

* `DOMAIN` is the domain in the route for your app.

* `HOSTNAME` is the host name in the route for your app.

* `PATH` is the path in the route for your app.

* `SPACE` is the space to which you want to move the route for your app.

* `ORG` is the org containing space to which you want to move the route for your app. If the space to which you want to move the route is within the same org as the space that contains the route, do not include the `-o` flag.
The following example command moves the route `example-app.example.com/example-path` with the `other-space` space in the `other-org` org:
```
cf move-route example.com --hostname example-app --path example-path -s other-space -o other-org
```

### Delete a route
Developers can delete a route from a space using the `cf delete-route` command.
To delete a HTTP route, identify the route using the host name, domain, and path:
```
$ cf delete-route private-domain.example.com --hostname example-app --path mypath
```
To delete a TCP route, identify the route using the domain and port.
```
$ cf delete-route tcp.private-domain.example.com --port 60000
```

### Routing requests to a specific app instance
Users can route HTTP requests to a specific app instance using the header `X-Cf-App-Instance`.

**Important**
Use of the `X-Cf-App-Instance` header is available only for users on the Diego architecture.
The format of the header is `X-Cf-App-Instance: APP_GUID:APP_INDEX`.
`APP_GUID` is an internal identifier for your app.
Use the `cf APP-NAME --guid` command to discover the `APP_GUID` for your app.
```
$ cf app example-app --guid
```
`APP_INDEX`, for example, `0`,`1`, `2`, or `3`, is an identifier for a particular app instance. Use the CLI command `cf app APP-NAME` to get statistics on each
instance of a particular app.
```
$ cf app example-app
```
The following example shows a request made to instance `9` of an app with GUID `5cdc7595-2e9b-4f62-8d5a-a86b92f2df0e` and mapped to route
`example-app.private-domain.example.com`.
```
$ curl example-app.private-domain.example.com -H "X-Cf-App-Instance: 5cdc7595-2e9b-4f62-8d5a-a86b92f2df0e:9"
```
If the `X-Cf-App-Instance` header is set to an invalid value, Gorouter returns a `400` status code and the response from Gorouter contains a
`X-Cf-Routererror` header with more information about the error. Before the routing release v0.197.0, Gorouter returned a `404` error.
These are the possible error responses:
| X-Cf-Routererror value | Reason for error
Response body | |
| --- | --- | --- |
| `invalid_cf_app_instance_header` | The value provided for `X-Cf-App-Instance` was an incorrectly formatted GUID. | None |
| `unknown_route` | The value provided for `X-Cf-App-Instance` is a correctly formatted GUID, but no instance is found with that GUID for the route
requested. | `400 Bad Request: Requested instance ('1') with guid ('aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa') does not exist for route
('example-route.cf.com')` |

## Domains
The term *domain* here differs from its common use and is specific to Cloud Foundry.
Likewise, shared domain and private domain refer to resources with specific meaning in Cloud Foundry. The use of *domain name*, *root domain*, and *subdomain* refers to DNS records.
Domains indicate to a developer that requests for any route created from the domain are routed to Cloud Foundry. This requires DNS to be configured out-of-band to resolve the domain name to the IP address of a load balancer configured to forward requests to the Cloud Foundryrouters. For more information about configuring DNS, see [DNS for domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#domains-dns).

### List domains for an org
When creating a route, developers select from domains available to them. Use the `cf domains` command to view a list of available domains for the targeted org:
```
$ cf domains
Getting domains in org example-org as user@example.com... OK
name status type
shared-domain.example.com shared
tcp-domain.example.com shared tcp
private-domain.example.com owned
```
This example displays three available domains: a shared HTTP domain `shared-domain.example.com`, a shared TCP domain `tcp-domain.example.com`, and a private
domain `private-domain.example.com`. For more information, see [Shared domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#shared-domains) and [Private domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#private-domains).

### HTTP versus TCP domains
By default, Cloud Foundry only supports routing of HTTP requests to apps.
HTTP domains indicate to a developer that only requests using the HTTP protocol are routed to apps mapped to routes created from the domain. Routing for HTTP domains is layer 7 and offers features like custom host names, sticky sessions, and TLS termination.
TCP domains indicate to a developer that requests over any TCP protocol, including HTTP, are routed to apps mapped to routes created from the domain. Routing for TCP domains is layer 4 and protocol-agnostic, so many features available to HTTP routing are not available for TCP routing. TCP domains are defined as being associated with the TCP router group. The TCP router group defines the range of ports available to be reserved with TCP routes. Only shared domains can use a TCP protocol.

### Shared domains
Admins manage shared domains, which are available to users in all orgs of a Cloud Foundry deployment. An admin can offer multiple shared domains to users. For example, an admin might offer developers the choice of creating routes for their apps from `shared-domain.example.com` and `cf.example-company.com`.
If a developer pushes an app without specifying a domain, a route is created for it from the first shared domain created in the system. All other operations involving route require the domain be specified. For more information, see [Routes](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#routes).
When using shared domains, you cannot have routes with the same host name and domain across different orgs and spaces.
Shared domains are HTTP by default, but can be configured to be TCP when associated with the TCP router group.

#### Create a shared domain
Admins can create an HTTP shared domain with the `cf create-shared-domain` command:
```
$ cf create-shared-domain shared-domain.example.com
```
To create a TCP shared domain, first discover the name of the TCP router group.

**Important**
cf CLI v7 does not support TCP routing or creating shared domains with router groups.
```
$ cf router-groups
Getting router groups as admin ...
name type
default-tcp tcp
```
Then create the shared domain using the `--router-group` option to associate the domain with the TCP router group.
```
$ cf create-shared-domain tcp-domain.example.com --router-group default-tcp
```

#### Delete a shared domain
Admins can delete a shared domain from Cloud Foundry with the `cf delete-shared-domain` command:
```
$ cf delete-shared-domain example.com
```

#### Internal domain
The internal domain is a special type of shared domain used for app communication internal to the platform. When you activate service discovery, the internal domain `apps.internal` becomes available for route mapping.
Admins can configure multiple internal domains. Add a custom internal domain name to the `internal_domains` property on the `bosh-dns-adapter` job. Then create an internal domain using the `--internal` option:
```
$ cf create-shared-domain shared-domain.example.com --internal
```
The `--router-group` option is not used with internal domains.

### Private domains
Org managers can add private domains, or custom domains, and give members of the org permission to create routes for privately registered domain names.
Private domains can be shared with other orgs and spaces. These are called as shared private domains and are not the same as shared domains. For more information, see [Shared domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html#shared-domains).
When using private domains, you can have routes with the same host name and domain name across different orgs and spaces. This cannot be done with shared domains.
Private domains can be HTTP or HTTPS only. TCP routing is supported for shared domains only.

#### Create a private domain
Org managers can create a private domain by running:

* **cf CLI v7**
```
$ cf create-private-domain example-org private-domain.example.com
```

* **cf CLI v6**
```
$ cf create-domain example-org private-domain.example.com
```
Org managers can create a private domain for a subdomain by running:

* **cf CLI v7**
```
$ cf create-private-domain example-org foo.private-domain.example.com
```

* **cf CLI v6**
```
$ cf create-domain example-org foo.private-domain.example.com
```

#### Sharing a private domain with one or more orgs
Org managers can grant or revoke access to a private domain to other orgs if they have permissions for these orgs.
As of cf CLI v7, `cf unshare-private-domain` command provides a warning and requires confirmation before it proceeds.
```
$ cf share-private-domain test-org private-domain.example.com
$ cf unshare-private-domain test-org private-domain.example.com
```

#### Delete a private domain
Org managers can delete a domain from Cloud Foundry with the `cf delete-domain` command:

* **cf CLI v7**:
```
$ cf delete-private-domain private-domain.example.com
```

**Important**
cf CLI v7 renames the `delete-domain` command to `delete-private-domain`.

* **cf CLI v6**:
```
$ cf delete-domain private-domain.example.com
```

### Requirements for parent and child domains
In the domain `example-app.shared-domain.example.com`, `shared-domain.example.com` is the parent domain of subdomain `example-app`. The following list describes requirements for creating domains:

* You can only create a private domain that is parent to a private subdomain.

* You can create a shared domain that is parent to either a shared or a private subdomain.
The domain `foo.example-app.shared-domain.example.com` is the child subdomain of `example-app.shared-domain.example.com`. The following list describes requirements for creating subdomains:

* You can create a private subdomain for a private parent domain only if the domains belong to the same org.

* You can create a private subdomain for a shared parent domain.

* You can only create a shared subdomain for a shared parent domain.

* You cannot create a shared subdomain for a private parent domain.

### DNS for domains
To create customized access to your apps, you can map specific or wildcard custom domains to Cloud Foundry by using your DNS provider.

#### Mapping Domains to your custom domain
To associate a registered domain name with a domain on Cloud Foundry, configure a CNAME record with your DNS provider, pointing at any shared
domain offered in Cloud Foundry.

##### Mapping a single domain to your custom domain
To map a single domain to a custom domain to Cloud Foundry, configure a CNAME record with your DNS provider.
Here are some example CNAME record mappings.
| Record set in custom domain | Type | Target in Cloud Foundry |
| --- | --- | --- |
| example-app.yourcustomdomain.com. | CNAME | example-app.shared-domain.example.com |
| www.yourcustomdomain.com. | CNAME | example-app.shared-domain.example.com |
After you create the CNAME mapping, your DNS provider routes your custom domain to `example-app.shared-domain.example.com`.
See your DNS provider documentation to find out if the trailing `.` is required.

##### Mapping multiple subdomains to your custom domain
Use a wildcard CNAME record to point all of the subdomains in your custom domain to shared-domain.example.com.
Each separately configured subdomain has priority over the wildcard configuration.
Here are some example wildcard CNAME record mappings.
| Record set in custom domain | Type | Target in Cloud Foundry |
| --- | --- | --- |
| \*.yourcustomdomain.com. | CNAME | \*.shared-domain.example.com |
| \*.yourcustomdomain.com. | CNAME | \*.example-app.shared-domain.example.com |
If you use a wildcard as the subdomain name, then your DNS provider can route from `*.YOURCUSTOMDOMAIN` to any of the following:

* `*.shared-domain.example.com`

* `foo.example-app.shared-domain.example.com`

* `bar.foo.example-app.shared-domain.example.com`

#### Configuring DNS for your registered root domain
To use your root domain for apps on Cloud Foundry, you can use custom DNS record types like ALIAS and ANAME, if your DNS provider offers them, or you can use subdomain redirection.

**Note**
Root domains are also called zone apex domains.
If your DNS provider supports using an ALIAS or ANAME record, configure your root domain with your DNS provider to point at a shared domain in
Cloud Foundry.
| Record | Name | Target | Note |
| --- | --- | --- | --- |
| ALIAS or ANAME | empty or @ | private-domain.example.com. | To decide whether to use an empty or @ value for the Name entry, see the documentation for your DNS provider. |
If your DNS provider does not support ANAME or ALIAS records, you can use subdomain redirection, also known as domain forwarding, to redirect requests for your root domain to a subdomain configured as a CNAME.

**Important**
If you use domain forwarding, SSL requests to the root domain might fail if the SSL certificate matches only the subdomain.
For more information about SSL certificates, see
the [Cloud Foundry documentation](https://docs.cloudfoundry.org/running/trusted-system-certificates.html).
Configure the root domain to point at a subdomain such as `www`, and configure the subdomain as a CNAME record pointing at a shared domain in
Cloud Foundry.
| Record | Name | Target | Note |
| --- | --- | --- | --- |
| URL or Forward | private-domain.example.com | www.private-domain.example.com | This method causes a `301 permanent redirect` to the subdomain you configure. |
| CNAME | www | example-app.shared-domain.example.com | |