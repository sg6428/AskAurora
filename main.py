from fastapi import FastAPI, HTTPException
from data.pull_data import pull_data_threaded
from vector_db.embeddings import transform_data, create_query_embedding
from vector_db.index import FaissIndex
from nlp.llm import query_llm_for_qa
import os
from pydantic import BaseModel

raw_data_dir = os.getenv("RAW_DATA_DIR", "data/raw_data")
api_url = os.getenv("API_URL", "https://november7-730026606190.europe-west1.run.app/messages")
page_limit = int(os.getenv("PAGE_LIMIT", 500))
model = os.getenv("MODEL", "gpt-oss:20b-cloud")

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