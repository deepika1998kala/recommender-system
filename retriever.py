import json
import numpy as np

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

with open("catalog.json", "r") as f:
    catalog = json.load(f)

texts = []

for item in catalog:

    text = f"""
    {item['name']}
    {item['description']}
    {item['test_type']}
    """

    texts.append(text)

embeddings = model.encode(texts)


def retrieve_assessments(query, top_k=5):

    query_embedding = model.encode([query])

    similarities = cosine_similarity(
        query_embedding,
        embeddings,
    )[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for idx in top_indices:
        results.append(catalog[idx])

    return results