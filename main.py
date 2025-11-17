from fastapi import FastAPI, HTTPException
from data.pull_data import pull_data_threaded
from vector_db.embeddings import transform_data, create_query_embedding
from vector_db.index import FaissIndex
from nlp.llm import query_llm_for_qa
import sys, os
from pathlib import Path
from pydantic import BaseModel

# Add the parent directory of AskAurora to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Initialize FAISS index and sentences list
faiss_index = FaissIndex(dim=384)
sentences = []

RAW_DATA_DIR = "data/raw_data"

# Run the data pulling and indexing process only if raw data directory is empty
if not os.path.exists(RAW_DATA_DIR) or len(os.listdir(RAW_DATA_DIR)) == 0:
    # Pull data 
    pull_data_threaded(RAW_DATA_DIR)

# Transform data and build FAISS index
sentences = transform_data(RAW_DATA_DIR, faiss_index)

# Initialize FastAPI app
app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_endpoint(request: QuestionRequest):
    global faiss_index, sentences

    # Get query embedding
    query_embedding = create_query_embedding(request.question)

    # Find nearest neighbors
    indices = faiss_index.search(query_embedding, top_k=10)
    print("indices", indices, type(indices))
    top_sentences = [sentences[i] for i in indices[0]]
    print("top_sentences", top_sentences)

    # Step 3: Query LLM
    response = query_llm_for_qa(request.question, top_sentences)

    return {"answer": response['answer']}