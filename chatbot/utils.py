import json
import os
from sentence_transformers import SentenceTransformer, util
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INTENTS_PATH = os.path.join(BASE_DIR, "intents.json")

# Cargar intents
with open(INTENTS_PATH, "r", encoding="utf-8") as f:
    intents = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

# Preparar embeddings de ejemplos
examples_embeddings = []
examples_intents = []

for intent in intents:
    for example in intent["examples"]:
        emb = model.encode(example)
        examples_embeddings.append(emb)
        examples_intents.append(intent["name"])

examples_embeddings = np.array(examples_embeddings)

def classify_intent(user_input: str, threshold=0.6):
    input_emb = model.encode(user_input)
    similarities = util.cos_sim(input_emb, examples_embeddings)[0].cpu().numpy()
    max_idx = np.argmax(similarities)
    max_score = similarities[max_idx]
    if max_score >= threshold:
        return examples_intents[max_idx]
    else:
        return "desconocido"

def get_response(intent_name: str):
    for intent in intents:
        if intent["name"] == intent_name:
            return intent["response"]
    return "Lo siento, no entiendo tu consulta."
