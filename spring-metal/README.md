

## Architecture

![Alt text](https://github.com/0pens0/spring-metal/blob/main/image.png?raw=true "Spring-metal AI topology")



## Installation

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



## Contributing
Contributions to this project are welcome. Please ensure to follow the existing coding style and add unit tests for any new or changed functionality.


