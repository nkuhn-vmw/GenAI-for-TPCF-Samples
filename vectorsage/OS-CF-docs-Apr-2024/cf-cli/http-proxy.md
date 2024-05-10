# Using the cf CLI with a proxy server
If you have an HTTP or SOCKS5 proxy server on your network between a host running the cf CLI and your API endpoint, you must set `https_proxy` with the hostname or IP address of the proxy server. The `https_proxy` environment variable holds the hostname or IP address of your proxy server.
The `https_proxy` is a standard environment variable. As with any environment variable, the specific steps you use to set it depends on your operating system.

## Format of https\_proxy
The `https_proxy` variable is set with hostname or IP address of the proxy server in URL format, as in the following example:
```
https_proxy=http://proxy.example.com
```
If the proxy server requires a username and password, you must include the credentials, as in the following example:
```
https_proxy=http://username:password@proxy.example.com
```
If the proxy server uses a port other than 80, you must include the port number, as in the following example:
```
https_proxy=http://username:password@proxy.example.com:8080
```
If the proxy server is a SOCKS5 proxy, you must specify the SOCKS5 protocol in the URL, as in the following example:
```
https_proxy=socks5://socks_proxy.example.com
```
The `cf ssh` command for cf CLI v7 does not work through a SOCKS5 proxy.

## Set https\_proxy in Mac OS or Linux
To set the `https_proxy` environment variable in Mac OS or Linux:

1. Use the command specific to your shell. For example, in bash, use the `export` command, as in the following example:
```
export https_proxy=http://my.proxyserver.com:8080
```

2. To make this change persistent, add the command to the appropriate profile file for the shell. For example, in bash, add a
line like the following example to your `.bash_profile` or `.bashrc` file:
```
https_proxy=http://username:password@hostname:port
export $https_proxy
```

## Set https\_proxy in Windows
To set the `https_proxy` environment variable in Windows:

1. Open the **Start** menu.

2. Right-click **Computer** and select **Properties**.
![An arrow points to 'Properties' as the last item of the right-click menu.](https://docs.cloudfoundry.org/cf-cli/images/properties.png)

3. In the left pane of the **System** window, click **Advanced system settings**.
![An arrow points to'Advanced system settings', which is the last item in the Control Panel Home.](https://docs.cloudfoundry.org/cf-cli/images/adv-settings.png)

4. In the **System Properties** window:

1. Select **Advanced**.

2. Click **Environment Variables**.![An arrow points to'Advanced system settings', which is the last item in the Control Panel Home.](https://docs.cloudfoundry.org/cf-cli/images/env-var.png)

5. Under **User variables**, click **New**.
![An arrow points to the 'New' button, which is the first button under the user variables table](https://docs.cloudfoundry.org/cf-cli/images/new.png)

6. For **Variable name**, enter `https_proxy`.

7. For **Variable value**, enter your proxy server information.
![Variable name text field has 'https_proxy' entered. Variable value text field has 'http://my.proxyserver.com:8080 entered.](https://docs.cloudfoundry.org/cf-cli/images/proxy.png)

8. Click **OK**.