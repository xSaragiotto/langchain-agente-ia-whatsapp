import os

from decouple import config

from langchain_text_splitters import RecursiveCharacterTextSplitter # Versão atualizada
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_huggingface import HuggingFaceEmbeddings


# os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
os.environ['HUGGINGFACE_API_KEY'] = config('HUGGINGFACE_API_KEY')

if __name__ == '__main__':
    file_path = '/app/rag/data/nakaya-dados.pdf'
    loader = PyPDFLoader(file_path)
    pdf_rag = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, # Quantidade de quebras do documento em chunks
        chunk_overlap=200, # Tamanho dos tokens de overlap
    )
    chunks = text_splitter.split_documents(
        documents=pdf_rag,
    )

    persist_directory = '/app/chroma_data' # Local de criação do bd

    embedding = HuggingFaceEmbeddings() # Usando o embedding padrão
    vector_store = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
    )
    vector_store.add_documents(
        documents=chunks,
    )

