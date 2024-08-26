# Binding credentials
A bindable service returns credentials that an application can consume in response to the `cf bind` API call.
Cloud Foundry writes these credentials to the
[`VCAP_SERVICES`](https://docs.cloudfoundry.org/devguide/deploy-apps/environment-variable.html#VCAP-SERVICES) environment variable.
In some cases, buildpacks can write a subset of these credentials to other
environment variables that frameworks might need.
Choose from the following list of credential fields if possible, though you can provide additional fields as
needed.
Refer to the
[Using Bound Services](https://docs.cloudfoundry.org/devguide/services/managing-services.html#use)
section of the *Managing Service Instances with the CLI* topic for information about how these
credentials are consumed.
If you provide a service that supports a connection string, provide the `uri` key for
buildpacks and application libraries to use.
| **Credentials** | **Description** |
| --- | --- |
| uri | Connection string of the form `DB-TYPE://USERNAME:PASSWORD@HOSTNAME:PORT/NAME`,
where `DB-TYPE` is a type of database such as mysql, postgres, mongodb, or amqp. |
| hostname | FQDN of the server host |
| port | Port of the server host |
| name | Name of the service instance |
| vhost | Name of the messaging server virtual host - a replacement for a `name` specific to AMQP providers |
| username | Server user |
| password | Server password |
The following is an example output of `ENV['VCAP_SERVICES']`.
Depending on the types of databases you are using, each database might return different
credentials.
```
VCAP_SERVICES=
{
cleardb: [
{
name: "cleardb-1",
label: "cleardb",
plan: "spark",
credentials: {
name: "ad_c6f4446532610ab",
hostname: "us-cdbr-east-03.cleardb.com",
port: "3306",
username: "b5d435f40dd2b2",
password: "ebfc00ac",
uri: "mysql://b5d435f40dd2b2:ebfc00ac@us-cdbr-east-03.cleardb.com:3306/ad_c6f4446532610ab",
jdbcUrl: "jdbc:mysql://b5d435f40dd2b2:ebfc00ac@us-cdbr-east-03.cleardb.com:3306/ad_c6f4446532610ab"
}
}
],
cloudamqp: [
{
name: "cloudamqp-6",
label: "cloudamqp",
plan: "lemur",
credentials: {
uri: "amqp://ksvyjmiv:IwN6dCdZmeQD4O0ZPKpu1YOaLx1he8wo@lemur.cloudamqp.com/ksvyjmiv"
}
}
{
name: "cloudamqp-9dbc6",
label: "cloudamqp",
plan: "lemur",
credentials: {
uri: "amqp://vhuklnxa:9lNFxpTuJsAdTts98vQIdKHW3MojyMyV@lemur.cloudamqp.com/vhuklnxa"
}
}
],
rediscloud: [
{
name: "rediscloud-1",
label: "rediscloud",
plan: "20mb",
credentials: {
port: "6379",
host: "pub-redis-6379.us-east-1-2.3.ec2.redislabs.com",
password: "1M5zd3QfWi9nUyya"
}
},
],
}
```