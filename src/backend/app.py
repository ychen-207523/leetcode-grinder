import os
from flask import Flask, request, jsonify
from openai import OpenAI

from s3_helper import upload_question_to_s3, get_random_question_from_s3

app = Flask(__name__, static_folder='../frontend', static_url_path='/')

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/get-random-question', methods=['GET'])
def get_random_question():
    """
    Endpoint to fetch a random LeetCode question from S3.
    """
    try:
        question = get_random_question_from_s3()
        if question:
            return jsonify(question), 200
        else:
            return jsonify({'error': 'No questions available.'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add-question', methods=['POST'])
def add_question():
    """
    Endpoint to add a new LeetCode question as a separate file.
    Expects JSON input with id, title, url, and difficulty.
    """
    try:
        data = request.get_json()

        # Validate input
        required_fields = ['id', 'title', 'url', 'difficulty']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields. Please provide id, title, url, and difficulty.'}), 400

        # Construct question data
        question = {
            'id': data['id'],
            'title': data['title'],
            'difficulty': data['difficulty'],
            'url': data['url']
        }

        # Upload question as a new file to S3
        upload_question_to_s3(question)

        return jsonify({'message': 'Question added successfully!'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat_with_gpt():
    try:
        data = request.get_json()
        if 'prompt' not in data:
            return jsonify({'error': 'Missing prompt field'}), 400

        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for algorithm and leetcode question."},
                {
                    "role": "user",
                    "content": data['prompt']
                }
            ]
        )
        # Extract AI's response
        message = response.choices[0].message
        return jsonify({'response': message}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
