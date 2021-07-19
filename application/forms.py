from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField

class TaskForm(FlaskForm):
    description = StringField("What is the task?")
    label = SelectField("Choose a label", choices=[])
    submit = SubmitField("Submit")

class LabelForm(FlaskForm):
    name = StringField("What is the label?")
    submit = SubmitField("Submit")