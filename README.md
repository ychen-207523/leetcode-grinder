# leetcode-grinder
## Description
Leetcode questions require grinding to get better. We need more than just daily new question but also review the old questions. 
This project ets up an AWS Lambda function to send a random completed LeetCode question daily via SNS. 
The questions are stored in S3 bucket as a json file.
The AWS EventBridge Scheduler triggers the Lambda to send the SNS message daily on 9:00 AM to wake up the user.
## Project Overview
- **Lambda Function**: The Lambda function is written in Python 3.8. It reads the questions from the S3 bucket and sends a random question to the SNS topic.
- **S3 Bucket**: The S3 bucket stores the questions in a json file.
- **SNS Topic**: The SNS topic sends the message to the user.
- **EventBridge Scheduler**: The EventBridge Scheduler triggers the Lambda function daily at 9:00 AM.
- **IAM Role**: The IAM role allows the Lambda function to access the S3 bucket and SNS topic.
- **CloudWatch Logs**: The CloudWatch Logs stores the logs of the Lambda function.
## Project Structure
```
leetcode-grinder/
│
├── src/
│   └── lambda/
│       └── send_LeetCode_daily_review.py  # Lambda function code
│
├── test/
│   └── test_send_LeetCode_daily_review.py  # Unit tests
│
├── README.md
└── .gitignore
```
## Steps to Deploy
### Prerequisites
- AWS Account
- IAM permissions to create and manage S3, Lambda, SNS, and EventBridge Scheduler resources.
- An email address to subscribe to SNS notifications
### Create the S3 Bucket and Upload questions.json
1. Go to the S3 Console.

2. Click Create Bucket:

   - Name the bucket `leetcode-completed-questions` (Or the one you choose).
   - Keep all default settings, then click Create Bucket.

3. Open the newly created bucket.

4. Click Upload:
   - Select or drag your questions.json file.
   - Click Upload.
5. Example content for questions.json:
```json
[
  {
    "id": 1,
    "title": "Two Sum",
    "difficulty": "Easy",
    "url": "https://leetcode.com/problems/two-sum/"
  },
  {
    "id": 2,
    "title": "Add Two Numbers",
    "difficulty": "Medium",
    "url": "https://leetcode.com/problems/add-two-numbers/"
  }
]
```
### Create an SNS Topic and Subscribe to It

1. Go to the SNS Console.

2. Click Topics > Create Topic:
   - Choose Standard.
   - Name the topic LeetCodeDailyReview.
   - Click Create Topic.
   - Copy the Topic ARN for later use.
   
3. Under Subscriptions, click Create Subscription:
   - Protocol: Email
   - Endpoint: Enter your email address.
   - Click Create Subscription.
   
4. Check your email inbox and confirm the subscription.

### Create an IAM Role for Lambda Execution
1. Go to the IAM Console.

2. Click Roles > Create Role:

   - Trusted entity type: AWS Service
   - Use case: Lambda
   - Click Next.
3. Attach the following policies:

   - AmazonS3ReadOnlyAccess: Allows Lambda to read the questions.json file from S3.
   - AmazonSNSFullAccess: Allows Lambda to publish messages to the SNS topic.

4. Add an Inline Policy to allow EventBridge to trigger Lambda:

   - Go to the Permissions tab of the role.
   - Click Add Permissions > Create Inline Policy.
   - Use this JSON:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Sid": "AllowSNSTopicPublish",
               "Effect": "Allow",
               "Action": "sns:Publish",
               "Resource": "arn:aws:sns:us-east-1:226063781515:LeetCodeDailyReview"
           },
           {
               "Sid": "AllowEventBridgeInvokeLambda",
               "Effect": "Allow",
               "Action": "lambda:InvokeFunction",
               "Resource": "arn:aws:lambda:us-east-1:226063781515:function:sendLeetCodeDailyReview"
           }
       ]
   }
   ```
5. Create .env file in the root directory and add the following environment variables:
```bash
S3_BUCKET_NAME=leetcode-completed-questions
S3_OBJECT_KEY=questions.json
SNS_TOPIC_ARN=arn:aws:sns:<your-region>:<your-arn-number>:LeetCodeDailyReview
```

6. Now, you should be able to test the lambda function locally
```bash
python -m unittest test.test_send_LeetCode_daily_review  
```
7. Deploy the function to AWS Lambda
 - Add your environment configuration to the Lambda function > Configuration > Environment variables.
 - Remove `dotenv` from the code.
 - Deploy the function to AWS Lambda.

8. The lambda function should be triggered daily at the time you set up in the EventBridge Scheduler.

## Future Improvements
Add backend automation to update the questions.json file with the latest completed questions.

