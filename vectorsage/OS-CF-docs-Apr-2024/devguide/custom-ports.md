# Configuring Cloud Foundry to route traffic to apps on custom ports
By default, apps only receive requests on port `8080` for both HTTP and TCP routing. Configuring custom app ports allows developers to bring workloads onto
Cloud Foundry that receive requests on ports other than `8080`. Here are some example use cases:

* Serving web client requests on one port, and stats and debugging on another

* Using TCP protocols that require multiple ports

* Running Docker images on Cloud Foundry
To use the `apps` and `route_mappings` Cloud Controller API endpoints to update the ports so the the app can receive requests, see [Procedure](https://docs.cloudfoundry.org/devguide/custom-ports.html#procedure).

## Flow of a request to an app
The table describes the Network Address Translation that occurs in the data path of a client request:
| Port Type | Description | Network Hop |
| --- | --- | --- |
| Route port | The port to which a client sends a request | Client to load balancer, load balancer to Gorouter |
| Back end port | The port on the VM where an application container is hosted, which is unique to the container | Gorouter to Diego Cell |
| App port | The port on the container, which must match a port on which the app is configured to receive requests | Diego Cell to application container |
The following diagram shows an example data path and Network Address Translation for TCP routing:
![Traffic flow-diagram for data path and Network Address Translation for TCP routing](https://docs.cloudfoundry.org/devguide/images/route_ports.png)
For HTTP routing, the route port is always `80` or `443`.

## Prerequisites
Before you follow the procedure to configure routing to your app on custom ports, you must have:

* An app pushed to Cloud Foundry that can receive requests on one or more custom ports.

* Routes for which you want traffic forwarded to your app on custom ports, which are mapped to the app.
If your app receives requests on two ports, and you want clients to be able to send requests to both of them, create two routes. These routes can be from HTTP or TCP domains.

## Procedure
In the following procedure, use API endpoints to map the routes to your app on the ports it uses to receive requests.
For more information about routes, see [Routes and Domains](https://docs.cloudfoundry.org/devguide/deploy-apps/routes-domains.html).
To configure your app to receive HTTP or TCP requests on custom ports:

1. Run:
```
cf app APP-NAME --guid
```
Where `APP-NAME` is the name of your app.

2. From the output, record:

* Under `guid`, the global unique identifier (GUID) of your app.

* Under `type`, the process type your app uses.

3. Retrieve the GUIDs of the routes for your app by running one of these commands, depending on whether your app uses HTTP or TCP routes:

* For HTTP routes, run:
```
cf curl /v3/apps/APP-GUID/routes?hosts=ROUTE-HOSTNAME
```
Where:

+ `APP-GUID` is the GUID of your app that you recorded in an earlier step.

+ `ROUTE-HOSTNAME` is the subdomain of the domain associated with the route. For example, in the route `example-app.shared-domain.example.com`, the host name is `example-app`.

* For TCP routes, run:
```
cf curl /v3/apps/APP-GUID/routes?port=PORT
```
Where:

+ `APP-GUID` is the GUID of your app that you recorded in an earlier step.

+ `PORT` is the port to which the TCP route sends requests.

4. From the output, record the GUIDs of the routes for your app.

5. For each route, update the ports to which it sends requests by running:
```
cf curl -X PATCH /v3/routes/ROUTE-GUID/destinations -d '{
"destinations": [
{
"app": {
"guid": "APP-GUID",
"process": {
"type": "PROCESS-TYPE"
}
},
"port": PORT,
"protocol": "PROTOCOL"
}
]
}'
```
Where:

* `APP-GUID` is the GUID of your app that you recorded in an earlier step.

* `ROUTE-GUID` is the GUID of a route that you recorded in an earlier step.

* `PORT` is a custom port on which your app is configured to receive requests.

* `PROTOCOL` is the protocol that the route uses. For HTTP routes, this value is either `http1` or `http2`. For TCP routes, this value is `tcp`.

* `PROCESS-TYPE` is the value of `type` that you recorded in an earlier step. This value is usually `web`.

**Caution**
This API call removes all destinations for a route and replaces them with the destinations you provide in the API request.

## Additional resources

* For more information about making requests to the Cloud Controller API (CAPI) `apps` endpoints, see the [CAPI V3 documentation](https://v3-apidocs.cloudfoundry.org/index.html#apps).