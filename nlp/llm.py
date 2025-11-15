from ollama import chat, ChatResponse

def query_llm_for_ner(prompt: str, model: str = "llama2") -> ChatResponse:
    response = chat(model=model, messages=[
        {
            "role": "system", "content": "You are an expert named entity recognition (NER) model. \
                Extract the name of the person from the given text. \
                Return only the name without any additional information. \
                Follow the following format: {\"Name\": \"<extracted_name>\"}. If no name is found, return {\"Name\": \"\"}."
        },
        {
            "role": "user", "content": prompt
        }
    ])
    return response['message']['content']

def query_llm_for_qa(user_name: str, asked_question: str, msg_history:str, model: str = "llama2") -> ChatResponse:
    response = chat(model=model, messages=[
        {
            "role": "system", "content": "You are an expert who answers questions about users based on the that user's messaging history. \
                You will be provided with a user's name and their messaging history. \
                You are supposed to answer the asked question by referring to all of their messages.\
                Only use the information present in the messaging history to answer the question. \
                Provide concise and accurate answers.\
                Follow the following format: {Answer: <your_answer_here>} \
                If the answer is not present in the messaging history, return {Answer: UNKNOWN}.\
                Only return the JSON object without any additional text."
        },
        {
            "role": "user", "content": f"User's Name: {user_name}\nUser's Messaging History: {msg_history}\nQuestion: {asked_question}"
        }
    ])
    return response['message']['content']
