# Using hardware security modules with CredHub
You can configure [AWS CloudHSM](https://aws.amazon.com/cloudhsm) devices to work with CredHub.

**Important**
If you use a [Luna SafeNet HSM](https://safenet.gemalto.com/data-encryption/hardware-security-modules-hsms/safenet-network-hsm/),
rather than AWS, skip over the device allocation portion of the documentation, and start with
[Initialize and Configure New HSMs](https://docs.cloudfoundry.org/credhub/hsm-config.html#initialize-and-configure).
If you store critical data in CredHub, configuring at least two Hardware Security Modules (HSMs) replicates your keys and provides redundancy and security in the event of an HSM failure. With a single HSM, device failure renders your CredHub data inaccessible.

## Preparation checklist
As you follow these procedures, you can collect or create these resources:

* The name of your encryption key.

* Your HSM certificate.

* Your HSM partition name and password.

* Your client certificate and private key.

* Your HSM partition serial numbers.

## Creating new AWS CloudHSMs
The following sections tell you how to create new AWS CloudHSMs:

### AWS environment prerequisites

**Note**
For high availability (HA), use at least two HSM instances. AWS documentation recommends that you also use a subnet for a publicly available Control Instance, but for this product that is unnecessary. CredHub acts as a Control Instance.
Before you create new AWS CloudHSMs, you must have:

* A Virtual Private Cloud (VPC).

* **For each HSM instance:** One private subnet in its own Availability Zone (AZ).

* An IAM role for the HSM with a policy equivalent to `AWSCloudHSMRole` policy.

* The Security Group must allow traffic from the CredHub security group on ports 22 (SSH) and 1792 (HSM).

### Creating new devices
To create new AWS CloudHSMs:

1. Install the AWS CLI from [AWS CloudHSM Command Line Tools](https://docs.aws.amazon.com/cloudhsm/latest/userguide/command-line-tools.html) in the AWS documentation.

2. Create SSH key pairs for all planned HSMs by running:
```
ssh-keygen -b 4096 -t rsa -N PASSWORD -f PATH-TO-SSH-KEY.pem
```
Where:

* `PASSWORD` is the password you create for the SSH key.

* `PATH-TO-SSH-KEY` is the filepath of your SSH key PEM file.

3. Create the `cloudhsm.conf` file with these values:
```
aws_access_key_id=ACCESS-KEY-ID
aws_secret_access_key=SECRET-ACCESS-KEY
aws_region=AWS-REGION
```
Where:

* `ACCESS-KEY-ID` is your AWS access key ID.

* `SECRET-ACCESS-KEY` is your AWS secret access key.

* `AWS-REGION` is your AWS region.

4. To create each HSM and place it in the appropriate subnet, run:
```
cloudhsm create-hsm \

--conf_file PATH-TO-CLOUDHSM.conf \

--subnet-id SUBNET-ID \

--ssh-public-key-file PATH-TO-SSH-KEY.pem.pub \

--iam-role-arn IAM-HSN-ROLE-ARN
```
Where:

* `PATH-TO-CLOUDHSM` is the filepath to your `cloudhsm.conf` file.

* `SUBNET-ID` is the ID of the subnet in which you want to place your HSM.

* `PATH-TO-SSH-KEY` is the filepath to your public SSH key PEM key.

* `IAM-HSM-ROLE-ARN` is the Amazon Resource Name (ARN) of your HSM’s IAM role. For more information, see [IAM ARNs](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-arns) in *IAM Identifiers* in the AWS documentation.

5. Assign the security group to each HSM:

1. Retrieve the Elastic Network Interface ID `EniID` of the HSM by running:
```
cloudhsm describe-hsm -H HSM-ARN -r AWS-REGION
```
Where:

* `HSM-ARN` is the ARN of your HSM.

* `AWS-REGION` is the AWS region of your HSM.

2. Edit the network interface to assign the security group by running:
```
aws ec2 modify-network-interface-attribute \

--network-interface-id ENI-ID \

--groups SECURITY-GROUP-ID
```
Where:

* `ENI-ID` is the `EniID` you retrieved in the previous step.

* `SECURITY-GROUP-ID` is the ID of the security group you want to assign to this HSM.

## Initializing and configuring new HSMs
The following sections describe the steps to initialize and configure your HSMs, whether they are Luna HSMs or AWS CloudHSMs. You must follow this procedure for each HSM you created.

### SSH onto HSM
To SSH onto HSM you want to initialize and configure using these steps:

1. Retrieve the IP address of your HSM by running:
```
cloudhsm describe-hsm -H HSM-ARN -r AWS-REGION
```
Where:

* `HSM-ARN` is the ARN of your HSM.

* `AWS-REGION` is the AWS region of your HSM.

2. SSH onto the HSM by running:
```
ssh -i path/to/ssh-key.pem manager@HSM-IP
```
Where `HSM-IP` is the IP address you retrieved in the previous step.

### Initializing and setting policies
To initialize your HSM and set its’ policies:

1. Initialize the HSM and create an admin password when you are prompted by running:
```
lunash:> hsm init -label LABEL
```
Where `LABEL` is the label you want to give the HSM.
Initialize all HSMs into the same cloning domain to guarantee high availability for your Cloud Foundry deployment.

1. Log in to the HSM using the password you just created by running:
```
lunash:> hsm login
```

2. Confirm that only FIPS algorithms are enabled. Run:
```
lunash:> hsm changePolicy -policy 12 -value 0
```

3. To confirm that `Allow cloning` and `Allow network replication` policy values are set to `On` on the HSM, run:
```
hsm showPolicies
```
If these values are not set to `On`, change them by running:
```
lunash:> hsm changePolicy -policy POLICY-CODE -value 1
```
Where `POLICY-CODE` is the numerical code of the `Allow cloning` or `Allow network replication` policy.

4. Validate that the `SO can reset partition PIN` is correctly set. If it’s set to `Off`, consecutive failed log in attempts permanently erase the partition once the failure count hits the configured threshold. If it’s set to `On`, the partition locks once the threshold is met. An HSM admin must unlock the partition, but no data is lost.
To set the policy to `On`, run:
```
lunash:> hsm changePolicy -policy 15 -value 1
```

### Retrieving the HSM certificate
To retrieve your HSM certificate:

1. Run:
```
scp -i path/to/ssh-key.pem \
manager@HSM-IP-ADDRESS:server.pem \
HSM-IP-ADDRESS.pem
```
Where `HSM-IP-ADDRESS` is the IP address of your HSM.
BOSH CredHub uses this certificate to validate the identity of the HSM when it connects to it.

### Creating the HSM partition
To create an HSM partition to hold the encryption keys:

1. Run:
```
lunash:> partition create -partition PARTITION-NAME -domain CLONING-DOMAIN
```
Where:

* `PARTITION-NAME` is the name you give the partition.

* `CLONING-DOMAIN` is the cloning domain of the HSM.

2. Create a password for the partition. The partition password must be the same for all partitions in the highly available partition group.

3. To retrieve the partition serial number, run:
```
lunash:> partition show -partition PARTITION-NAME
```
Where `PARTITION-NAME` is the name of the partition you created.

4. Record the `Partition SN` shown in the output of the command you ran in the previous step.

## Creating and registering HSM clients
Clients that communicate with the HSM must provide a client certificate to establish a client authenticated session. You must set up each client certificate on the HSM and assign access rights for your partition.

### Establishing a network trust link between client and HSMs
To establish a network trust link between a client and your HSMs:

1. Create a certificate for the client by running:
```
openssl req \

-x509 \

-newkey rsa:4096 \

-days NUMBER-OF-DAYS \

-sha256 \

-nodes \

-subj "/CN=CLIENT-HOSTNAME-OR-IP" \

-keyout CLIENT-HOSTNAME-OR-IP.pem \

-out CLIENT-HOSTNAME-OR-IP.pem
```
Where:

* `NUMBER-OF-DAYS` is the number of days you want the network trust link to be valid.

* `CLIENT-HOSTNAME-OR-IP` is the hostname or IP address of the client.

2. Copy the client certificate to your HSM by running:
```
scp -i path/to/ssh-key.pem \
CLIENT-HOSTNAME-OR-IP.pem \
manager@HSM-IP:CLIENT-HOSTNAME-OR-IP.pem
```
Where `CLIENT-HOSTNAME-OR-IP` is the hostname or IP address of the client.

### Registering HSM client host and partitions
To register a client host and partitions for your HSM:

1. Create a client by running:
```
lunash:> client register -client CLIENT-NAME -hostname CLIENT-HOSTNAME
```
Where:

* `CLIENT-NAME` is the name of the client.

* `CLIENT-HOSTNAME` is the hostname of your planned CredHub instances.

2. (Optional) If you are only planning to run one CredHub instance, you can also register a client with the planned CredHub IP address by running:
```
lunash:> client register -client CLIENT-NAME -ip CLIENT-IP-ADDRESS
```
Where:

* `CLIENT-NAME` is the name of the client.

* `CLIENT-IP-ADDRESS` is the IP address of your planned CredHub instance.

3. Assign the partition that you created in the previous section to the client by running:
```
lunash:> client assignPartition -client CLIENT-NAME -partition PARTITION-NAME
```
Where:

* `CLIENT-NAME` is the name of the client.

* `PARTITION-NAME` is the name of the partition you created.

## Setting HSM encryption keys
You can set which key is used for encryption operations by defining the encryption key name in the deployment manifest file. By default, a key that exists on the HSM is used for encryption operations. If a key does not exist on the HSM, CredHub creates it automatically in the referenced partition.
When you generate a new key, review the list of keys on each HSM to validate that key replication is occurring. If new keys do not propagate among the HSMs, you can get locked out of the HSMs.
To review stored keys on a partition:

1. Run:
```
lunash:> partition showContents -partition PARTITION-NAME
```
Where `PARTITION-NAME` is the name of the partition on which your keys are stored.

## Getting ready for deployment
Now you can deploy CredHub with your new HSMs.
Edit your manifest file as shown here:
```
credhub:
properties:
encryption:
keys:

- provider_name: primary
encryption_key_name: ENCRYPTION-KEY-NAME
active: true
providers:

- name: primary
type: hsm
partition: PARTITION-NAME
partition_password: PARTITION-PASSWORD
client_certificate: CLIENT-CERTIFICATE
client_key: CLIENT-PRIVATE-KEY
servers:

- host: 10.0.0.1
port: 1792
certificate: HSM-CERTIFICATE
partition_serial_number: PARTITION-SERIAL-NUMBER

- host: 10.0.0.10
port: 1792
certificate: HSM-CERTIFICATE
partition_serial_number: PARTITION-SERIAL-NUMBER
```
Where:

* `ENCRYPTION-KEY-NAME` is the encryption key you set in [Setting HSM encryption keys](https://docs.cloudfoundry.org/credhub/hsm-config.html#hsm-encryption-keys).

* `PARTITION-NAME` is the name of the partition you created in [Creating the HSM partition](https://docs.cloudfoundry.org/credhub/hsm-config.html#create-hsm-partition).

* `PARTITION-PASSWORD` is the password of the partition you created in [Creating the HSM Partition](https://docs.cloudfoundry.org/credhub/hsm-config.html#create-hsm-partition).

* `CLIENT-CERTIFICATE` is the client certificate you created in [Establishing a network trust link between client and HSMs](https://docs.cloudfoundry.org/credhub/hsm-config.html#establish-network-trust-link).

* `CLIENT-PRIVATE-KEY` is the private key you created in [Establishing a network trust link between client and HSMs](https://docs.cloudfoundry.org/credhub/hsm-config.html#establish-network-trust-link).

* `HSM-CERTIFICATE` is one of the HSM certificates you retrieved in [Retrieving the HSM certificate](https://docs.cloudfoundry.org/credhub/hsm-config.html#retrieve-hsm-certificate).

* `PARTITION-SERIAL-NUMBER` is the partition serial number you retrieved in [Creating the HSM partition](https://docs.cloudfoundry.org/credhub/hsm-config.html#create-hsm-partition).

## Renewing or rotating a client certificate
The generated client certificate has a fixed expiration date. After expiration the HSM no longer accepts it.
To rotate or renew this certificate at any time:

1. Generate a new certificate for the client by running:
```
openssl req \

-x509 \

-newkey rsa:4096 \

-days NUMBER-OF-DAYS \

-sha256 \

-nodes \

-subj "/CN=CLIENT-HOSTNAME-OR-IP" \

-keyout CLIENT-HOSTNAME-OR-IPKey.pem \

-out CLIENT-HOSTNAME-OR-IP.pem
```
Where:

* `NUMBER-OF-DAYS` is the number of days you want the network trust link to be valid.

* `CLIENT-HOSTNAME-OR-IP` is the hostname or IP address of the client.

2. Copy the client certificate to each HSM by running:
```
scp -i path/to/ssh-key.pem \
CLIENT-HOSTNAME-OR-IP.pem \
manager@HSM-IP:CLIENT-HOSTNAME-OR-IP.pem
```
Where `CLIENT-HOSTNAME-OR-IP` is the hostname or IP address of the client.

3. (Optional) Review the client’s partition assignments by running:
```
lunash:> client show -client CLIENT-NAME
```
Where `CLIENT-NAME` is the name of the client.

4. Remove the existing client by running:
```
lunash:> client delete -client CLIENT-NAME
```
Where `CLIENT-NAME` is the name of the client.

**Important**
When you remove the existing client, all partition assignments are deleted.

5. Register the client again by running:
```
lunash:> client register -client CLIENT-NAME -ip CLIENT-IP
```
Where:

* `CLIENT-NAME` is the name of the client.

* `CLIENT-IP` is the IP address of the client.

6. Assign the partition assignments again by running:
```
lunash:> client assignPartition -client CLIENT-NAME -partition PARTITION-NAME
```
Where:

* `CLIENT-NAME` is the name of the client.

* `PARTITION-NAME` is the name of the partition to which the client is assigned.

7. (Optional) Validate the new certificate fingerprint by running:
```
lunash:> client fingerprint -client CLIENT-NAME
```
Where `CLIENT-NAME` is the name of the client.
If you need to, you can compare the fingerprint to your locally stored certificate by running:
```
openssl x509 -in clientcert.pem -outform DER | md5sum
```