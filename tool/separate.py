import json
import os

def separate_questions_into_files(input_file):
    # Create a directory to store the individual question files
    output_dir = "questions_by_id"
    os.makedirs(output_dir, exist_ok=True)

    # Read the questions.json file
    with open(input_file, "r") as file:
        questions = json.load(file)

    # Iterate through each question and save it into a separate file
    for question in questions:
        question_id = question["id"]
        output_file = os.path.join(output_dir, f"{question_id}.json")
        with open(output_file, "w") as q_file:
            json.dump(question, q_file, indent=4)

    print(f"All questions have been separated into individual files in the '{output_dir}' directory.")

# Call the function with your JSON file
separate_questions_into_files("questions.json")