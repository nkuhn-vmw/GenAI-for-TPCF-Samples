# Tanzu GPT: Python Edition

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
➜  ~ cf create-service postgres on-demand-postgres-db tanzu-gpt-postgres
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

