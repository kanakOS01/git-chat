import os
from dotenv import load_dotenv
import mindsdb_sdk

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

conn = mindsdb_sdk.connect("http://localhost:47334")

project_query = "CREATE PROJECT IF NOT EXISTS gitbot;"

ml_engine_query = f"""
CREATE ML_ENGINE IF NOT EXISTS gitbot.openai_engine
FROM openai
USING
    openai_api_key = '{OPENAI_API_KEY}'
"""



llm_query = """CREATE MODEL IF NOT EXISTS gitbot.openai_llm
PREDICT response
USING
    engine = 'openai_engine',
    model_name = 'gpt-4o',
    prompt_template = "Use the following pieces of context belonging to a github repo to answer the question at the end.\nIf you don't know the answer, just say that you don't know, don't try to make up an answer.\nAssume the user is a beginner and explain things properly.\nMention the source of the context at the end of the answer.\n\n{{context}}\n\nQuestion: {{question}}\n\nHelpful Answer: ",
    temperature = 0
"""

embeddings_query = """
CREATE MODEL IF NOT EXISTS gitbot.openai_embeddings
PREDICT response
USING 
    engine = 'openai_engine',
    mode = 'embedding',
    model_name = 'text-embedding-ada-002',
    question_column = 'content'
"""

# weaviate_query = f"""
# CREATE DATABASE IF NOT EXISTS vector_store
# WITH ENGINE = "weaviate",
#     PARAMETERS = {{
#         "weaviate_url": "{WEAVIATE_CLUSTER_URL}",
#         "weaviate_api_key": "{WEAVIATE_API_KEY}"
#     }};
# """

# Executing above queries
conn.query(project_query).fetch()
conn.query(ml_engine_query).fetch()
conn.query(llm_query).fetch()
conn.query(embeddings_query).fetch()
# conn.query(weaviate_query).fetch()
