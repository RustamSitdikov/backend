#!/usr/bin/env python

from app import app, jsonrpc
from flask import request, redirect, url_for, jsonify, flash, send_from_directory, render_template
from app import model

LIMIT = 10


@jsonrpc.method('index')
@app.route('/')
def index():
    return jsonify()


@jsonrpc.method('login')
@app.route('/login/', methods={'GET', 'POST'})
def login():
    if request.method == 'POST':
        return jsonify(request.form)
    return jsonify()


@jsonrpc.method('search_users')
@app.route('/search_users', methods=['GET'])
def search_users():
    query = request.args.get('query', default=None, type=str)
    limit = request.args.get('limit', default=LIMIT, type=int)
    users = model.search_users(query=query, limit=limit)
    return users


@jsonrpc.method('search_chats')
@app.route('/search_chats', methods=['GET'])
def search_chats():
    query = request.args.get('query', default=None, type=str)
    limit = request.args.get('limit', default=LIMIT, type=int)
    chats = model.search_chats(query=query, limit=limit)
    return chats


@jsonrpc.method('list_chats')
@app.route('/list_chats/', methods=['GET'])
def list_chats():
    chats = model.list_chats()
    return chats


@jsonrpc.method('create_pers_chat')
@app.route('/create_pers_chat', methods=['GET', 'POST'])
def create_pers_chat():
    user_id = request.args.get('user_id', default=None, type=int)
    if request.method == 'POST':
        chat = model.create_personal_chat(user_id=user_id)
        return chat
    chat = model.get_personal_chat(user_id=user_id)
    return chat


@jsonrpc.method('create_group_chat')
@app.route('/create_group_chat', methods=['GET', 'POST'])
def create_group_chat():
    topic = request.args.get('topic', default=None, type=str)
    if request.method == 'POST':
        chat = model.create_group_chat(topic=topic)
        return chat
    chat = model.get_group_chat(topic=topic)
    return chat


@jsonrpc.method('add_members_to_group_chat')
@app.route('/add_members_to_group_chat', methods=['POST'])
def add_members_to_group_chat():
    chat_id = request.args.get('chat_id', default=None, type=int)
    user_ids = request.args.get('user_ids', default=None, type=str)
    model.add_members_to_group_chat(chat_id=chat_id, user_ids=user_ids)
    return jsonify()


@jsonrpc.method('leave_group_chat')
@app.route('/leave_group_chat', methods=['POST'])
def leave_group_chat():
    chat_id = request.args.get('chat_id', default=None, type=int)
    model.leave_group_chat(chat_id=chat_id)
    return jsonify()


@jsonrpc.method('send_message')
@app.route('/send_message', methods=['POST'])
def send_message():
    # TODO: переделать этот метод
    chat_id = request.args.get('chat_id', default=None, type=int)
    content = request.args.get('content', default=None, type=str)
    attachment_id = request.args.get('attachment_id', default=None, type=int)
    message = model.send_message(chat_id=chat_id, content=content, attachment_id=attachment_id)
    return message


@jsonrpc.method('read_message')
@app.route('/read_message', methods=['GET'])
def read_message():
    message_id = request.args.get('message_id', default=None, type=int)
    chat = model.read_message(message_id=message_id)
    return chat


@jsonrpc.method('upload_file')
@app.route('/upload_file', methods=['POST'])
def upload_file():
    chat_id = request.args.get('chat_id', default=None, type=int)
    content = request.args.get('content', default=None, type=str)
    attachment_id = model.upload_file(chat_id=chat_id, content=content)
    attachment = model.get_attachment(attachment_id=attachment_id)
    return attachment
