# leetcode-grinder
## Description
Leetcode questions require grinding to get better. We need more than just daily new question but also review the old questions. 
This project ets up an AWS Lambda function to send a random completed LeetCode question daily via SNS. 
The questions are stored in S3 bucket as a json file.
The AWS EventBridge Scheduler triggers the Lambda to send the SNS message daily on 9:00 AM to wake up the user.
