from flask import Flask, request, jsonify
from s3_helper import upload_question_to_s3

app = Flask(__name__)


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


if __name__ == '__main__':
    app.run(debug=True)
