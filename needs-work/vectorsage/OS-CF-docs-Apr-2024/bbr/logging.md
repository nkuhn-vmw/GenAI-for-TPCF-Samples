# BBR logging
This topic provides information about BBR logging. Use this information when troubleshooting a failed backup or restore using BBR.
By default, BBR displays:

* The backup and restore scripts that it finds

* When it starts or finishes a stage, such as `pre-backup scripts` or `backup scripts`

* When the process is complete

* When any error occurs
BBR writes any errors associated with stack traces to a file in the form of `bbr-TIMESTAMP.err.log` in the current directory.
If more logging is needed, use the optional `--debug` flag to print the following information:

* Logs about the API requests made to the BOSH server

* All commands executed on remote instances

* All commands executed on local environment

* stdout and stderr streams for the backup and restore scripts when they are executed