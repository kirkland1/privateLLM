from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from services.rag_service import RAGService
import os
import shutil

app = FastAPI(title="Private LLM API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG service
rag_service = RAGService()

class Query(BaseModel):
    text: str
    context: Optional[List[str]] = None

class Response(BaseModel):
    answer: str
    sources: Optional[List[str]] = None

@app.get("/")
async def root():
    return {"message": "Private LLM API is running"}

@app.post("/query", response_model=Response)
async def query_endpoint(query: Query):
    try:
        result = rag_service.query(query.text)
        return Response(
            answer=result["answer"],
            sources=result["sources"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        # Create uploads directory if it doesn't exist
        os.makedirs("data/uploads", exist_ok=True)
        
        # Save the uploaded file
        file_path = f"data/uploads/{file.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Ingest the document
        rag_service.ingest_documents("data/uploads")
        
        return {"message": f"Successfully uploaded and processed {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 