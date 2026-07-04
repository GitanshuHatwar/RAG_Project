
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


# -----------------------------
# Chroma DB Location
# -----------------------------
PERSIST_DIRECTORY = "db/chroma_db"

# -----------------------------
# Embedding Model
# -----------------------------
embedding_model = OllamaEmbeddings(
    model="nomic-embed-text:latest"
)

print("Loading Vector Store...")

db = Chroma(
    persist_directory=PERSIST_DIRECTORY,
    embedding_function=embedding_model,
    collection_metadata={"hnsw:space": "cosine"},
)

# -----------------------------
# User Query
# -----------------------------
query = "In which year did facebook purchased whatsapp and instagram"

# -----------------------------
# Retriever
# -----------------------------
retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k": 3,
        "score_threshold": 0.7
    },
)

relevant_docs = retriever.invoke(query)

# -----------------------------
# Display Retrieved Documents
# -----------------------------
print(f"\nUser Query: {query}")

print("\n----- Retrieved Context -----\n")

for i, doc in enumerate(relevant_docs, 1):
    print(f"Document {i}")
    print(doc.page_content)
    print("-" * 80)

# Synthetic Questions: 
#Who is the Founder of FoMoCo?
#Facebook bought Whatsapp and Instagram in which year?
#Why did mark created facesmash?

#To check chuking out of bound questions.
#Who founded Tesla?
#Is Mark Zukerburg a good person
#Who is faster Ford or Ferrari
