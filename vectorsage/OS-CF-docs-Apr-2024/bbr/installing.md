# Installing BOSH Backup and Restore (BBR)
This topic describes how to install BOSH Backup and Restore (BBR).
To use BBR, you must be able to connect to a VM on the BOSH internal network so
that BBR can access your BOSH deployment or BOSH Director.
Usually, this VM is a jumpbox deployment from which you can run BBR commands.
For more information, see [Backing up with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/backup.html)
and [Restoring with BOSH Backup and Restore](https://docs.cloudfoundry.org/bbr/restore.html).

## Prerequisite
A jumpbox is a separate, hardened VM on your network that provides a controlled
means of access to the VMs other computers on your network.
For an example jumpbox deployment, see the
[jumpbox-deployment](https://github.com/cloudfoundry/jumpbox-deployment) GitHub repository.

## Step 1: Configure your jumpbox
Configure your jumpbox to meet the following requirements:

* Your jumpbox must be able to communicate with the network that contains your BOSH deployment.

* Your jumpbox must have sufficient space for the backup.

* Your jumpbox must be in the same network as the deployed VMs because BBR connects to the VMs at their private IP addresses.

* BBR copies the backed-up data from the VMs to the jumpbox, so you should have minimal network latency between the VMs and the jumpbox to reduce transfer times.
Consult the following table for more information about the network access permissions required by BBR.
| VM | Default port | Description |
| --- | --- | --- |
| BOSH Director | 25555 | BBR interacts with the BOSH Director API. |
| Deployed instances | 22 | BBR uses SSH to orchestrate the backup on the instances. |
| BOSH Director UAA | 8443 | BBR interacts with the UAA API for authentication, if necessary. |

## Step 2: Transfer BBR to your jumpbox
If you run your BBR command from the jumpbox, perform the following
steps to transfer the `bbr` binary to your jumpbox:

1. Download the latest BBR release from the
[bosh-backup-and-restore](https://github.com/cloudfoundry-incubator/bosh-backup-and-restore/releases) GitHub repository.

2. Extract the `bbr` binary file from the BBR release.

3. To add executable permissions to the `bbr` binary file, run `chmod a+x bbr`:
```
$ chmod a+x bbr
```

4. To securely copy the `bbr` binary file to your jumpbox, run:
```
scp LOCAL-PATH-TO-BBR/bbr JUMPBOX-USER/JUMPBOX-ADDRESS
```
If your jumpbox has access to the internet, you can also SSH into your jumpbox and use `wget`:
```
$ ssh JUMPBOX-USER/JUMPBOX-ADDRESS -i YOUR-CERTIFICATE.pem
$ wget BBR-RELEASE-URL
$ chmod a+x bbr
```