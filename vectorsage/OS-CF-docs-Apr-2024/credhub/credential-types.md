# CredHub credential types

* [Credential types](https://docs.cloudfoundry.org/credhub/credential-types.html#cred-types)

* [CredHub types in releases](https://docs.cloudfoundry.org/credhub/credential-types.html#consuming-types)

* [Enabling CredHub automatic generation in releases](https://docs.cloudfoundry.org/credhub/credential-types.html#enable-auto-generation)
There are different credential types that are supported by CredHub.
You can use these credentials to simplify generating and managing multi-part credentials.
For example, a TLS certificate contains three parts: the root certificate authority (CA),
the certificate, and the private key. CredHub supports all these parts, which helps keep connection requests
from being rejected erroneously.

## Credential types
CredHub supports the following credential types:
| Type | Description |
| --- | --- |
| `value` | A single string value for arbitrary configurations and other non-generated or validated strings. |
| `json` | An arbitrary JSON object for static configurations with many values. |
| `user` | Three string values for username, password, and password hash. |
| `password` | A single string value for passwords and other random string credentials. Values for this type can be automatically generated. |
| `certificate` | An object containing a root CA, certificate, and private key. Use this type for key pair apps that utilize a certificate, such as TLS connections. Values for this type can be automatically generated. |
| `rsa` | An object containing an RSA public key and private key without a certificate. Values for this type can be automatically generated. |
| `ssh` | An object containing an SSH-formatted public key and private key. Values for this type can be automatically generated. |
Each credential type supports distinct parameters for customizing how credentials are generated.
These include minimum password lengths, required characters, and certificate fields.
Credentials have a maximum size of 64 KB. For more information, see [CredHub API documentation](https://docs.cloudfoundry.org/api/credhub/).
For every credential type, secret values are encrypted before storage. For example, the private key of a certificate type credential and the password of a user type credential are encrypted before storage. For JSON and value type credentials, the full contents are encrypted before storage.

## CredHub types in releases
The BOSH Director interpolates the key value from the credential response for a deployment variable.
For example, in a deployment that contains the password credential previously referenced, BOSH substitutes `"nZaowPHTl0CQYVyYA0nV7ayHVulCBU3WTmwJKiZm"` for the variable. The behavior is also similar for other credential types.
For example, for the certificate credential previously referenced, BOSH substitutes the following object:
```
{
"ca": "-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----",
"certificate": "-----BEGIN CERTIFICATE-----...-----END CERTIFICATE-----",
"private_key": "-----BEGIN EXAMPLE RSA PRIVATE KEY-----...-----END EXAMPLE RSA PRIVATE KEY-----"
}
```
Similarly, the object can be translated into YAML format:
```
ca: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE------
certificate: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE------
private\_key: |

-----BEGIN EXAMPLE RSA PRIVATE KEY-----
...

-----END EXAMPLE RSA PRIVATE KEY------
```
If you want to leverage a non string typed credential, you can update your release to properly use the new format.
The following example shows how to configure a release to accept the certificate and password credential types that are previously referenced. The following sample Release Job Spec includes an example to instruct users on how to define the values if they are not using a CredHub credential.

### Release job spec
```

---
name: demo
properties:
demo.tls:
description: "Certificate and private key for TLS connection to API"
example: |
ca: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE-----
certificate: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE-----
private_key: |

-----BEGIN EXAMPLE RSA PRIVATE KEY-----
...

-----END EXAMPLE RSA PRIVATE KEY-----
admin-password:
description: "Admin password for the application"
example: nZaowPHTl0CQYVyYA0nV7ayHVulCBU3WTmwJKiZm
```

### ERB job template
```
erb
api-ca=<<span>%=</span> p("demo.tls.ca") %>
api-certificate=<<span>%=</span> p("demo.tls.certificate") %>
api-private-key=<<span>%=</span> p("demo.tls.private_key") %>
admin-password=<<span>%=</span> p("admin-password") %>
```

### Deployment manifest file
CredHub and BOSH are integrated to provide the option of generating the required credential values on deployment. You can define these generation parameters in the deployment manifest file in the `variables` section, as shown in the following example:
```

---
name: demo-deploy
variables:

- name: demo-ca
type: certificate
options:
is_ca: true
common_name: 'Demo Certificate Authority'

- name: demo-tls
type: certificate
options:
ca: demo-ca
common_name: example.com
alternative_names:

- example.com

- www.example.com
extended_key_usage:

- client_auth

- name: admin-password
type: password
options:
length: 40
instance_groups:
properties:
demo:
tls: ((demo-tls))
admin-password: ((demo-password))
```
Updating a release for other types is similar to the previous example. Keep track of the key name for each value you wish to use.