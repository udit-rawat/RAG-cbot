# File: data_preprocessing.py
# Description: Downloads a small text corpus, cleans it, and splits it into chunks.

from datasets import load_dataset
import re
import os


def clean_text(text):
    """
    Cleans the text by removing extra whitespaces and non-alphanumeric characters.
    """
    text = re.sub(
        r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'[^\w\s.,!?]', '', text)  # Remove special characters
    return text.strip()


def chunk_text(text, chunk_size=200):
    """
    Splits the text into chunks of approximately `chunk_size` words.
    """
    words = text.split()
    chunks = [' '.join(words[i:i + chunk_size])
              for i in range(0, len(words), chunk_size)]
    return chunks


def load_and_preprocess_data():
    """
    Downloads the dataset, cleans the text, and splits it into chunks.
    """
    # Load the wikitext dataset from Hugging Face
    print("Downloading the wikitext dataset...")
    dataset = load_dataset("wikitext", "wikitext-2-raw-v1", split="train")

    # Clean and chunk the dataset
    cleaned_chunks = []
    for example in dataset:
        if example['text'].strip():  # Skip empty lines
            cleaned_text = clean_text(example['text'])
            chunks = chunk_text(cleaned_text)
            cleaned_chunks.extend(chunks)

    return cleaned_chunks


def save_cleaned_chunks(cleaned_chunks, output_dir="data"):
    """
    Saves the cleaned chunks to a file.
    """
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Save the cleaned chunks to a file
    output_file = os.path.join(output_dir, "cleaned_chunks.txt")
    with open(output_file, "w") as f:
        for chunk in cleaned_chunks:
            f.write(chunk + "\n")
    print(f"Saved {len(cleaned_chunks)} cleaned chunks to '{output_file}'.")


if __name__ == "__main__":
    # Step 1: Download and preprocess the data
    cleaned_chunks = load_and_preprocess_data()

    # Step 2: Save the cleaned chunks to a file
    save_cleaned_chunks(cleaned_chunks)
