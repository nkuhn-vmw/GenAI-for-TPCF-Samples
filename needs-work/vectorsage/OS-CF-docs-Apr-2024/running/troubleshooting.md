# Troubleshooting Cloud Foundry
This guide provides help with diagnosing and resolving issues encountered when
installing and running Cloud Foundry.
This topic assumes you are using [BOSH CLI v2](https://bosh.io/docs/cli-v2.html).

## Troubleshoot Cloud Foundry installation issues
An installation or update can fail for reasons that have nothing to do with the
software that you are installing.
If an installation or update fails once, start over and try again.
If it fails a second time, use the following information to troubleshoot the
issue.

### Timeouts in “creating bound missing vms” phase
When deploying Cloud Foundry with BOSH, the “creating bound missing vms” phase
occurs after package compilation.
A process in the “creating bound missing vms” phase can time out if a BOSH Agent
fails to start correctly or if the Agent cannot connect to the NATS message bus.
```
. . .
Started preparing package compilation > Finding packages to compile. Done (00:00:00)
Started creating bound missing vms
Started creating bound missing vms > api_worker_z1/0. Failed: Timed out pinging to 1da06ba3de2f after 600 seconds (00:12:45)
Error 450002: Timed out pinging to 1da06ba3de2f after 600 seconds
```
Perform the following steps to determine the cause of the time out:

* [Use your IaaS console](https://docs.cloudfoundry.org/running/troubleshooting.html#boot-check) to make sure the timed-out virtual machine (VM) is booting correctly

* [Check the agent log](https://docs.cloudfoundry.org/running/troubleshooting.html#handshake) on the VM that timed out for a handshake connection
between the BOSH Director and the Agent

* [Use the Netcat networking utility](https://docs.cloudfoundry.org/running/troubleshooting.html#netcat) to test for routing
issues to the NATS IP and port from the VM that timed out

#### Use your IaaS console to make sure the timed-out VM is booting correctly
For details on how to use your IaaS console to make sure the timed out VM is
booting correctly, see your IaaS documentation.

#### Check the agent log on the VM that timed out for a handshake connection between the BOSH Director and the agent

1. Use your IaaS virtualization console to open a terminal window on the VM that
timed out and log in as root.

2. Open the `/var/vcap/bosh/log/current` log file in a text editor.

3. Search the log file for a “handshake” between the BOSH Director and the BOSH
Agent.
This connection is represented in the log as a `ping` and a `pong`:
```
. . .
2013-10-03_14:35:48.58456 #[608] INFO: Message: {"method"=>"**ping**", "arguments"=>[], reply_to"=>"director.b668-1660944090e4"}
2013-10-03_14:35:48.60182 #[608] INFO: reply_to:director.b668-1660944090e4: payload: {:value=>"**pong**"}
```

4. If the handshake does not complete, the Agent cannot communicate with the
Director.

#### Use Netcat to test for routing issues to the NATS IP

1. Use your IaaS virtualization console to open a terminal window on the VM that
timed out and log in as root.

2. Open the `/var/vcap/bosh/log/current` log file in a text editor.

3. Search the beginning of the log file for a line labeled **INFO: loaded
new infrastructure settings**.
This line contains a JSON blob of key/value pairs representing the expected
infrastructure for the BOSH Agent.
In this line, locate the IP address and port following

**nats://nats:nats@**.
```
. . .
2013-10-03_14:35:21.83222 #[608] INFO: loaded new infrastructure settings: {"vm"=>{"name"=>"vm-4d80ede4-b0a5", "id"=>"vm-360"}, {"user"=>"agent", "password"=>"agent"}}, "mbus"=>"nats://nats:nats@**192.0.2.17:4222**", "env"=>{"bosh"}}}}}
```

4. Run the [Netcat](http://nmap.org/ncat/) command `nc -v IP-ADDRESS PORT` to
determine whether it is possible to establish a connection between the NATS
message bus and this VM.
```
$ nc -v 192.0.2.17 4222
Connection to 192.0.2.17 4222 port [tcp/*] succeeded!
```

### Out of Disk Space error
If, during installation, log files fill all available disk space on a computer,
the operating system reports an “Out of Disk Space” error.
To resolve this issue, delete these log files from the `tmp` directory of the
affected computer manually or by rebooting.

## Troubleshoot Cloud Foundry operation issues
If you have not done so already, set an alias for the BOSH Director of the environment you are
troubleshooting. You need this alias to run the BOSH CLI commands in this section.
Run the following command to create a local alias for the BOSH Director using the BOSH CLI:
```
bosh alias-env MY-ENV -e DIRECTOR-IP-ADDRESS --ca-cert PATH/TO/CERT
```
Replace the placeholder text with the following:

* `MY-ENV`: Enter an alias for the BOSH Director, such as `dev` or `prod`.

* `DIRECTOR-IP-ADDRESS`: Enter the IP address of your BOSH Director VM.

* `PATH/TO/CERT`: Enter the path to the Director CA certificate.
For example:
```
$ bosh alias-env dev -e 10.0.0.3 --ca-cert /var/workspaces/default/ca_certificate
```

### Use the BOSH CLI for troubleshooting

1. Run `bosh -e MY-ENV login` and provide your credentials to log in to the BOSH Director.
Replace `MY-ENV` with the alias you set for your BOSH Director.
```
$ bosh -e dev login
User ():
Password ():
```

2. Use the following BOSH commands to troubleshoot your deployment:

* [VMs](https://docs.cloudfoundry.org/running/troubleshooting.html#vms): Lists all VMs in a deployment

* [Cloud check](https://docs.cloudfoundry.org/running/troubleshooting.html#cloudcheck): Cloud consistency check and interactive repair

* [SSH](https://docs.cloudfoundry.org/running/troubleshooting.html#ssh): Start an interactive session or execute commands with a VM

#### BOSH VMs
`bosh vms` provides an overview of the virtual machines (VMs) BOSH is managing as part of the current deployment.
To use this command, run `bosh -e MY-ENV -d MY-DEPLOYMENT vms`.
Replace `MY-ENV` with your environment, and `MY-DEPLOYMENT` with a deployment. `-d MY-DEPLOYMENT` is optional.
```
$ bosh -e prod -d cf vms
```
`bosh vms` may show a VM in an **unknown** state.
Run `bosh cloud-check` on VMs in an unknown state to have BOSH attempt to
diagnose the problem.
You can also use `bosh vms` to identify VMs in your deployment, then use
`bosh ssh` to SSH into an identified VM for further troubleshooting.
`bosh vms` supports the following arguments:

* `--vitals`: Overview also includes load, CPU, memory usage,
swap usage, system disk usage, ephemeral disk usage, and persistent disk usage
for each VM

* `--dns`: Overview also includes the DNS A record for each VM

#### BOSH cloud check
`bosh cloud-check` attempts to detect differences between the VM state database
that the BOSH Director maintains and the actual state of the VMs.
To use this command, run `bosh -e MY -d MY-DEPLOYMENT cloud-check`.
You can also use the alias `bosh cck`.
Replace `MY-ENV` with your environment, and `MY-DEPLOYMENT` with a deployment. `-d MY-DEPLOYMENT` is optional.
```
$ bosh -e dev -d mysql cck
```
For each difference detected, `bosh cloud-check` offers repair options:

* `Reboot VM`: Instructs BOSH to reboot a VM. Rebooting can resolve many
transient errors.

* `Ignore problem`: Instructs `bosh cloud-check` to do nothing.
You might want to instruct `bosh cloud-check` to ignore a problem in order to run
`bosh ssh` and attempt troubleshooting directly on the machine.

* `Reassociate VM with corresponding instance`: Updates the BOSH Director state
database.
Use this option if you believe that the BOSH Director state database is in error
and that a VM is correctly associated with a job.

* `Recreate VM using last known apply spec`: Instructs BOSH to destroy a VM and
recreate it from the deployment manifest the installer provides.
Use this option if a VM is corrupted.

* `Delete VM reference`: Instructs BOSH to delete a VM reference in the Director
state database.
If a VM reference exists in the state database, BOSH expects to find an agent
running on the VM.
Select this option only if you know this reference is in error.
Once you delete the VM reference, BOSH can no longer control the VM.

##### Example scenarios

**Unresponsive Agent**
```
$ bosh -e prod -d example-deployment cck
ccdb/0 (vm-3e37133c-bc33-450e-98b1-f86d5b63502a) is not responding:

- Ignore problem

- Reboot VM

- Recreate VM using last known apply spec

- Delete VM reference (DANGEROUS!)
```

**Missing VM**
```
$ bosh -e prod -d example-deployment cck
VM with cloud ID `vm-3e37133c-bc33-450e-98b1-f86d5b63502a' missing:

- Ignore problem

- Recreate VM using last known apply spec

- Delete VM reference (DANGEROUS!)
```

**Unbound Instance VM**
```
$ bosh -e prod -d example-deployment cck
VM vm-3e37133c-bc33-450e-98b1-f86d5b63502a' reports itself asccdb/0' but does not have a bound instance:

- Ignore problem

- Delete VM (unless it has persistent disk)

- Reassociate VM with corresponding instance
```

**Out of Sync VM**
```
$ bosh -e prod -d example-deployment cck
VM vm-3e37133c-bc33-450e-98b1-f86d5b63502a' is out of sync: expectedcf-d7293430724a2c421061: ccdb/0', got `cf-d7293430724a2c421061: nats/0':

- Ignore problem

- Delete VM (unless it has persistent disk)
```

#### BOSH SSH
Use `bosh ssh` to open secure shells into the VMs in your deployment.
To use `bosh ssh`:

1. Run `ssh-keygen -t rsa` to provide BOSH with the correct public key.

2. Accept the defaults.

3. Identify a VM to SSH into. Run `bosh -e MY-ENV -d MY-DEPLOYMENT vms` to list the VMs in the given deployment. Replace `MY-ENV` with your environment alias and `MY-DEPLOYMENT` with the deployment name.

4. Run `bosh -e MY-ENV -d MY-DEPLOYMENT ssh VM-NAME/GUID`. For example:
```
$ bosh -e dev -d cf-deployment ssh diego-cell/abcd0123-a012-b345-c678-9def01234567
```

### View BOSH logs
You can access BOSH logs by two methods:

* Using the `bosh ssh` command to access the log location

* Using the `bosh logs` command to output the logs to standard output or to a
file

#### Using the BOSH SSH command
Use `bosh ssh` to open secure shells into the VMs in your deployment, then
access the logs on the VM.
To use `bosh ssh`:

1. Run `ssh-keygen -t rsa` to provide BOSH with the correct public key.

2. Accept the defaults.

3. Identify a VM to SSH into. Run `bosh -e MY-ENV -d MY-DEPLOYMENT vms` to list the VMs in the given deployment. Replace `MY-ENV` with your environment alias and `MY-DEPLOYMENT` with the deployment name.

4. Run `bosh -e MY-ENV -d MY-DEPLOYMENT ssh VM-NAME/GUID`. For example:
```
$ bosh -e dev -d cf-deployment ssh diego-cell/abcd0123-a012-b345-c678-9def01234567
```

5. Review the `/var/vcap/bosh/log/current` log file.

#### Using the BOSH logs command
Use `bosh logs` to output BOSH logs to standard output or to a file.
To use `bosh logs`:

1. Identify a VM. Run `bosh -e MY-ENV -d MY-DEPLOYMENT vms` to list the VMs in the given deployment. Replace `MY-ENV` with your environment alias and `MY-DEPLOYMENT` with the deployment name.

2. Run `bosh -e MY-ENV -d MY-DEPLOYMENT logs VM-NAME/GUID` to view the logs from the identified VM. For example:
```
$ bosh -e dev -d cf-deployment logs diego-cell/abcd0123-a012-b345-c678-9def01234567
```

### Log in to a non-responsive BOSH VM
A VM under heavy system load can stop responding to some commands but still
function in a limited way.
If the VM does not respond to `bosh ssh`, use the following steps to open a
secure shell in a more direct manner:

1. Run `bosh -e MY-ENV -d MY-DEPLOYMENT vms` and note the IP address of the non-responsive VM.
```
$ bosh -e prod -d cf-deployment vms
```

2. Run `ssh -t vcap@IP-ADDRESS 'sh'` where IP-ADDRESS is the IP address of the
non-responsive VM.
```
$ ssh -t vcap@192.0.2.53 'sh'
```

### Terminate a BOSH SSH session
Use `~.`, entered at the beginning of a new line, to terminate a `bosh ssh` or
`ssh` session.
To terminate a `bosh ssh` or `ssh` initiated from the jumpbox or other server,
use `~~.`, entered at the beginning of a new line.
The outermost secure shell session consumes the second `~` and passes the
remaining `~.` command to the inner `ssh` session.

### Debug a failing job

1. Run `bosh -e MY-ENV -d MY-DEPLOYMENT vms` to determine which job VMs in your deployment are failing.
Note the job name and index of the failing VM.

2. Run `bosh -e MY-ENV -d MY-DEPLOYMENT ssh VM-NAME/GUID` to open a secure shell into the failing VM.

3. Run `sudo su -` to enter the root environment with root privileges.

4. Run `monit summary` to determine which processes are not running.

5. Review the log files found in `/var/vcap/sys/log/` to determine the root
cause of the process failures.
Some of these logs are formatted using steno with timestamps instead of human-formatted dates.
You can use `steno-prettify` to make the logs more human-readable.

6. Use `monit restart all` or `monit restart PROCESS` to start the processes.
Execute the following commands to set up steno-prettify in the cloudcontroller:
```
export CC_JOB_DIR=/var/vcap/jobs/cloud_controller_ng
source $CC_JOB_DIR/bin/ruby_version.sh
CC_PACKAGE_DIR=/var/vcap/packages/cloud_controller_ng
export BUNDLE_GEMFILE=$CC_PACKAGE_DIR/cloud_controller_ng/Gemfile
export HOME=/home/vcap # rake needs it to be set to run tasks
if [ -f $BUNDLE_GEMFILE ]; then
alias steno-prettify="bundle exec steno-prettify"
echo "ready to use steno-prettify alias, try steno-prettify on one of the following files:"
find /var/vcap/sys/log/ -name "*.log" | egrep -v "err|out|ctl" | xargs ls -al
else
echo "could not find Gemfile into ${STENO_DIR}:" `ls -al ${BUNDLE_GEMFILE}`
fi
```

### View Cloud Controller diagnostics
If your BOSH deployment experiences a resource spike, an infinite loop, or another undesirable performance issue, see the Cloud Controller (CC) diagnostics JSON file for debugging.
The file contains data that are unavailable in the output from [Cloud Foundry logging](https://docs.cloudfoundry.org/running/managing-cf/logging.html), including stack traces for running threads.
Follow the instructions below to SSH into the Cloud Controller VM and populate the diagnostics file with updated information.

1. Provide BOSH with the correct public key.
```
$ ssh-keygen -t rsa
```

2. Accept the defaults.

3. Begin an SSH session to the deployment.
```
$ bosh -e prod -d cf-deployment ssh diego-cell/abcd0123-a012-b345-c678-9def01234567
```

4. Enter the number corresponding to the `cloud_controller` from the list of VMs.

5. Retrieve the PID of the CC process.
```
$ cat /var/vcap/sys/run/cloud_controller_ng/cloud_controller_ng.pid
```

6. Send the user defined `USR1` signal to the CC process to populate the JSON log file for reference. This command does not terminate the CC process.
```
$ kill -USR1 CLOUD-CONTROLLER-PID
```

7. Navigate to the JSON file in the diagnostics directory to see the record of the `USR1` signal passed to your CC VM.
The value of the `cc.directories.diagnostics` property in `/var/vcap/jobs/cloud_controller_ng/config/cloud_controller_ng.yml` contains the location of the diagnostics directory.
The default location of the diagnostics directory is `/var/vcap/data/cloud_controller_ng/diagnostics`.

### Use the interactive Cloud Controller shell
The Cloud Controller jobs embeds a [pry shell](http://pryrepl.org/). This may allow users to interact with
cc\_ng classes, such as scripting some operations, or to access the cc\_db using model classes.
```
$ cd /var/vcap/jobs/cloud_controller_ng
$ bin/console
[...]
```

### Troubleshoot Cloud Foundry databases
The `postgres` BOSH job hosts the different databases used by Cloud Foundry, such as `diego`, `ccng`, and `uaadb`. If the `postgres` job reaches 100% persistent disk usage, it can impact performance. Perform the following steps to diagnose your `postgres` job:

1. Retrieve the credentials for the `postgres` job from your BOSH manifest.

2. Connect to the database using the PostgreSQL client of your choice. Alternatively, you can connect to the database using a PostgreSQL web interface such as [phppgadmin-cf](https://github.com/cloudfoundry-community/phppgadmin-cf/) or open an SSH tunnel to the database using `cf ssh`.

3. Use the following SQL query to identify the largest schema:
```
SELECT schema_name,
pg_size_pretty(sum(table_size)::bigint),
(sum(table_size) / pg_database_size(current_database())) * 100
FROM (
SELECT pg_catalog.pg_namespace.nspname as schema_name,
pg_relation_size(pg_catalog.pg_class.oid) as table_size
FROM pg_catalog.pg_class
JOIN pg_catalog.pg_namespace ON relnamespace = pg_catalog.pg_namespace.oid
) t
GROUP BY schema_name
ORDER BY schema_name
```

4. Using the output from the above query, identify the largest table.

### Force a VM recreate
If BOSH or an operator identifies a VM as corrupted, BOSH can recreate the VM.
This recreation function can fail if a drain script on the VM is broken or times
out.
To resolve this issue:

1. SSH into the VM and use the `sv stop agent` command to stop the BOSH Agent.
```
$ bosh -e dev -d cf-deployment ssh diego-cell/abcd0123-a012-b345-c678-9def01234567
$ sv stop agent
```

2. Let the BOSH Health Monitor automatically restart the VM.
To follow the status of this process:

* Run `bosh -e MY-ENV tasks` to determine the task ID of the “scan and fix” task.
Add `-d MY-DEPLOYMENT` to view tasks for a specific deployment.
```
$ bosh -e dev -d cf-deployment tasks
```

* Run `bosh -e MY-ENV task TASK-ID` with the task ID of the “scan and fix” task.
```
$ bosh -e dev task 83
```