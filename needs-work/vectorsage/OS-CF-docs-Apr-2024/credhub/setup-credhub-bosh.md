# Setting up and deploying CredHub with BOSH

* [Preparing for deployment](https://docs.cloudfoundry.org/credhub/setup-credhub-bosh.html#setup)

* [Configuring the BOSH Director](https://docs.cloudfoundry.org/credhub/setup-credhub-bosh.html#configure)

* [Using CredHub](https://docs.cloudfoundry.org/credhub/setup-credhub-bosh.html#using-credhub)
You can deploy a BOSH Director with CredHub so that you can use credential variables in your
deployment manifests.
If you use the [bosh-deployment](https://github.com/cloudfoundry/bosh-deployment) repository on
GitHub, include the `credhub.yml` file to enable CredHub on the BOSH Director VM.
CredHub exists on a virtual machine (VM) with the BOSH Director, UAA, and other high level components.
A deployment manifest configured with variables calls to CredHub which passes the credential to the
appropriate components.
Once configured, any variable in a BOSH deployment manifest with the syntax `((variable-name))` causes
the BOSH Director to retrieve the variable value from CredHub at deployment time. You can tell your
manifest already uses CredHub if the fields with secure data have `((variables))` formatted with
double parentheses.

## Preparing for deployment
To prepare to deploy a BOSH Director with CredHub:

1. Set up your BOSH Director.
The following configuration steps assume that you have an existing BOSH Director. If you do not have a BOSH Director, see [Deploying BOSH with create-env](https://bosh.io/docs/init.html) in the BOSH documentation.

2. Configure UAA on your Director.

3. (Optional) Configure an external database.

4. (Optional) Configure a Luna HSM.

* Configure the HSM to allow access from the deployed CredHub instance.

* Grant the operator all of the required permissions to use the HSM.
For more information about the required HSM values and how to configure an HSM, see [Using hardware security modules with CredHub](https://docs.cloudfoundry.org/credhub/hsm-config.html).

## Configuring the BOSH Director
To configure your BOSH Director with CredHub:

1. Download the latest CredHub release from the [Releases](https://github.com/pivotal/credhub-release/releases) page in the CredHub repository on GitHub.

2. Update the deployment manifest to include the latest CredHub release. For example:
```
releases:

- name: bosh
url: https://bosh.io/d/github.com/cloudfoundry/bosh?v=261.2
version: 261.2
sha1: d4635b4b82b0dc5fd083b83eb7e7405832f6654b

# ...

- name: credhub
url: https://bosh.io/d/github.com/pivotal-cf/credhub-release?v=0.6.1
version: 0.6.1
sha1: 5ab4c4ef3d67f8ea07d78b1a87707e7520a97ab7
```
For more information, see [Latest Version](https://bosh.io/releases/github.com/pivotal-cf/credhub-release?all=1) in *credhub Release* in the BOSH documentation.

3. Add the CredHub job to the BOSH Director instance:
```
instance_groups:

- name: bosh
instances: 1
jobs:

- {name: nats, release: bosh}

- {name: redis, release: bosh}

- {name: postgres, release: bosh}

- {name: blobstore, release: bosh}

- {name: director, release: bosh}

- {name: health_monitor, release: bosh}

- {name: uaa, release: uaa-release}

- {name: credhub, release: credhub}
resource_pool: default

# ...
```

4. (Optional) Add variable generation specifications for CredHub properties.
```
variables:

- name: credhub-ca
type: certificate
options:
is_ca: true
common_name: 'CredHub CA'

- name: credhub-tls
type: certificate
options:
ca: credhub-ca
common_name: credhub.example.com
alternative_names:

- 10.0.0.10

- 127.0.0.1

- name: credhub-encryption-password
type: password
```

5. Add CredHub properties to the deployment manifest, as in the following example. This example includes a configuration to use a hardware security module (HSM) for encryption.
```
properties:
credhub:
port: 8844
log_level: info
tls:
certificate: ((credhub-tls.certificate))
private_key: ((credhub-tls.private_key))
data_storage:
type: mysql
host: mysql.example.com
port: 3306
database: credhub
username: user
password: PASSWORD
require_tls: true
tls_ca: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE-----
authentication:
uaa:
url: "https://uaa.example.com:8443"
verification_key: |

-----BEGIN PUBLIC KEY-----
...

-----END PUBLIC KEY-----
mutual_tls:
trusted_cas:

- |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE-----
encryption:
keys:

- provider_name: corp-hsm
encryption_key_name: KEY-NAME
active: true
providers:

- name: corp-hsm
type: hsm
partition: PARTITION-NAME
partition_password: PARTITION-PASSWORD
client_certificate: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE-----
client_key: |

-----BEGIN EXAMPLE RSA PRIVATE KEY-----
...

-----END EXAMPLE RSA PRIVATE KEY-----
servers:

- host: hsm.example.com
port: 1792
partition_serial_number: 123456
certificate: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE-----
```
Where:

* `PASSWORD` is the password for your CredHub instance.

* `KEY-NAME` is your CredHub encryption key.

* `PARTITION-NAME` is the name of the HSM partition on which your CredHub encryption key is stored.

* `PARTITION-PASSWORD` is the password of the HSM partition on which your CredHub encryption key is stored.
Alternatively, you can use the internal software-based encryption provider with the configuration below. This method derives a 256-bit key from the provided encryption password and utilized AES256-GCM encryption.
```
...
encryption:
providers:

- name: main
type: internal
keys:

- provider_name: main
encryption_password: ((credhub-encryption-password))
active: true
...
```
For the full list of CredHub properties and default values, see [credhub job](https://bosh.io/jobs/credhub?source=github.com/pivotal-cf/credhub-release) in the BOSH documentation.

6. Add CredHub CLI and your BOSH Director and CredHub UAA clients.
```
properties:
uaa:
clients:
credhub_cli:
override: true
authorized-grant-types: password,refresh_token
scope: credhub.read,credhub.write
authorities: uaa.none
access-token-validity: 120
refresh-token-validity: 1800
secret: ""
director_to_credhub:
override: true
authorized-grant-types: client_credentials
scope: uaa.none
authorities: credhub.read,credhub.write
access-token-validity: 43200
secret: CUSTOM-CLIENT-SECRET
```
Where `CUSTOM-CLIENT-SECRET` is the client secret you set for the BOSH Director.

7. Enable the configuration server feature of the BOSH Director and configure it to utilize CredHub:
```
properties:
director:
address: bosh.EXAMPLE.com
name: director-name
config_server:
enabled: true
url: "https://127.0.0.1:8844/api/"
ca_cert: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE-----
uaa:
url: "https://127.0.0.1:8443"
client_id: director_to_credhub
client_secret: EXAMPLE-SECRET
ca_cert: |

-----BEGIN CERTIFICATE-----
...

-----END CERTIFICATE-----
```

8. (Optional) Configure the BOSH Director Postgres server with an additional database named `credhub`. If you are using the internal BOSH Director database, you must provision an additional database for the CredHub data. If you use an external database, you must create the database on your database server before deploying.
```
properties:
postgres: &db
host: 127.0.0.1
port: 5432
user: postgres
password: POSTGRES-PASSWORD
database: bosh
additional_databases: [credhub]
adapter: postgres
```
Where `POSTGRES-PASSWORD` is the password for your Postgres server.

9. (Optional) Seed initial CredHub users to UAA. Users must have both `credhub.read` and `credhub.write access` scopes.
```
properties:
uaa:
scim:
users:

- name: CREDHUB-USER
password: USER-PASSWORD
groups:

- credhub.read

- credhub.write

- name: OTHER-CREDHUB-USER
password: OTHER-USER-PASSWORD
groups:

- credhub.read

- credhub.write
```
Where:

* `CREDHUB-USER` and `OTHER-CREDHUB-USER` are the CredHub users you want to seed to UAA.

* `CREDHUB-PASSWORD` and `OTHER-CREDHUB-PASSWORD` are the passwords for the CredHub users you want to seed to UAA.

10. Deploy the BOSH Director. For more information, see [Deploying](https://bosh.io/docs/deploying/) in the BOSH documentation.

## Using CredHub
To use CredHub:

1. Create CredHub users in UAA. To authenticate with CredHub to manage credentials, you must have a UAA user account with the scopes `credhub.read` and `credhub.write`. To create users in UAA, see [Creating and managing users with the UAA CLI](https://docs.cloudfoundry.org/uaa/uaa-user-management.html) . Alternatively, you can configure UAA with an external LDAP provider. For more information, see [User Account and Authentication LDAP Integration](https://github.com/cloudfoundry/uaa/blob/master/docs/UAA-LDAP.md) in the CloudFoundry User Account and Authentication (UAA) Server repository on GitHub.

2. Install the CredHub CLI to manage stored credentials. Download the CredHub CLI from the [Releases](https://github.com/cloudfoundry-incubator/credhub-cli/releases) page in the CredHub CLI repository on GitHub.

3. Target the CredHub API by running:
```
credhub api CREDHUB-API-TARGET
```
Where `CREDHUB-API-TARGET` is the URL of your CredHub API server.

4. Authenticate with CredHub by running:
```
credhub login --client-name= CLIENT-NAME --client-secret= CLIENT-SECRET
```
Where:

* `CLIENT-NAME` is the name of the UAA client.

* `CLIENT-SECRET` is the secret for the UAA client.

5. Place or generate credentials in CredHub using the CredHub CLI:

* To place credentials in CredHub, run:
```
credhub set --type ssh --name /static/ssh_key --public ~/ssh.pub --private ~/ssh.key
```

* To generate credentials in CredHub, run:
```
credhub generate --type ssh --name /generated/ssh_key
```

6. Update your BOSH deployment manifests. Once you have a BOSH Director that integrates with CredHub, you can update your deployment manifests to use it. The following example is a deployment manifest using two credentials: one stored in CredHub, and one that is generated by CredHub. You can define credentials that you want to be generated automatically in the `variables` section.
```
name: Sample-Manifest
releases:

- name: shell
url: https://bosh.io/d/github.com/cloudfoundry-community/shell-boshrelease?v=3.2.0
sha1: 893b10af531a7519da99bb8656cc07b8277d1692

#...
variables:

- name: generated/ssh\_key
type: ssh
jobs:

- name: shell
instances: 1
persistent\_disk: 0
resource\_pool: vms
networks:

- name: private
static\_ips: 10.0.0.100
default: [dns, gateway]
templates:

- name: shell
release: shell
properties:
shell:
users:

- name: shell
ssh\_keys:

- ((/static/ssh\_key))

- ((generated/ssh\_key))
```