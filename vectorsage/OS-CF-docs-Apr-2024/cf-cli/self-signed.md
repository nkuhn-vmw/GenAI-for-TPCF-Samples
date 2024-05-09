# Using the cf CLI with a self-signed certificate
This topic describes how developers use the Cloud Foundry Command Line Interface (cf CLI)
to communicate securely with a Cloud Foundry deployment with a self-signed certificate.
You can use the cf CLI to communicate securely with a Cloud Foundry deployment without
specifying `--skip-ssl-validation` under the following conditions:

* The deployment uses a self-signed certificate.

* The deployment uses a certificate that is signed by a self-signed certificate authority (CA), or a certificate signed by a certificate that is signed by a self-signed CA.
Before following the procedure below, the developer must obtain either the self-signed certificate or the intermediate and CA certificates used to sign the deployment’s certificate. The developer can obtain these certificates from the Cloud Foundry operator or from the deployment manifest. For more information about how to retrieve certificates from the deployment manifest, see [Securing Traffic into Cloud Foundry](https://docs.cloudfoundry.org/adminguide/securing-traffic.html).

## Installing the certificate on physical machines
The certificates you must insert into your local trust store vary depending on the configuration of your deployment:

* If the deployment uses a self-signed certificate, you must insert the self-signed certificate into your local trust store.

* If the deployment uses a certificate that is signed by a self-signed CA, or a certificate signed by a certificate that is signed by a self-signed CA, you must insert the self-signed certificate and any intermediate certificates into your local trust store.

### Installing the Certificate on Mac OS X
To place the certificate file `server.crt` into your local trust store for Mac OS X:

1. Run:
```
sudo security add-trusted-cert -d -r trustRoot -k /Library/Keychains/System.keychain server.crt
```

### Installing the certificate on Linux
To place the certificate file `server.crt` into your trust store for Linux:

1. Run one of the following commands, depending on your Linux distribution:

* For Debian, Ubuntu, or Gentoo, run:
```
cat server.crt >> /etc/ssl/certs/ca-certificates.crt
```

* For Fedora or RHEL, run:
```
cat server.crt >> /etc/pki/tls/certs/ca-bundle.crt
```
The previous examples set the certificate permanently on your machine across all users and require `sudo` permissions. To set the certificate only in your current terminal or script, run one of these commands:

* Option 1:
```
export SSL_CERT_FILE=PATH-TO-SERVER.crt
```
Where `PATH-TO-SERVER.crt` is the filepath of the `server.crt` certificate file.

* Option 2:
```
export SSL_CERT_DIR=PATH-TO-SERVER-DIRECTORY
```
Where `PATH-TO-SERVER-DIRECTORY` is the directory of the `server.crt` certificate file.

### Installing the certificate on Windows
To place the certificate file `server.crt` into your local trust store for Windows:

1. Right-click the certificate file.

2. Click **Install Certificate**.

3. Choose to install the certificate as the **Current User** or **Local Machine**.

4. From the certification store list, select **Trusted Root Certification Authorities**.