# Deploying BOSH on GCP
This topic describes how to use the [bosh-bootloader](https://github.com/cloudfoundry/bosh-bootloader)
command-line tool to set up an environment for Cloud Foundry on Google Cloud
Platform (GCP) and deploy a [BOSH Director](https://bosh.io/docs/bosh-components.html#director).

## Overview
After completing this topic, you will have the following:

1. A BOSH Director instance

2. A bastion instance

3. A set of randomly generated BOSH Director credentials

4. A generated key pair that allows you to SSH into the BOSH Director and any instances that BOSH deploys

5. A copy of the manifest used to deploy the BOSH Director

**Note**: A [manifest](https://bosh.io/docs/deployment-manifest.html) is a YAML file that defines the components and properties of a BOSH deployment.

6. A basic cloud config

**Note**: A [cloud config](https://bosh.io/docs/cloud-config.html) is a YAML file that defines IaaS-specific configuration for BOSH.

7. A set of load balancers

**Note**: bosh-bootloader creates the load balancers, but you must still configure DNS to point your domains to the load balancers. See the [Setting Up DNS for Your Environment](https://docs.cloudfoundry.org/deploying/common/dns_prereqs.html) topic for more information.

## Step 1: Download Dependencies
Perform the following steps to download the required dependencies for bosh-bootloader:

1. Download [Terraform](https://www.terraform.io/downloads.html) v0.9.1 or later. Unzip the file and move it to somewhere in your PATH:
```
$ unzip ~/Downloads/terraform*
$ sudo mv ~/Downloads/terraform /usr/local/bin/terraform
```

2. Download [BOSH CLI v2+](https://bosh.io/docs/cli-v2.html#install). Make the binary executable and move it to somewhere in your PATH:
```
$ chmod +x ~/Downloads/bosh-cli-*
$ sudo mv ~/Downloads/bosh-cli-* /usr/local/bin/bosh
```

3. Perform one of the following procedures to download and install bosh-bootloader:

* On Mac OS X, use Homebrew:
```
$ brew install cloudfoundry/tap/bbl
```

* Download the latest bosh-bootloader from [GitHub](https://github.com/cloudfoundry/bosh-bootloader/releases/latest). Make the binary executable and move it to somewhere in your PATH:
```
$ chmod +x ~/Downloads/bbl-*
$ sudo mv ~/Downloads/bbl-* /usr/local/bin/bbl
```

4. Download and install the [gcloud CLI](https://cloud.google.com/sdk/downloads).

## Step 2: Create an IAM Service Account
Perform the following steps to create the Identity and Access Management (IAM) service account that bosh-bootloader needs to interact with GCP:

1. If you installed the gcloud CLI for the first time, initialize it:
```
$ gcloud init
```

2. Create the IAM service account for bosh-bootloader with the gcloud CLI:
```
$ gcloud iam service-accounts create bbl-user --display-name "BBL"
```

3. Navigate to the GCP Console and under **Project info**, retrieve your **Project ID**.

4. Create keys for the service account, replacing `YOUR-PROJECT-ID` with the project ID you retrieved in the previous step:
```
$ gcloud iam service-accounts keys create \

--iam-account='bbl-user@YOUR-PROJECT-ID.iam.gserviceaccount.com' \
bbl-user.key.json
```
This command outputs a `bbl-user.key.json` file. Store this file in a safe and secure place.

5. Add the Editor role to the service account:
```
$ gcloud projects add-iam-policy-binding YOUR-PROJECT-ID \

--member='serviceAccount:bbl-user@YOUR-PROJECT-ID.iam.gserviceaccount.com' \

--role='roles/editor'
```

## Step 3: Create Infrastructure, Bastion, BOSH Director, and Load Balancers
Run the following command to create the required infrastructure,
deploy a bastion, deploy a BOSH director and create load balancers
for Cloud Foundry:
```
$ bbl plan \

--iaas gcp \

--gcp-service-account-key PATH-TO/bbl-user.key.json \

--gcp-region YOUR-GCP-REGION \

--lb-type cf \

--lb-cert YOUR-CERT.crt \

--lb-key YOUR-KEY.key \

--lb-domain YOUR-SYSTEM-DOMAIN
$ bbl up
```
Replace the placeholders as follows:

* `PATH-TO` is the path to the `bbl-user.key.json` file, created in the previous section.

* `YOUR-GCP-REGION` is your GCP region, such as `us-central1`.

* `YOUR-CERT.crt` and `YOUR-KEY.key` are the path to your Certificate Authority (CA) certificate and key. This enables SSL/TLS termination at your load balancer.

* `YOUR-SYSTEM-DOMAIN` is the DNS domain name for your Cloud Foundry instance. Cloud Foundry uses this domain name when deploying apps. For example, if you select the name `cloud.example.com`, Cloud Foundry deploys each of your apps as `APP-NAME.cloud.example.com`.
The `bbl up` command takes five to eight minutes to complete.
When `bbl plan` or `bbl up` is run, files in the `--state-dir` (or present working
directory) will be created, modified, or deleted.

**Note**: The **bbl state directory**
contains credentials and other metadata related to your BOSH Director and
infrastructure. Back up this directory and store it in a safe location.
To extract information from the bbl state, use `bbl`.
For example, to obtain your BOSH Director address, run the following command:
```
$ bbl director-address
https://YOUR-DIRECTOR-ADDRESS
```
Run `bbl` to see the full list of values from the state file that you can print.
You must always run `bbl` from the directory that contains `bbl-state.json`.
For test and development environments, you can also generate your own
CA certificate and key with a tool such as [certstrap](https://github.com/square/certstrap).

## Step 4: Update DNS Records
The `--lb-*` flags create an NS record in Google’s CloudDNS. You can view
this record by navigating to the [GCP Console](https://console.cloud.google.com/) and selecting **Networking > Cloud DNS**.
The data associated with the record will have the following format:
```
ns-cloud-e1.googledomains.com.
ns-cloud-e2.googledomains.com.
...
```
From your domain registrar, delegate DNS authority for your hosted zone to the
four CloudDNS name servers. To do this, replace your registrar’s NS records for
the domain with the NS record values listed in CloudDNS.
After a few minutes, your system domain should resolve to your GCP load balancer.

## Step 5: Connect to the BOSH Director
Run the following to connect to the BOSH Director:
```
$ eval "$(bbl print-env)"
```

## Destroy the BOSH Resources
You can use `bbl destroy` to delete the BOSH Director infrastructure in your GCP environment.
Use this command if `bbl up` does not complete successfully and you want to reset your environment,
or if you want to destroy the resources created by bosh-bootloader for any other reason.
To delete load balancers only:
```
$ bbl plan
$ bbl up
```
To delete the infrastructure, bastion, director, and load balancers:
```
$ bbl destroy
```