from flask import Flask, request, jsonify, send_file
from flask_pymongo import PyMongo
from datetime import datetime
from mongo_api import MongoAPI
from s3_api import s3API
from helpers import generate_metadata
from dotenv import load_dotenv
from bson import ObjectId
import io
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
flask_port = int(os.getenv('FLASK_PORT'))

# setting up MongoDB
app.config['MONGO_URI'] = os.getenv('MONGODB_URI')
mongo = PyMongo(app)
mongoObj = MongoAPI(mongo)

# setting up s3
aws_access_key_id=str(os.getenv('AWS_ACCESS_KEY_ID'))
aws_secret_access_key=str(os.getenv('AWS_SECRET_ACCESS_KEY'))
bucket_name = str(os.getenv('AWS_S3_BUCKET_NAME'))
endpoint_url = str(os.getenv('MINIO_ENDPOINT_URL'))
s3Obj = s3API(aws_access_key_id, aws_secret_access_key, endpoint_url)

@app.route('/files/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file provided'}), 400
    
    file_id = str(ObjectId()) # Generate a new ObjectId
    file_bytes = file.read()
    file_type = file.content_type
    file_obj = io.BytesIO(file_bytes) # Wrap file_bytes in io.BytesIO

    metadata = generate_metadata(file_id, file.filename, len(file_bytes), file_type)
    
    # Upload to S3
    try:
        s3Obj.upload_to_s3(bucket_name, file_id, file_obj, file_type)
    except Exception as e:
        return jsonify({'error': f'Error uploading to S3: {str(e)}'}), 500

    # Save metadata to MongoDB
    try:
        mongoObj.save_file_metadata(metadata)
    except Exception as e:
        return jsonify({'error': f'Error saving metadata to MongoDB: {str(e)}'}), 500

    return jsonify({'fileId': file_id}), 201

@app.route('/files/<file_id>', methods=['GET'])
def read_file(file_id):
    # Read from MongoDB
    try:
        file_metadata = mongoObj.get_file_metadata(str(file_id))
    except Exception as e:
        return jsonify({'error': f'Error retrieving metadata from MongoDB: {str(e)}'}), 500
    
    if not file_metadata:
        return jsonify({'error': 'File not found'}), 404

    # Download from S3
    try:
        file_data = s3Obj.download_from_s3(bucket_name, file_id)
    except Exception as e:
        return jsonify({'error': f'Error downloading from S3: {str(e)}'}), 500

    return send_file(io.BytesIO(file_data), as_attachment=True, download_name=file_metadata['file_name'], mimetype=file_metadata['file_type'])

@app.route('/files/<file_id>', methods=['PUT'])
def update_file(file_id):
    file = request.files.get('file')
    form_data = request.form.to_dict()

    if not file:
        # case: if they want to change the file name of existing file and not the file itself.
        # PS: they cant change size, type, id without changing file itself so considering only filename change for metadata updation
        try:
            new_metadata = {
                "file_name": form_data["file_name"]
            }
        except:
            return jsonify({'error': 'No file nor new file_name metadata provided'}), 404
    else:
        file_bytes = file.read()
        file_obj = io.BytesIO(file_bytes) # Wrap file_bytes in io.BytesIO
        file_type = file.content_type

        new_metadata = generate_metadata(file_id, file.filename, len(file_bytes), file_type)

        # Upload to S3
        try:
            s3Obj.upload_to_s3(bucket_name, file_id, file_obj, file_type)
        except Exception as e:
            return jsonify({'error': f'Error uploading to S3: {str(e)}'}), 500

    # Update metadata in MongoDB
    try:
        result = mongoObj.update_file_metadata(file_id, new_metadata)
        if result.matched_count == 0:
            return jsonify({'error': f'File not found with the specified file_id.'}), 400
    except Exception as e:
        return jsonify({'error': f'Error updating metadata in MongoDB: {str(e)}'}), 500

    return jsonify({'message': 'File updated successfully'}), 200

@app.route('/files/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    # Delete file from S3
    try:
        s3Obj.delete_from_s3(bucket_name, file_id)
    except Exception as e:
        return jsonify({'error': f'Error deleting from S3: {str(e)}'}), 500

    # Delete metadata from MongoDB
    try:
        result = mongoObj.delete_file_metadata(file_id)
        if result.deleted_count == 0:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Error deleting metadata from MongoDB: {str(e)}'}), 500

    return jsonify({'message': 'File deleted successfully'}), 200

@app.route('/files', methods=['GET'])
def list_files():
    # Fetch list of files from MongoDB
    try:
        files = mongoObj.list_files_metadata()
    except Exception as e:
        return jsonify({'error': f'Error retrieving file list from MongoDB: {str(e)}'}), 500

    if len(files) == 0:
        return jsonify("No files, empty bucket."), 200

    return jsonify(files), 200

if __name__ == '__main__':
    app.run(host="localhost", port=flask_port, debug=True)
