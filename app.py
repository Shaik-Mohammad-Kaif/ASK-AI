from dotenv import load_dotenv
import os
import google.generativeai as genai
import gradio as gr

# Load environment variables
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    api_key = "AIzaSyAR0ikdThRLjUQ8w6qZT2D_uk1FX4_v3AE"  # Replace with your actual key or remove in production
genai.configure(api_key=api_key)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Define the function to get responses from Gemini API
def get_gemini_response(question, history=[]):
    response = chat.send_message(question, stream=True)
    response_text = ""
    for chunk in response:
        response_text += chunk.text
    history.append((question, response_text))
    return history, history

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown(
        """
        <h1 style='text-align: center; font-size: 2.5em; color: #F97316;'>Ask AI Q&A Chatbot 🤖</h1>
        <p style='text-align: center; font-size: 1.1em; max-width: 600px; margin: auto;'>
            Welcome to the Ask AI Q&A Chatbot! 
        </p>
        """
    )
    
    chatbot = gr.Chatbot(label="Chat History", elem_id="chatbox")
    msg = gr.Textbox(label="", placeholder="Type your question here...", lines=1)
    
    with gr.Row():
        submit = gr.Button("Submit", variant="primary")
        clear = gr.Button("Clear Chat", variant="secondary")
    
    def clear_chat():
        return [], []

    # Define interaction flow with chatbot
    submit.click(get_gemini_response, [msg, chatbot], [chatbot, chatbot])
    clear.click(clear_chat, None, [chatbot, chatbot])

    gr.Markdown(
        """
        <footer style='text-align: center; margin-top: 30px;'>
            Developed by <strong>SHAIK MOHAMMAD KAIF</strong><br>
            <div style="margin-top: 10px; display: inline-flex; gap: 15px; justify-content: center;">
                <a href="https://github.com/Shaik-Mohammad-Kaif" target="_blank">
                    <img src="https://img.icons8.com/ios-glyphs/30/ffffff/github.png" 
                         alt="GitHub" width="30" height="30">
                </a>
                <a href="https://www.linkedin.com/in/shaik-mohammad-kaif-ba0366243/" target="_blank">
                    <img src="https://img.icons8.com/ios-filled/30/ffffff/linkedin.png" 
                         alt="LinkedIn" width="30" height="30">
                </a>
            </div>
        </footer>
        """
    )

# Launch the Gradio interface
demo.launch(share = True)
