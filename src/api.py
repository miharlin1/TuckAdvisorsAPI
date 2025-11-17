from flask import Flask, request, jsonify
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
import database as db

app = Flask(__name__)


@app.route('/api/markdown', methods=['GET'])
def get_markdown():
    """
    GET endpoint: Returns the current markdown string.
    No parameters required.
    """
    markdown = db.get_latest_markdown()
    if not markdown:
        return jsonify({
            "error": "No markdown found in database"
        }), 404
    
    return jsonify({"markdown": markdown}), 200


@app.route('/api/markdown', methods=['POST'])
def update_markdown():
    if not request.is_json: #check if the request is a JSON
        return jsonify({"error": "Content-Type must be application/json"}), 400
    
    data = request.get_json()
    
    if "text" not in data:
        return jsonify({"error": "Request body must contain 'text' field"}), 400
    
    text_to_append = data["text"]
    updated_content = db.append_to_markdown(text_to_append)
    
    if updated_content is None:
        return jsonify({"error": "No markdown found in database"}), 404
    
    return jsonify({"markdown": updated_content}), 200


if __name__ == '__main__':
    if not db.DB_PATH.exists():
        print("ERROR: Database not initialized. Run: python3 init_db.py")
        exit(1)
    
    print("GPT Analysis API running on http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)

