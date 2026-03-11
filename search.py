# import numpy as np
# from sentence_transformers import SentenceTransformer
# from vector_store import store

# model = SentenceTransformer("BAAI/bge-small-en-v1.5")

# def search(query: str, top_k: int = 10):
#     query_vec = model.encode(query)
#     embeddings = np.array(store["embeddings"])

#     # Cosine Similarity
#     scores = embeddings @ query_vec / (
#         np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_vec)
#     )

#     top_indices = np.argsort(scores)[::-1][:top_k]
#     results = [store["chunks"][i] for i in top_indices]
#     return results


# OLD CODE ABOVE



import numpy as np
from sentence_transformers import SentenceTransformer
from vector_store import store

model = SentenceTransformer("BAAI/bge-small-en-v1.5")

def search(query: str, top_k: int = 10):
    query_vec = model.encode(query)
    embeddings = np.array(store["embeddings"])

    # Cosine Similarity
    scores = embeddings @ query_vec / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(query_vec)
    )

    top_indices = np.argsort(scores)[::-1]

    # Deduplicate while preserving score order
    seen = set()
    results = []
    for i in top_indices:
        chunk = store["chunks"][i]
        if chunk not in seen:
            seen.add(chunk)
            results.append(chunk)
        if len(results) == top_k:
            break

    return results