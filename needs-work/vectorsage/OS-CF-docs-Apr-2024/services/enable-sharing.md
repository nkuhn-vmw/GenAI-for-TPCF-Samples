# Service Instance sharing
You can allow instances of your services to be shared across spaces and orgs within Cloud Foundry.
This allows apps running in different spaces and orgs to use the same service instance.
If you have Space Developer permissions in the space where the service instance was created, you are responsible
for sharing, unsharing, updating, and deleting the service instance.
For more information about the developer and administrator tasks related to service instance sharing, see
[Sharing Service Instances](https://docs.cloudfoundry.org/devguide/services/sharing-instances.html).

## Enabling service instance sharing
Service brokers must explicitly activate service instance sharing by setting a flag in their service-level
metadata object.
This allows service instances, of any service plan, to be shared across orgs and spaces.
The `"shareable"` flag must be set to `true` in the service-level metadata to activate service
instance sharing. If the flag is set to `false` or is absent, sharing is deactivated.
An example catalog:
```
{
"services":[{
"id":"766fa866-a950-4b12-adff-c11fa4cf8fdc",
"name": "example-service",
"metadata": {
"shareable": true
}
}]
}
```

## Binding permissions based on instance sharing
When a service instance is created in one space and shared into another, you can bind your apps to the
service instance from both spaces.
You might want to have the service broker return credentials with different permissions depending on
which space an app is bound from.
For example, a messaging service can permit writes from the originating space and only reads
from any spaces that the service is shared into.
To determine whether the space of the app is the same as the originating space of the service instance,
the service broker can compare the `context.space_guid` and `bind_resource.space_guid` fields in the binding request.
The `context.space_guid` field represents the space where the service instance was created,
and `bind_resource.space_guid` represents the space of the app involved in the binding.

## Security considerations
You must consider the following before enabling service instance sharing:

* [Service keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html)
can only be generated if you have access to the space where the service instance was created.
This verifies that only developers with access to this space have visibility
into where and how many times the service instance is used. It is not possible
to distinguish between service keys created when targeting the originating space
and those created when targeting the space where the instance has been shared to.
Also, unsharing an instance from a space does not delete any service keys.

* Consider the impact of giving out excessive permissions for service bindings,
especially bindings that originate from spaces that the service instance has
been shared into. For example, a messaging service can permit writes from the
originating space and only reads from any shared spaces.
For more information,
see [Binding Permissions Based on Instance Sharing](https://docs.cloudfoundry.org/services/enable-sharing.html#binding-permissions).

* You can generate unique credentials for each binding. This makes sure that
developers can unshare a service instance at any time. Unsharing an instance
deletes any service bindings and revokes access for those credentials.
Unsharing an instance prevents unauthorized
future access from developers and apps that saved the credentials that they were
previously provided using the service binding.

* Consider the impact of a service instance dashboard being accessed by users
of shared service instances. If authenticating through SSO,
see [Dashboard Single Sign-On](https://docs.cloudfoundry.org/services/dashboard-sso.html).