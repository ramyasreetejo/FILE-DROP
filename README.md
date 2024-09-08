# FILE DROP

FILE DROP is a Dropbox-like service where users can upload, retrieve, and manage their files through a set of RESTful APIs. The service also supports the storage of metadata for each uploaded file, such as the file name, creation timestamp, file size, file type.

### TECH STACK:
* Python with Flask - Backend Server
* MongoDB - Metadata Storage
* AWS S3 - File storage (Used minio as an alternative to AWS S3 which supports all operations that S3 file storage supports)

### Features/APIs:

**Upload File API**: Allow users to upload files onto the platform
* Endpoint: POST /files/upload
* Input: File upload / File binary data
* Output: A unique file identifier
* Metadata Saved: File id, File name, Created at timestamp, File size, File type

**Read File API**: Retrieve a specific file based on a unique identifier - File Id
* Endpoint: GET /files/{fileId}
* Input: Unique file identifier - File Id
* Output: File data / File binary data
  
**Update File API**: Update an existing file or its metadata based on a unique identifier - File Id
* Endpoint: PUT /files/{fileId}
* Input: New File / New file binary data / new metadata (new file name for an existing file)
* Output: Success Message

**Delete File API**: Delete a specific file based on a unique identifier - File Id
* Endpoint: DELETE /files/{fileId}
* Input: Unique file identifier - File Id
* Output: Success Message or Error Message

**List Files API**: List all available files and their metadata.
* Endpoint: GET /files
* Input: None
* Output: A list of file metadata objects, including file_id, file_name, file_size, file_type, created_at.

### Setup and run the server:

* Make sure MongoDb is installed on your system, direct install or docker container will work.
* Incase of AWS S3, make sure access key id, secret access key are provided in variables.
* Incase of using minio: provide minio endpoint url, signature_version s3v4 config along with minioadmin as access key id, secret access key while setting up s3 client using boto3. minio can be accessed at: http://localhost:9001/browser
* once mongodb and minio server are up and running, proceed to run requirements.txt to install all dependencies or run:
  _pip3 install Flask boto3 pymongo flask_pymongo python-dotenv_
* edit .env file accordingly and run create_bucket.py to create a base s3 bucket to store all the files.
* finally run app.py to start the server on the specified port loaded from the .env file
* Use the functionality via postman by hitting the apis with appropriate data and files.

Ta-da!! You have a running FILE DROP server on your local :)
