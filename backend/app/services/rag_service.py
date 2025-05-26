from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, TextLoader
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

    def ingest_documents(self, directory_path: str):
        """Ingest documents from a directory"""
        loader = DirectoryLoader(
            directory_path,
            glob="**/*.txt",
            loader_cls=TextLoader
        )
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
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