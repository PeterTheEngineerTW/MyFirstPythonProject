from flask_app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    status = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            'name': self.name,
            'status': int(self.status),
            'id': self.id
        }
