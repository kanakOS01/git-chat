import os
import weaviate
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import TextLoader
from langchain_weaviate.vectorstores import WeaviateVectorStore

load_dotenv()
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
# os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
# os.environ["WEAVIATE_API_KEY"] = os.getenv("WEAVIATE_API_KEY")

def setup_weaviate_client():
    weaviate_client = weaviate.connect_to_wcs(
        cluster_url=os.getenv('WEAVIATE_CLUSTER_URL'),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY"))
    )

    return weaviate_client

def setup_google_genai():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        api_key=os.getenv("GOOGLE_API_KEY")
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        api_key=os.getenv("GOOGLE_API_KEY")
    )

    return embeddings, llm

def setup_weaviate_vector_store(weaviate_client, embeddings, collection):
    if collection not in weaviate_client.collections.list_all():
        weaviate_client.collections.create(collection)
    
    vector_store = WeaviateVectorStore(
        client=weaviate_client,
        text_key="files", 
        index_name=collection,
        embedding=embeddings
    )

    return vector_store

if __name__ == "__main__":
    
    
    # loader = TextLoader("requirements2.txt")
    # docs = loader.load()

    # embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    # weaviate_client = weaviate.connect_to_wcs(
    #     cluster_url="https://gitbot-test-cluster-lswb4nem.weaviate.network",
    #     auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
    # )

    # print("Test" in weaviate_client.collections.list_all())

    # weaviate_collection = weaviate_client.collections.get("Test")

    # store = WeaviateVectorStore(
    #     client=weaviate_client, text_key="record", index_name="Test", embedding=embeddings
    # )
    # print(store)

    # query = "asdfgsadfasdgasdfhwertjrdf"
    # docs = store.similarity_search(query)

    for i, doc in enumerate(docs):
        print(f"\nDocument {i+1}:")
        print(doc.metadata)

    weaviate_client.close()
