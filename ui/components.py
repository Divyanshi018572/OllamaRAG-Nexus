import streamlit as st

def header():
    st.markdown("""
    <div style='text-align: center; padding: 1rem 0 3rem 0;'>
        <h1>🚀 NexuRAG Nexus</h1>
        <p style='color: #94a3b8; font-size: 1.2rem;'>Advanced Document Intelligence — Local & Secure</p>
    </div>
    """, unsafe_allow_html=True)

def sidebar_settings(ollama_models, groq_models, groq_available):
    with st.sidebar:
        st.image("https://raw.githubusercontent.com/ollama/ollama/main/docs/ollama.png", width=80)
        st.title("Nexus Control")
        
        st.subheader("🤖 Model Selection")
        provider = st.radio("Provider", ["Ollama (Local)", "Groq (Cloud)"], index=0 if not groq_available else 1)
        
        if provider == "Ollama (Local)":
            model = st.selectbox("Model", ollama_models)
            use_groq = False
        else:
            if not groq_available:
                st.error("Groq API Key not found in .env or secrets.")
                st.stop()
            model = st.selectbox("Model", groq_models)
            use_groq = True
            
        st.divider()
        st.subheader("⚙️ Analysis Settings")
        temperature = st.slider("Creativity (Temp)", 0.0, 1.0, 0.1)
        
        return provider, model, use_groq, temperature

def knowledge_hub(engine, process_file_func):
    st.subheader("🧠 Knowledge Hub")
    uploaded_files = st.file_uploader(
        "Upload documents to your knowledge base", 
        type=["pdf", "txt"], 
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("📥 Process & Index"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Indexing {uploaded_file.name}..."):
                    text = process_file_func(uploaded_file)
                    if not text.startswith("Error"):
                        chunks = engine.add_document(text, uploaded_file.name)
                        st.toast(f"Added {uploaded_file.name} ({chunks} chunks)", icon="✅")
                    else:
                        st.error(f"Failed to process {uploaded_file.name}")
            st.success("Knowledge Base Updated!")

    st.divider()
    if st.button("🗑️ Reset Database", type="secondary"):
        engine.clear_database()
        st.warning("Knowledge base has been cleared.")
        st.rerun()
