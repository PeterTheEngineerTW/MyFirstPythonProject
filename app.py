from flask import request, jsonify, make_response
from flask_app import app
from exception.exception import InvalidInput
from service.task_service import TaskService
from werkzeug.exceptions import HTTPException
import json

task_service = TaskService()

@app.route('/tasks')
def get_tasks():
    tasks = [task.to_dict() for task in task_service.get_all_tasks()]
    response = make_response(jsonify({'result': tasks}))
    response.headers['Content-Type'] = 'application/json'
    return response, 200

@app.route('/task', methods=['POST'])
def post_task():
    json_data = request.get_json(force=True)
    task_name = json_data['name']

    if len(task_name) == 0:
        raise InvalidInput("Task name cannot be empty")

    task = task_service.create_task(task_name)
    response = make_response(jsonify({'result': task.to_dict()}))
    response.headers['Content-Type'] = 'application/json'
    return response, 201

@app.route('/task/<id_>', methods=['PUT', 'DELETE'])
def put_or_delete_task(id_):
    task_id = id_

    if request.method == 'PUT':
        json_data = request.get_json(force=True)
        task_name = json_data['name']
        task_status = json_data['status']

        if int(task_id) != int(json_data['id']):
            raise InvalidInput("Id has to be the same in payload")
        if len(task_name) == 0:
            raise InvalidInput("Task name cannot be empty")
        if task_status not in {0, 1}:
            raise InvalidInput("Status has to be either 1 or 0")

        task = task_service.update_task_by_id(task_id, task_name, task_status)
        response = make_response(jsonify(task.to_dict()))
        response.headers['Content-Type'] = 'application/json'
        return response, 200

    if request.method == 'DELETE':
        task_service.delete_task_by_id(task_id)
        response = make_response()
        response.headers['Content-Type'] = 'application/json'
        return response, 200

@app.errorhandler(InvalidInput)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(KeyError)
def handle_key_error(error):
    response = jsonify({'message': "field missing in payload"})
    response.status_code = 400
    return response

@app.errorhandler(ValueError)
def handle_value_error(error):
    response = jsonify({'message': "a field is of incorrect type"})
    response.status_code = 400
    return response

@app.errorhandler(TypeError)
def handle_value_error(error):
    response = jsonify({'message': "a field is of incorrect type"})
    response.status_code = 400
    return response

@app.errorhandler(HTTPException)
def handle_http_exception(error):
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description,
    })
    response.content_type = "application/json"
    return response

if __name__ == '__main__':
    app.run()