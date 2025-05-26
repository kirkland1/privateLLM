# Private LLM with RAG

This project implements a private LLM application with Retrieval-Augmented Generation (RAG) capabilities. It uses Ollama for the LLM, LangChain for RAG implementation, and Flutter for the frontend interface.

## Features

- Local LLM using Ollama with llama2 model
- Document ingestion and vector storage using Chroma
- RAG implementation with LangChain
- Modern Flutter UI for interaction
- FastAPI backend for serving the LLM and RAG functionality
- Support for text document ingestion
- Real-time chat interface with source citations
- Document upload functionality

## Prerequisites

- Python 3.8+
- Flutter SDK
- Ollama installed and running locally
- Git

### Installing Ollama

1. Visit [Ollama's official website](https://ollama.ai/) and download the appropriate version for your OS
2. Install Ollama following the platform-specific instructions
3. Pull the llama2 model:
```bash
ollama pull llama2
```

### Installing Flutter

1. Visit [Flutter's official website](https://flutter.dev/docs/get-started/install)
2. Download and install Flutter SDK
3. Add Flutter to your PATH
4. Verify installation:
```bash
flutter doctor
```

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd private-llm
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
flutter pub get
```

4. Create necessary directories:
```bash
mkdir -p data/uploads data/chroma
```

## Running the Application

1. Start Ollama (if not already running):
```bash
ollama serve
```

2. Start the backend server:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

3. Run the Flutter application:
```bash
cd frontend
flutter run
```

## Usage

### Document Upload

1. Click the upload button (📎) in the top-right corner of the application
2. Select a text document (.txt) to upload
3. Wait for the upload and processing to complete
4. You'll see a success message when the document is processed

### Chat Interface

1. Type your question in the text input field at the bottom of the screen
2. Press Enter or click the send button to submit your question
3. The AI will process your question and provide an answer
4. Source citations will be displayed below the answer if available

### Supported File Types

Currently, the application supports:
- Text files (.txt)

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── core/         # Core functionality
│   │   ├── models/       # Data models
│   │   ├── services/     # Business logic
│   │   └── utils/        # Utility functions
│   └── requirements.txt  # Python dependencies
├── frontend/
│   ├── lib/
│   │   ├── screens/      # UI screens
│   │   ├── widgets/      # Reusable widgets
│   │   ├── services/     # API services
│   │   └── models/       # Data models
│   └── pubspec.yaml      # Flutter dependencies
└── data/
    ├── uploads/          # Uploaded documents
    └── chroma/           # Vector database
```

## Technical Details

### Backend Components

- **FastAPI**: Web framework for the backend API
- **LangChain**: RAG implementation and document processing
- **Chroma**: Vector database for document storage
- **Ollama**: Local LLM integration
- **Sentence Transformers**: Text embeddings using all-MiniLM-L6-v2

### Frontend Components

- **Flutter**: Cross-platform UI framework
- **Provider**: State management
- **HTTP**: API communication
- **File Picker**: Document upload handling
- **Markdown**: Rich text rendering

## Troubleshooting

### Common Issues

1. **Ollama not running**
   - Ensure Ollama is installed and running
   - Check if the llama2 model is pulled
   - Verify Ollama is accessible at localhost:11434

2. **Backend connection issues**
   - Check if the FastAPI server is running
   - Verify the correct port (8000) is being used
   - Check for any error messages in the terminal

3. **Document upload failures**
   - Ensure the file is in a supported format
   - Check file permissions
   - Verify the uploads directory exists

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 