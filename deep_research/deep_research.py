import gradio as gr
from dotenv import load_dotenv
from research_manager import ResearchManager

load_dotenv(override=True)


async def run(query: str):
    validate_and_submit(query)
    async for chunk in ResearchManager().run(query):
        yield chunk

def validate_and_submit(text):
    if not text or not text.strip():
        raise gr.Error("Textbox is empty or null!") # Displays a red alert box in the UI
    return f"Success: {text}"
with gr.Blocks(theme=gr.themes.Default(primary_hue="sky")) as ui:
    gr.Markdown("# Deep Research")
    query_textbox = gr.Textbox(label="What topic would you like to research?")
    submit_button = gr.Button("Submit", variant="primary",size="sm", scale=0, min_width=0)
    report = gr.Markdown(label="Report")
    
    submit_button.click(fn=run, inputs=query_textbox, outputs=report)
    query_textbox.submit(fn=run, inputs=query_textbox, outputs=report)

ui.launch(inbrowser=True)

