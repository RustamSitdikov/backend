#!/usr/bin/env python

import json
import unittest
from app import app, db
from flask_jsonrpc.proxy import ServiceProxy


class AppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config.from_object('config.TestingConfig')

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        self.app = app.test_client()
        self.service = ServiceProxy('http://localhost:5000/api')
        db.create_all()

    def tearDown(self):
        db.drop_all()
        pass

    def test_index(self):
        pass

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
        user_id = 1
        chat_id = 1
        content = 'Hi'
        attachnment_id = None

        rv = self.service.api.send_message(user_id=user_id, chat_id=chat_id, content=content, attachment_id=attachnment_id)
        result = rv['result']
        self.assertEqual(content, result['content'])

    def test_read_message(self):
        user_id = 1
        chat_id = 1
        content = 'Hi'
        attachnment_id = None

        rv = self.service.api.send_message(user_id=user_id, chat_id=chat_id, content=content, attachment_id=attachnment_id)
        message_id = rv['result']['message_id']

        rv = self.service.api.read_message(user_id=user_id, message_id=message_id)
        result = rv['result']

        self.assertEqual(content, result['last_message'])
        self.assertEqual(chat_id, result['chat_id'])

    def test_list_messages(self):
        user_ids = [1, 2]
        chat_id = 1
        contents = ['Hi', 'Hello']
        attachnment_id = None

        for (user_id, content) in zip(user_ids, contents):
            rv = self.service.api.send_message(user_id=user_id, chat_id=chat_id, content=content, attachment_id=attachnment_id)

        rv = self.service.api.list_messages(chat_id=chat_id)
        results = rv['result']
        for i, result in enumerate(results):
            self.assertEqual(user_ids[i], result['user_id'])
            self.assertEqual(contents[i], result['content'])

    def test_upload_file(self):
        pass


if __name__ == "__main__":
    unittest.main()