from groq import Groq
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.document_transformers import EmbeddingsClusteringFilter
from langchain_huggingface import HuggingFaceEmbeddings
import torch

device = "cpu"  # force CPU

# If you use SentenceTransformer directly:
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("model-name", device=device)

client = Groq(api_key="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")
def groq_response(text):
  try:
    prompt = f"""Generate a concise summary focussed on keeping the flow and facts of the text:
          
          content:
          {text}  # Increased context window
          """
    response = client.chat.completions.create(
         model="llama3-8b-8192",
         messages=[{"role": "user", "content": prompt}],
         temperature=0.1,
         max_tokens=256
     )
   
    text = response.choices[0].message.content
    return text
  except Exception as e:
        print(f"Groq API error: {e}")
        return ""

    
def summarize_document_with_kmeans_clustering(text, llm, embeddings):
    filter = EmbeddingsClusteringFilter(embeddings=embeddings, num_clusters=10)
    
    try:
       result = filter.transform_documents(documents=text)
       checker_chain = load_summarize_chain(llm ,chain_type="stuff")
       summary = checker_chain.run(result)
       return summary
    except Exception as e:
       return str(e)
    
model_name = "BAAI/bge-base-en-v1.5"
model_kwargs = {"device": "cuda"} # CUDA for GPU support
encode_kwargs = {"normalize_embeddings": True}
embeddings = HuggingFaceEmbeddings(
     model_name=model_name,
     model_kwargs=model_kwargs,
     encode_kwargs=encode_kwargs
)

def summarize_doc(text):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        docs = text_splitter.create_documents([text])
        
        # Summarize using KMeans clustering
        summary = summarize_document_with_kmeans_clustering(docs, groq_response, embeddings)
        
        return summary
    except Exception as e:
        print(f"Error in summarization: {e}")
        return ""