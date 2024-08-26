# Security event logging
Here you can learn how to activate and interpret security event logging for the Cloud Controller, the User Account and Authentication (UAA) server, and CredHub.
You can use these logs to retrieve information about a subset of requests to the Cloud Controller, UAA server, and CredHub for security or compliance purposes.

## Cloud Controller logging

**Note** By default, Cloud Foundry does not enable Cloud Controller request logging. To enable this feature, you must set the `cc.security_event_logging.enabled` property in your Cloud Foundry manifest to `true` and redeploy.
The Cloud Controller logs security events to syslog. You must configure a syslog drain to forward your system logs to a log management service.
For more information, see [Configuring System Logging](https://docs.cloudfoundry.org/running/managing-cf/logging-config.html) and [Using Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html).

### Formatting log entries
Cloud Controller logs security events in the [Common Event Format](https://kc.mcafee.com/resources/sites/MCAFEE/content/live/CORP_KNOWLEDGEBASE/78000/KB78712/en_US/CEF_White_Paper_20100722.pdf) (CEF). CEF specifies the following format for log entries:
```
CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension
```
Entries in the Cloud Controller log use the following format:
```
CEF:CEF_VERSION|cloud_foundry|cloud_controller_ng|CC_API_VERSION|
SIGNATURE_ID|NAME|SEVERITY|rt=TIMESTAMP suser=USERNAME suid=USER_GUID
cs1Label=userAuthenticationMechanism cs1=AUTH_MECHANISM
cs2Label=vcapRequestId cs2=VCAP_REQUEST_ID request=REQUEST
requestMethod=REQUEST_METHOD cs3Label=result cs3=RESULT
cs4Label=httpStatusCode cs4=HTTP_STATUS_CODE src=SOURCE_ADDRESS
dst=DESTINATION_ADDRESS cs5Label=xForwardedFor cs5=X_FORWARDED_FOR_HEADER
```
See the following list for a description of the properties shown in the Cloud Controller log format:

* `CEF_VERSION`: The version of CEF used in the logs.

* `CC_API_VERSION`: The current Cloud Controller API version.

* `SIGNATURE_ID`: The method and path of the request. For example, `GET /v2/app:GUID`.

* `NAME`: The same as `SIGNATURE_ID`.

* `SEVERITY`: An integer that reflects the importance of the event.

* `TIMESTAMP`: The number of milliseconds since the Unix epoch.

* `USERNAME`: The name of the user who originated the request.

* `USER_GUID`: The GUID of the user who originated the request.

* `AUTH_MECHANISM`: The user authentication mechanism. This can be `oauth-access-token`, `basic-auth`, or `no-auth`.

* `VCAP_REQUEST_ID`: The VCAP request ID of the request.

* `REQUEST`: The request path and parameters. For example, `/v2/info?MY-PARAM=VALUE`.

* `REQUEST_METHOD`. The method of the request. For example, `GET`.

* `RESULT`: The meaning of the HTTP status code of the response. For example, `success`.

* `HTTP_STATUS_CODE`. The HTTP status code of the response. For example, `200`.

* `SOURCE_ADDRESS`: The IP address of the client who originated the request.

* `DESTINATION_ADDRESS`: The IP address of the Cloud Controller VM.

* `X_FORWARDED_FOR_HEADER`: The contents of the X-Forwarded-For
header of the request. This is empty if the header is not present.

### Examples of log entries
The following list provides several example requests with the corresponding Cloud Controller log entries.

* An anonymous `GET` request:
```
CEF:0|cloud_foundry|cloud_controller_ng|2.54.0|GET /v2/info|GET
/v2/info|0|rt=1460690037402 suser= suid= request=/v2/info
requestMethod=GET src=127.0.0.1 dst=192.0.2.1
cs1Label=userAuthenticationMechanism cs1=no-auth cs2Label=vcapRequestId
cs2=c4bac383-7cc9-4d9f-b1c0-1iq8c0baa000 cs3Label=result cs3=success
cs4Label=httpStatusCode cs4=200 cs5Label=xForwardedFor
cs5=198.51.100.1
```

* A `GET` request with basic authentication:
```
CEF:0|cloud_foundry|cloud_controller_ng|2.54.0|GET /v2/syslog_drain_urls|GET
/v2/syslog_drain_urls|0|rt=1460690165743 suser=bulk_api suid=
request=/v2/syslog_drain_urls?batch_size\=1000 requestMethod=GET
src=127.0.0.1 dst=192.0.2.1 cs1Label=userAuthenticationMechanism
cs1=basic-auth cs2Label=vcapRequestId cs2=79187189-e810-33dd-6911-b5d015bbc999
::eat1234d-4004-4622-ad11-9iaai88e3ae9 cs3Label=result cs3=success
cs4Label=httpStatusCode cs4=200 cs5Label=xForwardedFor cs5=198.51.100.1
```

* A `GET` request with OAuth access token authentication:
```
CEF:0|cloud_foundry|cloud_controller_ng|2.54.0|GET /v2/routes|GET
/v2/routes|0|rt=1460689904925 suser=admin suid=c7ca208f-8a9e-4aab-
92f5-28795f86d62a request=/v2/routes?inline-relations-depth\=1&q\=
host%3Adora%3Bdomain_guid%3B777-1o9f-5f5n-i888-o2025cb2dfc3
requestMethod=GET src=127.0.0.1 dst=192.0.2.1
cs1Label=userAuthenticationMechanism cs1=oauth-access-token
cs2Label=vcapRequestId cs2=79187189-990i-8930-52b2-9090b2c5poz0
::5a265621-b223-4520-afae-ab7d0ee7c75b cs3Label=result cs3=success
cs4Label=httpStatusCode cs4=200 cs5Label=xForwardedFor cs5=198.51.100.1
```

* A `GET` request that results in a 404 error:
```
CEF:0|cloud_foundry|cloud_controller_ng|2.54.0|GET /v2/apps/7f310103-
39aa-4a8c-b92a-9ff8a6a2fa6b|GET /v2/apps/7f310103-39aa-4a8c-b92a-
9ff8a6a2fa6b|0|rt=1460691002394 suser=bob suid=a00i2026-55io-3983-
555o-40e611410aec request=/v2/apps/7f310103-39aa-4a8c-b92a-9ff8a6a2fa6b
requestMethod=GET src=127.0.0.1 dst=192.0.2.1
cs1Label=userAuthenticationMechanism cs1=oauth-access-token cs2Label=vcapRequestId
cs2=49f21579-9eb5-4bdf-6e49-e77d2de647a2::9f8841e6-e04a-498b-b3ff-d59cfe7cb7ea
cs3Label=result cs3=clientError cs4Label=httpStatusCode cs4=404
cs5Label=xForwardedFor cs5=198.51.100.1
```

* A `POST` request that results in a 403 error:
```
CEF:0|cloud_foundry|cloud_controller_ng|2.54.0|POST /v2/apps|POST
/v2/apps|0|rt=1460691405564 suser=bob suid=4f9a33f9-fb13-4774-a708-
f60c939625cd request=/v2/apps?async\=true requestMethod=POST
src=127.0.0.1 dst=192.0.2.1 cs1Label=userAuthenticationMechanism
cs1=oauth-access-token cs2Label=vcapRequestId cs2=booc03111-9999-4003-88ab-
20i9r33333ou::5a4993fc-722f-48bc-aff4-99b2005i9bb5 cs3Label=result
cs3=clientError cs4Label=httpStatusCode cs4=403 cs5Label=xForwardedFor
cs5=198.51.100.1
```

## UAA logging
UAA logs security events to a file located at `/var/vcap/sys/log/uaa/uaa.log` on the UAA virtual machine (VM). Because these logs are rotated, you must configure a syslog drain to forward your system logs to a log management service.
For more information, see [Configuring System Logging](https://docs.cloudfoundry.org/running/managing-cf/logging-config.html) and [Using Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html).

### Log Events
UAA logs identify the following categories of events:

* Authorization and Password Events

* SCIM Administration Events

* Token Events

* Client Administration Events

* UAA Administration Events
To learn more about the names of the events included in these categories and the information they record in the UAA logs, see [User Account and Authentication Service Audit Requirements](https://docs.cloudfoundry.org/running/managing-cf/uaa-audit-requirements.html).

### Examples of log entries
The following sections provide several example requests with the corresponding UAA log entries.

#### Successful user authentication
```
Audit: TokenIssuedEvent ('["openid","scim.read","uaa.user",
"cloud_controller.read","password.write","cloud_controller.write",
"scim.write"]'): principal=a42026d6-5533-1884-eef2-838abcd0i3e3,
origin=[client=cf, user=bob], identityZoneId=[uaa]
```

* This entry records a `TokenIssuedEvent`.

* UAA issued a token associated with the scopes `"openid","scim.read","uaa.user",
"cloud_controller.read","password.write","cloud_controller.write","scim.write"` to the user `bob`.

#### Failed user authentication
```
Audit: UserAuthenticationFailure ('bob@example.com'):
principal=61965469-c821-46b7-825f-630e12a51d6c,
origin=[remoteAddress=198.51.100.1, clientId=cf],
identityZoneId=[uaa]
```

* This entry records a `UserAuthenticationFailure`.

* The user `bob@example.com` originating at `198.51.100.1` failed to authenticate.

#### Successful user creation
```
Audit: UserCreatedEvent ('["user_id=61965469-c821-
46b7-825f-630e12a51d6c","username=bob@example.com"]'):
principal=91220262-d901-44c0-825f-633i33b55d6c,
origin=[client=cf, user=admin, details=(198.51.100.1,
tokenType=bearertokenValue=<TOKEN>,
sub=20i03423-dd8e-33e1-938d-e9999e30f500,
iss=https://uaa.example.com/oauth/token)], identityZoneId=[uaa]
```

* This entry records a `UserCreatedEvent`.

* The `admin` user originating at `198.51.100.1` created a user named `bob@example.com`.

#### Successful user deletion
```
Audit: UserDeletedEvent ('["user_id=61965469-c821-
46b7-825f-630e12a51d6c","username=bob@example.com"]'):
principal=61965469-c821-46b7-825f-630e12a51d6c,
origin=[client=admin, details=(remoteAddress=198.51.100.1,
tokenType=bearertokenValue=<TOKEN>,
sub=admin, iss=https://uaa.example.com/oauth/token)], identityZoneId=[uaa]
```

* This entry records a `UserDeletedEvent`.

* The `admin` user originating at `198.51.100.1` deleted a user named `bob@example.com`.

## CredHub logging
CredHub logs security events to a file located at `/var/vcap/sys/log/credhub/credhub_security_events.log` on the CredHub VM. Because these logs are rotated, you must configure a syslog drain to forward your system logs to a log management service.
For more information, see [Configuring System Logging](https://docs.cloudfoundry.org/running/managing-cf/logging-config.html) and [Using Log Management Services](https://docs.cloudfoundry.org/devguide/services/log-management.html).

### Format for Log Entries
CredHub logs security events in the [Common Event Format](https://kc.mcafee.com/resources/sites/MCAFEE/content/live/CORP_KNOWLEDGEBASE/78000/KB78712/en_US/CEF_White_Paper_20100722.pdf) (CEF). CEF specifies the following format for log entries:
```
CEF:Version|Device Vendor|Device Product|Device Version|Signature ID|Name|Severity|Extension
```
Entries in the CredHub log use the following format:
```
CEF:0|cloud_foundry|credhub|CREDHUB_SERVER_VERSION|
SIGNATURE_ID|NAME|0|rt=TIMESTAMP suser=USERNAME suid=USER_GUID
cs1Label=userAuthenticationMechanism cs1=AUTH_MECHANISM
request=REQUEST requestMethod=REQUEST_METHOD
cs3Label=versionUuid cs3=VERSION_UUID
cs4Label=httpStatusCode cs4=HTTP_STATUS_CODE src=SOURCE_ADDRESS dst=DESTINATION_ADDRESS
cs2Label=resourceName cs2=RESOURCE_NAME
cs5Label=resourceUuid cs5=RESOURCE_UUID deviceAction=OPERATION
cs6Label=requestDetails cs6=REQUEST_DETAILS
```
See the following list for a description of the properties shown in the CredHub log.

* `CEF_VERSION`: The version of CEF used in the logs.

* `CREDHUB_SERVER_VERSION`: The current CredHub server version.

* `SIGNATURE_ID`: The method and path of the request. For example, `GET /v2/app:GUID`.

* `NAME`: The same as `SIGNATURE_ID`.

* `TIMESTAMP`: The number of milliseconds since the Unix epoch.

* `USERNAME`: The name of the user who originated the request, as defined by UAA. In the case of mTLS, no-auth, or not defined, this value is empty.

* `USER_GUID`: The “actor” identifier. For example, `mtls-app:GUID`. If there is no authenticated user, this value is empty.

* `AUTH_MECHANISM (cs1)`: The user authentication mechanism. This can be `oauth-access-token`, `mtls-auth`, or `no-auth`.

* `REQUEST`: The request path and parameters. For example, `/v2/info?MY-PARAM=VALUE`.

* `REQUEST_METHOD`: The method of the request. For example, `GET`.

* `HTTP_STATUS_CODE (cs4)`. The HTTP status code of the response. For example, `200`.

* `SOURCE_ADDRESS`: The IP address of the client who originated the request.

* `DESTINATION_ADDRESS`: The IP address of the CredHub VM.

* `RESOURCE_NAME (cs2)`: The credential path name. For example, `/my/awesome/credential`.

* `RESOURCE_UUID (cs5)`: The top-level credential UUID. This is not the credential version.

* `VERSION_UUID (cs3)`: The credential version UUID.

* `OPERATION (deviceAction)`: The device action. The possible operations include the following:

+ `get`

+ `set`

+ `generate`

+ `regenerate`

+ `bulk-regenerate`

+ `delete`

+ `find`

+ `get-permissions`

+ `add-permission`

+ `delete-permission`

+ `interpolate`

+ `info`

+ `version`

+ `health`

+ `key-usage`

+ `update-transitional-version`

* `REQUEST_DETAILS (cs6)`: A JSON blob that differs per request.
The CredHub logs include descriptions for each custom label. For example, the
logs include `cs2Label=resourceName` to define the `cs2` label. The value
for `resourceName` appears in the log next to `cs2=/path/to/credential`.

### Example Log Entries
The following sections provide several example requests with the corresponding CredHub log entries.

#### Accessing a credential
```
CEF:0|cloud_foundry|credhub|2.0.0-beta.28|GET /api/v1/data|
GET /api/v1/data|0|rt=1530901816757
suser=app:3c538393-d192-4e23-8c83-456654b3fa6c
suid=mtls-app:3c538393-d192-4e23-8c83-456654b3fa6c
cs1Label=userAuthenticationMechanism
cs1=mutual_tls request=/api/v1/data?path=0b353167-0d5a-48c7-5036-7eaa
requestMethod=GET
cs3Label=versionUuid cs3=null
cs4Label=httpStatusCode cs4=200 src=10.0.0.1 dst=credhub.service.cf.internal
cs2Label=resourceName cs2=null
cs5Label=resourceUuid cs5=null deviceAction=FIND
cs6Label=requestDetails
cs6={"nameLike":null,"path":"0b353167-0d5a-48c7-5036-7eaa","paths":null}
```

* A user authenticated to the CredHub instance using `mutual_tls` from `10.0.0.1`.

* The authenticated user accessed a CredHub credential.

#### Setting a credential
```
CEF:0|cloud_foundry|credhub|2.0.0-beta.28|PUT /api/v1/data|
PUT /api/v1/data|0|rt=1530901097921
suser=cc_service_key_client suid=uaa-client:cc_service_key_client
cs1Label=userAuthenticationMechanism
cs1=uaa request=/api/v1/data requestMethod=PUT
cs3Label=versionUuid cs3=32b3d5bf-463a-4045-a6b5-65c97e61059a
cs4Label=httpStatusCode cs4=200 src=10.0.0.1 dst=credhub.service.cf.internal
cs2Label=resourceName cs2=/1530901097842989110
cs5Label=resourceUuid cs5=ccda25c5-a40a-4512-b6f5-a42f8c3b5c4c deviceAction=SET
cs6Label=requestDetails
cs6={"name":"/1530901097842989110","type":"json","mode":null,
"additionalPermissions":[{"actor":"uaa-client:cc_service_key_client",
"allowedOperations":["READ","WRITE","DELETE","WRITE_ACL","READ_ACL"]}]}
```

* A user authenticated to the CredHub instance with UAA from `10.0.0.1`.

* The authenticated user set a CredHub credential.

#### Generating a credential
```
CEF:0|cloud_foundry|credhub|2.0.0-beta.28|POST /api/v1/data|
POST /api/v1/data|0|rt=1530901403532
suser=app:3c538393-d192-4e23-8c83-456654b3fa6c
suid=mtls-app:3c538393-d192-4e23-8c83-456654b3fa6c
cs1Label=userAuthenticationMechanism
cs1=mutual_tls request=/api/v1/data requestMethod=POST
cs3Label=versionUuid cs3=8c21b7b3-d4bf-4d8a-a0c5-64c8c207cb40
cs4Label=httpStatusCode cs4=200 src=10.0.0.1 dst=credhub.service.cf.internal
cs2Label=resourceName cs2=/0b353167-0d5a-48c7-5036-7eaa/2
cs5Label=resourceUuid cs5=1d55cff3-5264-434c-a127-0810f341cb2b deviceAction=GENERATE
cs6Label=requestDetails cs6={"name":"/my/awesome/credential","type":"password",
"mode":null,"additionalPermissions":[{"actor":"mtls-app:3c538393-d192-4e23-8c83-456654b3fa6c",
"allowedOperations":["READ","WRITE","DELETE","WRITE_ACL","READ_ACL"]}]}
```

* A user authenticated to the CredHub instance using `mutual_tls` from `10.0.0.1`.

* The authenticated user generated a password credential named `/my/awesome/credential`.