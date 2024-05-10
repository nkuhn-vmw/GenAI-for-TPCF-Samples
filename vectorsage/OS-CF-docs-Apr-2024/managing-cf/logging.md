# Cloud Foundry logging
This section contains information for debugging Cloud Foundry system components.

## Component logging
In `cf-deployment`, the components should all be configured in a similar way:

* All of the job’s log files are located in the directory `/var/vcap/sys/log/<job-name>` of the machine on which the job is running.

* Any output written directly to the job’s stdout and stderr is written to `<job-name>.stdout.log` and `<job-name>.stderr.log`, respectively.

* Jobs might also write main logs to a file named `<job-name>.log`.

* BOSH might also write logs for different lifecycle hooks to additional file paths, see [BOSH Update Lifecycle](https://bosh.io/docs/job-lifecycle/) for more details.

## Log forwarding
BOSH VMs can be configured to forward component logs to remote syslog endpoints by applying the [enable-component-syslog.yml](https://github.com/cloudfoundry/cf-deployment/blob/main/operations/addons/enable-component-syslog.yml) ops file to a BOSH runtime config or manifest. The ops file requires some operator configuration ([example](https://github.com/cloudfoundry/cf-deployment/blob/main/operations/addons/example-vars-files/vars-enable-component-syslog.yml)), including the following variables:

* `syslog_address`: IP or DNS address of the syslog server

* `syslog_custom_rule`: Custom rsyslog rules

* `syslog_fallback_servers`: List of fallback servers to be used if the primary syslog server is down

* `syslog_permitted_peer`: Accepted fingerprint (SHA1) or name of remote peer

* `syslog_port`: Port of the syslog server
Further configuration options can be found in the [syslog\_forwarder spec](https://github.com/cloudfoundry/syslog-release/blob/main/jobs/syslog_forwarder/spec).