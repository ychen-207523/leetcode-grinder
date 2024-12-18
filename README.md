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