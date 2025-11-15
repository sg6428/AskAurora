# create records in the database sharded by user_id
from AskAurora.db.database import Database
import json
from tinydb import TinyDB, Query
import os
from collections import defaultdict

DB_PATH = "db.json"

# Initialize the database and the Query object
db = TinyDB(DB_PATH)
User = Query()

def process_and_update_db(raw_messages):
    print("Process")
    # Processes a small chunk of raw messages and inserts them into the TinyDB database.
    
    temp_user_data = defaultdict(lambda: {"messages": []})
    
    for message_item in raw_messages:
        user_id = message_item.get("user_id")
        username = message_item.get("user_name")
        
        if not user_id: continue
        
        # Initialize user details
        if "user_id" not in temp_user_data[user_id]:
            temp_user_data[user_id]["user_id"] = user_id
            temp_user_data[user_id]["user_name"] = username
        
        # Create the new message structure
        new_message = {
            "text": message_item.get("message"),
            "timestamp": message_item.get("timestamp"),
            "mesage_id": message_item.get("id")
        }
        temp_user_data[user_id]["messages"].append(new_message)

    
    # Update TinyDB for each unique user in the chunk
    for user_id, new_data in temp_user_data.items():     
        db.upsert(
            {
                'user_id': user_id, 
                'name': new_data['user_name'], 
                'messages': new_data['messages']
            },
            # find the existing document
            User.user_id == user_id
        )
        
        existing_doc = db.get(User.user_id == user_id)
        
        if existing_doc:
            # Document exists: Append messages to the list
            existing_messages = existing_doc.get('messages', [])
            existing_messages.extend(new_data['messages'])
            db.update({'messages': existing_messages}, User.user_id == user_id)
        else:
            # Document is new: Insert the whole document
            db.insert(new_data)

    print("END Process")

def transform_raw_data_to_db():
    print("Transform")
    # read all json files in raw_data directory one by one and transform them into the database
    raw_data_dir = "/Users/admin/Documents/dev/Aurora_Assessment/AskAurora/raw_data"
    for filename in os.listdir(raw_data_dir):
        if filename.endswith(".json"):
            file_path = os.path.join(raw_data_dir, filename)
            with open(file_path, 'r') as f:
                raw_messages = json.load(f)
                process_and_update_db(raw_messages)


if __name__ == "__main__":
    transform_raw_data_to_db()

