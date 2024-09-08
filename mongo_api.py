from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

class MongoAPI:
    def __init__(self, mongo):
        self.mongo = mongo
        self.collection = self.mongo.db['files']  # Access the collection

    def save_file_metadata(self, metadata):
        insertedId = self.collection.insert_one(metadata).inserted_id
        return str(insertedId)

    def get_file_metadata(self, file_id):
        file_metadata = self.collection.find_one({'_id': ObjectId(file_id)})
        if file_metadata:
            return file_metadata
        return None

    def update_file_metadata(self, file_id, updates):
        # Ensure that we only update fields that are present in the `updates` dictionary
        update_data = {key: value for key, value in updates.items() if key in {'file_name', 'file_size', 'file_type', 'created_at'}}
        result = self.collection.update_one(
            {'file_id': file_id},
            {'$set': update_data}
        )
        return result

    def delete_file_metadata(self, file_id):
        result = self.collection.delete_one({'_id': ObjectId(file_id)})
        return result

    def list_files_metadata(self):
        files = self.collection.find()
        return [{key: value for key, value in file.items() if key != '_id'} for file in files]

