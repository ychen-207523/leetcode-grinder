import os
import unittest
from dotenv import load_dotenv
from src.lambda_handler.send_LeetCode_daily_review import lambda_handler

# Load environment variables from .env file
load_dotenv()

class TestLambdaFunction(unittest.TestCase):
    def test_lambda_handler_execution(self):
        # Basic event and context
        event = {}
        context = {}

        # Call Lambda function directly
        response = lambda_handler(event, context)

        # Validate the response
        self.assertEqual(response['statusCode'], 200)
        self.assertIn("Message sent successfully", response['body'])

if __name__ == "__main__":
    unittest.main()
