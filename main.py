import model
import streamlit as st

if __name__ == '__main__':
    st.title("GitChat")
    st.subheader("Answer Questions about a Github Repo")
    repo_url = st.text_input(label=":violet[Enter the repo URL]", placeholder="https://github.com/owner/repo")
    question = st.text_input(label=":violet[Enter you question]")