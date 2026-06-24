from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma


persistent_directory = "db/chroma_db"

embedding_model = OllamaEmbeddings(
    model = "nomic-embed-text:latest"
)

print("---creating vector store ---")

db = Chroma(
    persist_directory = persistent_directory,
    embedding_function = embedding_model,
    collection_metadata={"hnsw:space": "cosine"}
)

query = "who created ford company"
# retriever = db.as_retriever(search_kwargs={"k":3})

retriever = db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={
        "k":3,
        "score_threshold":0.7
    }
)
relevant_docs = retriever.invoke(query)

print(f"User Query : {query}")

print("--- Context  ----")
for i, doc in enumerate(relevant_docs ,1):
    print(f"Document {i}:\n{doc.page_content}\n")
