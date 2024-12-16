import os
import sys
import unittest

from src.lambda_handler.send_LeetCode_daily_review import lambda_handler


class TestLambdaFunction(unittest.TestCase):
    def test_lambda_handler_execution(self):
        # Basic event and context
        event = {}
        context = {}

        # Call Lambda function directly
        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)
        self.assertIn("Message sent successfully", response['body'])


if __name__ == "__main__":
    unittest.main()
