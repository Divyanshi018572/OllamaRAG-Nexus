import os
import streamlit as st
from core.models import get_ollama_models, get_groq_models, is_groq_available
from core.processors import process_file
from core.engine import RAGEngine, get_answer_from_ollama, get_answer_from_groq
from ui.components import header, sidebar_settings, knowledge_hub

# Page Config
st.set_page_config(
    page_title="NexuRAG | Document Intelligence",
    page_icon="🚀",
    layout="wide"
)

# Load CSS
def load_css(file_path):
    with open(file_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("ui/assets/styles.css")

# Initialize Engine
if "engine" not in st.session_state:
    st.session_state.engine = RAGEngine()

# Sidebar & Global Settings
groq_available = is_groq_available()
provider, model, use_groq, temperature = sidebar_settings(
    get_ollama_models(), 
    get_groq_models(), 
    groq_available
)

# Header
header()

# Main Layout
tab1, tab2 = st.tabs(["💬 Nexus Chat", "🧠 Knowledge Hub"])

with tab2:
    knowledge_hub(st.session_state.engine, process_file)

with tab1:
    # Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if "sources" in message:
                st.caption(f"Sources: {', '.join(message['sources'])}")

    # Ask Question
    if prompt := st.chat_input("Query the knowledge base..."):
        # Display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # RAG Logic
        with st.chat_message("assistant"):
            with st.spinner("Analyzing knowledge base..."):
                context, sources = st.session_state.engine.search(prompt)
                
                try:
                    if use_groq:
                        api_key = os.getenv("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY")
                        answer = get_answer_from_groq(model, prompt, context, api_key)
                    else:
                        answer = get_answer_from_ollama(model, prompt, context)
                    
                    st.markdown(answer)
                    if sources:
                        st.caption(f"Sources: {', '.join(sources)}")
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "sources": sources
                    })
                except Exception as e:
                    st.error(f"Error generating answer: {str(e)}")
