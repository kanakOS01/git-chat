import os
from dotenv import load_dotenv
import mindsdb_sdk

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEAVIATE_CLUSTER_URL = os.getenv("WEAVIATE_CLUSTER_URL")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

conn = mindsdb_sdk.connect("http://localhost:47334")

project_query = "CREATE PROJECT IF NOT EXISTS gitbot;"

ml_engine_query = f"""
CREATE ML_ENGINE IF NOT EXISTS gitbot.gemini_engine
FROM google_gemini
USING
    google_gemini_api_key = '{GOOGLE_API_KEY}'
"""

llm_query = """CREATE MODEL IF NOT EXISTS gitbot.gemini_llm
PREDICT response
USING
    engine = 'gemini_engine',
    model_name = 'gemini-pro',
    column = 'question',
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

# Executing above queries
conn.query(project_query).fetch()
conn.query(ml_engine_query).fetch()
conn.query(llm_query).fetch()
# conn.query(embeddings_query).fetch()
