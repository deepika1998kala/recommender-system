import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def build_embeddings():

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

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings, dtype=np.float32))

    faiss.write_index(index, "shl.index")

    print("Embeddings created")


if __name__ == "__main__":
    build_embeddings()