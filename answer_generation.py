from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# -----------------------------
# Chroma DB Location
# -----------------------------
PERSIST_DIRECTORY = "db/chroma_db"

# -----------------------------
# Embedding Model
# -----------------------------
embedding_model = OllamaEmbeddings(model="nomic-embed-text:latest")

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
    search_kwargs={"k": 3, "score_threshold": 0.7},
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

# -----------------------------
# Combine Context
# -----------------------------
context = "\n\n".join(doc.page_content for doc in relevant_docs)

combined_input = f"""
Answer the question ONLY using the context below.

Context:
{context}

Question:
{query}

If the answer cannot be found in the context, reply exactly:

"I don't have enough information about this query."
"""

# -----------------------------
# Gemini Model
# -----------------------------
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0,
)

messages = [
    SystemMessage(
        content=(
            "You are a helpful AI assistant. "
            "Answer ONLY using the provided context. "
            "Do not make up information."
        )
    ),
    HumanMessage(content=combined_input),
]

# -----------------------------
# Generate Response
# -----------------------------
response = llm.invoke(messages)

print("\n========== Generated Response ==========\n")
print(response.content)
