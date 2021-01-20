from flask_app import db
from model.task import Task
from exception.exception import InvalidInput

class TaskService:

    def create_task(self, task_name):
        task = Task(name=task_name, status=0)
        db.session.add(task)
        db.session.commit()
        return task

    def get_all_tasks(self):
        return Task.query.all()

    def update_task_by_id(self, task_id, task_name, task_status):
        task = Task.query.get(task_id)
        if task is None:
            raise InvalidInput("Task not found for id {}".format(task_id))
        task.name = task_name
        task.status = task_status
        db.session.commit()
        return task

    def delete_task_by_id(self, task_id):
        task = Task.query.get(task_id)
        if task is None:
            raise InvalidInput("Task not found for id {}".format(task_id))
        db.session.delete(task)
        db.session.commit()
