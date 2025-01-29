# **RAG-CBot**

A Retrieval-Augmented Generation (RAG) chatbot that uses a vector database for semantic search and stores chat history in a MySQL database. The chatbot is served via a Flask API.

---

## **Table of Contents**

1. [Installation](#installation)
2. [MySQL Setup](#mysql-setup)
3. [Testing Endpoints](#testing-endpoints)
4. [Environment Variables](#environment-variables)
5. [Docker Setup](#docker-setup)
6. [AWS Deployment](#aws-deployment)
7. [GitHub CI/CD](#github-cicd)

---

## **Installation**

### **Prerequisites**

- Python 3.8+
- MySQL
- Ollama (for llama3.2:latest model inference)

### **Install Ollama**

- **macOS**:

  ```bash
  brew install ollama
  ```

  Start the Ollama server:

  ```bash
  ollama serve
  ```

  Pull the Llama3.2 model:

  ```bash
  ollama pull llama3.2:latest
  ```

- **Windows**:
  Download the Ollama installer from [Ollama Releases](https://github.com/jmorganca/ollama/releases).
  Start the Ollama server and pull the Llama3.2 model as shown above.

### **Set Up a Virtual Environment**

1. Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

2. Activate the virtual environment:

   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## **MySQL Setup**

### **Install MySQL**

- **macOS**:
  ```bash
  brew install mysql
  ```
- **Windows**:
  Download and install MySQL from the [official website](https://dev.mysql.com/downloads/installer/).

### **Create Database and User**

1. Log in to MySQL:

   ```bash
   mysql -u root -p
   ```

2. Create the database:

   ```sql
   CREATE DATABASE chat_history;
   ```

3. Create a user and grant permissions:

   ```sql
   CREATE USER 'rag_user'@'localhost' IDENTIFIED BY 'secure_password'; -- replace it with the username and password of your choice!
   GRANT ALL PRIVILEGES ON chat_history.* TO 'rag_user'@'localhost';
   FLUSH PRIVILEGES;
   ```

4. Exit MySQL:
   ```sql
   exit;
   ```

---

## **Testing Endpoints**

### **Run the Flask App**

```bash
python app.py
```

### **Test Endpoints**

- **`/chat` Endpoint**:

  ```bash
  curl -X POST http://127.0.0.1:5000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What is machine learning?"}'
  ```

- **`/history` Endpoint**:
  ```bash
  curl http://127.0.0.1:5000/history
  ```

### **Run Unit Tests**

1. Navigate to the `test` directory:

   ```bash
   cd test
   ```

2. Run the tests:
   ```bash
   python -m unittest discover
   ```

---

## **Environment Variables**

Create a `.env` file in the root directory with the following layout:

```env
# File: .env
# Replace the values below with your MySQL credentials.
MYSQL_HOST=localhost
MYSQL_USER=rag_user
MYSQL_PASSWORD=secure_password
MYSQL_DATABASE=chat_history
```

---

## **Docker Setup**

### **Dockerfile**

```Dockerfile
# File: Dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the Flask app port
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
```

### **docker-compose.yml**

```yaml
# File: docker-compose.yml
version: "3.8"

services:
  rag-cbot:
    build: .
    ports:
      - "5000:5000"
    environment:
      - MYSQL_HOST=mysql
      - MYSQL_USER=rag_user
      - MYSQL_PASSWORD=secure_password
      - MYSQL_DATABASE=chat_history
    depends_on:
      - mysql

  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: chat_history
      MYSQL_USER: rag_user
      MYSQL_PASSWORD: secure_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### **Run the Application with Docker**

1. Build and start the containers:

   ```bash
   docker-compose up --build
   ```

2. Access the Flask app at:
   ```
   http://localhost:5000
   ```

---

## **AWS Deployment**

### **1. Set Up an EC2 Instance**

1. Launch an EC2 instance (e.g., Amazon Linux 2).
2. SSH into the instance:

   ```bash
   ssh -i your-key.pem ec2-user@your-ec2-ip
   ```

3. Install Docker and Docker Compose:

   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

4. Clone your repository:

   ```bash
   git clone https://github.com/your-username/rag-cbot.git
   cd rag-cbot
   ```

5. Run the application:
   ```bash
   docker-compose up --build
   ```

---

## **GitHub CI/CD**

### **Set Up GitHub Self-Hosted Runner**

1. Follow the [GitHub Actions self-hosted runner setup guide](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners).

2. Add a `.github/workflows/deploy.yml` file to your repository:

   ```yaml
   name: Deploy RAG-CBot

   on:
       push:
           branches:
               - main

   jobs:
       deploy:
           runs-on: self-hosted
           steps:
               - name: Checkout code
                   uses: actions/checkout@v2

               - name: Deploy with Docker Compose
                   run: |
                       docker-compose down
                       docker-compose up --build -d
   ```

3. Push the changes to trigger the deployment.

---

## **S3 for Data Storage (Optional)**

If you want to store the FAISS index or other data in S3:

1. Create an S3 bucket.
2. Use the `boto3` library to upload/download files:

   ```python
   import boto3

   s3 = boto3.client('s3')
   s3.upload_file('data/faiss_index.bin', 'your-bucket-name', 'faiss_index.bin')
   ```

---
