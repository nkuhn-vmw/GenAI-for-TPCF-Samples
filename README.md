# GenAI for Tanzu Application Service: Application Samples

This repo is designed to hold applications written to demo the new GenAI for TAS tile.
[See Product Page to Sign Up for the Beta](https://tanzu.vmware.com/application-service/private-ai) to get in contact with the TAS GenAI team.

See example Applications:
1. [Gradio Chat](https://github.com/nkuhn-vmw/GenAI-for-TAS-Samples/tree/main/gradio-chat) This is the sample chat application from fastchat modified to use GenAI for TAS as the backend LLM.
2. [Spring Music (Taylor's Version)](https://github.com/nkuhn-vmw/GenAI-for-TAS-Samples/tree/main/spring-music-taylors-version) A modifed version of the classic "Spring Music" Cloud Foundry application infuesed with some Spring AI magic. This app will add a "Spring Music Assistant" when the GenAI for TAS service is bound to this application.
3. [Tanzu GPT Python Edition](https://github.com/nkuhn-vmw/GenAI-for-TAS-Samples/tree/main/tanzu-gpt-python) Based on the orginal application used at the VMware Explore hackathon -- this python application can be configured to use the GenAI for TAS tile and Tanzu Postgres tile to have a "chat-gpt" style applications that can be enhanced with pgvector embeddings. 