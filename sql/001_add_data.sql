INSERT INTO users (nick, name, avatar)
VALUES
    ('fenya', 'Rustam Sitdikov', DEFAULT),
    ('mialinx', 'Dmitry Smal', DEFAULT),
    ('toshunster', 'Anton Kukhtichev', DEFAULT);

INSERT INTO chats (is_group_chat, topic, last_message)
VALUES
    ('TRUE', 'Backend MIPT', DEFAULT ),
    ('TRUE', 'Frontend MIPT', DEFAULT ),
    ('TRUE', 'Android MIPT', DEFAULT ),
    ('FALSE', 'mialinx', DEFAULT ),
    ('FALSE', 'toshunster', DEFAULT );