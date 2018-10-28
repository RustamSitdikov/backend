DROP SCHEMA IF EXISTS messenger;
CREATE SCHEMA IF NOT EXISTS messenger AUTHORIZATION fenya;
ALTER SCHEMA messenger OWNER TO fenya;

DROP TABLE IF EXISTS messenger.users;
CREATE TABLE IF NOT EXISTS messenger.users (
    user_id SERIAL PRIMARY KEY,
    nick TEXT NOT NULL CONSTRAINT user_nick_check CHECK (length(nick) < 32),
    name TEXT NOT NULL CONSTRAINT user_name_check CHECK (length(name) < 64),
    avatar TEXT NOT NULL DEFAULT '' CONSTRAINT user_avatar_check CHECK (length(avatar) < 100)
);

DROP TABLE IF EXISTS messenger.chats;
CREATE TABLE IF NOT EXISTS messenger.chats (
    chat_id SERIAL PRIMARY KEY,
    is_group_chat BOOLEAN NOT NULL,
    topic TEXT NOT NULL DEFAULT '' CONSTRAINT chat_topic_check CHECK (length(topic) < 100),
    last_message TEXT NOT NULL CONSTRAINT chat_last_message_check CHECK (length(last_message) < 65536)
);

DROP TABLE IF EXISTS messenger.messages;
CREATE TABLE IF NOT EXISTS messenger.messages (
    message_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES messenger.users(user_id),
    chat_id INTEGER NOT NULL REFERENCES messenger.chats(chat_id),
    content TEXT NOT NULL CONSTRAINT message_content_check CHECK (length(content) < 65536),
    added_at TIMESTAMP NOT NULL DEFAULT NOW()
);

DROP TABLE IF EXISTS messenger.members;
CREATE TABLE IF NOT EXISTS messenger.members (
    member_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES messenger.users(user_id),
    chat_id INTEGER NOT NULL references messenger.chats(chat_id),
    new_messages INTEGER NOT NULL,
    last_read_message_id INTEGER NOT NULL REFERENCES messenger.messages(message_id)
);

DROP TABLE IF EXISTS messenger.attachments;
CREATE TABLE IF NOT EXISTS messenger.attachments (
    attach_id SERIAL PRIMARY KEY,
    chat_id INTEGER NOT NULL REFERENCES messenger.chats(chat_id),
    user_id INTEGER NOT NULL REFERENCES messenger.users(user_id),
    message_id INTEGER NOT NULL REFERENCES messenger.messages(message_id),
    type TEXT NOT NULL CONSTRAINT attachment_type_check CHECK (length(type) < 16),
    url TEXT NOT NULL CONSTRAINT attachment_url_check CHECK (length(url) < 64)
);