# 🚀 NexuRAG: Advanced Local RAG Suite

NexuRAG is a professional-grade Retrieval-Augmented Generation (RAG) suite designed to provide high-performance document intelligence locally and securely. Built with **Streamlit**, **LangChain**, and **Ollama**, it allows you to ingest any PDF or TXT file and chat with your documents using state-of-the-art LLMs.

## ✨ Features
- **Dynamic Knowledge Hub**: Upload and index multiple documents on the fly.
- **Persistent Vector Store**: Uses ChromaDB to keep your knowledge base ready between sessions.
- **Hybrid Provider Support**: Seamlessly switch between local **Ollama** models and lightning-fast **Groq** cloud models.
- **Premium UI**: Sleek dark mode interface with glassmorphic cards and intuitive navigation.
- **Local & Secure**: Your data never leaves your machine when using local providers.

## 🛠️ Setup Instructions

### 1. Prerequisites
- [Ollama](https://ollama.com/) installed and running.
- Python 3.9+ installed.

### 2. Pull Required Models
Run the following commands to ensure you have the local intelligence:
```bash
ollama pull llama3.2:3b
ollama pull qwen2.5-coder:1.5b
```

### 3. Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/ollama-nexus.git
   cd ollama-nexus
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Configuration
Create a `.env` file in the root directory if you wish to use Groq:
```env
GROQ_API_KEY=your_api_key_here
```

### 5. Run the Application
```bash
streamlit run app.py
```

## 📁 Project Structure
- `core/`: Business logic for RAG and file processing.
- `ui/`: Reusable Streamlit components and premium styling.
- `data/`: Persistent storage for uploads and vector embeddings.

## 📜 License
MIT License. Free to use and modify.
