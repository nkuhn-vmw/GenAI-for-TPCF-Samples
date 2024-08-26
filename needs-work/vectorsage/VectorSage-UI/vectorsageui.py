from urllib.parse import urljoin
from typing import List
from dataclasses import dataclass, field
import gradio
import  json
import logging
import requests

# Setup logging
logging.basicConfig(level=logging.INFO)

@dataclass
class VectorSageUI:
    llm_rag_services_host: str
    listen_port: int
    cached_knowledgebases: List[str] = field(default_factory=list)
    current_knowledgebase: str = None

    ### GRADIO TOP LEVEL FUNCTIONS
    def _init_history(self, messages_history: gradio.State):
        messages_history = []
        return messages_history

    def _process_user_input(self, user_query: gradio.Textbox, history: gradio.Chatbot):
        return "", history + [[user_query, None]]

    def _complete_chat(self, history: gradio.Chatbot, messages_history: gradio.State, message_textbox: gradio.Textbox):
        # Get the user query
        user_query = history[-1][0]
        
        # Prepare to concantenate the stream of data
        history[-1][1] = ""

        # No History for now. 
        # messages = messages_history

        if self.current_knowledgebase:
            url = urljoin(self.llm_rag_services_host, "respond_to_user_query")
            # we will just initate a stream and do nothing with the messages. 
            with requests.post(url, data = {
                            "query": user_query,
                            "topic_display_name": self.current_knowledgebase,
                            "do_lost_in_middle_reorder": True,
                            "stream": True
                        }
                        , stream=True) as response_stream:
                
                for line in response_stream.iter_lines(decode_unicode=True):
                    if line.startswith("data:"):
                        data = line[5:]
                        if data:
                            if data[0] == ' ':  # SSE Standard - Remove white space in front, if any
                                data = data[1:]

                            # Parse the JSON string and unescape newline characters
                            unescaped_data = json.loads(data).replace("\\n", "\n")
                            history[-1][1] += unescaped_data

                    yield history, messages_history, gradio.Textbox(placeholder="Providing response. Please wait...", interactive=False)

                logging.info(f"Completion Reason: {response_stream.reason}")
        # Update the chat history with the LLM response and return
        messages_history += [{"role": "assistant", "content": history[-1][1] }]

        yield history, messages_history, gradio.Textbox(placeholder="Enter Your Query Here", interactive=True)
        
    # Get the list of Knowledge Bases available
    def _fetch_dropdown_knowledge_options(self):
        """Fetch options for the dropdown from the database."""
        endpoint = urljoin(self.llm_rag_services_host,"list_knowledge_bases")
        response = requests.get(endpoint,params= {"topic_display_name_only": True})
        knowledge_bases_names_json = response.json()['knowledge_bases']
        knowledge_base_names = [kbnames for kbnames in knowledge_bases_names_json]
        return knowledge_base_names

    def _handle_dropdown_selection(self, selected_topic: str):
        """Handle the dropdown selection and fetch more data."""
        logging.info(f"handling dropdown - selected: {selected_topic}")
        self.current_knowledgebase = selected_topic

    def _refresh_dropdown_data(self):
        """Function to refresh dropdown data from the database."""
        kb_list = self._fetch_dropdown_knowledge_options()
        self.cached_knowledgebases = kb_list
        cur_kb = self.current_knowledgebase
        
        if (cur_kb == None and len(kb_list) > 0) or (cur_kb != None and len(kb_list) > 0 and cur_kb not in kb_list):
            self.current_knowledgebase = kb_list[0]

        return gradio.Dropdown(choices=self.cached_knowledgebases, label="Select Knowledge Base", value=self.current_knowledgebase, interactive=True)

    def start(self):
        with gradio.Blocks(fill_height=True) as grai_ui:
            gradio.Markdown("""<h1><center>VectorSage - GenAI on TAS</center></h1>""")
            with gradio.Accordion("Configure AI",open=False) as scene_accordion:
                with gradio.Row():
                    kb_dropdown = self._refresh_dropdown_data()
                    refresh_button = gradio.Button("Refresh List")

            kb_dropdown.change(self._handle_dropdown_selection, inputs=[kb_dropdown], outputs=[], preprocess=False, postprocess=False)
            refresh_button.click(self._refresh_dropdown_data, inputs=[], outputs=kb_dropdown)
            
            chatbot = gradio.Chatbot(scale=2)
            message_textbox = gradio.Textbox(placeholder="Enter Your Query Here")
            clear_button = gradio.Button("Clear Session")
            message_history = gradio.State([])
            
            # UI Init
            grai_ui.load( 
                            lambda: None, None, chatbot, queue=False
                        ).then(
                            self._refresh_dropdown_data, inputs=[], outputs = [kb_dropdown]
                            ).success(
                                self._init_history, [message_history], [message_history]
                                )

            # Chained actions on submission
            clear_button.click(
                            lambda: None, None, chatbot, queue=False
                            ).success(
                                        self._init_history, [message_history], [message_history]
                                    )
                        
            message_textbox.submit(
                                    self._process_user_input, [message_textbox, chatbot], [message_textbox, chatbot], queue=False
                                ).then(
                                        self._complete_chat, [chatbot, message_history, message_textbox], [chatbot, message_history, message_textbox]
                                      )

        grai_ui.launch(server_name="0.0.0.0", server_port = self.listen_port, debug = True)    


