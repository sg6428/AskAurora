import faiss
import numpy as np
import os

class FaissIndex:
    def __init__(self, dim, index_file="faiss_index.bin"):
        self.dim = dim
        self.index_file = index_file
        if os.path.exists(self.index_file):
            self.index = faiss.read_index(self.index_file)
        else:
            self.index = faiss.IndexFlatL2(self.dim)

    def add_embeddings(self, embeddings):
        embeddings = np.array(embeddings).astype('float32')
        self.index.add(embeddings)
        print(f"Added {len(embeddings)} embeddings to the index")

    def search(self, query_embedding, top_k=3):
        query_embedding = np.array(query_embedding).astype('float32')
        _, indices = self.index.search(query_embedding, top_k)
        return indices

    def save_index(self):
        faiss.write_index(self.index, self.index_file)