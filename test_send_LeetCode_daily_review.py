import unittest
from unittest.mock import patch, MagicMock
import json

# Import the Lambda function handler
from send_LeetCode_daily_review import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    @patch('send_LeetCode_daily_review.boto3.client')
    def test_random_question_selection(self, mock_boto_client):
        # Mock S3 client
        mock_s3 = MagicMock()
        mock_boto_client.side_effect = lambda service, **kwargs: mock_s3 if service == 's3' else MagicMock()

        # Mock S3 response with sample JSON data
        sample_questions = [
            {"id": 1642, "title": "Furthest Building You Can Reach", "difficulty": "Medium", "url": "https://leetcode.com/problems/furthest-building-you-can-reach/"},
            {"id": 1, "title": "Two Sum", "difficulty": "Easy", "url": "https://leetcode.com/problems/two-sum/"},
            {"id": 42, "title": "Trapping Rain Water", "difficulty": "Hard", "url": "https://leetcode.com/problems/trapping-rain-water/"}
        ]
        mock_s3.get_object.return_value = {
            'Body': MagicMock(read=lambda: json.dumps(sample_questions).encode('utf-8'))
        }

        # Mock SNS client
        mock_sns = MagicMock()
        mock_boto_client.side_effect = lambda service, **kwargs: mock_s3 if service == 's3' else mock_sns
        mock_sns.publish.return_value = {"MessageId": "mock-message-id"}  # Mock publish response

        # Call the Lambda handler
        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Verify that SNS publish was called
        mock_sns.publish.assert_called_once()

        # Verify the random question is in the SNS message
        sns_call_args = mock_sns.publish.call_args[1]
        self.assertIn("LeetCode Daily Review", sns_call_args['Subject'])
        self.assertIn("Title", sns_call_args['Message'])

    @patch('send_LeetCode_daily_review.boto3.client')
    def test_empty_json_file(self, mock_boto_client):
        # Mock S3 client to return an empty JSON file
        mock_s3 = MagicMock()
        mock_boto_client.side_effect = lambda service, **kwargs: mock_s3 if service == 's3' else MagicMock()
        mock_s3.get_object.return_value = {
            'Body': MagicMock(read=lambda: b'[]')
        }

        # Mock SNS client
        mock_sns = MagicMock()
        mock_boto_client.side_effect = lambda service, **kwargs: mock_s3 if service == 's3' else mock_sns

        # Call the Lambda handler
        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Verify no SNS message was sent
        mock_sns.publish.assert_not_called()

        # Verify response contains error status
        self.assertEqual(response['statusCode'], 404)
        self.assertIn('No questions found', response['body'])

    @patch('send_LeetCode_daily_review.boto3.client')
    def test_s3_file_not_found(self, mock_boto_client):
        # Mock S3 client to raise an exception
        mock_s3 = MagicMock()
        mock_boto_client.side_effect = lambda service, **kwargs: mock_s3 if service == 's3' else MagicMock()
        mock_s3.get_object.side_effect = Exception("S3 file not found")

        # Mock SNS client
        mock_sns = MagicMock()
        mock_boto_client.side_effect = lambda service, **kwargs: mock_s3 if service == 's3' else mock_sns

        # Call the Lambda handler
        event = {}
        context = {}
        response = lambda_handler(event, context)

        # Verify response contains error status
        self.assertEqual(response['statusCode'], 500)
        self.assertIn('Error reading S3 file', response['body'])


if __name__ == '__main__':
    unittest.main()
