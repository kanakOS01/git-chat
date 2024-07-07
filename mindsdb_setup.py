import mindsdb_sdk

conn = mindsdb_sdk.connect("http://localhost:47334")
gitbot = conn.get_project('gitbot')
llm = gitbot.get_model('openai_llm')

def query(context, question):
    response =  llm.predict({
        'context': context,
        'question': question
    })

    response = response.iloc[0]['response']
    return response
    
if __name__ == '__main__':
    response = query("My name is Kanak.", "How are you?")
    print(response)