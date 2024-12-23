import boto3
import json
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
bucket_name = os.getenv("S3_BUCKET_NAME")
folder_prefix = os.getenv("FOLDER_PREFIX")
topic_arn = os.getenv("AWS_SNS_TOPIC_ARN")

# Initialize AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')


def lambda_handler(event, context):
    print("Starting Lambda function execution...")

    try:
        # Step 1: List objects in the folder
        print(f"Listing objects in S3 bucket: '{bucket_name}' with prefix: '{folder_prefix}'...")
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)
        if 'Contents' not in response:
            print("Error: No files found in the specified folder.")
            return {"statusCode": 404, "body": "No questions available."}

        question_files = [obj['Key'] for obj in response['Contents'] if obj['Key'].endswith('.json')]
        print(f"Found question files: {question_files}")

        # Step 2: Randomly select a file
        if not question_files:
            print("Error: No question files found.")
            return {"statusCode": 404, "body": "No questions available."}

        random_file = random.choice(question_files)
        print(f"Fetching '{random_file}' from S3 bucket: '{bucket_name}'...")

        # Step 3: Fetch the selected file
        obj = s3.get_object(Bucket=bucket_name, Key=random_file)
        question_data = json.loads(obj['Body'].read().decode('utf-8'))
        print(f"Successfully fetched and parsed question: {question_data}")

        # Step 4: Send message via SNS
        message = (
            f"LeetCode Daily Review:\n\n"
            f"Title: {question_data['title']} ({question_data['difficulty']})\n"
            f"URL: {question_data['url']}"
        )
        print("Preparing to publish message to SNS...")
        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="Your LeetCode Daily Review!"
        )
        print("Message published successfully to SNS.")
        return {"statusCode": 200, "body": "Message sent successfully."}

    except Exception as e:
        print(f"Error: {str(e)}")
        return {"statusCode": 500, "body": f"Error processing request: {str(e)}"}
