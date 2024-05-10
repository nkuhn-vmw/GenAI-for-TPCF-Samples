# Using a proxy server with Cloud Foundry buildpacks
You can use a proxy server with buildpacks for your application.

## Using a proxy server
You can assign proxy servers to environment variables. Proxy servers can be used to monitor your application’s traffic or to fetch your application’s dependencies.
A buildpack uses a proxy server if that buildpack contacts the internet during staging.
The binary buildpack does not use a proxy server because it does not access the internet during staging.

## Setting environment variables
If you are using a Java buildpack, the `http_proxy` and `https_proxy` environment variables are not supported at runtime. The Java buildpack does not add the functionality to make proxies work at runtime.
To set your environment variables:

1. Add the following to the `env` block of your application manifest YAML file:
```

---
env:
http\_proxy: http://YOUR-HTTP-PROXY:PORT
https\_proxy: https://YOUR-HTTPS-PROXY:PORT
```
Where:

* `YOUR-HTTP-PROXY` is the address of your proxy server for HTTP requests.

* `YOUR-HTTPS-PROXY` is the address of your proxy server for HTTPS requests.

* `PORT` is the port number you are using for your proxy server.

2. Set the environment variables with the Cloud Foundry Command Line Interface (cf CLI) `cf set-env` command:
```
cf set-env YOUR-APP http_proxy "http://YOUR-HTTP-PROXY:PORT"
```
```
cf set-env YOUR-APP https_proxy "https://YOUR-HTTPS-PROXY:PORT"
```
Where:

* `YOUR-APP` is the name of your application.

* `YOUR-HTTP-PROXY` is the address of your proxy server for HTTP requests.

* `YOUR-HTTPS-PROXY` is the address of your proxy server for HTTPS requests.

* `PORT` is the port number you are using for your proxy server.

## Un-setting environment variables
Removing an environment variable from the application manifest YAML file is not sufficient to unset the environment variable.
You must also unset the environment variables with the Cloud Foundry Command Line Interface (cf CLI) `cf unset-env` command:
```
cf unset-env YOUR-APP ENV_VAR_NAME
```
For example:
```
cf unset-env YOUR-APP https_proxy
```
Where:

* `YOUR-APP` is the name of your application.

* `ENV_VAR_NAME` is the name of the environment variable.