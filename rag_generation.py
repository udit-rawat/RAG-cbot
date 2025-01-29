# File: rag_generation.py
# Description: Implements the RAG pipeline for generating answers using Llama3.2 via Ollama API.

import ollama
from embed_store import load_cleaned_chunks, load_faiss_index, retrieve_top_k_chunks
from sentence_transformers import SentenceTransformer

# Load the FAISS index and cleaned chunks


def load_resources():
    """
    Loads the FAISS index and cleaned chunks.
    """
    print("Loading resources...")
    chunks = load_cleaned_chunks('data/cleaned_chunks.txt')
    index = load_faiss_index('data/faiss_index.bin')
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return chunks, index, model

# Generate an answer using Llama3.2


def generate_answer(query, context_chunks):
    """
    Generates an answer using Llama3.2 via Ollama API.
    """
    # Combine the context chunks into a single string
    context = "\n".join(context_chunks)

    # Generate the answer using Llama3.2
    response = ollama.generate(
        model="llama3.2:latest",
        prompt=f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    )
    return response['response']

# RAG pipeline


def rag_pipeline(query, chunks, index, model, k=4):
    """
    Implements the RAG pipeline:
    1. Convert query to embedding.
    2. Retrieve top-k relevant chunks.
    3. Concatenate chunks into context.
    4. Generate answer using Llama3.2.
    """
    # Step 1: Retrieve top-k relevant chunks
    top_chunks = retrieve_top_k_chunks(query, model, index, chunks, k)

    # Step 2: Generate answer using Llama3.2
    answer = generate_answer(query, top_chunks)

    return answer, top_chunks


if __name__ == "__main__":
    # Step 1: Load resources
    chunks, index, model = load_resources()

    # Step 2: Test the RAG pipeline
    query = "What is the motto of the Nameless?"
    answer, top_chunks = rag_pipeline(query, chunks, index, model)

    # Display the results
    print(f"\nQuery: {query}")
    print(f"\nAnswer:\n{answer}")
    print("\nTop 4 Relevant Chunks:")
    for i, chunk in enumerate(top_chunks):
        print(f"\nChunk {i+1}:\n{chunk}")
