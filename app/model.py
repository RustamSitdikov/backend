from app import db
from .db import transaction
from .utils import get_mime_type
from config import Config

LIMIT = 10
FALSE = 'FALSE'
TRUE = 'TRUE'


# User
def get_user(user_id):
    return db.query_one(
        """
        SELECT user_id as user_id, nick as nick, name as name, avatar as avatar
        FROM users
        WHERE user_id = %(user_id)s
        """, user_id=int(user_id)
    )


def search_users(query, limit):
    query = ''.join(['%%', query, '%%'])
    return db.query_all(
        """
        SELECT user_id as user_id, nick as nick, name as name, avatar as avatar
        FROM users
        WHERE nick LIKE %(query)s
        OR name LIKE %(query)s
        ORDER BY nick DESC
        LIMIT %(limit)s
        """, query=str(query), limit=int(limit)
    )


def list_users():
    return db.query_all(
        """
        SELECT user_id as user_id, nick as nick, name as name, avatar as avatar
        FROM users
        """
    )


# Chat
def get_chat(chat_id):
    return db.query_one(
        """
        SELECT chat_id as chat_id, topic as topic, is_group_chat as is_group_chat, last_message as last_message
        FROM chats
        WHERE chat_id = %(chat_id)s
        """, chat_id=int(chat_id)
    )


def get_personal_chat(user_id):
    return db.query_one(
        """
        SELECT chats.chat_id as chat_id, chats.topic as topic, chats.is_group_chat as is_group_chat, chats.last_message as last_message
        FROM chats, members
        WHERE chats.chat_id = members.chat_id
        AND members.user_id = %(user_id)s
        AND chats.is_group_chat = FALSE
        """, user_id=int(user_id)
    )


def get_group_chat(topic):
    return db.query_one(
        """
        SELECT chat_id as chat_id, topic as topic, is_group_chat as is_group_chat, last_message as last_message
        FROM chats
        WHERE topic = %(topic)s
        AND is_group_chat = TRUE
        """, topic=str(topic)
    )


def search_chats(query, limit):
    query = ''.join(['%%', query, '%%'])
    return db.query_all(
        """
        SELECT chat_id as chat_id, topic as topic, is_group_chat as is_group_chat, last_message as last_message
        FROM chats
        WHERE topic LIKE %(query)s
        ORDER BY topic DESC
        LIMIT %(limit)s
        """, query=str(query), limit=int(limit)
    )


def list_chats():
    return db.query_all(
        """
        SELECT chat_id as chat_id, topic as topic, is_group_chat as is_group_chat, last_message as last_message
        FROM chats
        """
    )


def create_chat(is_group_chat, topic):
    return db.query_one(
        """
        INSERT INTO chats (is_group_chat, topic)
        VALUES (%(is_group_chat)s, %(topic)s)
        RETURNING chat_id
        """, is_group_chat=bool(is_group_chat), topic=str(topic)
    )


@transaction
def create_personal_chat(user_id):
    topic = get_user(user_id=user_id)['nick']
    chat_id = create_chat(is_group_chat=FALSE, topic=topic)
    member_id = create_member(user_id=user_id, chat_id=chat_id)
    chat = get_chat(chat_id=chat_id)
    return chat


@transaction
def create_group_chat(topic):
    chat_id = create_chat(is_group_chat=TRUE, topic=topic)
    chat = get_chat(chat_id=chat_id)
    return chat


@transaction
def add_members_to_group_chat(chat_id, user_ids):
    pass


@transaction
def leave_group_chat(chat_id):
    pass


# Message
def get_message(message_id):
    return db.query_one(
        """
        SELECT message_id as message_id, user_id as user_id, chat_id as chat_id,
        content as content, added_at as added_at
        FROM messages
        WHERE message_id = %(message_id)s
        """, message_id=int(message_id)
    )


def create_message(user_id, chat_id, content):
    message_id = db.query_one(
        """
        INSERT INTO messages (user_id, chat_id, content, added_at)
        VALUES (%(user_id)s, %(chat_id)s, %(content)s, DEFAULT)
        RETURNING message_id;
        """, user_id=int(user_id), chat_id=int(chat_id), content=str(content)
    )
    return message_id


def list_messages(chat_id, limit):
    return db.query_all(
        """
        SELECT user_id as user_id, nick as nick, name as name, 
        message_id as message_id, content as content, added_at as added_at
        FROM messages
        JOIN users USING (user_id)
        WHERE chat_id = %(chat_id)s
        ORDER BY added_at DESC
        LIMIT %(limit)s
        """, chat_id=int(chat_id), limit=int(limit))


@transaction
def send_message(chat_id, content, attachment_id=None):
    pass


@transaction
def read_message(message_id):
    message = get_message(message_id)


# Member
def get_member(user_id, chat_id):
    return db.query_one(
        """
        SELECT user_id as user_id, chat_id as chat_id, 
        new_messages as new_messages, last_read_message_id as last_read_message_id
        FROM members
        WHERE user_id = %(user_id)s
        AND chat_id = %(chat_id)s
        """, user_id=int(user_id), chat_id=int(chat_id)
    )


def create_member(user_id, chat_id):
    return db.query_one(
        """
        INSERT INTO members (user_id, chat_id)
        VALUES (%(user_id)s, %(chat_id)s)
        RETURNING member_id;
        """, user_id=int(user_id), chat_id=int(chat_id)
    )


# Attachment
def get_attachment(attachment_id):
    return db.query_one(
        """
        SELECT attachment_id as attachment_id, user_id as user_id, chat_id as chat_id,
        message_id as message_id, mime_type as mime_type, url as url
        FROM attachments
        WHERE attachment_id = %(attachment_id)s
        """, attachment_id=int(attachment_id)
    )


# TODO: протестировать
def create_attachment(user_id, chat_id, message_id, url, mime_type):
    attachment_id = db.query_one(
        """
        INSERT INTO attachments (user_id, chat_id, message_id, mime_type, url)
        VALUES (%(user_id)s, %(chat_id)s, %(message_id)s, %(mime_type)s, %(url)s)
        RETURNING attachment_id;
        """, user_id=int(user_id), chat_id=int(chat_id), message_id=int(message_id),
        mime_type=str(mime_type), url=str(url)
    )
    return attachment_id


# TODO: протестировать
def save_file(filename, content):
    url = '/'.join([Config.UPLOAD_FOLDER, filename])
    with open(url, 'w') as file:
        file.write(content)
    return url


# TODO: протестировать
def upload_file(user_id, chat_id, content):
    message_id = create_message(user_id=user_id, chat_id=chat_id, content=content)
    url = save_file(filename=message_id, content=content)
    mime_type = get_mime_type(url)
    attachment_id = create_attachment(user_id=user_id, chat_id=chat_id,
                                      message_id=message_id, url=url, mime_type=mime_type)
    return attachment_id
