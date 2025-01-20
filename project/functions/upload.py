import os
import json
from io import BytesIO
from urllib.parse import parse_qs
import base64

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def lambda_handler(event, context):
    # Check if the request method is POST
    if event['httpMethod'] == 'POST':
        # Parse the multipart form data
        try:
            body = event['body']
            content_type = event['headers'].get('Content-Type', '')

            if 'multipart/form-data' in content_type:
                # Process the file from the base64 encoded body
                file_data = base64.b64decode(body.split(',')[1])
                file = BytesIO(file_data)

                # Get file name and save it
                filename = 'uploaded_image.jpg'  # You can generate a unique filename here
                file_path = os.path.join('uploads', filename)

                # Save the file to the uploads directory
                with open(file_path, 'wb') as f:
                    f.write(file.read())

                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'File uploaded successfully!', 'filename': filename})
                }
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'message': 'Invalid file format'})
                }
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'message': str(e)})
            }

    return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method Not Allowed'})
    }
