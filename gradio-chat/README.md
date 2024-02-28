# Gradio Chat

This is a simple python sample application to be used in Cloud Foundry and Tanzu Application Service.

It makes use of the new GenAI for TAS tile to offer a simple chat style application.

In order to get started with this application, query your Tanzu Application Service marketplace:
~~~
➜  ~ cf marketplace
Getting all service offerings from marketplace in org kuhn-labs / space genai-samples as admin...

offering                plans                                  description                                                                                                                                                                                                                   broker
app-autoscaler          standard                               Scales bound applications in response to load                                                                                                                                                                                 app-autoscaler
postgres                on-demand-postgres-db                  Postgres service to provide on-demand dedicated instances configured as database.                                                                                                                                             postgres-odb                                                                                                                                                            p-dataflow                                                                                                                                                                                                          scheduler-for-pcf
genai-service           shared-ai-plan                         The GenAI for TAS service provides access to the on-demand creation of an Open API-compatible endpoint and Large Language Model.                                                                                              genai-service
~~~

Gradio Chat will require GenAI for TAS to start correctly.

Provision the GenAI service:

Create a service instance for the GenAI for TAS "shared-ai-plan" - using the service name `gradio-chat-genai-service`

~~~
 ~ cf create-service genai-service shared-ai-plan gradio-chat-genai-service
Creating service instance gradio-chat-genai-service in org kuhn-labs / space homelab as admin...

Service instance gradio-chat-genai-service created.
OK
~~~

Now that the services have been provisioned, go ahead and push the application.

~~~
 ~ cf push
Pushing app gradio-chat to org kuhn-labs / space genai-samples as admin...
Applying manifest file /Users/nkuhn/Documents/tanzu-ai-samples/gradio-chat/manifest.yml...

Updating with these attributes...
  ---
  applications:
  - name: gradio-chat
    memory: 1G
+   default-route: true
+   buildpack: python_buildpack
    services:
      gradio-chat-genai-service
Manifest applied
Packaging files to upload...
Uploading files...
 2.28 KiB / 2.28 KiB [===========================================================================================================================================================================================================================================================================] 100.00% 1s

Waiting for API to complete processing files...

Staging app and tracing logs...
   Downloading python_buildpack...
...
...
...
 Uploading complete
   Cell 29b55d6b-c415-47fe-871a-e58735030ef0 stopping instance 14f87c7d-8417-48b4-ab03-d32933d30073
   Cell 29b55d6b-c415-47fe-871a-e58735030ef0 destroying container for instance 14f87c7d-8417-48b4-ab03-d32933d30073

Waiting for app gradio-chat to start...

Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...
Instances starting...

name:              gradio-chat
requested state:   started
routes:            gradio-chat.apps.tas-kdc.kuhn-labs.com
last uploaded:     Wed 28 Feb 00:44:53 EST 2024
stack:             cflinuxfs4
buildpacks:
	name               version   detect output   buildpack name
	python_buildpack   1.8.15    python          python

type:            web
sidecars:
instances:       1/1
memory usage:    1024M
start command:   python app.py
     state     since                  cpu    memory        disk       logging         details
#0   running   2024-02-28T05:45:20Z   0.0%   42.7K of 1G   8K of 1G   9B/s of 16K/s
~~~


Now that the application is up and running you should be good to go!