import model
import streamlit as st

if __name__ == '__main__':
    st.title("GitChat")
    st.subheader("Answer Questions about a Github Repo")
    collection = st.text_input("Enter the repo url")
    if collection.strip() != "":
        collection = collection.split("/")[-2] + "/" + collection.split("/")[-1]
    question = st.text_input("Enter your question about the repo")
    if st.button("Answer"):
        st.write_stream(model.query(collection, question))