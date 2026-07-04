# imports

import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter , RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAI
from dotenv import load_dotenv
import ollama

load_dotenv()

print("Pipeline started")


# Function to laod  the documents
def load_documents(docs_path="docs"):
    print(f"Loading documents from {docs_path}...")

    if not os.path.exists(docs_path):
        raise FileNotFoundError(f"The specified path '{docs_path}' does not exist.")

    loader = DirectoryLoader(docs_path, glob="**/*.txt", loader_cls=TextLoader)
    documents = loader.load()

    if len(documents) == 0:
        raise FileNotFoundError(
            f"NO .txt files found in {docs_path}. Please add your company documents"
        )

    for i, doc in enumerate(documents[:2]):
        print(f"\nDocument {i+1}:")
        print(f" Source: {doc.metadata['source']}")
        print(f" Content lenght: {len(doc.page_content)} characters")
        print(f" Content preview:{doc.page_content[:100]}...")
        print(f" metadata: {doc.metadata}")

    return documents


def split_documents(documents, chunk_size=800, chunk_overlap=0):
    """split documents into smaller chunks with overlap"""
    print("Splitting ddocuemtns into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size, 
        chunk_overlap = chunk_overlap
    )
    chunks = text_splitter.split_documents(documents)

    if chunks:

        for i , chunk in enumerate(chunks[:5]):
            print(f"\n--Chunk {i+1}")
            print(f"Source: {chunk.metadata['source']}")
            print(f"lenght: {len(chunk.page_content)} characters")
            print(f"Content:")
            print(chunk.page_content)
            print("-" * 50)

        if len(chunks) > 5:
            print(f"\n... and {len(chunks) - 5} more chunks")

    return chunks


# def create_vector_store(chunks, persist_directory="db/chroma_db"):
#     print("Vectorinzing the Chunks")

#     embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

#     print("--Creating vector store ---")
#     vectorstore = Chroma.from_documents(
#         documents = chunks,
#         embedding = embedding_model,
#         persist_directory = persist_directory,
#         collection_metadata = {"hnsw:space":"cosine"}
#     )

#     print("---Finished creating vector store ---")

#     print(f"Vector store created and saved to {persist_directory}")
#     return vectorstore


def create_vector_store(chunks, persist_directory="db/chroma_db"):
    print("Vectorizing the chunks using Ollama...")

    embedding_model = OllamaEmbeddings(
        model="nomic-embed-text:latest"
    )

    print("--- Creating vector store ---")

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory=persist_directory,
        collection_metadata={"hnsw:space": "cosine"}
    )

    print("--- Finished creating vector store ---")
    print(f"Vector store created and saved to {persist_directory}")

    return vectorstore


# Main function to call all subfunctions
def main():

    documents = load_documents("docs")
    print(f"\nTotal docuemtns loadad : {len(documents)}")

    chunks = split_documents(documents)

    vectorstore = create_vector_store(chunks)


if __name__ == "__main__":
    main()
