# GenAI for Tanzu Application Service: Application Samples

This repo is designed to hold applications written to demo the new GenAI for TAS tile.

[See Product Page to Sign Up for the Beta](https://tanzu.vmware.com/application-service/private-ai) for GenAI for TAS. A team member will reach out and schedule a call to get you on-boarded in the beta program.

See example Applications below:

1. [Gradio Chat](https://github.com/nkuhn-vmw/GenAI-for-TAS-Samples/tree/main/gradio-chat) This is the sample chat application from fastchat modified to use GenAI for TAS as the backend LLM.

2. [Spring Music (Taylor's Version)](https://github.com/nkuhn-vmw/GenAI-for-TAS-Samples/tree/main/spring-music-taylors-version) A modifed version of the classic "Spring Music" Cloud Foundry application infused with magic from the new [Spring AI project](https://github.com/spring-projects/spring-ai). This app will add a "Spring Music Assistant" when the GenAI for TAS service is bound to this application.

3. [Tanzu GPT Python Edition](https://github.com/nkuhn-vmw/GenAI-for-TAS-Samples/tree/main/tanzu-gpt-python) Based on the orginal application used at the VMware Explore hackathon -- this python application can be configured to use the GenAI for TAS tile and Tanzu Postgres tile to have a "chat-gpt" style applications that can be enhanced with pgvector embeddings. 

4. [VectorSage](https://github.com/nkuhn-vmw/GenAI-for-TAS-Samples/tree/main/vectorsage) An advanced chatbot demonstrating Retrieval Augmented Generation (RAG) with Knowledgebase, in-context learning controls and streaming output. This is a python application that utilizes the GenAI Tile with multi-model processing (`hkunlp/instructor-xl` and `mistralai/MistralAI-7B-Instruct-v0.2`). The PostgresDb Tile was also utilized with Vector support. 
