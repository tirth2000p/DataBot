import json
from difflib import get_close_matches

from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo.mongo_client import MongoClient


uri = "mongodb+srv://tirth2000p:tirth123@knowledgebase.irvbgyk.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

app = Flask(__name__)

# MongoDB connection
db = client.chatbot_db  # Use your preferred database name
knowledge_base = db.knowledge_base  # Use your preferred collection name


CORS(app)

conversation_state = {
    'learning_mode': False,
    'previous_question': ''
}

# def load_knowledge_base(file_path: str) -> dict:
#     with open(file_path, 'r') as file:
#         data: dict = json.load(file)
#     return data
#
#
# def save_knowledge_base(file_path: str, data: dict):
#     with open(file_path, 'w') as file:
#         json.dump(data, file, indent=2)


# def find_best_match(user_question: str, question: list[str]) -> str | None:
#     matches: list = get_close_matches(user_question, question, n=1, cutoff=0.60)
#     return matches[0] if matches else None

def find_best_match(user_question):
    question_list = [q['question'] for q in knowledge_base.find()]
    matches = get_close_matches(user_question, question_list, n=1, cutoff=0.60)
    return matches[0] if matches else None


# def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
#     for q in knowledge_base["questions"]:
#         if q["question"] == question:
#             return q["answer"]

def get_answer_for_question(question):
    answer_doc = knowledge_base.find_one({"question": question})
    return answer_doc['answer'] if answer_doc else None


@app.route('/chat', methods=['POST'])
def chat_bot():
    global conversation_state
    user_input = request.json.get('message')

    if user_input.lower() == 'quit':
        conversation_state = {'learning_mode': False, 'previous_question': ''}
        return jsonify({'response': 'Goodbye!'})

    if conversation_state['learning_mode']:
        if user_input.lower() != "skip":
            knowledge_base.insert_one({"question": conversation_state['previous_question'], "answer": user_input})
            conversation_state = {'learning_mode': False, 'previous_question': ''}
            return jsonify({'response': 'Thank you for the new information!'})
        else:
            conversation_state = {'learning_mode': False, 'previous_question': ''}
            return jsonify({'response': 'Skipped learning new information.'})

    best_match = find_best_match(user_input)
    if best_match:
        return jsonify({'response': get_answer_for_question(best_match)})
    else:
        conversation_state = {'learning_mode': True, 'previous_question': user_input}
        return jsonify({'response': "I don't know. Can you teach me?"})

@app.route('/', methods=['GET'])
def initial():
    return jsonify({'Works': "out"})

if __name__ == '__main__':
    app.run(debug=True)
