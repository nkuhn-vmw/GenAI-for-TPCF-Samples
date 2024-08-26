# Available Cloud Controller API client libraries
Here is a list of the client libraries you can use with the Cloud Foundry API (CAPI)
.

## CAPI overview
CAPI is the entry point for most operations within the Cloud Foundry
platform. You can use it to manage orgs, spaces, and apps, which includes user roles and permissions. You can also use CAPI to manage the services provided by your Cloud Foundry deployment, including provisioning, creating, and binding them to apps.

## Client libraries
While you can develop apps that use CAPI by calling it directly as in the API documentation, you might want to use an existing client library. See the following available client libraries.

### Supported
Cloud Foundry supports the following clients for CAPI:

* [Java](https://github.com/cloudfoundry/cf-java-client)

* [Scripting](http://cli.cloudfoundry.org/en-US/cf/curl.html) with the Cloud Foundry Command Line Interface (cf CLI)

### Experimental
The following client is experimental and is a work in progress:

* [Golang](https://godoc.org/github.com/cloudfoundry/cli/api/cloudcontroller)

### Unofficial
Cloud Foundry does not support the following clients, but might be supported by third parties:

* Golang:

+ [cloudfoundry-community/go-cfclient](https://github.com/cloudfoundry-community/go-cfclient)

* Python:

+ [cloudfoundry-community/cf-python-client](https://github.com/cloudfoundry-community/cf-python-client)

+ [hsdp/python-cf-api](https://github.com/hsdp/python-cf-api)