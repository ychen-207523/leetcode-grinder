import boto3
import json
import random

def lambda_handler(event, context, s3=None, sns=None):
    # Use provided clients or create new ones (default behavior)
    if s3 is None:
        s3 = boto3.client('s3')
    if sns is None:
        sns = boto3.client('sns')

    bucket_name = 'leetcode-completed-questions'
    key = 'questions.json'

    try:
        # Read the JSON file from S3
        response = s3.get_object(Bucket=bucket_name, Key=key)
        questions = json.loads(response['Body'].read().decode('utf-8'))
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error reading S3 file: {str(e)}')
        }

    # Handle empty file case
    if not questions:
        return {
            'statusCode': 404,
            'body': json.dumps('No questions found in the JSON file.')
        }

    # Pick a random question
    random_question = random.choice(questions)
    message = f"LeetCode Daily Review:\n\nTitle: {random_question['title']} ({random_question['difficulty']})\nURL: {random_question['url']}"

    try:
        # Publish the message to the SNS topic
        sns.publish(
            TopicArn='arn:aws:sns:region:account-id:LeetCodeDailyReview',
            Message=message,
            Subject='Your LeetCode Daily Review!'
        )
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error publishing to SNS: {str(e)}')
        }

    return {
        'statusCode': 200,
        'body': json.dumps(f'Successfully sent message for question: {random_question["title"]}')
    }
