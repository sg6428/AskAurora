from ollama import Client
from dotenv import load_dotenv
import os
import json

load_dotenv()

client_api_key = os.getenv("OLLAMA_API_KEY")

client = Client(
    host="https://ollama.com",
    headers={"Authorization": f"Bearer {client_api_key}"}
)

def query_llm_for_qa(asked_question, top_sentences, model="gpt-oss:20b-cloud"):
    messages = [
        {
            "role": "system", "content": "You are a helpful assistant that provides answers based on the provided context.\
                You will be given a question and some context sentences. Use the context to answer the question as accurately as possible.\
                Respond only in following JSON format: {\"answer\": \"your answer here\"}"
        },
        {
            "role": "user", "content": f"question:{asked_question}, context sentences:{top_sentences}"
        }
    ]

    response = client.chat(model, messages=messages, stream=False)
    answer_json = json.loads(response['message']['content'])

    return answer_json
