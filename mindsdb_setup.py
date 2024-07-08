import mindsdb_sdk

conn = mindsdb_sdk.connect("http://localhost:47334")
gitbot = conn.get_project('gitbot')
llm = gitbot.get_model('openai_llm')

def query(context, question):
    prompt = "Use the following pieces of context belonging to a github repo to answer the question at the end.\nIf you don't know the answer, just say that you don't know, don't try to make up an answer.\nAssume the user is a beginner and explain things properly.\nMention the source of the context at the end of the answer.\n\n{{context}}\n\nQuestion: {{question}}\n\nHelpful Answer: ",

    response =  llm.predict({
        'prompt': prompt
    })

    response = response.iloc[0]['response']
    
if __name__ == '__main__':
    response = query("My name is Kanak.", "How are you?")
    print(response)