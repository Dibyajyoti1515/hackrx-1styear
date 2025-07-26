# HackRx 6.0 - LLM-Powered Query-Retrieval System

This is a complete solution for the HackRx 6.0 hackathon challenge that implements an intelligent document processing system using free and open-source technologies.

## Features

- **Document Processing**: Supports PDF and DOCX files
- **Semantic Search**: Uses ChromaDB for vector storage and Sentence Transformers for embeddings
- **Free LLM Integration**: Uses open-source models via Hugging Face Transformers
- **Explainable AI**: Provides detailed rationale for each decision
- **RESTful API**: FastAPI-based API following the HackRx specification

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   uvicorn main:app --reload
   ```

3. **Test the API**
   The API will be available at `http://localhost:8000`
   
   API Documentation: `http://localhost:8000/docs`

## API Usage

**Endpoint**: `POST /hackrx/run`

**Sample Request**:
```json
{
    "documents": "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D",
    "questions": [
        "What is the grace period for premium payment?",
        "What is the waiting period for pre-existing diseases?"
    ]
}
```

## File Structure

- `main.py`: FastAPI application and API endpoints
- `document_processor.py`: Document parsing and text extraction
- `vector_store.py`: ChromaDB integration for semantic search
- `llm_processor.py`: Language model integration and response generation
- `requirements.txt`: Python dependencies
- `Dockerfile`: Container configuration for deployment

## Docker Deployment

1. **Build the Docker image**:
   ```bash
   docker build -t hackrx-solution .
   ```

2. **Run the container**:
   ```bash
   docker run -p 8000:8000 hackrx-solution
   ```

## System Architecture

1. **Document Processing**: Downloads and extracts text from PDFs/DOCX
2. **Text Chunking**: Intelligently splits text with overlap for context preservation
3. **Embedding Generation**: Creates vector embeddings using Sentence Transformers
4. **Vector Storage**: Stores and retrieves embeddings using ChromaDB
5. **Query Processing**: Performs semantic search to find relevant context
6. **Answer Generation**: Uses open-source LLM to generate answers with explanations

## Customization

- **Change LLM Model**: Modify the model in `llm_processor.py` (e.g., use Llama 3.1)
- **Adjust Chunk Sizes**: Configure chunk_size and overlap in `main.py`
- **Vector Database**: Switch ChromaDB to FAISS or Pinecone in `vector_store.py`

## Notes

- This solution uses only free and open-source components
- The system provides explainable AI with decision rationale
- All responses include confidence scores and source citations
- The architecture is modular and easily extensible

## Troubleshooting

- If you encounter GPU issues, the system will fallback to CPU processing
- For large documents, consider adjusting chunk sizes for better performance
- OCR functionality requires additional setup for scanned PDFs

## License

Open source - feel free to modify and extend for your needs.