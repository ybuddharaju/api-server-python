# test_todoserver.py
import unittest
import json
from todoserver import app
app.testing = True

def json_body(resp):
    return json.loads(resp.data.decode("utf-8"))

class TestTodoserver(unittest.TestCase):
    def test_get_empty_list_of_tasks(self):
        client = app.test_client()
        resp = client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], json_body(resp))

    def test_create_a_task_and_get_its_details(self):
        client = app.test_client()
        # verify test pre-conditions
        resp = client.get("/tasks/")
        self.assertEqual([], json_body(resp))
        # create new task
        new_task_data = {
            "summary": "Get milk",
            "description": "One gallon organic whole milk",
        }
        resp = client.post("/tasks/",
                           data=json.dumps(new_task_data))
        self.assertEqual(201, resp.status_code)
        data = json_body(resp)
        self.assertIn("id", data)
        # get task details
        task_id = data["id"]
        resp = client.get("/tasks/{:d}/".format(task_id))
        self.assertEqual(200, resp.status_code)
        task = json_body(resp)
        self.assertEqual(task_id, task["id"])
        self.assertEqual("Get milk", task["summary"])
        self.assertEqual("One gallon organic whole milk",
                         task["description"])


