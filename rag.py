import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STORE = os.path.join(BASE_DIR, "backend", "storage")
os.makedirs(STORE, exist_ok=True)

os.makedirs(STORE, exist_ok=True)
print("RAG STORE PATH:", STORE)

def store_doc(doc_type, text):
    with open(f"{STORE}/{doc_type}.txt", "w", encoding="utf-8") as f:
        f.write(text)

def retrieve_context(doc_type, query, k=2000):
    path = f"{STORE}/{doc_type}.txt"
    if not os.path.exists(path):
        return ""
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text[:k]  # simple truncation (cheap & works)
