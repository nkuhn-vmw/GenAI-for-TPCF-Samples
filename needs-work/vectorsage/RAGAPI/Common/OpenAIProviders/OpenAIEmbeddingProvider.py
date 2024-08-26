from Common.OpenAIProviders.OpenAIProvider import OpenAIProvider
from typing import List
import httpx


class OpenAIEmbeddingProvider(OpenAIProvider):
    model_name: str = ""
    def __init__(self, 
                 api_base: str,
                 api_key:str, 
                 embed_model_name: str,
                 is_instructor_model: bool = False
                ):
        super().__init__(api_base=api_base,
                         api_key=api_key,
                         http_client=httpx.Client(verify=False)
                        )
        self.model_name = embed_model_name
        self.is_instructor_model = is_instructor_model
        
    def get_embeddings_with_instructions(self, instruction, text):
        return self._generate_single_embedding(text=[instruction, text])
    
    def get_embeddings(self, text:str):
        return self._generate_single_embedding(text=text)
    
    def get_embeddings(self, texts:List[str]):
        return self._generate_multi_embedding(texts=texts)

    def _generate_multi_embedding(self, texts):
        try:
            response = self.oai_client.embeddings.create(
                                                         input=texts,
                                                         model=self.model_name
                                                        )
            return [data.embedding for data in response.data]
        except Exception as e:
            raise Exception(f"Error generating embedding for '{texts}': {e}")
    
    def _generate_single_embedding(self, text):
        try:
            return self.oai_client.embeddings.create(
                                                      input = [text], 
                                                      model=self.model_name
                                                    ).data[0].embedding
        except Exception as e:
            raise Exception(f"Error generating embedding for '{text}': {e}")
