

## Architecture
This example will deploy the popular [Open-webui](https://openwebui.com/) to tPCF.

You can wire up many GenAI Services/LLMs to open-webui-cf for testing. 
This is a great tool to test out many different models and provide a tool to provide a local "Chat GPT" style interface.

This is a rather large python application, it may take a few minutes for the cf push to complete.

***See Architecture diagram:***
![Alt text](https://github.com/nkuhn-vmw/GenAI-for-TPCF-Samples/blob/main/open-webui-cf/open-webui-cf-arch.png "Spring-metal AI Architecture")

## Create Service Intances for open-webui-cf

```bash
#Create Chat Service
cf create-service genai gemma2:2b gemma2:2b

#Create Embedding Service
cf create-service genai nomic-embed-text nomic-embed-text

```

### Deploy
```bash
cd ./open-webui-cf  #navigate to open-webui-cf dir
cf push
```

## Contributing
Contributions to this project are welcome. Please ensure to follow the existing coding style and add unit tests for any new or changed functionality.


