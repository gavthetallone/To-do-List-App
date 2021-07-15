from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class TaskForm(FlaskForm):
    description = StringField("What is the task?")
    submit = SubmitField("Submit")