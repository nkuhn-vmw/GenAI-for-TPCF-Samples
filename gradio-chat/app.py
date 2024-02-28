
import os
from openai import OpenAI
import gradio
import httpx
from cfenv import AppEnv


env = AppEnv()
env.name  # 'test-app'
env.port  # 5000

llm = env.get_service(label='genai-service')

http_client = httpx.Client(
    verify = False
)

openai_client = OpenAI(
    # This is the default and can be omitted
    base_url = llm.credentials['api_base'],
    api_key = llm.credentials['api_key'],
    http_client = http_client,
)

prompt = "Enter Your Query Here"
def api_calling(prompt):
    completions = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
         messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = completions.choices[0].message.content
    return message
def message_and_history(input, history):
    history = history or []
    s = list(sum(history, ()))
    s.append(input)
    inp = ' '.join(s)
    output = api_calling(inp)
    history.append((input, output))
    return history, history
block = gradio.Blocks(theme=gradio.themes.Monochrome())
with block:
    gradio.Markdown("""<h1><center>Gradio Chat:
    ChatBot with Gradio and OpenAI</center></h1>
    """)
    chatbot = gradio.Chatbot()
    message = gradio.Textbox(placeholder=prompt)
    state = gradio.State()
    submit = gradio.Button("SEND")
    submit.click(message_and_history, 
                 inputs=[message, state], 
                 outputs=[chatbot, state])
block.launch(server_name = "0.0.0.0", server_port = env.port,debug = True)