# File: embed_store.py
# Description: Generates embeddings for text chunks, stores them in a FAISS index, and implements retrieval.

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load the cleaned chunks from the previous phase


def load_cleaned_chunks(input_file="data/cleaned_chunks.txt"):
    """
    Loads the cleaned chunks from a file.
    """
    with open(input_file, "r") as f:
        chunks = [line.strip() for line in f.readlines()]
    return chunks

# Generate embeddings and create a FAISS index


def generate_embeddings_and_index(chunks):
    """
    Generates embeddings for the chunks and stores them in a FAISS index.
    """
    # Load the sentence embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Generate embeddings for the chunks
    print("Generating embeddings...")
    chunk_embeddings = model.encode(chunks)

    # Create a FAISS Flat Index
    dimension = chunk_embeddings.shape[1]  # Dimension of the embeddings
    index = faiss.IndexFlatL2(dimension)  # L2 distance for similarity search
    index.add(chunk_embeddings)  # Add embeddings to the index

    print(f"FAISS index created with {len(chunks)} chunks.")
    return model, index

# Retrieve top-k relevant chunks for a query


def retrieve_top_k_chunks(query, model, index, chunks, k=4):
    """
    Retrieves the top-k most relevant chunks for a given query.
    """
    # Convert query to embedding
    query_embedding = model.encode([query])

    # Search the FAISS index
    distances, indices = index.search(query_embedding, k)

    # Retrieve the top-k chunks
    top_k_chunks = [chunks[i] for i in indices[0]]
    return top_k_chunks

# Save the FAISS index to disk


def save_faiss_index(index, output_file="data/faiss_index.bin"):
    """
    Saves the FAISS index to a file.
    """
    faiss.write_index(index, output_file)
    print(f"FAISS index saved to '{output_file}'.")

# Load the FAISS index from disk


def load_faiss_index(input_file="data/faiss_index.bin"):
    """
    Loads the FAISS index from a file.
    """
    index = faiss.read_index(input_file)
    print(f"FAISS index loaded from '{input_file}'.")
    return index


if __name__ == "__main__":
    # Step 1: Load the cleaned chunks
    chunks = load_cleaned_chunks()

    # Step 2: Generate embeddings and create a FAISS index
    model, index = generate_embeddings_and_index(chunks)

    # Step 3: Save the FAISS index to disk
    save_faiss_index(index)

    # Step 4: Test retrieval
    query = "When was the American Civil War fought?"
    top_chunks = retrieve_top_k_chunks(query, model, index, chunks, k=4)
    print(f"\nTop 4 chunks for query: '{query}':")
    for i, chunk in enumerate(top_chunks):
        print(f"\nChunk {i+1}:\n{chunk}")
