from flask_jsonrpc.proxy import ServiceProxy

server = ServiceProxy('http://localhost:5000/api')

# postgresql = testing.postgresql.Postgresql()

# print(server.add_members_to_group_chat(chat_id=1, user_ids=[1, 2]))
# print(server.create_personal_chat(1, 2))
print(server.leave_group_chat(user_id=2, chat_id=1))