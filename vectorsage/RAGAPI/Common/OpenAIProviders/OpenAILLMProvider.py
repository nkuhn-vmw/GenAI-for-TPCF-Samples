from Common.OpenAIProviders.OpenAIProvider import OpenAIProvider
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from typing import Iterable
import httpx


class OpenAILLMProvider(OpenAIProvider):
    model_name: str = ""
    def __init__(self, 
                 api_base: str,
                 api_key:str, 
                 llm_model_name: str,
                 temperature: float = 1.0
                ):
        super().__init__(api_base=api_base,
                         api_key=api_key,
                         http_client=httpx.Client(verify=False)
                        )
        self.model_name = llm_model_name
        self.temperature = temperature
        
    def chat_completion(self, user_assistant_messages: Iterable[ChatCompletionMessageParam]):
        response = self.oai_client.chat.completions.create(
                                                    model = self.model_name,
                                                    response_format={ "type": "json_object" },
                                                    messages= user_assistant_messages,
                                                    temperature = self.temperature,
                                                    stream=False
                                                )
        return response.choices[0].message.content
    
    def stream_chat_completion(self, user_assistant_messages: Iterable[ChatCompletionMessageParam]):
        stream = self.oai_client.chat.completions.create(
                                                    model = self.model_name,
                                                    response_format={ "type": "json_object" },
                                                    messages= user_assistant_messages,
                                                    temperature = self.temperature,
                                                    stream=True
                                                )
        return stream

