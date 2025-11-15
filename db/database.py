from tinydb import TinyDB, Query

class Database:
    def __init__(self, db_path='raw.json'):
        self.db = TinyDB(db_path)

    def insert_message(self, message: dict):
        self.db.insert(message)

    def insert_multiple_messages(self, messages: list):
        self.db.insert_multiple(messages)

    def get_all_messages(self):
        return self.db.all()

    def find_message_by_id(self, message_id):
        return self.db.get(doc_id=message_id)