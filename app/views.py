#!/usr/bin/env python

from app import app
from flask import request, redirect, url_for, jsonify, flash, send_from_directory, render_template
from werkzeug.utils import secure_filename
import os


@app.route('/')
def index():
    return 'Index'


@app.route('/login/', methods={'GET', 'POST'})
def login():
    if request.method == 'POST':
        return jsonify(request.form)
    return jsonify()


@app.route('/search_users', methods=['GET'])
def search_users():
    query = request.args.get('query', default=None, type=str)
    limit = request.args.get('limit', default=10, type=int)
    return jsonify(users=["User1", "User2", "User3"])


@app.route('/search_chats', methods=['GET'])
def search_chats():
    query = request.args.get('query', default=None, type=str)
    limit = request.args.get('limit', default=10, type=int)
    return jsonify(chats=["Chat1", "Chat2", "Chat3"])


@app.route('/list_chats/', methods=['GET'])
def list_chats():
    return jsonify(chats=["Chat1", "Chat2", "Chat3"])


@app.route('/create_pers_chat', methods=['GET', 'POST'])
def create_pers_chat():
    user_id = request.args.get('user_id', default=None, type=int)
    if request.method == 'POST':
        return jsonify(request.form)
    return jsonify(chat="Chat")


@app.route('/create_group_chat', methods=['GET', 'POST'])
def create_group_chat():
    topic = request.args.get('topic', default=None, type=str)
    if request.method == 'POST':
        return jsonify(request.form)
    return jsonify(chat="Chat")


@app.route('/add_members_to_group_chat', methods=['POST'])
def add_members_to_group_chat():
    chat_id = request.args.get('chat_id', default=None, type=int)
    user_ids = request.args.get('user_ids', default=None, type=str)  # TODO: переделать type в list, разобраться с десериализацией объектов в Flask
    return jsonify()


@app.route('/leave_group_chat', methods=['POST'])
def leave_group_chat():
    chat_id = request.args.get('chat_id', default=None, type=int)
    return jsonify()


@app.route('/send_message', methods=['POST'])
def send_message():
    chat_id = request.args.get('chat_id', default=None, type=int)
    content = request.args.get('content', default=None, type=str)
    attach_id = request.args.get('attach_id', default=None, type=int)
    return jsonify(request.form)


@app.route('/read_message', methods=['GET'])
def read_message():
    message_id = request.args.get('message_id', default=None, type=int)
    return jsonify(chat="Chat")


@app.route('/upload_file', methods=['POST'])
def upload_file():
    chat_id = request.args.get('chat_id', default=None, type=int)
    content = request.args.get('content', default=None, type=str)
    return jsonify(request.form)
