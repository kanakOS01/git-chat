import model
import streamlit as st

if __name__ == '__main__':
    st.title("GitChat")
    st.subheader("Answer Questions about a Github Repo")
    repo_url = st.text_input("Enter the repo URL", placeholder="https://github.com/owner/repo")
    if repo_url.strip() != "":
        collection = repo_url.split("/")[-2] + "/" + repo_url.split("/")[-1]
    question = st.text_input("Enter your question about the repo")
    
    if st.button("Answer"):
        with st.spinner("Checking collection status..."):
            weaviate_client = model.setup_weaviate_client()
            embeddings, llm = model.setup_google_genai()
            is_new_collection, vector_store = model.setup_weaviate_vector_store(
                weaviate_client=weaviate_client, embeddings=embeddings, collection=collection
            )
        
        if is_new_collection:
            with st.spinner("Creating a new collection for the repo. This may take a while..."):
                with st.spinner("Cloning the repo..."):
                    model.clone_repo(repo_url)
                with st.spinner("Uploading files to Weaviate..."):
                    model.load_repo_files(vector_store, collection)
                model.delete_local_repo()
        
        answer_stream = model.query(collection, question, vector_store, llm)
        st.write_stream(answer_stream)
