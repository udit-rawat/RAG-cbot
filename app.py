# File: app.py
# Description: Implements a Flask API for the RAG chatbot and stores chat history in MySQL.

from flask import Flask, request, jsonify, render_template
import mysql.connector
from datetime import datetime
from rag_generation import load_resources, rag_pipeline
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# MySQL configuration from environment variables
db_config = {
    'host': os.getenv('MYSQL_HOST'),
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'database': os.getenv('MYSQL_DATABASE')
}

# Create MySQL connection


def get_db_connection():
    """
    Creates and returns a MySQL connection.
    """
    conn = mysql.connector.connect(**db_config)
    return conn

# Create chat history table if it doesn't exist


def initialize_database():
    """
    Initializes the MySQL database and creates the chat_history table.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME,
            role ENUM('user', 'system'),
            content TEXT
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Store a message in the chat history


def store_message(role, content):
    """
    Stores a user query or system answer in the chat history.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO chat_history (timestamp, role, content)
        VALUES (%s, %s, %s)
    """, (datetime.now(), role, content))
    conn.commit()
    cursor.close()
    conn.close()

# Retrieve chat history


def get_chat_history():
    """
    Retrieves the chat history from the database.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("USE chat_history")
    cursor.execute("SELECT * FROM chat_history ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return rows

# Flask endpoint: / (Homepage)


@app.route('/')
def home():
    """
    Serves the index.html file as the homepage.
    """
    return render_template('index.html')

# Flask endpoint: /chat


@app.route('/chat', methods=['POST'])
def chat():
    """
    Accepts a user query, generates an answer, and stores the query and answer in the database.
    """
    data = request.json
    query = data.get('query')

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Load resources (FAISS index, chunks, and model)
    chunks, index, model = load_resources()

    # Generate answer using the RAG pipeline
    answer, top_chunks = rag_pipeline(query, chunks, index, model)

    # Store user query and system answer in the database
    store_message('user', query)
    store_message('system', answer)

    # Return the answer and top chunks (optional)
    return jsonify({
        "answer": answer,
        "top_chunks": top_chunks  # Optional: for debugging
    })

# Flask endpoint: /history


@app.route('/history', methods=['GET'])
def history():
    """
    Returns the chat history from the database.
    """
    chat_history = get_chat_history()
    return jsonify(chat_history)


if __name__ == "__main__":
    # Initialize the database
    initialize_database()

    # Run the Flask app
    app.run(debug=True)
