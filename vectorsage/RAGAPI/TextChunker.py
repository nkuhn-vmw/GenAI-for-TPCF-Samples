from abc import ABC, abstractmethod
import en_core_web_sm
from transformers import AutoTokenizer
import numpy as np
import os

class TextChunker(ABC):
    @abstractmethod
    def chunk_text(text:str, token_chunk_size:int):
        """
        Subclasses must implement this method
        """
        pass  

class ModelTokenizedTextChunker(TextChunker):
    __TEXT_OVERLAP_SENTENCE_LEVEL = -1 # Overlap at a sentence granularity instead of number of characters

    def __init__(self, model_tokenizer_path, text_overlap=__TEXT_OVERLAP_SENTENCE_LEVEL):
        try:
            self.nlp = en_core_web_sm.load()
            self.nlp.add_pipe('sentencizer')
        except Exception as e:
            raise RuntimeError(f"Failed to load Spacy model: {e}")
 
        self.model_tokenizer = AutoTokenizer.from_pretrained(model_tokenizer_path,truncation=True)
        self.text_overlap = int(text_overlap)
        os.environ["TOKENIZERS_PARALLELISM"] = "false"
            
    def chunk_text(self, text:str, token_chunk_size:int=128):
        chunks = []
        current_token_chunk_length = 0
        overlap_text_chunk = ""
        doc = self.nlp(text)
        previous_sentence = ""
        
        # iteratively tokenize each sentence and tally its length and the actual sentence text
        # if the next sentence is going to exceed the chunk size, stop and save it to the chunks array and create an overlap of text
        for sent in doc.sents:
            tokenized_sent = self.model_tokenizer(sent.text, truncation=True, return_tensors="np", padding=False, max_length=token_chunk_size)["input_ids"]        

            if current_token_chunk_length + tokenized_sent.shape[1] <= token_chunk_size:
                # It is safe to continue adding the sentences to our chunk
                overlap_text_chunk += sent.text
                current_token_chunk_length += tokenized_sent.shape[1]
            else:
                # At this point, we're going to exceed the specified max token chunk size, so let's dump the existing buffered
                # chunk and start a new chunk. Add an overlap of text to enable a continue flow of information, in case we truncate paragraphs. 
                chunks.append(overlap_text_chunk)

                if self.text_overlap == self.__TEXT_OVERLAP_SENTENCE_LEVEL:
                    overlap_text_chunk = previous_sentence  # This may break the token_chunk_size rule
                else:    
                    overlap_text_chunk = overlap_text_chunk[-self.text_overlap:] if self.text_overlap < len(overlap_text_chunk) else overlap_text_chunk
                overlap_text_chunk += sent.text
                tokenized_overlap_chunk = self.model_tokenizer(overlap_text_chunk, return_tensors="np", padding=False, truncation=True, max_length=token_chunk_size)["input_ids"] 
                current_token_chunk_length = tokenized_overlap_chunk.shape[1]
            
            previous_sentence = sent.text
        
        # adding the last piece to our text chunk, if it doesn't contain the initial overlap text
        if len(overlap_text_chunk) > 0:
            chunks.append(overlap_text_chunk)    

        return chunks
