import os, numpy as np
import openai

OPENAI_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_KEY

def get_embedding(text, model="text-embedding-3-small"):
    text = text[:32000]
    resp = openai.Embedding.create(input=text, model=model)
    return np.array(resp["data"][0]["embedding"], dtype="float32")

