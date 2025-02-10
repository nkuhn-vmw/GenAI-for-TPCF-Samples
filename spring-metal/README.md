

## Architecture

![Alt text](https://github.com/nkuhn-vmw/GenAI-for-TPCF-Samples/blob/main/spring-metal/spring-metal-arch.png "Spring-metal AI Architecture")

## Create Service Intances for Spring-Metal

```bash
#Create Chat Service
cf create-service genai gemma2:2b spring-metal-chat

#Create Embedding Service
cf create-service genai nomic-embed-text spring-metal-embed

#Create Postgres DB
cf create-service postgres on-demand-postgres-db spring-metal-db
```

#### Compile Spring-Metal with maven
```bash
mvn clean package -DskipTests
```

#### Deploy
```bash
cf push
```

## Contributing
Contributions to this project are welcome. Please ensure to follow the existing coding style and add unit tests for any new or changed functionality.


