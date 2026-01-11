# PersonalChatbot

A Retrieval-Augmented Generation (RAG) chatbot that answers questions based on a local knowledge base of uploaded documents, enhanced with natural language processing and session memory.

## Description

PersonalChatbot is a web-based application that allows users to upload documents (PDFs, text files, etc.) and interact with an AI-powered chatbot. The system uses embeddings and vector search to retrieve relevant context from the uploaded documents, then generates responses using a language model. It features a FastAPI backend for handling API requests and a Streamlit frontend for the user interface.

## Features

- **Document Upload**: Upload multiple documents to build your personal knowledge base
- **Intelligent Q&A**: Ask questions and get context-aware answers based on your documents
- **Vector Search**: Uses embeddings for efficient retrieval of relevant information
- **Session Memory**: Maintains conversation history for contextual responses
- **Web Interface**: User-friendly Streamlit UI for easy interaction
- **REST API**: FastAPI-based backend with endpoints for chat and document management
- **Extensible**: Modular architecture for easy customization and extension

## Architecture

The application consists of three main components:

- **API (`api/`)**: FastAPI server handling chat requests, document uploads, and QA pipeline
- **Client (`client/`)**: Streamlit web application for user interaction
- **Config (`config/`)**: Configuration files (YAML-based settings)
- **Data (`data/`)**: Storage for embeddings, uploads, and vector store data

Key modules:

- `qa_pipeline.py`: Orchestrates the question-answering process
- `embeddings.py`: Handles text embedding generation
- `vector_store.py`: Manages vector storage and similarity search
- `utils.py`: Utility functions
- `schemas.py`: Pydantic models for API validation

## Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git (for cloning the repository)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/PersonalChatbot.git
   cd PersonalChatbot
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   _Note: You'll need to create a `requirements.txt` file with the necessary packages. Based on the code, you'll likely need:_

   - fastapi
   - uvicorn
   - streamlit
   - requests
   - pydantic
   - numpy
   - sentence-transformers (or similar for embeddings)
   - faiss-cpu (or similar for vector storage)
   - python-multipart (for file uploads)

## Configuration

The application uses a YAML configuration file located at `config/settings.yaml`. Currently, this file is empty, but you can add settings such as:

```yaml
# Example configuration
embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
vector_store_type: "faiss"
max_upload_size: 10MB
api_host: "localhost"
api_port: 8000
```

## Running the Application

1. **Start the API server:**

   ```bash
   cd api
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start the client (in a separate terminal):**

   ```bash
   cd client
   streamlit run app.py
   ```

3. **Access the application:**
   - Web UI: Open your browser and go to `http://localhost:8501`
   - API documentation: Visit `http://localhost:8000/docs` for interactive API docs

## Usage

1. **Upload Documents:**

   - Use the file uploader in the Streamlit interface to upload your documents
   - Supported formats: PDF, TXT, DOCX (depending on your text extraction implementation)

2. **Ask Questions:**

   - Type your question in the text input field
   - Click "Ask" to get a response based on your uploaded documents
   - View the sources used to generate the answer

3. **API Usage:**
   - **Chat endpoint:** `POST /api/chat` with JSON body `{"prompt": "your question", "history": []}`
   - **Upload endpoint:** `POST /api/upload` with multipart form data containing files

## API Endpoints

- `GET /`: Health check
- `POST /api/chat`: Send a chat message and receive a response
- `POST /api/upload`: Upload documents for processing

For detailed API documentation, visit `http://localhost:8000/docs` when the server is running.

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add your feature'`
5. Push to the branch: `git push origin feature/your-feature`
6. Submit a pull request

## Testing

Run tests using pytest (if implemented):

```bash
pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with FastAPI, Streamlit, and modern NLP techniques
- Inspired by retrieval-augmented generation research

## Support

If you encounter any issues or have questions, please open an issue on the GitHub repository.
