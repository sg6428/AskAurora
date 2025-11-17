from fastapi import FastAPI, HTTPException
from data.pull_data import pull_data_threaded
from vector_db.embeddings import transform_data, create_query_embedding
from vector_db.index import FaissIndex
from nlp.llm import query_llm_for_qa
import os
from pydantic import BaseModel
from config import config

raw_data_dir = config["raw_data_dir"]
api_url = config["api_url"]
page_limit = config["page_limit"]
model = config["model"]


# Initialize FAISS index and sentences list
faiss_index = FaissIndex(dim=384)
sentences = []

# Run the data pulling and indexing process only if raw data directory is empty
if not os.path.exists(raw_data_dir) or len(os.listdir(raw_data_dir)) == 0:
    pull_data_threaded(api_url, page_limit, raw_data_dir)

# Transform data and build FAISS index
sentences = transform_data(raw_data_dir, faiss_index)

# Initialize FastAPI app
app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_endpoint(request: QuestionRequest):
    global faiss_index, sentences

    try:
        # Get query embedding
        query_embedding = create_query_embedding(request.question)

        # Find nearest neighbors
        indices = faiss_index.search(query_embedding, top_k=10)
        top_sentences = [sentences[i] for i in indices[0]]

        # Step 3: Query LLM
        response = query_llm_for_qa(request.question, top_sentences, model)

        return {"answer": response['answer']}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")