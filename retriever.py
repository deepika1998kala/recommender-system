import json
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

catalog = []

with open("catalog.json", "r") as f:
    catalog = json.load(f)


def fake_embedding(text):

    return np.random.rand(384)


def retrieve_assessments(query, top_k=5):

    query_embedding = fake_embedding(query)

    similarities = []

    for item in catalog:

        text = f"""
        {item['name']}
        {item['description']}
        {item['test_type']}
        """

        item_embedding = fake_embedding(text)

        similarity = cosine_similarity(
            [query_embedding],
            [item_embedding],
        )[0][0]

        similarities.append(similarity)

    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []

    for idx in top_indices:
        results.append(catalog[idx])

    return results