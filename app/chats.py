#!/usr/bin/env python
import os

from flask import (Blueprint, request, jsonify, render_template, send_from_directory, flash, redirect, url_for, abort)
from flask import current_app as app
from werkzeug.utils import secure_filename

chats = Blueprint('chats', __name__, url_prefix='/chats')


@chats.route('/list/', methods=['GET'])
def get_chats():
    return jsonify({"chats": ["Chat1", "Chat2", "Chat3"]})


@chats.route('/search/', methods=['GET'])
@chats.route('/search/<string:query>/', methods=['GET'])
@chats.route('/search/<string:query>/<int:limit>', methods=['GET'])
def search_chats(query=None, limit=None):
    chats = dict(chats=["Chat1", "Chat2", "Chat3"])
    return jsonify(chats=chats)


@chats.route('/create/', methods=['GET', 'POST'])
@chats.route('/create/<string:chatname>', methods=['GET', 'POST'])
def create_chat(chatname=None):
    if request.method == 'POST':
        return jsonify(request.form)
    return render_template('chats/create.html')


@chats.route('/leave/<int:chat_id>', methods=['GET'])
def leave_chat(chat_id=None):
    return jsonify()


@chats.route('/invite/<int:chat_id>', methods=['POST'])
def invite_to_chat(chat_id=None):
    return jsonify()


@chats.route('/send/<int:chat_id>', methods=['POST'])
@chats.route('/send/<int:chat_id>/<string:content>', methods=['POST'])
@chats.route('/send/<int:chat_id>/<string:content>/<int:attach_id>', methods=['POST'])
def send_message_to_chat(chat_id=None, content=None, attach_id=None):
    return jsonify()


@chats.route('/read/<int:message_id>', methods=['GET'])
def read_message_from_chat(message_id=None):
    return jsonify()


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@chats.route('/uploaded/<string:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@chats.route('/upload/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        return jsonify(request.form)
        # if 'file' not in request.files:
        #     flash('No file part')
        #     return redirect(request.url)
        # file = request.files['file']
        # if file.filename == '':
        #     flash('No selected file')
        #     return redirect(request.url)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return redirect(url_for('chats.uploaded_file', filename=filename))
    return render_template('chats/upload.html')
