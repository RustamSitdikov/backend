import json
import unittest

from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'Index', rv.data)
        self.assertEqual('text/html', rv.mimetype)

        index = "index"
        rv = self.app.post('/', data=dict(index=index))
        self.assertEqual(405, rv.status_code)

    def test_login(self):
        rv = self.app.get('/login/')
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data, {})
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

        login = "Login"
        rv = self.app.post('/login/', data=dict(login=login))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data["login"], login)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_search_users(self):
        rv = self.app.get('/search_users?query={}&limit={}'.format("something", 1))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data['users'], ["User1", "User2", "User3"])
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

        users = "users"
        rv = self.app.post('/search_users', data=dict(users=users))
        self.assertEqual(405, rv.status_code)

    def test_search_chats(self):
        rv = self.app.get('/search_chats?query={}&limit={}'.format("something", 1))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data['chats'], ["Chat1", "Chat2", "Chat3"])
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

        chats = "chats"
        rv = self.app.post('/search_chats', data=dict(chats=chats))
        self.assertEqual(405, rv.status_code)

    def test_list_chats(self):
        rv = self.app.get('/list_chats/')
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data['chats'], ["Chat1", "Chat2", "Chat3"])
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

        chats = "chats"
        rv = self.app.post('/search_chats', data=dict(chats=chats))
        self.assertEqual(405, rv.status_code)

    def test_create_pers_chat(self):
        chat = "Chat"
        user_id = 1

        rv = self.app.get('/create_pers_chat?user_id={}'.format(user_id))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data["chat"], chat)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

        rv = self.app.post('/create_pers_chat?user_id={}'.format(user_id), data=dict(chat=chat))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data["chat"], chat)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_create_group_chat(self):
        chat = "Chat"
        topic = "topic"

        rv = self.app.get('/create_group_chat?user_id={}'.format(topic))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data["chat"], chat)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

        rv = self.app.post('/create_group_chat?user_id={}'.format(topic), data=dict(chat=chat))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data["chat"], chat)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_add_members_to_group_chat(self):
        chat_id = 1
        user_ids = [1, 2, 3]

        rv = self.app.get('/add_members_to_group_chat?chat_id={}&user_ids={}'.format(chat_id, user_ids))
        self.assertEqual(405, rv.status_code)

        member = "Member"
        rv = self.app.post('/add_members_to_group_chat?chat_id={}&user_ids={}'.format(chat_id, user_ids), data=dict(member=member))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data, {})
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_leave_group_chat(self):
        chat_id = 1

        rv = self.app.get('/leave_group_chat?chat_id={}'.format(chat_id))
        self.assertEqual(405, rv.status_code)

        member = "Member"
        rv = self.app.post('/leave_group_chat?chat_id={}'.format(chat_id), data=dict(member=member))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data, {})
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_send_message(self):
        chat_id = 1
        content = "content"
        attach_id = 2

        rv = self.app.get('/send_message?chat_id={}&content={}&attach_id={}'.format(chat_id, content, attach_id))
        self.assertEqual(405, rv.status_code)

        message = "Message"
        rv = self.app.post('/send_message?chat_id={}&content={}&attach_id={}'.format(chat_id, content, attach_id), data=dict(message=message))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data["message"], message)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_read_message(self):
        message_id = 1
        chat = "Chat"

        rv = self.app.get('/read_message?message_id={}'.format(message_id))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data["chat"], chat)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

        rv = self.app.post('/read_message?message_id={}'.format(message_id), data=dict(chat=chat))
        self.assertEqual(405, rv.status_code)

    def test_upload_file(self):
        chat_id = 1
        content = "content"

        rv = self.app.get('/upload_file?chat_id={}&content={}'.format(chat_id, content))
        self.assertEqual(405, rv.status_code)

        attach = "Attach"
        rv = self.app.post('/upload_file?chat_id={}&content={}'.format(chat_id, content), data=dict(attach=attach))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data["attach"], attach)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()