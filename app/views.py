#!/usr/bin/env python

from app import app, jsonrpc, model, s3_session, s3_client
from flask import jsonify
from .utils import get_mime_type
import base64
import hmac
import hashlib
import time

LIMIT = 10


@jsonrpc.method('api.index')
def index():
    return jsonify().json


@jsonrpc.method('api.login')
def login():
    return jsonify().json


@jsonrpc.method('api.search_users')
def search_users(query=None, limit=LIMIT):
    if query is not None:
        users = model.search_users(query=query, limit=limit)
        return users


@jsonrpc.method('api.list_users')
def list_users():
    users = model.list_users()
    return users


@jsonrpc.method('api.search_chats')
def search_chats(query=None, limit=LIMIT):
    if query is not None:
        chats = model.search_chats(query=query, limit=limit)
        return chats


@jsonrpc.method('api.list_chats')
def list_chats():
    chats = model.list_chats()
    return chats


@jsonrpc.method('api.create_personal_chat')
def create_personal_chat(user_id=None, companion_id=None):
    if user_id is None:
        return

    chat = model.get_personal_chat(user_id=user_id)
    if chat is None:
        chat = model.create_personal_chat(user_id=user_id, companion_id=companion_id)
    return chat


@jsonrpc.method('api.create_group_chat')
def create_group_chat(topic=None):
    if topic is not None:
        chat = model.get_group_chat(topic=topic)
        if chat is None:
            chat = model.create_group_chat(topic=topic)
        return chat


@jsonrpc.method('api.add_members_to_group_chat')
def add_members_to_group_chat(chat_id=None, user_ids=None):
    if chat_id is not None and user_ids is not None:
        model.add_members_to_group_chat(chat_id=chat_id, user_ids=user_ids)
        return jsonify().json


@jsonrpc.method('api.leave_group_chat')
def leave_group_chat(user_id=None, chat_id=None):
    if user_id is not None and chat_id is not None:
        model.leave_group_chat(chat_id=chat_id, user_id=user_id)
        return jsonify().json


@jsonrpc.method('api.send_message')
def send_message(user_id=None, chat_id=None, content=None, attachment_id=None):
    if user_id is not None and chat_id is not None and content is not None:
        message = model.send_message(user_id=user_id, chat_id=chat_id, content=content, attachment_id=attachment_id)
        return message


@jsonrpc.method('api.read_message')
def read_message(user_id=None, message_id=None):
    if user_id is not None and message_id is not None:
        chat = model.read_message(user_id=user_id, message_id=message_id)
        return chat


@jsonrpc.method('api.list_messages')
def list_messages(chat_id=None, limit=LIMIT):
    if chat_id is not None:
        messages = model.list_messages(chat_id=chat_id, limit=limit)
        return messages


@jsonrpc.method('api.upload_file')
def upload_file(user_id=None, chat_id=None, content=None, filename=None):
    if user_id is not None and chat_id is not None and content is not None and filename is not None:
        content = base64.b64decode(content).decode('utf-8')
        url = filename
        mime_type = get_mime_type(filename)
        key = s3_client.put_object(Bucket=app.config['S3_BUCKET_NAME'], Key=filename, Body=content)['result']
        attachment = model.upload_file(user_id=user_id, chat_id=chat_id, url=url, mime_type=mime_type)
        return attachment


@jsonrpc.method('api.download_file')
def download_file(filename):
    response = s3_client.get_object(Bucket=app.config['S3_BUCKET_NAME'], Key=filename)
    content = response.get('Body').read().decode('utf-8')['result']
    return content


@jsonrpc.method('api.generate_key')
def generate_key(key, message):
    key = bytes(key, 'utf-8')
    message = bytes(message, 'utf-8')

    digester = hmac.new(key, message, hashlib.sha1)
    signature = digester.digest()

    return base64.b16encode(signature)


@jsonrpc.method('api.get_file')
def get_file(filename):
    response = s3_client.get_object(Bucket=app.config['S3_BUCKET_NAME'], Key=filename)

    now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    string_to_sign = "GET\n\n\n\nx-amz-date:{}\n/{}/{}".format(now, app.config['S3_BUCKET_NAME'], filename)
    signature = generate_key(app.config['S3_ACCESS_KEY_ID'], string_to_sign).decode('utf-8')

    response.headers['Authorization'] = "AWS {}:{}".format(app.config['S3_ACCESS_KEY_ID'], signature)
    response.headers['X-Amz-Date'] = now
    response.headers['Date'] = now
    response.headers['Host'] = "{}.hb.bizmrg.com".format(app.config['S3_BUCKET_NAME'])
    response.headers['X-Accel-Redirect'] = "/s3/{}".format(filename)

    return response

