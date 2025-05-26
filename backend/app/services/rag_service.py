from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    DirectoryLoader,
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredFileLoader
)
from langchain.llms import Ollama
from langchain.chains import RetrievalQA
import os

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.vectorstore = None
        self.llm = Ollama(model="llama2")
        self.initialize_vectorstore()

    def initialize_vectorstore(self):
        """Initialize or load the vector store"""
        persist_directory = "data/chroma"
        if os.path.exists(persist_directory):
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )
        else:
            self.vectorstore = Chroma(
                persist_directory=persist_directory,
                embedding_function=self.embeddings
            )

    def get_loader_for_file(self, file_path: str):
        """Get the appropriate loader for a file based on its extension"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.txt':
            return TextLoader(file_path)
        elif file_extension == '.pdf':
            return PyPDFLoader(file_path)
        elif file_extension == '.docx':
            return Docx2txtLoader(file_path)
        else:
            # Fallback to unstructured loader for other file types
            return UnstructuredFileLoader(file_path)

    def ingest_documents(self, directory_path: str):
        """Ingest documents from a directory"""
        # Get all files in the directory
        files = []
        for root, _, filenames in os.walk(directory_path):
            for filename in filenames:
                if filename.endswith(('.txt', '.pdf', '.docx')):
                    files.append(os.path.join(root, filename))

        if not files:
            raise ValueError("No supported files found in the directory")

        # Load and process each file
        all_documents = []
        for file_path in files:
            try:
                loader = self.get_loader_for_file(file_path)
                documents = loader.load()
                all_documents.extend(documents)
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
                continue

        if not all_documents:
            raise ValueError("No documents were successfully loaded")

        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(all_documents)
        
        # Add to vector store
        self.vectorstore.add_documents(texts)
        self.vectorstore.persist()

    def query(self, query_text: str):
        """Query the RAG system"""
        retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )
        
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=True
        )
        
        result = qa_chain({"query": query_text})
        
        return {
            "answer": result["result"],
            "sources": [doc.page_content for doc in result["source_documents"]]
        } 