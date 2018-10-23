import json
import unittest

from app import app


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_index(self):
        rv = self.app.get('/')
        self.assertEqual(200, rv.status_code)
        self.assertEqual(b'OK', rv.data)
        self.assertEqual('text/html', rv.mimetype)

    def test_get_users(self):
        rv = self.app.get('/users/list/')
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data['users'], ["User1", "User2", "User3"])
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_get_chats(self):
        rv = self.app.get('/chats/list/')
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data['chats'], ["Chat1", "Chat2", "Chat3"])
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_create_chat(self):
        chatname = "chatname"
        rv = self.app.post('/chats/create/', data=dict(chatname=chatname))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data[chatname], chatname)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_upload_file(self):
        file = "file"
        rv = self.app.post('/chats/upload/', data=dict(file=file))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data[file], file)
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_leave_chat(self):
        chat_id = 1
        rv = self.app.get('/chats/leave/{}'.format(chat_id))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data, {})
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_invite_to_chat(self):
        chat_id = 1
        rv = self.app.get('/chats/invite/{}'.format(chat_id))
        self.assertEqual(405, rv.status_code)

        rv = self.app.post('/chats/invite/{}'.format(chat_id))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data, {})
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_send_message_to_chat(self):
        chat_id = 1
        content = "Hello"
        attach_id = 2

        rv = self.app.get('/chats/send/{0}/{1}/{2}'.format(chat_id, content, attach_id))
        self.assertEqual(405, rv.status_code)

        rv = self.app.post('/chats/send/{0}/{1}/{2}'.format(chat_id, content, attach_id))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data, {})
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def test_read_message_from_chat(self):
        chat_id = 1
        rv = self.app.get('/chats/leave/{}'.format(chat_id))
        data = json.loads(rv.get_data(as_text=True))
        self.assertEqual(data, {})
        self.assertEqual(200, rv.status_code)
        self.assertEqual('application/json', rv.mimetype)

    def tearDown(self):
        pass


if __name__ == "__main__":
    unittest.main()