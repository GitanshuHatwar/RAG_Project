import os
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_openai import OpenAI
from dotenv import load_dotenv
import ollama

load_dotenv()


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

def main():
    print("this is the main function")


if __name__ == "__main__":
    main()
