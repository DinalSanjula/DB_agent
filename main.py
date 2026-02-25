from fastapi import FastAPI

from db_agent import query_db_with_natural_language
from user_routes import router as user_routes
from invoice_routes import router as invoice_router
from agent_routes import router as agent_router
import gradio as gr
from uuid import uuid4

app = FastAPI(
    title="CClarke ORM implementation with DB Agent"
)

def db_agent_gradio_ui():
    with gr.Blocks() as db_ui:
        gr.Markdown("DB Agent")
        gr.Markdown("Ask questions from your database with natural language")

        thread_id = gr.State(str(uuid4()))
        chatbot = gr.Chatbot(label="Conversation")
        msg = gr.Textbox(label="Enter your question")

        def respond(message:str, history:list,current_thread_id:str):
            result = query_db_with_natural_language(message, thread_id=current_thread_id)

            history = history +[
                {"role":"user","content":message},
                {"role":"assistant","content":result}
            ]

            return history,"",current_thread_id,

        msg.submit(
            respond,
            inputs=[msg,chatbot,thread_id],
            outputs=[chatbot,msg,thread_id]
        )
        return db_ui

app = gr.mount_gradio_app(app,db_agent_gradio_ui(),path="/agent/ui")

app.include_router(user_routes)
app.include_router(invoice_router)
app.include_router(agent_router)