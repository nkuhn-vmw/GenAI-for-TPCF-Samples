from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
import os
from cfenv import AppEnv
env = AppEnv()
llm = env.get_service(label='genai-service')
base_url = llm.credentials['api_base']
api_key = llm.credentials['api_key']

DEFAULT_EMBED_MODEL = "text-embedding-ada-002"
DEFAULT_LLM = "gpt-3.5-turbo"


class DefaultEmbedder(OpenAIEmbedding):
	def __init__(self, model=DEFAULT_EMBED_MODEL):
		super().__init__(model=model, api_key=api_key, api_base=base_url, dimensions=1024)

class DefaultLLM(OpenAI):
	def __init__(self, model=DEFAULT_LLM):
		super().__init__(model=model, api_key=api_key, api_base=base_url)