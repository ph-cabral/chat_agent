from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from vectordb import VectorDB
from llm import LLMClient
from loader import load_initial_data

app = FastAPI(title="RAG RRHH API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_db = VectorDB()
llm_client = LLMClient()

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]

@app.on_event("startup")
async def startup_event():
    print("Cargando archivos iniciales...")
    load_initial_data()
    print("✅ Carga completada!")

@app.get("/")
async def root():
    return {"status": "ok", "message": "RAG RRHH API funcionando"}

@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    try:
        results = []
        for file in files:
            content = await file.read()
            file_path = f"/app/data/{file.filename}"
            
            os.makedirs("/app/data", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(content)
            
            vector_db.add_document(file_path, file.filename)
            results.append({"filename": file.filename, "status": "processed"})
        
        return {"message": "Archivos procesados", "files": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        relevant_docs = vector_db.search(request.question, top_k=request.top_k)
        context = "\n\n".join([doc["text"] for doc in relevant_docs])
        answer = llm_client.generate_answer(request.question, context)
        
        return QueryResponse(
            answer=answer,
            sources=[{"filename": doc["metadata"]["filename"], 
                     "score": doc["score"]} for doc in relevant_docs]
        )
    except Exception as e:
        import traceback
        print("ERROR COMPLETO:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/health")
async def health():
    return {
        "qdrant": vector_db.is_healthy(),
        "ollama": llm_client.is_healthy()
    }
