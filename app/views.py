#!/usr/bin/env python

from app import jsonrpc, model
from flask import jsonify

LIMIT = 10


@jsonrpc.method('index')
def index():
    return jsonify().json


@jsonrpc.method('login')
def login():
    return jsonify().json


@jsonrpc.method('search_users')
def search_users(query=None, limit=LIMIT):
    if query is not None:
        users = model.search_users(query=query, limit=limit)
        return users


@jsonrpc.method('list_users')
def list_users():
    users = model.list_users()
    return users


@jsonrpc.method('search_chats')
def search_chats(query=None, limit=LIMIT):
    if query is not None:
        chats = model.search_chats(query=query, limit=limit)
        return chats


@jsonrpc.method('list_chats')
def list_chats():
    chats = model.list_chats()
    return chats


@jsonrpc.method('create_personal_chat')
def create_personal_chat(user_id=None, companion_id=None):
    if user_id is None:
        return

    chat = model.get_personal_chat(user_id=user_id)
    if chat is None:
        chat = model.create_personal_chat(user_id=user_id, companion_id=companion_id)
    return chat


@jsonrpc.method('create_group_chat')
def create_group_chat(topic=None):
    if topic is not None:
        chat = model.get_group_chat(topic=topic)
        if chat is None:
            chat = model.create_group_chat(topic=topic)
        return chat


@jsonrpc.method('add_members_to_group_chat')
def add_members_to_group_chat(chat_id=None, user_ids=None):
    if chat_id is not None and user_ids is not None:
        model.add_members_to_group_chat(chat_id=chat_id, user_ids=user_ids)
        return jsonify().json


@jsonrpc.method('leave_group_chat')
def leave_group_chat(user_id=None, chat_id=None):
    if user_id is not None and chat_id is not None:
        model.leave_group_chat(chat_id=chat_id, user_id=user_id)
        return jsonify().json


@jsonrpc.method('send_message')
def send_message(user_id=None, chat_id=None, content=None, attachment_id=None):
    if user_id is not None and chat_id is not None and content is not None:
        message = model.send_message(user_id=user_id, chat_id=chat_id, content=content, attachment_id=attachment_id)
        return message


@jsonrpc.method('read_message')
def read_message(user_id=None, message_id=None):
    if user_id is not None and message_id is not None:
        chat = model.read_message(user_id=user_id, message_id=message_id)
        return chat


@jsonrpc.method('list_messages')
def list_messages(chat_id=None, limit=LIMIT):
    if chat_id is not None:
        messages = model.list_messages(chat_id=chat_id, limit=limit)
        return messages


@jsonrpc.method('upload_file')
def upload_file(user_id=None, chat_id=None, content=None):
    if user_id is not None and chat_id is not None and content is not None:
        attachment = model.upload_file(user_id=user_id, chat_id=chat_id, content=content)
        return attachment
