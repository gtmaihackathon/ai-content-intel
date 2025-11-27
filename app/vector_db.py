import faiss, numpy as np

class FAISSIndex:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.asset_map = []  # map idx -> asset_id

    def add(self, vectors, asset_ids):
        self.index.add(vectors)
        self.asset_map.extend(asset_ids)

    def search(self, query_vector, top_k=5):
        D, I = self.index.search(np.array([query_vector]), top_k)
        results = [(self.asset_map[i], float(D[0][j])) for j, i in enumerate(I[0])]
        return results

