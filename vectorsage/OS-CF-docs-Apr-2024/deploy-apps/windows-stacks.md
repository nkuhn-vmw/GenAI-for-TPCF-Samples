# Restaging your apps on a Windows stack
This topic explains how you can restage apps on a new Windows stack. It also describes what stacks are and lists the supported Windows stacks on Cloud Foundry v4-0.
To restage a Windows app on a new Linux stack, see [Changing stacks](https://docs.cloudfoundry.org/devguide/deploy-apps/stacks.html).
You can also use the Stack Auditor plug-in for the Cloud Foundry Command Line Interface (cf CLI) when changing stacks. See [Using the Stack Auditor plug-in](https://docs.cloudfoundry.org/adminguide/stack-auditor.html).

## Overview
A stack is a prebuilt root file system (rootfs) that supports a specific operating system. For example, Linux-based systems need `/usr` and `/bin` directories at their root and Windows needs `/windows`. The stack works in tandem with a buildpack to support apps running in compartments. Under Diego architecture, cell VMs can support multiple stacks.

**Note**
Docker apps do not use stacks.

## Available stacks
If you push your CF v4-0 app to a Windows stack, you must use `windows`.
The `windows2016` stack is not supported on CF.

## Restaging apps on a new stack
For security, stacks receive regular updates to address Common Vulnerabilities and Exposures ([CVEs](http://www.ubuntu.com/usn/)). Apps pick up on these stack changes through new releases of CF. However, if your app links statically to a library provided in the rootfs, you have to manually restage it to pick up the changes.
It can be difficult to know what libraries an app statically links to, and it depends on the languages you are using. One example is an app that uses a Ruby or Python binary, and links out to part of the C standard library. If the C library requires an update, you might need to recompile the app and restage it.
To restage an app on a new stack:

1. Use the `cf stacks` command to list the stacks available in a deployment.
```
$ cf stacks
Getting stacks in org MY-ORG / space development as developer@example.com...
OK
name description
windows2016 Windows Server 2016
windows Windows Server
```

2. To change your stack and restage your app, run:
```
cf push MY-APP -s STACK-NAME
```
Where:

* MY-APP is the name of the app.

* STACK-NAME is the name of the new stack.For example, to restage your app on the `windows` stack, run `cf push MY-APP -s windows`:
```
$ cf push MY-APP -s windows
Using stack windows...
OK
Creating app MY-APP in org MY-ORG / space development as developer@example.com...
OK
...
requested state: started
instances: 1/1
usage: 1G x 1 instances
urls: MY-APP.cfapps.io
last uploaded: Wed Apr 8 23:40:57 UTC 2015
state since cpu memory disk

#0 running 2015-04-08 04:41:54 PM 0.0% 57.3M of 1G 128.8M of 1G
```

## Stacks API
For API information, see the “Stacks” section of the [Cloud Foundry API documentation](http://apidocs.cloudfoundry.org).