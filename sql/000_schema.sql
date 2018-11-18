DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    nick TEXT NOT NULL CONSTRAINT user_nick_check CHECK (length(nick) < 32),
    name TEXT NOT NULL CONSTRAINT user_name_check CHECK (length(name) < 64),
    avatar TEXT DEFAULT NULL CONSTRAINT user_avatar_check CHECK (length(avatar) < 100)
);
DROP INDEX IF EXISTS user_nick_idx;
CREATE UNIQUE INDEX user_nick_idx ON users (nick);

DROP TABLE IF EXISTS chats CASCADE;
CREATE TABLE IF NOT EXISTS chats (
    chat_id SERIAL PRIMARY KEY,
    is_group_chat BOOLEAN NOT NULL,
    topic TEXT NOT NULL CONSTRAINT chat_topic_check CHECK (length(topic) < 100),
    last_message TEXT DEFAULT NULL
);

DROP TABLE IF EXISTS messages CASCADE;
CREATE TABLE IF NOT EXISTS messages (
    message_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    chat_id INTEGER NOT NULL REFERENCES chats(chat_id),
    content TEXT NOT NULL CONSTRAINT message_content_check CHECK (length(content) < 65536),
    added_at TIMESTAMP NOT NULL DEFAULT NOW()
);

DROP TABLE IF EXISTS members CASCADE;
CREATE TABLE IF NOT EXISTS members (
    member_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    chat_id INTEGER NOT NULL references chats(chat_id),
    new_messages INTEGER NOT NULL DEFAULT 0,
    last_read_message_id INTEGER DEFAULT NULL REFERENCES messages(message_id)
);

DROP TABLE IF EXISTS attachments CASCADE;
CREATE TABLE IF NOT EXISTS attachments (
    attachment_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(user_id),
    chat_id INTEGER NOT NULL REFERENCES chats(chat_id),
    message_id INTEGER NOT NULL REFERENCES messages(message_id),
    type TEXT NOT NULL CONSTRAINT attachment_type_check CHECK (length(type) < 16),
    url TEXT NOT NULL CONSTRAINT attachment_url_check CHECK (length(url) < 64)
);