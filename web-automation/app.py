import gradio as gr
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from ActionEngine import ActionEngine

MAX_CHARS = 1500

from cfenv import AppEnv

env = AppEnv()

# Use this action_engine instead to have a local inference
# action_engine = ActionEngine(llm=DefaultLocalLLM())

action_engine = ActionEngine()

## Setup chrome options
chrome_options = Options()
chrome_options.add_argument("--headless") # Ensure GUI is off
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--window-size=1600,900")
chrome_options.add_argument("--disable-dev-shm-usage")

# Set path to chrome/chromedriver as per your configuration

base_url = "https://www.irs.gov/"

instructions = ["Click on the 'Pay' item on the menu, between 'File' and 'Refunds'",
                "Click on 'Pay Now with Direct Pay' just below 'Pay from your Bank Account'",
                "Click on 'Make a Payment', just above 'Answers to common questions'",]

import os.path
homedir = os.path.expanduser("~")
chrome_options.binary_location = f"{homedir}/chrome-linux64/chrome"
webdriver_service = Service(f"{homedir}/chromedriver-linux64/chromedriver")


title = """
<div align="center">
  <h1> Welcome to Web Automation with GenAI on Tanzu Application Service</h1>
  <p>Redefining internet surfing by transforming natural language instructions into seamless browser interactions.</p>
</div>
"""

# Choose Chrome Browser
driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)

def process_url(url):
    driver.get(url)
    driver.save_screenshot("screenshot.png")
    # This function is supposed to fetch and return the image from the URL.
    # Placeholder function: replace with actual image fetching logic.
    return "screenshot.png"

def process_instruction(query, url_input):
    if url_input != driver.current_url:
        driver.get(url_input)
    state = driver.page_source
    query_engine = action_engine.get_query_engine(state)
    streaming_response = query_engine.query(query)

    source_nodes = streaming_response.get_formatted_sources(MAX_CHARS)

    print(str(streaming_response))

    return str(streaming_response), source_nodes

def exec_code(code, source_nodes, full_code):

    print(full_code)
    print(code)
    code = code.split("```")[0]
    html = driver.page_source
    try:
        exec(code)
        output = "Successful code execution"
        status = """<p style="color: green; font-size: 20px; font-weight: bold;">Success!</p>"""
        full_code += code
    except Exception as e:
        output = f"Error in code execution: {str(e)}"
        status = """<p style="color: red; font-size: 20px; font-weight: bold;">Failure! Open the Debug tab for more information</p>"""
    return output, code, html, status, full_code

def update_image_display(img):
    driver.save_screenshot("screenshot.png")
    url = driver.current_url
    return "screenshot.png", url

def show_processing_message():
    return "Processing..."

def update_image_display(img):
    driver.save_screenshot("screenshot.png")
    url = driver.current_url
    return "screenshot.png", url


with gr.Blocks() as demo:
    with gr.Tab("Web automation with GenAI on Tanzu Application Service"):
      with gr.Row():
          gr.HTML(title)
      with gr.Row():
          url_input = gr.Textbox(value=base_url, label="Enter URL and press 'Enter' to load the page.")
      
      with gr.Row():
          with gr.Column(scale=7):
              image_display = gr.Image(label="Browser", interactive=False)
          
          with gr.Column(scale=3):
              with gr.Accordion(label="Full code", open=False):
                  full_code = gr.Code(value="", language="python", interactive=False)
              code_display = gr.Code(label="Generated code", language="python",
                                      lines=5, interactive=True)
              
              status_html = gr.HTML()
      with gr.Row():
          with gr.Column(scale=8):
              text_area = gr.Textbox(label="Enter instructions and press 'Enter' to generate code.")
              gr.Examples(examples=instructions, inputs=text_area)
    with gr.Tab("Debug"):
      with gr.Row():
          with gr.Column():
              log_display = gr.Textbox(interactive=False, lines=20)
          with gr.Column():
              source_display = gr.Code(language="html", label="Retrieved nodes", interactive=False, lines=20)
      with gr.Row():
          with gr.Accordion(label="Full HTML", open=False):
              full_html = gr.Code(language="html", label="Full HTML", interactive=False, lines=20)

    # Linking components
    url_input.submit(process_url, inputs=url_input, outputs=image_display)
    text_area.submit(show_processing_message, outputs=[status_html]).then(
        process_instruction, inputs=[text_area, url_input], outputs=[code_display, source_display]
        ).then(
        exec_code, inputs=[code_display, source_display, full_code], 
        outputs=[log_display, code_display, full_html, status_html, full_code]
    ).then(
        update_image_display, inputs=image_display, outputs=[image_display, url_input]
    )
demo.launch(server_name = "0.0.0.0", server_port = env.port,debug = True)