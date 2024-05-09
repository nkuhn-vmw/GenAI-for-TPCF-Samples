# Cloud Controller Blobstore Configuration
This topic explains how to configure a blobstore for the Cloud Controller.

## Overview
The [`cf-deployment`](https://github.com/cloudfoundry/cf-deployment/blob/master/operations/README.md) GitHub repository provides ops files with several common blobstore configurations.
By default, `cf-deployment` uses the WebDAV blobstore, and no additional ops files are needed.
If you want to configure your blobstore manually, see the topics below for guidance.
The Cloud Controller has four types of objects that need to be stored in a blobstore: `buildpacks`, `droplets`, `packages`, and `resource_pool`. By default, the blobstore configuration uses the Fog Ruby gem, but can also use the WebDAV protocol.
This document describes the following common blobstore configurations:

* [Fog with AWS Credentials](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#fog-aws-creds)

* [Fog with AWS Server Side Encryption](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#fog-aws-sse)

* [Fog with AWS IAM Instance Profiles](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#fog-aws-iam)

* [Fog with Google Cloud Storage](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#fog-gcs)

* [Fog with Google Cloud Storage Service Accounts](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#fog-gcs-service-account)

* [Fog with Azure Storage](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#fog-azure)

* [Fog with Other S3 Compatible Stores](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#fog-s3-other)

* [Fog with NFS](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#fog-local-nfs)

* [WebDAV](https://docs.cloudfoundry.org/deploying/common/cc-blobstore-config.html#webdav) internal blobstore

## Fog with AWS Credentials
To use Fog blobstores with AWS credentials, do the following:

1. Insert the following configuration into your manifest under `properties.cc`:
```
cc:
buildpacks:
blobstore_type: fog
buildpack_directory_key: YOUR-AWS-BUILDPACK-BUCKET
fog_connection: &fog_connection
aws_access_key_id: AWS-ACCESS-KEY
aws_secret_access_key: AWS-SECRET-ACCESS-KEY
provider: AWS
region: us-east-1
droplets:
blobstore_type: fog
droplet_directory_key: YOUR-AWS-DROPLET-BUCKET
fog_connection: *fog_connection
packages:
blobstore_type: fog
app_package_directory_key: YOUR-AWS-PACKAGE-BUCKET
fog_connection: *fog_connection
resource_pool:
blobstore_type: fog
resource_directory_key: YOUR-AWS-RESOURCE-BUCKET
fog_connection: *fog_connection
```

2. Replace `AWS-ACCESS-KEY` and `AWS-SECRET-ACCESS-KEY` with your AWS credentials.

3. Replace `YOUR-AWS-BUILDPACK-BUCKET`, `YOUR-AWS-DROPLET-BUCKET`, `YOUR-AWS-PACKAGE-BUCKET`, and `YOUR-AWS-RESOURCE-BUCKET` with the names of your AWS buckets. Do not use periods (`.`) in your AWS bucket names. In the AWS console, you must assign your credentials an IAM policy that allows all S3 actions on all of these buckets.

4. (Optional) Provide additional configuration through the `fog_connection` hash, which is passed through to the Fog gem.

## Fog with AWS Server-Side Encryption
AWS S3 offers Server-Side Encryption at rest. For more information, see [Protecting Data Using Server-Side Encryption](http://docs.aws.amazon.com/AmazonS3/latest/dev/serv-side-encryption.html).

**AWS SSE-S3 blobstore encryption**

1. Insert the following configuration into your manifest under `properties.cc`:
```
cc:
buildpacks:
blobstore_type: fog
buildpack_directory_key: YOUR-AWS-BUILDPACK-BUCKET
fog_connection: &fog_connection
aws_access_key_id: AWS-ACCESS-KEY
aws_secret_access_key: AWS-SECRET-ACCESS-KEY
provider: AWS
region: us-east-1
fog_aws_storage_options: &fog_aws_storage_options
encryption: 'AES256'
droplets:
blobstore_type: fog
droplet_directory_key: YOUR-AWS-DROPLET-BUCKET
fog_connection: *fog_connection
fog_aws_storage_options: *fog_aws_storage_options
packages:
blobstore_type: fog
app_package_directory_key: YOUR-AWS-PACKAGE-BUCKET
fog_connection: *fog_connection
fog_aws_storage_options: *fog_aws_storage_options
resource_pool:
blobstore_type: fog
resource_directory_key: YOUR-AWS-RESOURCE-BUCKET
fog_connection: *fog_connection
fog_aws_storage_options: *fog_aws_storage_options
```

2. Replace `AWS_ACCESS_KEY` and `AWS_SECRET_ACCESS_KEY` with your AWS credentials.

3. Replace `YOUR-AWS-BUILDPACK-BUCKET`, `YOUR-AWS-DROPLET-BUCKET`, `YOUR-AWS-PACKAGE-BUCKET`, and `YOUR-AWS-RESOURCE-BUCKET` with the names of your AWS buckets. Do not use periods (`.`) in your AWS bucket names. In the AWS console, you must assign your credentials an IAM policy that allows all S3 actions on all of these buckets.

4. You can provide further configuration through the `fog_connection` hash, which is passed through to the Fog gem.

5. `fog_aws_storage_options` takes a hash with the key `encryption`. Operators can set its value to a type of encryption algorithm. In the configuration information above, `encryption` is set to `AES256` to enable AWS SSE-S3 encryption.

6. You can provide further configuration through the `fog_aws_storage_options` hash, which is passed through to the Fog gem.

**AWS SSE-KMS blobstore encryption**

1. Obtain your KMS Key ID. For information about managing KMS keys, see the [AWS Key Management Service Getting Started guide.](http://docs.aws.amazon.com/kms/latest/developerguide/getting-started.html)

2. Insert the following configuration into your manifest under `properties.cc`:
```
cc:
buildpacks:
blobstore_type: fog
buildpack_directory_key: YOUR-AWS-BUILDPACK-BUCKET
fog_connection: &fog_connection
aws_access_key_id: AWS-ACCESS-KEY
aws_secret_access_key: AWS-SECRET-ACCESS-KEY
provider: AWS
region: us-east-1
fog_aws_storage_options: &fog_aws_storage_options
encryption: 'aws:kms'
x-amz-server-side-encryption-aws-kms-key-id: "YOUR-AWS-KMS-KEY-ID"
droplets:
blobstore_type: fog
droplet_directory_key: YOUR-AWS-DROPLET-BUCKET
fog_connection: *fog_connection
fog_aws_storage_options: *fog_aws_storage_options
packages:
blobstore_type: fog
app_package_directory_key: YOUR-AWS-PACKAGE-BUCKET
fog_connection: *fog_connection
fog_aws_storage_options: *fog_aws_storage_options
resource_pool:
blobstore_type: fog
resource_directory_key: YOUR-AWS-RESOURCE-BUCKET
fog_connection: *fog_connection
fog_aws_storage_options: *fog_aws_storage_options
```

3. Replace `AWS-ACCESS-KEY` and `AWS-SECRET-ACCESS-KEY` with your AWS credentials.

4. Replace `YOUR-AWS-BUILDPACK-BUCKET`, `YOUR-AWS-DROPLET-BUCKET`, `YOUR-AWS-PACKAGE-BUCKET`, and `YOUR-AWS-RESOURCE-BUCKET` with the names of your AWS buckets. Do not use periods (`.`) in your AWS bucket names. In the AWS console, you must assign your credentials an IAM policy that allows all S3 actions on all of these buckets.

5. You can provide further configuration through the `fog_connection` hash, which is passed through to the Fog gem.

6. Replace `YOUR-AWS-KMS-KEY-ID` with your KMS Key ID.

7. `fog_aws_storage_options` takes a hash with the key `encryption`. Operators can set its value to a type of encryption algorithm. In the configuration information above, `encryption` is set to `aws:kms` to enable AWS SSE-KMS encryption.

8. You can provide further configuration through the `fog_aws_storage_options` hash, which is passed through to the Fog gem.

## Fog with AWS IAM Instance Profiles
To configure Fog blobstores to use [AWS IAM Instance Profiles](http://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html), do the following:

1. Configure an additional `cloud-controller` IAM role with the following policy to give access to the S3 buckets you plan to use:
```
{
"Version": "2012-10-17",
"Statement": [{
"Effect": "Allow",
"Action": [ "s3:\*" ],
"Resource": [
"arn:aws:s3:::YOUR-AWS-BUILDPACK-BUCKET",
"arn:aws:s3:::YOUR-AWS-BUILDPACK-BUCKET/\*",
"arn:aws:s3:::YOUR-AWS-DROPLET-BUCKET",
"arn:aws:s3:::YOUR-AWS-DROPLET-BUCKET/\*",
"arn:aws:s3:::YOUR-AWS-PACKAGE-BUCKET",
"arn:aws:s3:::YOUR-AWS-PACKAGE-BUCKET/\*",
"arn:aws:s3:::YOUR-AWS-RESOURCE-BUCKET",
"arn:aws:s3:::YOUR-AWS-RESOURCE-BUCKET/\*",
]
}]
}
```
Replace `YOUR-AWS-BUILDPACK-BUCKET`, `YOUR-AWS-DROPLET-BUCKET`, `YOUR-AWS-PACKAGE-BUCKET`, and `YOUR-AWS-RESOURCE-BUCKET` with the names of your AWS buckets. Do not use periods (`.`) in your AWS bucket names.
If you use the AWS console, an IAM Role is automatically assigned to an IAM Instance Profile with the same name, `cloud-controller`. If you do not use the AWS console, you must create an IAM Instance Profile with a single assigned IAM Role. For more information, see [Step 4: Create an IAM Instance Profile for Your Amazon EC2 Instances](https://docs.aws.amazon.com/codedeploy/latest/userguide/getting-started-create-iam-instance-profile.html) in the AWS documentation.

2. In your [BOSH cloud config](https://bosh.io/docs/cloud-config/), create a [VM extension](https://bosh.io/docs/cloud-config/#vm-extensions) to add the IAM Instance Profile you created to VMs using the extension.
```
vm_extensions:

- cloud_properties:
iam_instance_profile: cloud-controller
name: cloud-controller-iam
```

3. In your Cloud Foundry deployment manifest, use the `cloud-controller-iam` VM extension you created for the instance groups containing `cloud_controller`, `cloud_controller_worker`, and `cloud_controller_clock`, as in the example below:
```
instance_groups:
...

- name: api
...
vm_extensions:

- cloud-controller-iam
...

- name: cc-worker
...
vm_extensions:

- cloud-controller-iam
...

- name: scheduler
...
vm_extensions:

- cloud-controller-iam
```

4. Insert the following configuration into your deployment manifest under `properties.cc`:
```
cc:
buildpacks:
blobstore_type: fog
buildpack_directory_key: YOUR-AWS-BUILDPACK-BUCKET
fog_connection: &fog_connection
provider: AWS
region: us-east-1
use_iam_profile: true
droplets:
blobstore_type: fog
droplet_directory_key: YOUR-AWS-DROPLET-BUCKET
fog_connection: *fog_connection
packages:
blobstore_type: fog
app_package_directory_key: YOUR-AWS-PACKAGE-BUCKET
fog_connection: *fog_connection
resource_pool:
blobstore_type: fog
resource_directory_key: YOUR-AWS-RESOURCE-BUCKET
fog_connection: *fog_connection
```
Replace `YOUR-AWS-BUILDPACK-BUCKET`, `YOUR-AWS-DROPLET-BUCKET`, `YOUR-AWS-PACKAGE-BUCKET`, and `YOUR-AWS-RESOURCE-BUCKET` with the names of your AWS buckets. Do not use periods (`.`) in your AWS bucket names.

5. (Optional) Provide other configuration with the `fog_connection` hash, which is passed through to the Fog gem.

## Fog with Google Cloud Storage
To configure your blobstores to use Google Cloud Storage Interoperability credentials, do the following:

1. Insert the following configuration into your manifest under `properties.cc`:
```
cc:
buildpacks:
blobstore_type: fog
buildpack_directory_key: YOUR-GCS-BUILDPACK-BUCKET
fog_connection: &fog_connection
provider: Google
google_storage_access_key_id: GCS-ACCESS-KEY
google_storage_secret_access_key: GCS-SECRET-ACCESS-KEY
droplets:
blobstore_type: fog
droplet_directory_key: YOUR-GCS-DROPLET-BUCKET
fog_connection: *fog_connection
packages:
blobstore_type: fog
app_package_directory_key: YOUR-GCS-PACKAGE-BUCKET
fog_connection: *fog_connection
resource_pool:
blobstore_type: fog
resource_directory_key: YOUR-GCS-RESOURCE-BUCKET
```

2. Create an Interoperability key using the [GCP instructions](https://cloud.google.com/storage/docs/migrating#keys).

3. Replace `GCS-ACCESS-KEY` and `GCS-SECRET-ACCESS-KEY` with your Cloud Storage credentials.

4. Replace `YOUR-GCS-BUILDPACK-BUCKET`, `YOUR-GCS-DROPLET-BUCKET`, `YOUR-GCS-PACKAGE-BUCKET`, and `YOUR-GCS-RESOURCE-BUCKET` with the names of your Cloud Storage buckets. Do not use periods (`.`) in your bucket names.

5. You can provide further configuration through the `fog_connection` hash, which is passed through to the Fog gem.

## Fog with Google Cloud Storage Service Accounts
To configure your blobstore to use Google Cloud Storage with a service account, do the following:

1. Create a custom Cloud IAM role with the following permissions:
```
storage.buckets.create
storage.buckets.get
storage.objects.create
storage.objects.delete
storage.objects.get
storage.objects.list
```
To create the custom role, follow the [Creating and Managing Custom Roles](https://cloud.google.com/iam/docs/creating-custom-roles) instructions in the GCP documentation. This role will be used for blobstore permissions.

2. Create a service account by following the [Creating and Managing Service Accounts](https://cloud.google.com/iam/docs/creating-managing-service-accounts) instructions in the GCP documentation and grant this service account the role you created in Step 1.
For additional information about granting roles to an existing service account, see [Granting Roles to a Service Account for Specific Resources](https://cloud.google.com/iam/docs/granting-roles-to-service-accounts#granting_access_to_a_service_account_for_a_resource) in the GCP documentation.

3. Create a service account JSON key for your service account by following the [Creating and Managing Service Account Keys](https://cloud.google.com/iam/docs/creating-managing-service-account-keys) instructions in the GCP documentation.
You need this key to configure your blobstore.

4. Insert the following configuration in your manifest under `properties.cc` for the `cloud_controller_ng` job:
```
cc:
buildpacks: &buildpacks
blobstore_type: fog
buildpack_directory_key: YOUR-GCS-BUILDPACK-BUCKET
fog_connection: &fog_connection
provider: Google
google_project: YOUR-GCS-PROJECT
google_client_email: YOUR-GCS-SERVICE-ACCOUNT-EMAIL
google_json_key_string: >
{
"type": "service_account",
"project_id": "YOUR-GCS-PROJECT",
...
}
droplets: &droplets
blobstore_type: fog
droplet_directory_key: YOUR-GCS-DROPLET-BUCKET
fog_connection: *fog_connection
packages: &packages
blobstore_type: fog
app_package_directory_key: YOUR-GCS-PACKAGE-BUCKET
fog_connection: *fog_connection
resource_pool: &resource_pool
blobstore_type: fog
fog_connection: *fog_connection
resource_directory_key: YOUR-GCS-RESOURCE-BUCKET
```
Replace the placeholders as follows:

* `YOUR-GCS-PROJECT` is the name of your GCP project.

* `YOUR-GCS-SERVICE-ACCOUNT-EMAIL` is the email of your GCP service account.

* `YOUR-GCS-BUILDPACK-BUCKET`, `YOUR-GCS-DROPLET-BUCKET`,
`YOUR-GCS-PACKAGE-BUCKET`, and `YOUR-GCS-RESOURCE-BUCKET` are the names of your Cloud Storage buckets.
Do not use periods in the bucket names.In `google_json_key_string`, provide your Cloud Storage credentials. Use spaces, not tabs, for indentation.

5. To update the `cloud_controller_worker` and `cloud_controller_clock` jobs with the same blobstore configuration, insert the following for both jobs under `properties.cc`:
```
cc:

# note these reference YAML anchors declared in the previous step
buildpacks: *buildpacks
droplets: *droplets
packages: *packages
resource_pool: *resource_pool
```

## Fog with Azure Storage
To configure your blobstores to use Azure Storage credentials, do the following:

1. Insert the following configuration into your manifest under `properties.cc`:
```
cc:
buildpacks:
blobstore_type: fog
buildpack_directory_key: YOUR-AZURE-BUILDPACK-CONTAINER
fog_connection: &fog_connection
provider: AzureRM
environment: AzureCloud
azure_storage_account_name: YOUR-AZURE-STORAGE-ACCOUNT-NAME
azure_storage_access_key: YOUR-AZURE-STORAGE-ACCESS-KEY
droplets:
blobstore_type: fog
droplet_directory_key: YOUR-AZURE-DROPLET-CONTAINER
fog_connection: *fog_connection
packages:
blobstore_type: fog
app_package_directory_key: YOUR-AZURE-PACKAGE-CONTAINER
fog_connection: *fog_connection
resource_pool:
blobstore_type: fog
resource_directory_key: YOUR-AZURE-RESOURCE-CONTAINER
fog_connection: *fog_connection
```

2. Replace `YOUR-AZURE-STORAGE-ACCOUNT-NAME` and `YOUR-AZURE-STORAGE-ACCESS-KEY` with your Azure Storage credentials.

3. Replace `YOUR-AZURE-BUILDPACK-CONTAINER`, `YOUR-AZURE-DROPLET-CONTAINER`,
`YOUR-AZURE-PACKAGE-CONTAINER`, and `YOUR-AZURE-RESOURCE-CONTAINER`
with the names of your Cloud Storage containers.
Azure container names must consist of
only lowercase alphanumeric characters and hyphens.
See [Azure’s storage name restrictions](https://docs.microsoft.com/en-us/azure/architecture/best-practices/naming-conventions#storage).

4. You can provide further configuration through the `fog_connection` hash, which is passed through to the Fog gem.

## Fog with Other S3 Compatible Stores
Using Fog blobstores with other S3 compatible stores, such as Minio or EMC Elastic Cloud Storage is similar to AWS, and uses the same Fog adapter, but requires slightly different configuration:

1. Insert the following configuration into your manifest under `properties.cc`:
```
cc:
buildpacks:
blobstore_type: fog
buildpack_directory_key: YOUR-S3-BUILDPACK-BUCKET
fog_connection: &fog_connection
provider: AWS
endpoint: S3-ENDPOINT
aws_access_key_id: S3-ACCESS-KEY
aws_secret_access_key: S3-SECRET-ACCESS-KEY
aws_signature_version: '2'
region: "''"
path_style: true
droplets:
blobstore_type: fog
droplet_directory_key: YOUR-S3-DROPLET-BUCKET
fog_connection: *fog_connection
packages:
blobstore_type: fog
app_package_directory_key: YOUR-S3-PACKAGE-BUCKET
fog_connection: *fog_connection
resource_pool:
blobstore_type: fog
resource_directory_key: YOUR-S3-RESOURCE-BUCKET
fog_connection: *fog_connection
```

2. Replace `S3-ENDPOINT` with the URL used to access your S3 API. This will typically look something like `http://S3-NAMESPACE.HOST:9020` but may vary for your server or network.

3. Replace `S3-ACCESS-KEY` and `S3-SECRET-ACCESS-KEY` with your S3 credentials. This key must have access to all S3 activities on the buckets you will specify below.

4. Replace `YOUR-S3-BUILDPACK-BUCKET`, `YOUR-S3-DROPLET-BUCKET`, `YOUR-S3-PACKAGE-BUCKET`, and `YOUR-S3-RESOURCE-BUCKET` with the names of your S3 buckets. Do not use periods (`.`) in your S3 bucket names.

5. (Optional) Provide additional configuration through the `fog_connection` hash, which is passed through to the Fog gem.

## Fog with NFS
To configure your blobstores to use an NFS-mounted directory, do the following:

1. Insert the following configuration into your manifest under `properties.cc`:
```
cc:
buildpacks:
blobstore_type: fog
buildpack_directory_key: YOUR-BUILDPACK-DIRECTORY-PREFIX
fog_connection: &fog_connection
provider: Local
local_root: '/var/vcap/data/nfs'
droplets:
blobstore_type: fog
droplet_directory_key: YOUR-DROPLET-DIRECTORY-PREFIX
fog_connection: *fog_connection
packages:
blobstore_type: fog
app_package_directory_key: YOUR-PACKAGE-DIRECTORY-PREFIX
fog_connection: *fog_connection
resource_pool:
blobstore_type: fog
resource_directory_key: YOUR-RESOURCE-DIRECTORY-PREFIX
fog_connection: *fog_connection
```

2. Replace `YOUR-BUILDPACK-DIRECTORY-PREFIX`, `YOUR-DROPLET-DIRECTORY-PREFIX`, `YOUR-PACKAGE-DIRECTORY-PREFIX`, and `YOUR-RESOURCE-DIRECTORY-PREFIX` with the names of the directories you will be using. If you do not specify these, Cloud Foundry will supply usable default values. It is important that `local_root` be set to `/var/vcap/data/nfs` because the Cloud Controller jobs expect the NFS volume to be mounted at that path.

3. (Optional) Provide other configuration with the `fog_connection` hash, which is passed through to the Fog gem.

4. Configure the `nfs_mounter` job for the `cloud_controller_ng`, `cloud_controller_worker`, and `cloud_controller_clock` instance groups. The `nfs_mounter` job specifies how to mount a remote NFS server onto a local directory.
```
name: nfs_mounter
properties:
nfs_server:
address: NFS-ENDPOINT
share: REMOTE-DIR-TO-MOUNT
share_path: '/var/vcap/data/nfs'
nfsv4: false
release: capi
```
Replace the placeholder text in the example above with the values you want to use. Sample values:

* `NFS-ENDPOINT`: `nfstestserver.service.cf.internal`

* `REMOTE-DIR-TO-MOUNT`: `/var/data/exported`

## WebDAV
To configure your blobstores to use the WebDAV protocol, perform the steps below:

1. Ensure your deployment manifest has a single instance of the blobstore job. For a working example, see the [example bosh-lite manifest](https://github.com/cloudfoundry/cf-release/blob/49a94e2/spec/fixtures/bosh-lite/cf-manifest.yml#L297-L329).

2. Insert the following configuration into your manifest under `properties.blobstore` and `properties.cc`:
```
blobstore:
admin_users:

- password: WEBDAV-BASIC-AUTH-PASSWORD
username: WEBDAV-BASIC-AUTH-USER
port: 8080
secure_link:
secret: WEBDAV-SECRET
tls:
cert: WEBDAV-CERT
port: 4443
private_key: WEBDAV-PRIVATE-KEY
ca_cert: WEBDAV-CA-CERT-BUNDLE
cc:
buildpacks:
blobstore_type: webdav
buildpack_directory_key: cc-buildpacks
webdav_config: &webdav_config
public_endpoint: WEBDAV-PUBLIC-ENDPOINT
private_endpoint: WEBDAV-PRIVATE-ENDPOINT
username: WEBDAV_BASIC-AUTH-USER
password: WEBDAV_BASIC-AUTH-PASSWORD
ca_cert: WEBDAV-CA-CERT-BUNDLE
droplets:
blobstore_type: webdav
droplet_directory_key: cc-droplets
webdav_config: *webdav_config
packages:
blobstore_type: webdav
app_package_directory_key: cc-packages
webdav_config: *webdav_config
resource_pool:
blobstore_type: webdav
resource_directory_key: cc-resources
webdav_config: *webdav_config
```

3. Configure your WebDAV blobstores by doing the following:

* Replace `WEBDAV-BASIC-AUTH-USER` and `WEBDAV-BASIC-AUTH-PASSWORD` with Basic AUTH credentials that Cloud Controller can use to communicate with your WebDAV installation.

* Replace `WEBDAV-SECRET` with a secret phrase used to sign URLs.

* Replace `WEBDAV-CERT`, `WEBDAV-PRIVATE-KEY`, and `WEBDAV-CA-CERT-BUNDLE` with proper TLS configuration that are used for the internal blobstore.

* Replace `WEBDAV-PUBLIC-ENDPOINT` with the public URL that resolves to your WebDAV installation. For example, `https://blobstore.SYSTEM-DOMAIN.example.com`.

* Replace `WEBDAV-PRIVATE-ENDPOINT` with a routable URL on your internal network. If not set, this defaults to `https://blobstore.service.cf.internal:4443`.

* Replace `WEBDAV-BASIC-AUTH-USER` and `WEBDAV-BASIC-AUTH-PASSWORD` with Basic AUTH credentials that Cloud Controller can use to communicate with your WebDAV installation.

4. Create a `webdav_config` hash to provide further configuration.