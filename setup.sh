#!/bin/bash

# HackRx 6.0 Setup Script
# This script sets up the complete LLM-Powered Query-Retrieval System

echo "🚀 Setting up HackRx 6.0 Solution..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv hackrx_env
source hackrx_env/bin/activate

# Install dependencies
echo "📋 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Download required models (this may take a few minutes)
echo "🤖 Downloading language models..."
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
python -c "from transformers import pipeline; pipeline('text-generation', model='distilgpt2')"

# Set up ChromaDB directory
echo "💾 Setting up vector database..."
mkdir -p ./chromadb_data

echo "✅ Setup complete!"
echo ""
echo "To start the application:"
echo "1. Activate virtual environment: source hackrx_env/bin/activate"
echo "2. Run the server: uvicorn main:app --reload"
echo "3. Open http://localhost:8000/docs for API documentation"
echo ""
echo "To test with sample data, use the API endpoint /hackrx/run"