#!/usr/bin/env python
import os

from flask import (Blueprint, request, jsonify, render_template, send_from_directory, flash, redirect, url_for)
from flask import current_app as app
from werkzeug.utils import secure_filename

chats = Blueprint('chats', __name__, url_prefix='/chats')


@chats.route('/', methods=['GET'])
def get_chats():
    chats = dict(chats=["Chat1", "Chat2", "Chat3"])
    return jsonify(chats=chats)


@chats.route('/<string:chatname>/', methods=['GET'])
def get_chat(chatname=None):
    return jsonify(chatname=chatname)


@chats.route('/search/', methods=['GET'])
def search_chats():
    chats = dict(chats=["Chat1", "Chat2", "Chat3"])
    return jsonify(chats=chats)


@chats.route('/create/', methods=['GET', 'POST'])
def create_chat():
    if request.method == 'POST':
        return jsonify(request.form)
    return render_template('chats/create.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


@chats.route('/uploaded/<filename>')
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
