import boto3
import json
import random
from dotenv import load_dotenv
import os
# Initialize AWS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

load_dotenv()

# Configuration: Update these values
bucket_name = os.getenv("S3_BUCKET_NAME")
key = os.getenv("S3_FILE_NAME")
topic_arn = os.getenv("AWS_SNS_TOPIC_ARN")

def lambda_handler(event, context):
    print("Starting Lambda function execution...")

    # Step 1: Read JSON file from S3
    try:
        clean_bucket_name = bucket_name.strip()
        print(f"Fetching '{key}' from S3 bucket: '{clean_bucket_name}'...")
        response = s3.get_object(Bucket=clean_bucket_name, Key=key)
        questions = json.loads(response['Body'].read().decode('utf-8'))
        print("Successfully fetched and parsed questions.json.")
    except s3.exceptions.NoSuchKey:
        print("Error: S3 file not found.")
        return {"statusCode": 500, "body": "Error: S3 file not found."}
    except Exception as e:
        print(f"Error fetching or reading file from S3: {str(e)}")
        return {"statusCode": 500, "body": "Error accessing S3."}

    # Step 2: Validate JSON Content
    if not questions:
        print("Error: No questions found in the JSON file.")
        return {"statusCode": 404, "body": "No questions available."}

    # Step 3: Randomly Select a Question
    try:
        random_question = random.choice(questions)
        print("Random question selected:", random_question)
        message = (
            f"LeetCode Daily Review:\n\n"
            f"Title: {random_question['title']} ({random_question['difficulty']})\n"
            f"URL: {random_question['url']}"
        )
    except Exception as e:
        print(f"Error processing questions: {str(e)}")
        return {"statusCode": 500, "body": "Error processing questions."}

    # Step 4: Publish Message to SNS
    try:
        print("Preparing to publish message to SNS...")
        sns.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject="Your LeetCode Daily Review!"
        )
        print("Message published successfully to SNS.")
    except Exception as e:
        print(f"Error publishing to SNS: {str(e)}")
        return {"statusCode": 500, "body": f"Error publishing to SNS: {str(e)}"}

    print("Lambda function completed successfully.")
    return {"statusCode": 200, "body": "Message sent successfully."}

