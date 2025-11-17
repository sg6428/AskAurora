from sentence_transformers import SentenceTransformer
import numpy as np
import json, os

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def create_user_msg_pair(data):
    user_msg_pairs = []
    for item in data:
        user_name = item.get('user_name', 'Unknown')
        message = item.get('message', '')
        user_msg_pairs.append(f"{user_name} - {message}")
    return user_msg_pairs

def transform_data(raw_data_dir, faiss_index):
    # read all json files in raw_data directory one by one
    sentences = []
    for filename in os.listdir(raw_data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(raw_data_dir, filename)
            with open(file_path, 'r') as f:
                raw_messages = json.load(f)
                sentences.extend(create_user_msg_pair(raw_messages))
    create_embeddings_raw_data(sentences, faiss_index)
    return sentences

def create_embeddings_raw_data(sentences, faiss_index):
    # generate embeddings
    embeddings = MODEL.encode(sentences)
    embeddings = np.array(embeddings).astype('float32')
    faiss_index.add_embeddings(embeddings)

def create_query_embedding(query):
    query_embedding = MODEL.encode([query])
    query_embedding = np.array(query_embedding).astype('float32')
    return query_embedding