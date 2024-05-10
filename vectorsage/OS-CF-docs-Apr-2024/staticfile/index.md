# Staticfile buildpack
You can configure and use the Staticfile buildpack in Cloud Foundry.

**Staticfile app**: An app or content that requires no backend code other than the
NGINX webserver, which the buildpack provides.
Examples of staticfile apps are front-end JavaScript apps, static HTML content, and HTML/JavaScript forms.

**Staticfile buildpack**: The buildpack that provides runtime support for staticfile apps and apps with back ends hosted elsewhere.
To find which version of NGINX the current Staticfile buildpack uses, see [Staticfile buildpack release notes](https://github.com/cloudfoundry/staticfile-buildpack/releases).

## Staticfile detection
If you create a file named `Staticfile` and locate it in the build directory of your app, Cloud Foundry automatically uses
the Staticfile buildpack when you push your app.
The `Staticfile` file can be an empty file, or it can contain configuration settings for your app.
For more information, see [Configuring the buildpack](https://docs.cloudfoundry.org/buildpacks/staticfile/index.html#configure) and [Pushing an App](https://docs.cloudfoundry.org/buildpacks/staticfile/index.html#push_app).

## Memory usage
NGINX requires 20 MB of RAM to serve static assets. When using the Staticfile buildpack, Cloud Foundry push the apps with the `-m 64M` option to reduce RAM allocation from the default 1 GB that are allocated to containers by default.

## Configure the buildpack
This section describes configuration options that are available for the Staticfile buildpack.
If you need to make configuration changes to NGINX that are not listed in the table, use the NGINX buildpack instead of the Staticfile buildpack. For more information, see [NGINX buildpack](https://docs.cloudfoundry.org/buildpacks/nginx/).

### Staticfile file configuration
To configure these options, add the configuration property as a new line in your `Staticfile` file as described in the following table:
| Staticfile configuration property | Description |
| --- | --- |
| `root: YOUR-DIRECTORY-NAME`
Example:
`root: public` | **Alternative root**: Specifies a root directory other than the default. Use this option to serve `index.html` and other assets, such as HTML, CSS, or JavaScript files, from a location other than the root directory.
For example, you can specify an alternate folder, `dist` or
`public`.
|
| `directory: visible` | **Directory list**: Displays an HTML page that shows a directory index for your site.
If your site is missing an `index.html` file, your app displays a directory list instead of the standard 404 error page.
|
| `ssi: enabled` | **SSI**: Activates Server Side Includes (SSI). You can embed the contents of one or more files into a web page on a web server. For general information about SSI, see [Server Side Includes](https://en.wikipedia.org/wiki/Server_Side_Includes) entry on Wikipedia.
|
| `pushstate: enabled` | **Pushstate routing**: Keeps browser-visible URLs clean for client-side JavaScript apps that serve multiple routes. For example, pushState routing allows a single JavaScript file to route to multiple anchor tagged URLs that look like `/some/path1` instead of `/some#path1`.
|
| `gzip: off` | **GZip file serving and compression**: Deactivate [gzip\_static](http://nginx.org/en/docs/http/ngx_http_gzip_static_module.html) and [gunzip](http://nginx.org/en/docs/http/ngx_http_gunzip_module.html) modules are activated by default. With these modules you can use NGINX to serve files stored in compressed GZ format and to decompress them for clients that do not support compressed content or responses.
You might want to deactivate compression under certain circumstances. For example,when you serve content to very old browser clients.
|
| `http_proxy: HTTP-URL`
`https_proxy: HTTPS-URL`
Example:
`http_proxy: http://www.example.com/`
`https_proxy: https://www.example.com/` | **Proxy support**: You can use a proxy when downloading dependencies during the staging of your app. |
| `enable_http2: true`
Alternatively, set the `ENABLE_HTTP2` environment variable to `true`.
| **Enable HTTP/2**: Serve requests over HTTP/2 instead of HTTP/1.1. This deactivates serving HTTP/1.1 traffic. |
| `force_https: true`
Alternatively, you can set the `FORCE_HTTPS` environment variable to `true`.
| **Force HTTPS**: Forces all requests to be sent through HTTPS. This redirects non-HTTPS requests as HTTPS requests.

**Note**Do not activate `FORCE_HTTPS` if you have a proxy server or load balancer loops. For example, if you use [Flexible SSL](https://support.cloudflare.com/hc/en-us/articles/200170416) with CloudFlare. |
| `host_dot_files: true` | **Dot files**: By default, hidden files, which start with a `.`, are not served by this buildpack. |
| `status_codes:`
`404: /404.html`
`500: /500.html` | **Status Codes**: You can define custom pages for HTTP STATUS codes instead of the default NGINX pages. |
| `http_strict_transport_security: true` | **HTTP Strict Transport Security (HSTS)**: Causes NGINX to respond to all requests with the header `Strict-Transport-Security: max-age=31536000`. This forces receiving browsers to make all subsequent requests over HTTPS. This setting defaults to a `max-age` of one year.

**Important**This setting persists in browsers for a long time, so you must enable this setting only *after* you ensure that you have completed your app configuration. |
| `http_strict_transport_security_include_subdomains: true` | **HSTS includes subdomains**: Causes NGINX to respond to all requests with the following header: `Strict-Transport-Security: max-age=31536000; includeSubDomains` This forces browsers to make all subsequent requests over HTTPS including subdomains. This setting defaults to a `max-age` of one year.

**Important**Setting this property to `true` also makes `http_strict_transport_security` default to true. |
| `http_strict_transport_security_preload: true` | **HSTS preload**: Causes NGINX to respond to all requests with the following
header: `Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`
This forces browsers to make all subsequent requests over HTTPS including subdomains and requests inclusion in browser-managed HSTS preload lists. For more information, see <https://hstspreload.org>. This setting defaults to a `max-age` of one year.

**Important**Setting this property to `true` also makes `http_strict_transport_security` and `http_strict_transport_security_include_subdomains` default to true. |

### Other configuration changes
Use the following instructions to make other configuration changes.

---

#### Basic authentication
You can enable basic authentication for your app or website.
You can create a hashed username and password pair for each user by using a site like [Htpasswd Generator](http://www.htaccesstools.com/htpasswd-generator/).

**Configuration**
Add a new `Staticfile.auth` file to the root or alternative root directory. In the new file, add one or more username and password entries using the following format: `USERNAME:HASHED_PASSWORD`
Example:
```
pat:$example1$DuUQEQp8$ZccZCHQElNSjrgerwSFC0
stevie:$example1$22derfaecZSJJRw4rKE$KKEWKSK
```

---

#### Custom location
You can specify custom location definitions with additional directives. For information about NGINX directives, see [Creating NGINX Plus and NGINX Configuration Files](https://docs.nginx.com/nginx/admin-guide/basic-functionality/managing-configuration-files) and [Alphabetical index of directives](https://nginx.org/en/docs/dirindex.html) in the *NGINX documentation*.

**Configuration**
To customize the `location` block of the NGINX configuration file:

1. Set an alternative `root` directory. The `location_include` property only works in conjunction with an alternative `root`. See the following example that includes a static content file:

* **Directory**: `public`

* **File**: `public/index.html`

2. Create a file with location-scoped NGINX directives. See the following example, which causes visitors of your site to receive the `X-MySiteName` HTTP header:

* **File**: `nginx/conf/includes/custom_header.conf`

* **Content**: `add_header X-MySiteName BestSiteEver;`

3. Set the `location_include` variable in your **Staticfile** to the path of the file from the previous step. This path is relative to `nginx/conf`.
Example:
```
...
root: public
location_include: includes/*.conf
...
```

---

#### Additional MIME type support
You can configure additional MIME types on your NGINX server.

**Configuration**
To add MIME types, add a `mime.types` file to your root folder, or to the alternate root folder, if you specified one.
For more information about the `mime.types` file, see [mime.types](https://www.nginx.com/resources/wiki/start/topics/examples/full/#mime-types") in the *NGINX documentation*.
Example MIME types file:
```
types {
text/html html htm shtml;
text/css css;
text/xml xml rss;
image/gif gif;
...
}
```

---

## Push an app
To push your app, you can use either the system Staticfile buildpack or specify a Staticfile buildpack.

### Option 1: Use the system Staticfile buildpack
To use the Staticfile buildpack installed in your deployment, run the following command in the root directory of the app.
The root directory of the app must contain a file named `Staticfile`.
```
cf push APP-NAME
```
Where `APP-NAME` is the name you want to give your app.

### Option 2: Specify a Staticfile buildpack
To explicitly specify a Staticfile buildpack, run the following command in the root directory of the app. You might want to specify a buildpack if your deployment does not have the Staticfile buildpack installed or the installed version is outdated.
```
cf push APP-NAME -b BUILDPACK-NAME-OR-PATH
```
Where:

* `APP-NAME` is the name you want to give your app.

* `BUILDPACK-NAME-OR-PATH` is either the name of a buildpack that is installed in your deployment or the path to a buildpack. You can find the Cloud Foundry Staticfile buildpack in the [Staticfile repository](https://github.com/cloudfoundry/staticfile-buildpack.git) on GitHub.

### Verifying the push
After you push the app, follow these steps to verify that the push was successful:

1. Find the URL of your app in the output of the `cf push` command. For example, the URL in the terminal output above is `my-app.example.com`.

2. In a browser, go to the URL to view your app.

## Example Staticfile buildpack apps
For different examples of apps that use the Staticfile buildpack, see the [fixtures](https://github.com/cloudfoundry/staticfile-buildpack/tree/master/fixtures) directory in the Staticfile buildpack GitHub repo.

## Help and support
A number of channels exist where you can get more help when using the Staticfile buildpack, or with developing your own Staticfile buildpack.

* **Staticfile Buildpack Repository in GitHub**: Find more information about using and extending the Staticfile buildpack in [GitHub repository](https://github.com/cloudfoundry/staticfile-buildpack).

* **Release Notes**: Find current information about this buildpack on the Staticfile buildpack [release page](https://github.com/cloudfoundry/staticfile-buildpack/releases) in GitHub.

* **Slack**: Join the #buildpacks channel in the [Cloud Foundry Slack community](http://slack.cloudfoundry.org/).