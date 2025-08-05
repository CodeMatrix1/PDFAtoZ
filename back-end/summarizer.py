from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import LLMChain
from langchain.document_transformers import EmbeddingsClusteringFilter
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


# ---- Embeddings Model Setup ----
model_name = "BAAI/bge-base-en-v1.5"
model_kwargs = {"device": "cpu"}
encode_kwargs = {"normalize_embeddings": True}

embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)
# ---- LLM (Groq) Setup ----
llm = ChatGroq(
    api_key=api_key,
    model_name="llama3-8b-8192",
    temperature=0.1,
    max_tokens=256
)

# ---- Prompt Template ----
summary_template = """
Generate a concise and factually accurate summary of the following content while preserving the logical flow:

Content:
{text}
"""

prompt = PromptTemplate(
    input_variables=["text"],
    template=summary_template
)

# ---- Summarization Chain using PromptTemplate ----
summary_chain = LLMChain(llm=llm, prompt=prompt)

# ---- Summarization Logic ----
def summarize_document_with_kmeans_clustering(documents, chain, embeddings):
    try:
        filter = EmbeddingsClusteringFilter(embeddings=embeddings, num_clusters=10)
        clustered_docs = filter.transform_documents(documents)

        # Combine text from clustered docs
        full_text = " ".join([doc.page_content for doc in clustered_docs])

        # Use LLMChain with prompt template
        summary = chain.run(text=full_text)
        return summary
    except Exception as e:
        return f"Error during summarization: {e}"

# ---- High-level Entry Point ----
def summarize_doc(text):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        docs = text_splitter.create_documents([text])
        summary = summarize_document_with_kmeans_clustering(docs, summary_chain, embeddings)
        return summary
    except Exception as e:
        print(f"Error in summarization: {e}")
        return ""
