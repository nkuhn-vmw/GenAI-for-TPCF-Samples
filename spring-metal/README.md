

## Architecture
For this example you will deploy the spring application ***spring-metal*** on tPCF.
You will also pre-create a Chat and Embedding service from the GenAI on tPCF tile.
You will also pre-create a simple postgres database for data and vector db support from the Postgres tile for tPCF.

We will use a two differnet LLM models ***gemma2*** for chat intference and ***nomic-embed-text*** for embedding.

***See Architecture diagram:***
![Alt text](https://github.com/nkuhn-vmw/GenAI-for-TPCF-Samples/blob/main/spring-metal/spring-metal-arch.png "Spring-metal AI Architecture")

### Create Service Intances for Spring-Metal

```bash
#Create Chat Service
cf create-service genai gemma2:2b spring-metal-chat

#Create Embedding Service
cf create-service genai nomic-embed-text spring-metal-embed

#Create Postgres DB
cf create-service postgres on-demand-postgres-db spring-metal-db
```

### Compile Spring-Metal with maven
```bash
# Install java 1.17 if not already installed
sudo apt install openjdk-17-jdk openjdk-17-jre
sudo update-java-alternatives --set /usr/lib/jvm/java-1.17.0-openjdk-amd64
export JAVA_HOME=/usr/lib/jvm/java-1.17.0-openjdk-amd64
```

```bash
cd ./spring-metal
mvn clean package -DskipTests
```

### Deploy
```bash
cf push
```

## Contributing
Contributions to this project are welcome. Please ensure to follow the existing coding style and add unit tests for any new or changed functionality.


