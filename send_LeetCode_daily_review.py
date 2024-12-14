import boto3
import json
import random

# Initialize S3 and SNS clients
s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    bucket_name = 'leetcode-completed-questions'
    key = 'questions.json'

    # Read the single JSON file from S3
    response = s3.get_object(Bucket=bucket_name, Key=key)
    questions = json.loads(response['Body'].read().decode('utf-8'))

    # Pick a random question
    if not questions:
        return {
            'statusCode': 404,
            'body': json.dumps('No questions found in the JSON file.')
        }
    random_question = random.choice(questions)

    # Construct the message
    message = f"LeetCode Daily Review:\n\nTitle: {random_question['title']} ({random_question['difficulty']})\nURL: {random_question['url']}"

    # Publish the message to the SNS topic
    topic_arn = 'arn:aws:sns:region:account-id:LeetCodeDailyReview'
    sns.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject='Get up and Study!!'
    )

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully sent message for question: {random_question["title"]}')
    }
