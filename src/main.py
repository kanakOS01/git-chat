import re
import streamlit as st
from weaviate_setup import retrieve_docs, setup_weaviate_client, load_repo_files
from mindsdb_setup import query

def is_github_url(repo_url):
    github_url_pattern = r'https?://github\.com/([a-zA-Z0-9\-_]+)/([a-zA-Z0-9\-_]+)'
    if re.match(github_url_pattern, repo_url):
        return True
    else:
        return False

if __name__ == '__main__':
    st.set_page_config(page_title="GitChat", page_icon="🤖", layout="centered")
    st.title("GitChat")
    st.subheader("Answer Questions about a Github Repo")
    repo_url = st.text_input(label=":violet[Enter the repo URL]", placeholder="https://github.com/owner/repo")
    question = st.text_input(label=":violet[Enter you question]")
    submit = st.button(label=":violet[Answer]")

    if is_github_url(repo_url.strip()):
        print(repo_url)
        with st.spinner("Checking repository status..."):
            is_new_collection, vector_store =  setup_weaviate_client(repo_url.strip())

        if is_new_collection:
            with st.spinner(f"Repository not present. Setting up {repo_url}"):
                load_repo_files(vector_store, repo_url.strip())
        
        if question and submit:
            with st.spinner("Fetching relevant docs..."):
                retrieved_docs = retrieve_docs(question, vector_store)
            
            with st.spinner():
                response = query(retrieved_docs, question)

            st.write(response)
