# Configuring SSH access for Cloud Foundry
This topic describes how to configure your Cloud Foundry deployment to allow SSH access to application instances, and includes details about load balancing SSH sessions.

## Cloud Foundry configuration
To enable SSH access to apps running on Diego, you must configure the properties in your deployment manifests by following the steps below.
To configure manifest properties, you can edit them directly or put them in stub files with [merge tags](https://github.com/cloudfoundry-incubator/spiff#-merge-) that you pass to `generate_deployment_manifest` or another spiff-based manifest-generation script.

### Generate a key pair
Enabling SSH access requires generating a RSA key pair for your SSH proxy. Generate a unique key pair for each deployment.
In recent versions of `cf-deployment`, this key pair is automatically generated and stored in `credhub`.

1. Generate your key pair, entering an empty string for the passphrase when prompted.
```
$ ssh-keygen -f ssh-proxy-host-key.pem
$ ssh-keygen -lf ssh-proxy-host-key.pem.pub | cut -d ' ' -f2 > ssh-proxy-host-key-fingerprint
```

**Note**
ssh-keygen print the SHA256 fingerprint hashes of the keys. To obtain MD5 hashes of the server key fingerprints, use the `-E` option to specify the hash algorithm.
```
$ ssh-keygen -f ssh-proxy-host-key.pem
$ ssh-keygen -E md5 -lf ssh-proxy-host-key.pem.pub | sed 's/MD5://' | cut -d ' ' -f2 > ssh-proxy-host-key-fingerprint
```

1. Locate your PEM-encoded private key in `ssh-proxy-host-key.pem` and your public key fingerprint in `ssh-proxy-host-key-fingerprint`. You will need to copy the contents of these files into your Cloud Foundry and Diego manifests.

### Configure your Cloud Foundry manifest
Your manifest for Cloud Foundry should include the following properties:
```
properties:
app_ssh:
host_key_fingerprint: HOST-KEY-FINGERPRINT
oauth_client_id: ssh-proxy
cc:
allow_app_ssh_access: true
default_app_ssh_access: SSH-ACCESS-FOR-NEW-APPS
uaa:
clients:
ssh-proxy:
authorized-grant-types: authorization_code
autoapprove: true
override: true
redirect-uri: /login
scope: openid,cloud_controller.read,cloud_controller.write,cloud_controller.admin
secret: SSH-PROXY-SECRET
```

1. Change `HOST-KEY-FINGERPRINT` to the public key fingerprint of the RSA key pair that you generated. It should be located in your `ssh-proxy-host-key-fingerprint` file.

2. Replace `SSH-ACCESS-FOR-NEW-APPS` with `true` to enable SSH access for new apps by default in spaces that allow SSH. If you set this property to `false`, developers can still enable SSH after pushing their apps by running `cf enable-ssh APP-NAME`. If an app is already deployed and running, the developer must restart the app before being able to SSH into it.

3. For `SSH-PROXY-SECRET`, provide a client secret that Diego will use to register the `ssh-proxy` client with your User Account and Authentication (UAA) server.

### Configure your Diego manifest
Your manifest for Diego should include the following properties:
```
properties:
ssh_proxy:
host_key: |

-----BEGIN EXAMPLE RSA PRIVATE KEY-----
YOUR-PRIVATE-KEY

-----END EXAMPLE RSA PRIVATE KEY-----
enable_cf_auth: true
enable_diego_auth: false
diego_credentials: ""
uaa_secret: SSH-PROXY-SECRET
```

1. `ssh_proxy.host_key`: Supply the PEM-encoded private key from the RSA key pair that you originally generated for your deployment. This key secures the SSH proxy that brokers connections to individual app containers.

2. Specify CF Authentication only by setting `enable_cf_auth` to `true` and `enable_diego_auth` to `false`, as in the example above.

3. For `SSH-PROXY-SECRET`, enter the same secret you provided in the `ssh-proxy.secret` field in your Cloud Foundry manifest.

## SSH load balancer configuration

### Using HAProxy
If you are using the HAProxy job as the Gorouter load balancer and you set the `cc.allow_app_ssh_access` property in your Cloud Foundry manifest to `true`, HAProxy serves as the load balancer for Diego’s SSH proxies. Use this configuration for deployments where all traffic on the system domain and its subdomains is directed towards the HAProxy job, as is the case for a BOSH-Lite Cloud Foundry deployment on the default `bosh-lite.com` domain.

### Using Elastic load balancers on AWS
For Amazon Web Services (AWS) deployments, where the infrastructure offers load-balancing as a service through Elastic Load Balancers (ELBs), the deployment operator can provision an ELB to load balance across the Diego SSH proxy instances. This ELB should be configured to listen to TCP traffic on the port given by the `app_ssh.port` property in the Cloud Foundry manifest and to send it to port `2222`.
In the Diego manifest, register the SSH proxies with your ELBs by editing the `cloud_properties` values.

* If you used the spiff-based manifest-generation templates to produce the Diego manifest, the `cloud_properties` hashes should be specified in the `iaas_settings.resource_pool_cloud_properties` section of the `iaas-settings.yml` stub.

* Otherwise, add the ELB identifier to the `elbs` property in the `cloud_properties` hash of the Diego manifest `access_zN` resource pools. For example:
```
resource_pools:

- cloud_properties:
elbs:

- test-SSHProxyEL-16O57T64U5UAL
name: access_z1
network: diego1

- cloud_properties:
elbs:

- test-SSHProxyEL-16O57T64U5UAL
name: access_z2
network: diego2

- cloud_properties:
elbs:

- test-SSHProxyEL-16O57T64U5UAL
name: access_z3
network: diego3
```

## Deactivate SSH
If you want to deactivate SSH access for a deployment:

1. Set the `cc.allow_app_ssh_access` property in your Cloud Foundry manifest to `false`.

2. Redeploy Cloud Foundry.
If you want to reset your deployment to remove all SSH proxy configuration:

1. Set the `cc.allow_app_ssh_access` property in your Cloud Foundry manifest to `false`.

2. Delete the `ssh-proxy` properties within `uaa.clients` in your Cloud Foundry manifest.

3. Redeploy Cloud Foundry.

4. Install the UAA Command Line Interface (UAAC).
```
$ gem install cf-uaac
```

5. Target your UAA server.
```
$ uaac target uaa.YOUR-SYSTEM-DOMAIN
```

6. Authenticate and retrieve your admin client token. When prompted with `Client secret`, enter your admin credentials.
```
$ uaac token client get admin
Client secret: ********************
Successfully fetched token via client credentials grant.
Target: https://uaa.YOUR-SYSTEM-DOMAIN
Context: admin, from client admin
```

7. Delete your `ssh-proxy` client.
```
$ uaac token client delete ssh-proxy
```

## Troubleshooting
If you receive an error message attempting to SSH into an app container, see the following list to help troubleshoot the issue.
| **Error** | **Reason** |
| --- | --- |
| `Error getting one time auth code` | Check that you have the `ssh-proxy` client registered with your UAA server. |
| `Error getting one time auth code` | Review the `uaa_secret` field in your Diego manifest and ensure that it matches the `Client secret` for the `ssh-proxy` client registered with your UAA server. |
| `Error opening SSH connection` | Verify that `enable_cf_auth` in your Diego manifest is set to `true`. |
| `Error opening SSH connection` | Check that you provided the correct private key in your Diego manifest. |
| `Server error, status code: 404` | Ensure that the `oath_client_id` in your Cloud Foundry manifest matches the client ID of the SSH proxy client you registered with your UAA server. The default client ID is `ssh-proxy`. |