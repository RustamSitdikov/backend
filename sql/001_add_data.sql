INSERT INTO users (nick, name, avatar)
VALUES
    ('fenya', 'Rustam Sitdikov', DEFAULT),
    ('mialinx', 'Dmitry Smal', DEFAULT),
    ('toshunster', 'Anton Kukhtichev', DEFAULT);

INSERT INTO chats (is_group_chat, topic, last_message)
VALUES
    ('TRUE', 'Backend MIPT', DEFAULT),
    ('TRUE', 'Frontend MIPT', DEFAULT),
    ('TRUE', 'Android MIPT', DEFAULT);

INSERT INTO members (user_id, chat_id, new_messages, last_read_message_id)
VALUES
    (1, 1, DEFAULT, DEFAULT),
    (2, 1, DEFAULT, DEFAULT);