#!/usr/bin/env python

from . import app, jsonrpc, model, s3_session, s3_client
from flask import jsonify, make_response
from .forms import wtform, SearchUsersForm, SearchChatsForm, CreatePersonalChatForm, CreateGroupChatForm, \
    AddMembersGroupChatForm, LeaveGroupChatForm, SendMessageForm, ReadMessageForm, ListMessagesForm, \
    UploadFileForm, DownloadFileForm, GenerateKeyForm, GetFileForm
from .db import transaction
import base64
import hmac
import hashlib
import time


@jsonrpc.method('api.index')
def index():
    return jsonify().json


@jsonrpc.method('api.login')
def login():
    return jsonify().json


@jsonrpc.method('api.search_users')
@transaction
@wtform(SearchUsersForm)
def search_users(query, limit):
    users = model.search_users(query=query, limit=limit)
    return users


@jsonrpc.method('api.list_users')
@transaction
def list_users():
    users = model.list_users()
    return users


@jsonrpc.method('api.search_chats')
@transaction
@wtform(SearchChatsForm)
def search_chats(query, limit):
    chats = model.search_chats(query=query, limit=limit)
    return chats


@jsonrpc.method('api.list_chats')
@transaction
def list_chats():
    chats = model.list_chats()
    return chats


@jsonrpc.method('api.create_personal_chat')
@transaction
@wtform(CreatePersonalChatForm)
def create_personal_chat(companion_id, user_id):
    chat = model.get_personal_chat(companion_id=companion_id)
    if chat is None:
        chat = model.create_personal_chat(companion_id=companion_id, user_id=user_id)
    return chat


@jsonrpc.method('api.create_group_chat')
@transaction
@wtform(CreateGroupChatForm)
def create_group_chat(topic):
    chat = model.get_group_chat(topic=topic)
    if chat is None:
        chat = model.create_group_chat(topic=topic)
    return chat


@jsonrpc.method('api.add_members_to_group_chat')
@transaction
@wtform(AddMembersGroupChatForm)
def add_members_to_group_chat(chat_id, user_ids):
    model.add_members_to_group_chat(chat_id=chat_id, user_ids=user_ids)
    return jsonify().json


@jsonrpc.method('api.leave_group_chat')
@transaction
@wtform(LeaveGroupChatForm)
def leave_group_chat(user_id, chat_id):
    # TODO: need to get user_id from session
    model.leave_group_chat(chat_id=chat_id, user_id=user_id)
    return jsonify().json


@jsonrpc.method('api.send_message')
@transaction
@wtform(SendMessageForm)
def send_message(user_id, chat_id, content, attachment_id):
    # TODO: need to get user_id from session
    message = model.send_message(user_id=user_id, chat_id=chat_id, content=content, attachment_id=attachment_id)
    return message


@jsonrpc.method('api.read_message')
@transaction
@wtform(ReadMessageForm)
def read_message(user_id, message_id):
    # TODO: need to get user_id from session
    chat = model.read_message(user_id=user_id, message_id=message_id)
    return chat


@jsonrpc.method('api.list_messages')
@transaction
@wtform(ListMessagesForm)
def list_messages(chat_id, limit):
    messages = model.list_messages(chat_id=chat_id, limit=limit)
    return messages


@jsonrpc.method('api.upload_file')
@transaction
@wtform(UploadFileForm)
def upload_file(user_id, chat_id, content, mime_type):
    # TODO: need to get user_id from session
    content = base64.b64decode(content).decode('utf-8')
    key = hashlib.md5(user_id + time.time())
    response = s3_client.put_object(Bucket=app.config['S3_BUCKET_NAME'], Key=key, Body=content)['result']
    attachment = model.upload_file(user_id=user_id, chat_id=chat_id, url=key, mime_type=mime_type)
    return attachment


@jsonrpc.method('api.download_file')
@wtform(DownloadFileForm)
def download_file(key):
    response = s3_client.get_object(Bucket=app.config['S3_BUCKET_NAME'], Key=key)
    content = response.get('Body').read().decode('utf-8')['result']
    return content


@jsonrpc.method('api.generate_key')
@wtform(GenerateKeyForm)
def generate_key(key, message):
    key = bytes(key, 'utf-8')
    message = bytes(message, 'utf-8')

    digester = hmac.new(key, message, hashlib.sha1)
    signature = digester.digest()

    return base64.b16encode(signature)


@jsonrpc.method('api.get_file')
@wtform(GetFileForm)
def get_file(key):
    response = make_response()

    now = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime())
    string_to_sign = "GET\n\n\n\nx-amz-date:{}\n/{}/{}".format(now, app.config['S3_BUCKET_NAME'], key)
    signature = generate_key(app.config['S3_ACCESS_KEY_ID'], string_to_sign).decode('utf-8')

    response.headers['Authorization'] = "AWS {}:{}".format(app.config['S3_ACCESS_KEY_ID'], signature)
    response.headers['X-Amz-Date'] = now
    response.headers['Date'] = now
    response.headers['Host'] = "{}.hb.bizmrg.com".format(app.config['S3_BUCKET_NAME'])
    response.headers['X-Accel-Redirect'] = "/s3/{}".format(key)

    return response

