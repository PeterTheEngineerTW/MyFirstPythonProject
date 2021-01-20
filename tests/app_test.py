import json
import unittest
from app import app
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Boolean, Unicode


class AppTest(unittest.TestCase):
    db_path = 'sqlite:////tmp/test.db'

    def create_table(self):
        self.engine = create_engine(self.db_path, echo=True)
        self.meta = MetaData()

        self.task = Table(
            'task', self.meta,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('name', Unicode(80), nullable=False),
            Column('status', Boolean, nullable=False),
        )

        self.meta.create_all(self.engine)

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_path
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.create_table()
        self.client = app.test_client()

    def tearDown(self):
        pass
        self.meta.drop_all(self.engine)


    def test_get_no_tasks(self):
        # Given
        # no task in db

        # When
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})

        # Then
        # return no task
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

    def test_get_one_tasks(self):
        # Given
        # one task in db
        payload = json.dumps({
            'name': '買早餐'
        })
        self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)

        # When
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})

        # Then
        # return one task
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))
        self.assertEqual(1, response_json['result'][0]['id'])
        self.assertEqual('買早餐', response_json['result'][0]['name'])
        self.assertEqual(0, response_json['result'][0]['status'])

    def test_get_two_tasks(self):
        # Given
        # two task in db
        payload1 = json.dumps({
            'name': '買早餐'
        })
        payload2 = json.dumps({
            'name': '買中餐'
        })
        self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload1)
        self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload2)

        # When
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})

        # Then
        # return two tasks
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response_json['result']))
        self.assertEqual(1, response_json['result'][0]['id'])
        self.assertEqual('買早餐', response_json['result'][0]['name'])
        self.assertEqual(0, response_json['result'][0]['status'])
        self.assertEqual(2, response_json['result'][1]['id'])
        self.assertEqual('買中餐', response_json['result'][1]['name'])
        self.assertEqual(0, response_json['result'][1]['status'])

    def test_post_one_tasks(self):
        # Given
        # no task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        # When
        payload = json.dumps({
            'name': '買晚餐'
        })
        self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        # return one task from get endpoint
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))
        self.assertEqual(1, response_json['result'][0]['id'])
        self.assertEqual('買晚餐', response_json['result'][0]['name'])
        self.assertEqual(0, response_json['result'][0]['status'])

    def test_post_one_tasks_empty_name(self):
        # Given
        # no task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        # When
        payload = json.dumps({
            'name': ''
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('Task name cannot be empty', response_json['message'])

    def test_post_one_tasks_missing_name(self):
        # Given
        # no task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        # When
        payload = json.dumps({
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('field missing in payload', response_json['message'])

    def test_post_one_tasks_not_json_payload(self):
        # Given
        # no task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        # When
        payload = 'name=睡覺'
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('Bad Request', response_json['name'])

    def test_post_one_tasks_not_json_payload(self):
        # Given
        # no task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        # When
        payload = json.dumps({
            'name': 123
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('a field is of incorrect type', response_json['message'])

    def test_post_two_tasks_consecutively(self):
        # Given
        # no task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        # When
        # post two tasks consecutively
        payload1 = json.dumps({
            'name': '上班'
        })
        payload2 = json.dumps({
            'name': '下班'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload1)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('上班', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload2)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(2, response_json['result']['id'])
        self.assertEqual('下班', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        # Then
        # return two task from get endpoint with auto incremented id
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(response_json['result']))
        self.assertEqual(1, response_json['result'][0]['id'])
        self.assertEqual('上班', response_json['result'][0]['name'])
        self.assertEqual(0, response_json['result'][0]['status'])
        self.assertEqual(2, response_json['result'][1]['id'])
        self.assertEqual('下班', response_json['result'][1]['name'])
        self.assertEqual(0, response_json['result'][1]['status'])

    def test_put_one_tasks(self):
        # Given
        # one task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        payload = json.dumps({
            'name': '沒得買'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('沒得買', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))

        # When
        payload = json.dumps({
            'id': 1,
            'name': '買買買',
            'status': 1
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_json['id'])
        self.assertEqual('買買買', response_json['name'])
        self.assertEqual(1, response_json['status'])

    def test_put_one_nonexist_task(self):
        # Given
        # no task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        # When
        payload = json.dumps({
            'id': 1,
            'name': '沒得買',
            'status': 1
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('Task not found for id 1', response_json['message'])

    def test_put_one_tasks_unmatch_id_in_payload(self):
        # Given
        # one task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        payload = json.dumps({
            'name': '沒得買'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('沒得買', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))

        # When
        payload = json.dumps({
            'id': 2,
            'name': '買買買',
            'status': 1
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('Id has to be the same in payload', response_json['message'])

    def test_put_one_tasks_invalid_status(self):
        # Given
        # one task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        payload = json.dumps({
            'name': '沒得買'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('沒得買', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))

        # When
        payload = json.dumps({
            'id': 1,
            'name': '買買買',
            'status': 2
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('Status has to be either 1 or 0', response_json['message'])

    def test_put_one_tasks_empty_task_name(self):
        # Given
        # one task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        payload = json.dumps({
            'name': '沒得買'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('沒得買', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))

        # When
        payload = json.dumps({
            'id': 1,
            'name': '',
            'status': 1
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('Task name cannot be empty', response_json['message'])

    def test_put_one_tasks_wrong_id_type(self):
        # Given
        # one task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        payload = json.dumps({
            'name': '沒得買'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('沒得買', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))

        # When
        payload = json.dumps({
            'id': 'id',
            'name': '打東東',
            'status': 0
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('a field is of incorrect type', response_json['message'])

    def test_put_one_tasks_same_status(self):
        # Given
        # one task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        payload = json.dumps({
            'name': '沒得買'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('沒得買', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))

        # When
        payload = json.dumps({
            'id': 1,
            'name': '買買買',
            'status': 0
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_json['id'])
        self.assertEqual('買買買', response_json['name'])
        self.assertEqual(0, response_json['status'])
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_json['id'])
        self.assertEqual('買買買', response_json['name'])
        self.assertEqual(0, response_json['status'])

    def test_delete_one_nonexist_task(self):
        # Given
        # no task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        # When
        response = self.client.delete('/task/1', headers={"Content-Type": "application/json"})

        # Then
        # return task not found msg
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('Task not found for id 1', response_json['message'])

    def test_put_one_tasks_boolean_status(self):
        # Given
        # one task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        payload = json.dumps({
            'name': '沒得買'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('沒得買', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))

        # When
        payload = json.dumps({
            'id': 1,
            'name': '買買買',
            'status': 0
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_json['id'])
        self.assertEqual('買買買', response_json['name'])
        self.assertEqual(0, response_json['status'])

        payload = json.dumps({
            'id': 1,
            'name': 'ABC',
            'status': False
        })
        response = self.client.put('/task/1', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, response_json['id'])
        self.assertEqual('ABC', response_json['name'])
        self.assertEqual(0, response_json['status'])

    def test_delete_one_tasks(self):
        # Given
        # one task in db
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))

        payload = json.dumps({
            'name': '沒得買'
        })
        response = self.client.post('/task', headers={"Content-Type": "application/json"}, data=payload)
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(201, response.status_code)
        self.assertEqual(1, response_json['result']['id'])
        self.assertEqual('沒得買', response_json['result']['name'])
        self.assertEqual(0, response_json['result']['status'])

        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(response_json['result']))

        # When
        response = self.client.delete('/task/1', headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)

        # Then
        # return no task from get endpoint
        self.assertEqual(200, response.status_code)
        response = self.client.get('/tasks', headers={"Content-Type": "application/json"})
        response_json = json.loads(str(response.data, 'utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(response_json['result']))