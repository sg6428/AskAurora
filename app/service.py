from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from AskAurora.data.pull_data import pull_data_threaded
from AskAurora.vector_db.embeddings import transform_data, create_query_embedding
from AskAurora.vector_db.index import FaissIndex
from AskAurora.nlp.llm import query_llm_for_qa

# Initialize FastAPI app
app = FastAPI()

# Initialize FAISS index and sentences list
faiss_index = FaissIndex(dim=384)
sentences = []

RAW_DATA_DIR = "../data/raw_data"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global faiss_index, sentences

    # Pull data 
    pull_data_threaded(RAW_DATA_DIR)

    # Transform data and build FAISS index
    sentences = transform_data(RAW_DATA_DIR, faiss_index)

@app.post("/ask")
async def ask_endpoint(question: str):
    global faiss_index, sentences

    # Get query embedding
    query_embedding = create_query_embedding(question)

    # Find nearest neighbors
    indices = faiss_index.search(query_embedding, top_k=3)
    top_sentences = [sentences[i] for i in indices]

    # Step 3: Query LLM
    response = query_llm_for_qa(question, top_sentences)

    return {"answer": response}

