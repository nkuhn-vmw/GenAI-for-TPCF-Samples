import httpx
from openai import OpenAI

class OpenAIProvider:
    oai_client: OpenAI

    def __init__(self, 
                 api_base: str, 
                 api_key: str, 
                 http_client: httpx.Client
                ):
        
        self.oai_client = OpenAI( base_url=api_base, 
                                  api_key=api_key, 
                                  http_client=http_client
                                )
        
        
