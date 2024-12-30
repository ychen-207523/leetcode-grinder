import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# AWS S3 Configuration
s3 = boto3.client('s3')
bucket_name = os.getenv("S3_BUCKET_NAME")
folder_prefix = os.getenv("FOLDER_PREFIX")


def upload_question_to_s3(question):
    """
    Upload a new question as a separate file to S3.
    Each file is named as <id>.json and stored in the folder prefix.
    """
    try:
        file_name = f"{question['id']}.json"
        key = f"{folder_prefix}/{file_name}"

        s3.put_object(
            Bucket=bucket_name,
            Key=key,
            Body=json.dumps(question, indent=4),
            ContentType='application/json'
        )
        print(f"Uploaded {file_name} to S3 successfully.")
    except Exception as e:
        raise Exception(f"Error uploading question to S3: {str(e)}")
