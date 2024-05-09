# Using a key management service with CredHub
You can connect CredHub to a third party Key Management Service (KMS) using Kubernetes API.
CredHub includes its’ own internal encryption. However, you might want to use the encryption provided by a
KMS instead.
To use a KMS, you must deploy a plug-in with CredHub. CredHub is compatible with plug-ins that implement the
KMS provider interface that is defined in the `protobuf` format. For more information,
see [Using a KMS provider for data encryption](https://kubernetes.io/docs/tasks/administer-cluster/kms-provider/) in the Kubernetes documentation.
The KMS interface comes from Kubernetes, but it’s not necessary to use Kubernetes when you write a plug-in.
For more information, see [Language Guide (proto3)](https://developers.google.com/protocol-buffers/docs/proto3) in the Google Protocol Buffers documentation.
Any plug-in that implements the KMS provider interface can be compatible with CredHub. Consult the
documentation for your KMS provider to learn if a plug-in exists.

* If a plug-in exists for your KMS provider, see [Building a BOSH release](https://docs.cloudfoundry.org/credhub/kms-plugin.html#build-a-release).

* If a plug-in has not been created for your KMS provider, see [Implementing the plug-in](https://docs.cloudfoundry.org/credhub/kms-plugin.html#implement).

## Implementing the plug-in
You can implement the KeyManagementService interface in any language.
The following example is written
in Go. For more information about the KeyManagementService interface, see the [sample-credhub-kms-plugin](https://github.com/pivotal/sample-credhub-kms-plugin/blob/85deb9b230a7b8c0d6a71a6d8ad1c37aa5be28ae/v1beta1/service.proto) repository on GitHub.
You must implement the following methods:
```
// This service defines the public APIs for remote KMS provider.
service KeyManagementService {
// Version returns the runtime name and runtime version of the KMS provider.
rpc Version(VersionRequest) returns (VersionResponse) {}
// Execute decryption operation in KMS provider.
rpc Decrypt(DecryptRequest) returns (DecryptResponse) {}
// Execute encryption operation in KMS provider.
rpc Encrypt(EncryptRequest) returns (EncryptResponse) {}
}
```
For sample plug-ins, see:

* [Plug-in](https://github.com/pivotal/sample-credhub-kms-plugin/blob/85deb9b230a7b8c0d6a71a6d8ad1c37aa5be28ae/plugin/plugin.go) that uses Base64 encoding for encryption in the sample-credhub-kms-plugin GitHub repository

* [Plug-in](https://github.com/kubernetes/kubernetes/blob/master/staging/src/k8s.io/apiserver/pkg/storage/value/encrypt/envelope/grpc_service.go) that connects to a fake KMS in the kubernetes GitHub repository

## Building a BOSH release
Because CredHub is deployed using BOSH, you must deploy the plug-in as a BOSH release on the
same instance group as CredHub.
To create a BOSH release for your plug-in, see [Creating a release](https://bosh.io/docs/create-release/) in
the BOSH documentation.
Your BOSH release must run the plug-in with a defined socket. You must reference this socket in your
CredHub BOSH manifest.
For an example of a BOSH release of a CredHub KMS plug-in with a defined socket, see
the [sample-credhub-kms-plugin-release](https://github.com/pivotal/sample-credhub-kms-plugin-release) repository on GitHub.

## Deploying CredHub with your plug-in release
To deploy CredHub with your plug-in, you must modify the CredHub BOSH manifest to include the new
encryption provider and keys.
You can modify the CredHub BOSH manifest using an ops file. An ops file is a YAML file that
includes multiple operations to be applied to a different YAML file, for example, a manifest.
For more information about how to create an ops file, see [Creating Ops Files](https://bosh.io/docs/cli-ops-files/) in the BOSH documentation.
To deploy CredHub with your plug-in:

1. Create an ops file. The following example modifies the CredHub BOSH manifest to work with `sample-credhub-kms-plugin`:
```

---

- type: replace
path: /releases/-
value:
name: sample-credhub-kms-plugin
version: latest

- type: replace
path: /instance_groups/name=credhub/jobs/name=credhub/properties/credhub/encryption/keys/-
value:
provider_name: sample
key_properties:
encryption_key_name: VALUE
active: true

- type: replace
path: /instance_groups/name=credhub/jobs/name=credhub/properties/credhub/encryption/providers/-
value:
name: sample
type: kms-plugin
connection_properties:
endpoint: /var/vcap/sys/run/kms-plugin/kms-plugin.sock

- type: replace
path: /instance_groups/name=credhub/jobs/-
value:
name: kms-plugin
release: sample-credhub-kms-plugin
properties:
kms-plugin:
socket_endpoint: /var/vcap/sys/run/kms-plugin/kms-plugin.sock

- type: replace
path: /instance_groups/name=credhub/jobs/name=credhub/properties/credhub/encryption/keys/provider_name=int/active
value: false
```
Where `VALUE` is your encryption key name.

2. To log in to your BOSH Director, run:
```
bosh -e ENV log-in
```
Where `ENV` is the name of your BOSH Director environment. For more information, see [Commands](https://bosh.io/docs/cli-v2/) in the BOSH documentation.

3. To deploy your CredHub with the plug-in, run:
```
bosh -d DEPLOYMENT-NAME credhub-manifest.yml -o OPS-FILE.yml
```
Where:

* `DEPLOYMENT-NAME` is the name of your CredHub BOSH deployment.

* `OPS-FILE` is the name of your ops file.