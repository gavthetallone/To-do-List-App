from . import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    label_id = db.Column(db.Integer, db.ForeignKey("label.id"))

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    tasks = db.relationship('Task', backref="label")
