import os
import weaviate
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import DirectoryLoader
from langchain_weaviate.vectorstores import WeaviateVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


def clone_repo(url):
    repo_name = url.split("/")[-1]
    repo_path = os.path.join("repo", repo_name)
    
    url = url + ".git"
    os.makedirs("repo", exist_ok=True)
    os.system(f"git clone {url} {repo_path}")


def delete_local_repo():
    os.system("rm -rf repo")


def setup_weaviate_client():
    weaviate_client = weaviate.connect_to_wcs(
        cluster_url=os.getenv("WEAVIATE_CLUSTER_URL"),
        auth_credentials=weaviate.auth.AuthApiKey(os.getenv("WEAVIATE_API_KEY")),
        skip_init_checks=True
    )

    return weaviate_client


def setup_google_genai():
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001", api_key=os.getenv("GOOGLE_API_KEY")
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_tokens=None,
        timeout=None,
        api_key=os.getenv("GOOGLE_API_KEY"),
    )

    return embeddings, llm


def setup_weaviate_vector_store(weaviate_client, embeddings, collection):
    is_new_collection = False
    collection = collection.replace("/", "__")
    all_collections = [key.lower() for key in weaviate_client.collections.list_all()]
    if collection not in all_collections:
        weaviate_client.collections.create(collection)
        is_new_collection = True

    vector_store = WeaviateVectorStore(
        client=weaviate_client,
        text_key="files",
        index_name=collection,
        embedding=embeddings,
    )

    return is_new_collection, vector_store


def load_repo_files(vector_store, collection):
    dir = collection.split("/")[1]

    unstructured_loader = DirectoryLoader(
        path=f"./repo/{dir}",
        # exclude=["**/.git/**"],
        glob=["**/*.pdf", "**/*.rst", "**/*.md", "**/*.doc", "**/*.docx", "**/*.pptx"],
        silent_errors=True,
        show_progress=True,
        use_multithreading=True,
        recursive=True,
        load_hidden=True,
    )
    text_loader = DirectoryLoader(
        path=f"./repo/{dir}",
        exclude=[
            "**/*.pdf",
            "**/*.rst",
            "**/*.md",
            "**/*.doc",
            "**/*.docx",
            "**/*.pptx",
        ],
        glob=["**/*.*"],
        silent_errors=True,
        show_progress=True,
        use_multithreading=True,
        recursive=True,
        load_hidden=True,
    )

    unstructured_docs = unstructured_loader.load()
    text_docs = text_loader.load()
    docs = unstructured_docs + text_docs

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    splits = text_splitter.split_documents(docs)

    vector_store.add_documents(documents=splits)


def format_docs(docs, collection):
    repo_owner, _ = collection.split("/")
    for doc in docs:
        source = doc.metadata["source"]
        doc.metadata["source"] = source[5:]
    formatted_docs =  "\n\n\n".join(
        "Source: " + doc.metadata["source"] + "\n\n" + doc.page_content for doc in docs
    )

    print(len(formatted_docs))
    return formatted_docs


def count_all_files(path):
    count = 0
    for _, _, files in os.walk(path):
        count += len(files)
    return count


def query(collection, question, vector_store, llm):
    # weaviate_client = setup_weaviate_client()
    # embeddings, llm = setup_google_genai()
    # is_new_collection, vector_store = setup_weaviate_vector_store(
    #     weaviate_client=weaviate_client, embeddings=embeddings, collection=collection
    # )

    # print("Collection exists" if not is_new_collection else "Creating Collection")
    # if is_new_collection:
    #     load_repo(vector_store, collection)

    retriever = vector_store.as_retriever(
        search_type="similarity", serach_kwargs={"k": 5}
    )
    # print(format_docs(retrieved_docs, collection))

    template = """Use the following pieces of context belonging to a github repo to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
Assume the user is a beginner and explain things properly.
Mention the source of the context at the end of the answer.

{context}

Question: {question}

Helpful Answer:"""

    rag_prompt = PromptTemplate.from_template(template)

    retrieved_docs = format_docs(retriever.invoke(question), collection)
    rag_chain = rag_prompt | llm | StrOutputParser()

    return rag_chain.stream({"context": retrieved_docs, "question": question})

if __name__ == "__main__":
    pass    
