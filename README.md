# Git Chat
Git Chat is a RAG application that allows you to have a q/a session with any github repository of your choice. This is especially helpful for beginners who find it difficult to understand complex open source code bases on github. 

It uses [weaviate cloud vector database](https://weaviate.io/) to store the embeddings, [MindsDB](https://www.mindsdb.com/) to host llm models and engines and facilitate queries with context and [streamlit](https://streamlit.io/) for UI along with [LangChain](https://www.langchain.com/) for some other processes.

## Getting started
#### Prerequisites
 - Python 3.7 or higher
 - Pip package manager
 - Docker

#### Setup

**1. Clone the Repository**
```bash
git clone https://github.com/kanakOS01/git-chat.git && cd git-chat
```

**2. Setup python virtual environment**

**3. Install dependencies**
```bash
pip install -r requirements
```

**4. Create .env file**
 - Create a .env file and add the following keys inside it
 - Get the google gemini api key [here](https://ai.google.dev/gemini-api/docs/api-key)
 - Get the weaviate api key and cluster url [here](https://console.weaviate.cloud/dashboard)
   - Create a new weaviate cluster and you will get the required api key and cluster url. Refer [this](https://weaviate.io/developers/weaviate/connections/connect-cloud) 
```
GOOGLE_API_KEY=""
WEAVIATE_API_KEY=""
WEAVIATE_CLUSTER_URL=""
```

**5. Setup MindsDB locally**
 - Run the MindsDB docker image.
```
docker run --name mindsdb_container -p 47334:47334 -p 47335:47335 mindsdb/mindsdb
```
 - Install google-generativeai package in this docker image
```
docker exec -it <container_id> /bin/bash
pip install google-generativeai
```

#### Start the application
 - Start `mindsdb_container`
```
docker start mindsdb_container
```

 - For a fresh setup run the python file using `python create_mindsdb_handlers.py`. This will create the required projects and models in you MindsDB container.

 - Run the application using
```
streamlit run main.py
```
 - The app will start on `localhost:8501`

### Note
- The repo data is stored in weaviate cloud. The data is persistent. If the repo is not present it is automatically created however this can take a long time depending on the size of the repository.
- It is recommended to use relatively smaller directories while testing (you may use a large repo although that will take some time)
- The process of embedding new repo data creates a transient `repo` subdirectory in the main directory. Make sure you do not have conflicting subdirectory.
