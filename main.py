from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("BAAI/bge-m3")

# Sample document
text = """
Groundwater level in Nagpur district has shown fluctuations
during the years 2023 and 2024. Water conservation measures
have improved recharge in some regions.
"""

# Simple chunking
chunk_size = 100
chunks = []

for i in range(0, len(text), chunk_size):
    chunks.append(text[i:i + chunk_size])

# Create embeddings
vector_store = []

for chunk in chunks:
    embedding = model.encode(chunk)

    vector_store.append({
        "text": chunk,
        "embedding": embedding
    })

# Check result
print("Number of chunks:", len(vector_store))
print("Embedding dimensions:", len(vector_store[0]["embedding"]))
print("\nFirst chunk:")
print(vector_store[0]["text"])