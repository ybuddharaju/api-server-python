# test_todoserver.py
import unittest
import json
from todoserver import app

class TestTodoserver(unittest.TestCase):
    def test_get_empty_list_of_tasks(self):
        client = app.test_client()
        resp = client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        data = json.loads(resp.data.decode("utf-8"))
        self.assertEqual([], data)