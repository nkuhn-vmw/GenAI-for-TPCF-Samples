# Troubleshooting CredHub
You can resolve errors that might occur when you deploy, upgrade, or interact with CredHub.

## Deployment failures
CredHub deployment failures include:

* Configuration errors

* Pre-start errors

* Post-start errors
For additional information about troubleshooting CredHub deployment failures,
see [Error list](https://github.com/pivotal-cf/credhub-release/blob/master/docs/troubleshooting-guide.md#error-list) in *Troubleshooting Guide* in the CredHub repository on GitHub.

### Configuration errors
Configuration errors occur before CredHub deploys.
For example:
```
Using deployment 'credhub'
Evaluating manifest:
yaml: line 63: could not find expected ':'
Exit code 1
```
Configuration errors start with `yaml` and occur before the BOSH task is created. They indicate an
error in parsing your manifest.
To correct a configuration error, review the structure of your manifest at the line specified in the
error message to ensure the format and indentation are valid.
Additionally, you might see the following error format:
```
Task 474
18:20:35 | Preparing deployment: Preparing deployment (00:00:13)
18:20:52 | Error: Unable to render instance groups for deployment. Errors are:

- Unable to render jobs for instance group 'credhub'. Errors are:

- Unable to render templates for job 'credhub'. Errors are:

- Error filling in template 'application.yml.erb' (line 22: Can't find property '["credhub.data_storage.type"]')
Started Thu Jan 26 18:20:35 UTC 2019
Finished Thu Jan 26 18:20:52 UTC 2019
Duration 00:00:17
Task 474 error
Updating deployment:
Expected task '474' to succeed but was state is 'error'
Exit code 1
```
This error occurs when a required field is not defined in the manifest. In the previous example,
the following configuration value is missing:
```
Can't find property '["credhub.data_storage.type"]'
```
Missing or invalid values might cause another similar error:
```
Task 697
21:27:55 | Preparing deployment: Preparing deployment (00:00:14)
21:28:13 | Error: Unable to render instance groups for deployment. Errors are:

- Unable to render jobs for instance group 'credhub'. Errors are:

- Unable to render templates for job 'credhub'. Errors are:

- Error filling in template 'pre-start.erb' (line 15: undefined method '[]' for nil:NilClass)
Started Thu Jan 26 21:27:55 UTC 2019
Finished Thu Jan 26 21:28:13 UTC 2019
Duration 00:00:18
Task 697 error
Updating deployment:
Expected task '697' to succeed but was state is 'error'
Exit code 1
```
When you are troubleshooting this error, use the line number and the template specified in the error message to identify the missing or invalid value.

### Pre-start errors
Pre-start errors occur when CredHub is unable to perform pre-start tasks. For example:
```
Task 789
22:34:08 | Preparing deployment: Preparing deployment (00:00:14)
22:34:26 | Preparing package compilation: Finding packages to compile (00:00:02)
22:34:28 | Updating instance dan-credhub: credhub/0261faa8-f5f4-4f6e-8ebe-3cfcba3f7190 (0) (canary) (00:00:18)
L Error: Action Failed get_task: Task c69563a2-51e7-4b10-5c64-bb084ef85863 result: 1 of 1 pre-start scripts failed. Failed Jobs: credhub.
22:34:46 | Error: Action Failed get_task: Task c69563a2-51e7-4b10-5c64-bb084ef85863 result: 1 of 1 pre-start scripts failed. Failed Jobs: credhub.
Started Thu Jan 26 22:34:08 UTC 2019
Finished Thu Jan 26 22:34:46 UTC 2019
Duration 00:00:38
Task 789 error
Updating deployment:
Expected task '789' to succeed but was state is 'error'
Exit code 1
```

#### Accessing logs
CredHub stores pre-start logs in the `/var/vcap/sys/log/credhub/pre-start.stderr.log` and `pre-start.stdout.log` files.
To access these logs when you are troubleshooting a pre-start error, you must SSH into the CredHub VM or SCP the logs from it.

### Post-start errors
Post-start errors occur when a post-start script fails. For example:
```
Task 478
20:03:32 | Preparing deployment: Preparing deployment (00:00:13)
20:03:49 | Preparing package compilation: Finding packages to compile (00:00:02)
20:03:52 | Updating instance credhub: credhub/0261faa8-f5f4-4f6e-8ebe-3cfcba3f7190 (0) (canary) (00:02:34)
L Error: Action Failed get_task: Task 5fe7ac60-4ccc-4bda-4ccb-6e88908597ef result: 1 of 1 post-start scripts failed. Failed Jobs: credhub.
20:06:27 | Error: Action Failed get_task: Task 5fe7ac60-4ccc-4bda-4ccb-6e88908597ef result: 1 of 1 post-start scripts failed. Failed Jobs: credhub.
Started Thu Jan 26 20:03:32 UTC 2019
Finished Thu Jan 26 20:06:27 UTC 2019
Duration 00:02:55
Task 478 error
Updating deployment:
Expected task '478' to succeed but was state is 'error'
Exit code 1
```

#### Accessing logs
The CredHub log is stored in the `/var/vcap/sys/log/credhub/credhub.log` file.
To access these logs when you are troubleshooting a post-start error, you must SSH into the CredHub VM or SCP the logs
from it.
The CredHub log is written according to the `log_level` variable,
specified in your manifest.
To locate the cause of the failure, search for `ERROR` in the logs. Because Monit attempts to restart a failing CredHub process, you might see multiple instances of the same error.
Additionally, you can review other log files in the `/var/vcap/sys/log/credhub` directory.

## Usability failures
Usability failures occur after a successful deployment of CredHub. If you receive an internal server error without a descriptive error message, review the CredHub log as described in [Accessing logs](https://docs.cloudfoundry.org/credhub/troubleshooting-credhub.html#app-logs).
For additional information about troubleshooting usability failures, see [Error List](https://github.com/pivotal-cf/credhub-release/blob/master/docs/troubleshooting-guide.md#error-list-1) in *Troubleshooting Guide* in the CredHub repository on GitHub.