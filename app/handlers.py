from flask import request, jsonify
import model
from app import app

@app.route('/messages')
def messages():
    chat_id = int(request.args.get('chat_id'))
    messages = model.list_messages_by_chat(chat_id)
    return jsonify(messages)