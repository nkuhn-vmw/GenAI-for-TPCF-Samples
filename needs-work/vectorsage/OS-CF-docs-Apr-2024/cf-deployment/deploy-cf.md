# Deploying Cloud Foundry
This topic describes how to deploy Cloud Foundry
using `cf-deployment`.
Before performing this procedure,
ensure you have prepared your environment
and deployed a BOSH Director.
For more information,
see the [Prepare Your Environment](https://docs.cloudfoundry.org/deploying/cf-deployment/#prepare) section
of the *Deploying Cloud Foundry with cf-deployment* topic.

## Step 1: Clone cf-deployment
Clone the `cf-deployment` repository:
```
$ git clone https://github.com/cloudfoundry/cf-deployment.git
```
This repository contains the canonical manifest for deploying Cloud Foundry, along with various ops files that specify operations to perform on the Cloud Foundry deployment manifest.

## Step 2: Select Your Ops Files
Use ops files to specify IaaS-specific configuration and to add custom
functionality to your Cloud Foundry deployment. Before deploying, BOSH reads the
ops files from the `operations` folder and applies the operations to your manifest.
All ops files are located in the [operations](https://github.com/cloudfoundry/cf-deployment/tree/master/operations) directory of the `cf-deployment` repository.
The following configurations require ops files:

* Deploying Cloud Foundry to any IaaS except Google Cloud Platform (GCP)

* Deploying Windows Diego cells to Cloud Foundry
To determine which ops files your IaaS requires, see the [IaaS-required Ops-files](https://github.com/cloudfoundry/cf-deployment/tree/master/operations#iaas-required-ops-files) table in the `cf-deployment`
repository.
To deploy Windows Diego Cells, use the [windows2019-cell.yml](https://github.com/cloudfoundry/cf-deployment/blob/main/operations/windows2019-cell.yml) ops file.
See the [Ops Files](https://github.com/cloudfoundry/cf-deployment#ops-files) section of the `cf-deployment` repository README for a description of all available ops files.

## Step 3: Determine Variables
`cf-deployment` requires additional information to provide environment-specific or sensitive configuration.
The BOSH CLI stores this information in a variables store file, which is provided by the operator with the `--vars-store` flag when [deploying Cloud Foundry](https://docs.cloudfoundry.org/deploying/cf-deployment/deploy-cf.html#deploy). This flag takes the name of a YAML file that the BOSH CLI will read and write to. If the file does not exist, the BOSH CLI will create it. If necessary credential values are not present, the BOSH CLI will generate new values based on the type information stored in `cf-deployment.yml.`
There are certain variables that BOSH cannot generate. By default, this is only the system domain. But depending on the ops files you have selected, you may need to provide variables in addition to the system domain.
Perform the following steps to determine your required variables and prepare them for the deploy:

1. Review the information in the [Step 2: Select Your Ops Files](https://docs.cloudfoundry.org/deploying/cf-deployment/deploy-cf.html#ops-files) section and create a list of the variables required by the ops files you have selected.

2. Determine the values for each of the variables. For example, the `aws_region` variable required by the `use-s3-blobstore.yml` ops file may have the value of `us-west-2`.

3. Choose one of the following methods for providing the variables when you [deploy Cloud Foundry](https://docs.cloudfoundry.org/deploying/cf-deployment/deploy-cf.html#deploy) below:

* Provide the variables in a YAML file specified with the `--vars-file` flag during the deploy. This is the recommended method for configuring external persistence services.

* Provide the variables by passing individual `-v` arguments for each variable. The syntax is `-v VAR-NAME=VAR-VALUE`.

**Note**: Variables passed with either `-v` or `--vars-file` will override those already in the var store, but will not be stored there.

* Insert the variables directly in the variables store file alongside BOSH-managed variables.

## Step 4: Upload Stemcell

1. Ensure you are logged in to your BOSH Director:
```
$ bosh -e YOUR-ENV log-in
```

2. Open the Cloud Foundry deployment manifest, `cf-deployment.yml`. In the final lines of the deployment manifest, locate the top-level property `stemcells` and retrieve the values for `os` and `version`. The following example specifies an Ubuntu Trusty 3421.11 stemcell:
```
stemcells:

- alias: default
os: ubuntu-trusty
version: "3421.11"
```
The following example specifies a Windows Server, version 1709 stemcell:
```
stemcells:

- alias: windows2016
os: windows2016
version: "1709.13"
```

3. Visit [Stemcells](https://bosh.io/stemcells) on bosh.io.

4. Locate the stemcell that corresponds to your IaaS and to the version specified above, and copy the URL to the stemcell.

5. Upload the stemcell:
```
$ bosh upload-stemcell YOUR-STEMCELL-URL
```

## Step 5: Deploy

1. Deploy `cf-deployment`:
```
$ bosh -e YOUR-ENV -d cf deploy cf-deployment/cf-deployment.yml \

--vars-store env-repository/deployment-vars.yml \

-v system_domain=YOUR-SYSTEM-DOMAIN \

-o cf-deployment/operations/YOUR-OPS-FILE-1

-o cf-deployment/operations/YOUR-OPS-FILE-2
[...]
```
Depending on your choices in the [Step 3: Determine Variables](https://docs.cloudfoundry.org/deploying/cf-deployment/deploy-cf.html#determine-vars) section, provide additional variables with `-v` or `--vars-file`.
If your variables store file does not exist, BOSH creates one at the path you specify with `--vars-store`. Store your variables store file in a safe and secure place. You will need it for all subsequent deploys.
When prompted to review the deployment manifest, enter `y` to continue.
The deploy may take several minutes. When the command completes, run `bosh vms` to check that the Cloud Foundry VMs are running.