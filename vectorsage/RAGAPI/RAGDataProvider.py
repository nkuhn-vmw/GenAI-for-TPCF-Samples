import itertools
from Common.Data.Database import RAGDatabase, KnowledgeBaseEmbedding
from Common.OpenAIProviders.OpenAIEmbeddingProvider import OpenAIEmbeddingProvider
from Common.OpenAIProviders.OpenAILLMProvider import OpenAILLMProvider
from werkzeug.datastructures import FileStorage
from typing import List, Dict, Any
from dataclasses import dataclass
import logging
import string
import json

from TextChunker import TextChunker

# Setup logging
logging.basicConfig(level=logging.INFO)

@dataclass
class RAGDataProvider:
    database: RAGDatabase
    oai_embed: OpenAIEmbeddingProvider
    oai_llm: OpenAILLMProvider
    chunker: TextChunker
    max_results_to_retrieve: int = 20

    def chunk_run(self, 
                    markdown_files: List[FileStorage],
                    topic_display_name: str,
                    token_chunk_size: int= 128,
                    output_embeddings: bool=True
                    ):
        kb = self.database.get_knowledge_base(topic_display_name)
        topic_domain = kb[0].topic_domain
        embed_instruction = f"Represent this {topic_domain} document for retrieval:"

        try: 
            results_list = []
            for file in markdown_files:
                logging.info("Reading in Markdown File...")
                markdown_content = file.read().decode('utf-8')

                logging.info("Chunking ...")
                text_chunks = self.chunker.chunk_text(markdown_content,
                                                      token_chunk_size=token_chunk_size)
                logging.info(f"Total Chunks: {len(text_chunks)}")
                
                logging.info("Generating embeddings...")
                chunk_list = []
                if self.oai_embed.is_instructor_model:
                    logging.info("Generating chunks with instructions...")
                    chunk_list =  [[embed_instruction, chunk] for chunk in text_chunks]
                else:
                    logging.info("Generating chunks without instructions...")
                    chunk_list = [chunk for chunk in text_chunks]
                
                embeddings = []
                if output_embeddings:
                    embeddings = self.oai_embed.get_embeddings(chunk_list)

                result = [KnowledgeBaseEmbedding(content=text_emb[0], 
                                                 embedding=text_emb[1], 
                                                 id=idx+1) 
                            for idx,text_emb in enumerate(itertools.zip_longest(text_chunks, embeddings, fillvalue=[]))]      
                results_list.append((file.filename, result))              

            return results_list
        except Exception as e:
            raise BufferError( f"Error processing file {file.filename}: {e}")

    def chunk_insert_into_database(self, 
                                           markdown_files: List[FileStorage],
                                           topic_display_name: str,
                                           token_chunk_size: int= 128):
        kb = self.database.get_knowledge_base(topic_display_name)
        topic_domain = kb[0].topic_domain
        target_embedding_table_name = kb[0].schema_table_name
        embed_instruction = f"Represent this {topic_domain} document for retrieval:"

        try: 
            for file in markdown_files:
                logging.info("Reading in Markdown File...")
                markdown_content = file.read().decode('utf-8')

                logging.info("Chunking ...")
                text_chunks = self.chunker.chunk_text(markdown_content,
                                                      token_chunk_size=token_chunk_size)
                logging.info(f"Total Chunks: {len(text_chunks)}")
                
                logging.info("Generating embeddings...")
                chunk_list = []
                if self.oai_embed.is_instructor_model:
                    logging.info("Generating chunks with instructions...")
                    chunk_list =  [[embed_instruction, chunk] for chunk in text_chunks]
                else:
                    logging.info("Generating chunks without instructions...")
                    chunk_list = [chunk for chunk in text_chunks]
                
                embeddings = self.oai_embed.get_embeddings(chunk_list)

                logging.info("Inserting embeddings into table...")
                self.database.insert_content_with_embeddings(
                                                contentwithembeddings=zip(text_chunks, embeddings), 
                                                schema_table_name=target_embedding_table_name
                                                )
        except Exception as e:
            raise BufferError( f"Error processing file {file.filename}: {e}")

    def create_knowledgebase(self,
                             topic_display_name:str,
                             vector_size: int,
                             topic_domain: str,
                             context_learning: List[Dict[str,Any]] = None):
        
        # Make table name singular. Don't use caps/punctuations for easier maintainance
        table_name = ''.join([word.lower().translate(str.maketrans('','',string.punctuation)) 
                                        for word in topic_display_name.split(' ')])
        
        # Make sure domain is just a single word.
        domain = '_'.join(topic_domain.split())

        knowledge_base = self.database.get_knowledge_base(topic_display_name=topic_display_name)

        message = ""
        if len(knowledge_base) == 0:
            self.database.create_knowledge_base(topic_display_name=topic_display_name,
                                                table_name=table_name,
                                                topic_domain=domain,
                                                vector_size=vector_size,
                                                context_learning=context_learning)
            message = f"Knowledge base {topic_display_name} created successfully."
        else:
            message = f"The Knowledge base {topic_display_name} already exists."
                
        return message

    def get_all_knowledgebases(self):
        return self.database.get_knowledge_base()
    
    def delete_knowledge_base(self, topic_display_name: str):
        self.database.delete_knowledge_base(topic_display_name=topic_display_name)

    def get_knowledge_base_context_learning(self, topic_display_name: str):
        return self.database.get_context_learning(topic_display_name=topic_display_name)

    def update_knowledge_base_context_learning(self, 
                                               topic_display_name: str, 
                                               new_context_learning: List[Dict[str,Any]]):
        self.database.update_context_learning(topic_display_name=topic_display_name,
                                              new_context_learning=new_context_learning)

    def clear_knowledgebase_embeddings(self, topic_display_name:str):
        # Fetching the table name using the topic display name
        knowledge_base = self.database.get_knowledge_base(topic_display_name)
        if knowledge_base is None or len(knowledge_base) == 0:
            raise Exception(f"{topic_display_name} Knowledge base not found.")
        
        schema_table_name = knowledge_base[0].schema_table_name

        # Deleting all embeddings from the table
        deleted_count = self.database.delete_knowledge_base_embeddings(schema_table_name)
        
        return deleted_count
    


    def respond_to_user_query(  self,
                                query: str, 
                                topic_display_name: str,
                                override_context_learning: List[Dict[str, Any]] = None, 
                                lost_in_middle_reorder: bool = False,
                                stream: bool=False
                                ):
        
        # prompt_template: str = """
        #     You will receive a query from a user, followed by a list of context data retrieved from a database. Each piece of context data is a chunk of relevant information, and multiple contexts are separated by a newline.
        #     Your task is to answer the user's query based solely on the provided context data. If the context data contains the necessary information to answer the query, construct your answer using only the words from the context. Never infer details from the context to produce a response. Be thorough but do not add details, invent new information or extrapolate beyond what is provided in the Context.
        #     If none of the provided context data helps in answering the query, your response will be "I don't have that information.". In your response to the user, don't tell the user to read/view the context or that context was provided but instead answer as an expert responding. You may use previous answers or queries but do not include them to this query.
        #     ---
        #     Query: {query}
        #     Context:
        #     {found_context}
        #     ---
        #     """
        prompt_template: str = """You are an expert assistant answering queries using only the provided context. Follow these guidelines:
1. Use only information from the context to answer the query. Ignore irrelevant details and provide complete sentences and information.
2. Do not infer, assume, or add information not explicitly mentioned in the context. Remain objective and avoid personal opinions or biases.
3. If the context lacks necessary information, respond with "I don't have enough information to answer this query."
4. Provide detailed, helpful, and well-structured responses without telling the user to refer, check or read the provided context or mentioning that you are using provided context.
5. Do not expand acronyms unless specified and provided in the context.
6. Minimize references to previous answers or queries.
7. Do not repeat the user's query in your response.
8. If available in the context, include relevant document and image links in your response.
Process the following query and context:
---
Query: {}
Context:
{}
---
Respond appropriately based on the guidelines above, without mentioning them to the user.
"""
        # prompt_template: str = """
        #     You are an assistant tasked with answering queries based solely on provided context data. Follow these guidelines:

        #     1. **Use Only Given Context**: Directly use information from the context to construct your answers. Some information maybe irrelevant, ignore them if necessary. Do not respond with incomplete information or sentences.
        #     2. **Avoid Inference**: Do not add information, make assumptions beyond the given context, or infer details not explicitly mentioned.
        #     3. **Respond to Insufficient Data**: If the context lacks necessary details to answer the query, respond with "I don't have that information."
        #     4. **Expert Response Format**: Be very detailed and helpful. Respond as an expert without prompting the user to check the context. Do not tell them you are provided context.
        #     5. **Avoid Expanding Acronyms**: Do not expand acronyms unless specified to do so and that it is provided in the context.
        #     6. **Minimize Previous History use**: You may use previous answers or queries but do not include them to this query.
        #     7. **Do Not Repeat The User**: Do not repeat the user's query.
        #     8. **Provide References or Links**: If available in the context, output the link to the documents and images in your response.

        #     Process the following query and context:
        #     ---
        #     Query: {}
        #     Context:
        #     {}
        #     ---
        #     Respond appropriately based on the guidelines above. Do not mention to the user about the guidelines.
        #     """
    
        # When larger number of chunks start coming in, LLMs tend to prioritize content
        # at the beggingin and and near the end - rather than the middle. 
        def _lost_in_the_middle_reorder(sorted_descending_similarity_chunks):
            shuffled_result = []
            for i, value in enumerate(sorted_descending_similarity_chunks[::-1]):
                if (i + 1) % 2 == 1:
                    shuffled_result.append(value)
                else:
                    shuffled_result.insert(0, value)
            return shuffled_result
        
        # Get the knowledge base
        kb = self.database.get_knowledge_base(topic_display_name=topic_display_name)[0]

        # Convert user query into an embedding with the instruction
        instruction = f"Represent this {kb.topic_domain} question for retrieving supporting documents:"
        query_embedding = self.oai_embed.get_embeddings_with_instructions(instruction, query)
        # Use the result to search for similar content from the vector db
        results = self.database.get_content_with_cosine_similarity(queryembedding=query_embedding, 
                                                                   schema_table_name=kb.schema_table_name,
                                                                   results_to_result=self.max_results_to_retrieve
                                                                  )
        # Get the length of results and a do a lost in middle reorder, if required
        numResults = min(len(results), self.max_results_to_retrieve)
        results = results[:numResults]
        if lost_in_middle_reorder:
            results = _lost_in_the_middle_reorder(results)

        # Use the found content and form a prompt
        found_context = "\n".join([ f"{idx+1}. {kbchunk.content}"  for idx, kbchunk in enumerate(results)])
        prompt = prompt_template.format(query, found_context)

        # Set the context learning from knowledge base, otherwise, override it with provided list
        context_learning = kb.context_learning
        if override_context_learning:
            context_learning = override_context_learning

        # Get the context learning and concatenate with the prompt to form a new prompt
        message = context_learning + [{"role": "user", "content": prompt}]

        response = None
        if stream:
            streaming_response = self.oai_llm.stream_chat_completion(message)

            for message in streaming_response:
                if message.choices[0].delta.content != None:
                    # Unfortunately, we have to deal with escaping newlines, otherwise
                    # some frontend libraries just strip the newlines out.
                    escaped_content = message.choices[0].delta.content.replace("\n", "\\n")
                    yield f"data: {json.dumps(escaped_content)}\n\n".encode('utf-8')
        else:
            # Send the new prompt to an LLM to generate a response.
            response = self.oai_llm.chat_completion(message)
            return response

