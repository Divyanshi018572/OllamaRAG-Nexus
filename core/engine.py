import os
import ollama
from groq import Groq
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

class RAGEngine:
    def __init__(self, persist_directory="data/vectorstore"):
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.splitter = RecursiveCharacterTextSplitter(chunk_size=700, chunk_overlap=100)
        
        # Initialize or load existing vectorstore
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

    def add_document(self, text, filename):
        """Splits text and adds to vectorstore."""
        chunks = self.splitter.split_text(text)
        metadata = [{"source": filename} for _ in chunks]
        
        self.vectorstore.add_texts(
            texts=chunks,
            metadatas=metadata
        )
        return len(chunks)

    def search(self, question, k=4):
        """Retrieves relevant chunks."""
        results = self.vectorstore.similarity_search(question, k=k)
        context = ""
        sources = []
        for res in results:
            context += res.page_content + "\n\n"
            sources.append(res.metadata.get("source", "Unknown"))
        return context, list(set(sources))

    def clear_database(self):
        """Resets the vectorstore."""
        self.vectorstore.delete_collection()
        self.vectorstore = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embeddings
        )

def get_answer_from_ollama(model, prompt, context):
    system_prompt = f"Answer the user question based ONLY on the provided context. Context:\n{context}"
    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response['message']['content']

def get_answer_from_groq(model, prompt, context, api_key):
    client = Groq(api_key=api_key)
    system_prompt = f"Answer the user question based ONLY on the provided context. Context:\n{context}"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
