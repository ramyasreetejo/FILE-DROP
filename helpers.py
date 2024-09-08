from datetime import datetime
from bson.objectid import ObjectId

# Helper function to generate file metadata
def generate_metadata(file_id, file_name, file_size, file_type):
    return {
        '_id': ObjectId(file_id),
        'file_id': file_id,
        'file_name': file_name,
        'file_size': file_size,
        'file_type': file_type,
        'created_at': datetime.utcnow()
    }