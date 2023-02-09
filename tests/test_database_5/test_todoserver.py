# test_todoserver.py
import unittest
import json
from todoserver import app
app.testing = True
app.init_db("sqlite:///:memory:")

def json_body(resp):
    return json.loads(resp.data.decode("utf-8"))

class TestTodoserver(unittest.TestCase):
    def setUp(self):
        app.erase_all_test_data()
        self.client = app.test_client()
        # verify test pre-conditions
        resp = self.client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], json_body(resp))

    def test_create_a_task_and_get_its_details(self):
        # verify test pre-conditions
        resp = self.client.get("/tasks/")
        self.assertEqual([], json_body(resp))
        # create new task
        new_task_data = {
            "summary": "Get milk",
            "description": "One gallon organic whole milk",
        }
        resp = self.client.post("/tasks/",
                           data=json.dumps(new_task_data))
        self.assertEqual(201, resp.status_code)
        data = json_body(resp)
        self.assertIn("id", data)
        # get task details
        task_id = data["id"]
        resp = self.client.get("/tasks/{:d}/".format(task_id))
        self.assertEqual(200, resp.status_code)
        task = json_body(resp)
        self.assertEqual(task_id, task["id"])
        self.assertEqual("Get milk", task["summary"])
        self.assertEqual("One gallon organic whole milk",
                         task["description"])

    def test_create_multiple_tasks_and_fetch_list(self):
        tasks = [
            {"summary":"Get milk",
             "description":"Half gallon of almond milk"},
            {"summary":"Go to gym",
             "description":"Leg day. Blast those quads!"},
            {"summary":"Wash car",
             "description":"Be sure to get wax coat"},
        ]
        for task in tasks:
            with self.subTest(task=task):
                resp = self.client.post("/tasks/",
                                        data=json.dumps(task))
                self.assertEqual(201, resp.status_code)
        # get list of tasks
        resp = self.client.get("/tasks/")
        self.assertEqual(200, resp.status_code)
        checked_tasks = json_body(resp)
        self.assertEqual(3, len(checked_tasks))
