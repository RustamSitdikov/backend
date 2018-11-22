import json
import unittest
import testing.postgresql
import psycopg2
import jsonlint

from app import app

# from flask_jsonrpc.proxy import ServiceProxy
# server = ServiceProxy('http://localhost:5000/api')


class AppTest(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.postgresql = testing.postgresql.Postgresql()

    def tearDown(self):
        self.postgresql.stop()

    def test_index(self):
        rv = self.app.post('/api/', data=dict(jsonrpc='2.0', method='index', params=[], id='1'))
        print(rv)

    def test_login(self):
        pass

    def test_search_users(self):
        pass

    def test_search_chats(self):
        pass

    def test_list_chats(self):
        pass

    def test_create_pers_chat(self):
        pass

    def test_create_group_chat(self):
        pass

    def test_add_members_to_group_chat(self):
        pass

    def test_leave_group_chat(self):
        pass

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

    def test_list_messages(self):
        pass

    def test_upload_file(self):
        pass


if __name__ == "__main__":
    unittest.main()