import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

def get_ollama_models():
    """Returns a list of available local models."""
    return ["llama3.2:3b", "qwen2.5-coder:1.5b"]

def get_groq_models():
    """Returns a list of available Groq models."""
    return ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]

def is_groq_available():
    """Checks if Groq API key is set."""
    return os.getenv("GROQ_API_KEY") is not None or "GROQ_API_KEY" in st.secrets
