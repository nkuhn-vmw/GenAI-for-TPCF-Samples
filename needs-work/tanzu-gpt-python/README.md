# Tanzu GPT: Python Edition

**Please note: This Application has been updated to work with the GenAI for TPCF tile versions 0.4.0 and higher.**
**You will need to update  INPUT_MODEL on the manifest.yml file to match a model you have deployed on the GenAI tile.**
**This assumes you are using ollama as a model provider**

This is a simple python sample application to be used in Cloud Foundry and Tanzu Application Service. It makes use of the new GenAI for TAS tile as well as the Tanzu Postgres tile to offer chatbot style workflows with full pgvector embedding support.

In order to get started with this application, query your Tanzu Application Service marketplace:
~~~
➜  ~ cf marketplace
Getting all service offerings from marketplace in org kuhn-labs / space genai-samples as admin...

offering                plans                                  description                                                                                                                                                                                                                   broker
app-autoscaler          standard                               Scales bound applications in response to load                                                                                                                                                                                 app-autoscaler
postgres                on-demand-postgres-db                  Postgres service to provide on-demand dedicated instances configured as database.                                                                                                                                             postgres-odb                                                                                                                                                            p-dataflow                                                                                                                                                                                                          scheduler-for-pcf
genai-service           shared-ai-plan                         The GenAI for TAS service provides access to the on-demand creation of an Open API-compatible endpoint and Large Language Model.                                                                                              genai-service
~~~

Tanzu GPT will require both a postgres database and LLM via GenAI for TAS to start correctly.

Provision these services:

Create a postgres database to use for pgvector embeddings - using the service name `tanzu-gpt-postgres`

~~~
 ~ cf create-service postgres on-demand-postgres-db tanzu-gpt-postgres
Creating service instance tanzu-gpt-postgres in org kuhn-labs / space homelab as admin...
OK
~~~

Create a service instance for the GenAI for TAS "shared-ai-plan" - using the service name `tanzu-gpt-genai-service`

~~~
 ~ cf create-service genai-service shared-ai-plan tanzu-gpt-genai-service
Creating service instance tanzu-gpt-genai-service in org kuhn-labs / space homelab as admin...

Service instance tanzu-gpt-genai-service created.
OK
~~~

Now that the services have been provisioned, go ahead and push the application.

~~~
 ~ cf push
Pushing app tanzu-gpt-python to org kuhn-labs / space genai-samples as admin...
Applying manifest file /Users/nkuhn/Documents/tanzu-ai-samples/tanzu-gpt-python/manifest.yml...

Updating with these attributes...
  ---
  applications:
  - name: tanzu-gpt-python
    memory: 1G
+   default-route: true
+   buildpack: python_buildpack
    services:
      tanzu-gpt-postgres
      tanzu-gpt-genai-service
Manifest applied
Packaging files to upload...
Uploading files...
....
....
....
Exit status 0
   Uploading droplet, build artifacts cache...
   Uploading droplet...
   Uploading build artifacts cache...
   Uploaded build artifacts cache (111.7M)

Waiting for app tanzu-gpt-python to start...

Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...

name:              tanzu-gpt-python
requested state:   started
routes:            tanzu-gpt-python.apps.tas-kdc.kuhn-labs.com
last uploaded:     Wed 28 Feb 00:34:42 EST 2024
stack:             cflinuxfs4
buildpacks:
	name               version   detect output   buildpack name
	python_buildpack   1.8.15    python          python

type:            web
sidecars:
instances:       1/1
memory usage:    1024M
start command:   streamlit run app.py --server.port 8080 --server.enableCORS false
     state     since                  cpu    memory        disk           logging          details
#0   running   2024-02-28T05:35:10Z   0.0%   67.7M of 1G   682.8M of 1G   56B/s of 16K/s
~~~


Now that the application is up and running you should be good to go!

