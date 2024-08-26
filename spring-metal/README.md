# Demo of Tanzu platform and SpringAI

![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.1.2-brightgreen.svg)
![AI LLM](https://img.shields.io/badge/AI-LLM-blue.svg)
![PostgreSQL](https://img.shields.io/badge/postgres-15.1-red.svg)
![Tanzu](https://img.shields.io/badge/tanzu-platform-purple.svg)

This repository contains artifacts necessary to build and run generative AI applications using Spring Boot and Tanzu Platform. The instructions below cover setup for both Cloud Foundry (cf) and Kubernetes (k8s) environments.

## Architecture

![Alt text](https://github.com/0pens0/spring-metal/blob/main/image.png?raw=true "Spring-metal AI topology")

## Prerequisites
- Ensure you have the latest version of the Tanzu CLI installed.
- Access to a Route53 domain and necessary AWS permissions.
- Configured egress settings (closed by default) to connect to external services.


## Installation

### Cloud Foundry Runtime

#### Preperations
Update the following in ```demo.sh``` according to your TPCF configurations

```bash
PGVECTOR_SERVICE_NAME="vector-db"
PGVECTOR_PLAN_NAME="on-demand-postgres-db"
PGVECTOR_EXTERNAL_PORT=1025 # Need TCP Router on the TPCF foundation enabled, and Service Gateways on the Postgres tile enabled.  Choose an available port 

GENAI_CHAT_SERVICE_NAME="genai-chat" 
GENAI_CHAT_PLAN_NAME="meta-llama/Meta-Llama-3-8B-Instruct" # plan must have chat capabilty

GENAI_EMBEDDINGS_SERVICE_NAME="genai-embed" 
GENAI_EMBEDDINGS_PLAN_NAME="nomic-embed-text" # plan must have Embeddings capabilty
```

#### Build

```bash
mvn clean package -DskipTests
```

#### Deployment
Run the demo script to create all services and push the spring-metal application

```bash
cf login -u admin -p YOUR_CF_ADMIN_PASSWORD
cf target -o YOUR_ORG -s YOUR_SPACE

./demo.sh cf
```
Notes:
- if your Cloud Foundry Runtime srrvices are hosted on a private network, you will need to create or update your postgres service with the TCP Router and Service instance gateway.  [Documentation](https://docs.vmware.com/en/VMware-Tanzu-Postgres-for-Tanzu-Application-Service/1.1/postgres/create-service-gateway-instance.html)
- The contents of your Kubernetes service secret can be viewed through the service key.  
  
### Kubernetes Runtime

#### Preperations

- Ensure the CF runtime services are installed and your CF CLI is targeted to the org/space you used above.
- Ensure you're logged into the tanzu platform and your kubernetes context is set to your space
- Template the Kubernetes services and bindings

```bash
tanzu login
tanzu context use <my-context>
tanzu project use <my-project>
tanzu space use <my-space>
export KUBECONFIG=~/.config/tanzu/kube/config 
./demo.sh prepare-k8s
```

#### Deployment - all in one

```bash

./demo.sh k8s
```

#### Deployment - step by step

##### Build

Follow these commands to build your application:

```bash
tanzu build config --containerapp-registry [YOUR CONTAINER REGISTRY] 
tanzu build -o build-output
```

##### Deploy

Follow these commands to deploy your application from the build-output folder:

```bash
tanzu deploy --from-build build-output
```

##### Bind

#### Create and bind the pre-provisioned services :
Create secrets to external Postgres (with pgvector) and GenAI control apis running on TPCF and bind them as pre-provisioned services 

```bash
tanzu context use <my-context>
kubectl apply -f .tanzu/services
```

### Cleanup

```bash
./demo.sh cleanup
```

### Troubleshooting

#### Issue: Problem with external service binding.
- **Solution:** Ensure that all credentials and connection details in `.tanzu/config/services` are correct and updated.

#### Issue: Application deployment fails.
- **Solution:** Check the build output for errors and verify the Tanzu configuration settings.

Browse your application through the app ingress link provided in the Space UI after deployment.

## Contributing
Contributions to this project are welcome. Please ensure to follow the existing coding style and add unit tests for any new or changed functionality.


