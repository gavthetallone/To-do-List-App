from . import app, db
from .models import Label, Task
from .forms import TaskForm, LabelForm
from flask import redirect, url_for, request, render_template

@app.route("/")
def home():
    tasks = Task.query.all()

    return render_template("home.html", tasks=tasks)

@app.route("/create", methods=["GET", "POST"])
def create():
    form = TaskForm()

    if request.method == "POST":
        new_task = Task(
            description=form.description.data,
            label_id=form.label.data
            )
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        labels = Label.query.all()
        form.label.choices = [(label.id, label.name) for label in labels]

        return render_template("create_task.html", form=form)

@app.route("/create_label", methods=["GET", "POST"])
def create_label():
    form = LabelForm()

    if request.method == "POST":
        new_label = Label(name=form.name.data)
        db.session.add(new_label)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return render_template("create_label.html", form=form)

@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    task = Task.query.get(id)
    form = TaskForm()

    if request.method == "POST":
        task.description = form.description.data
        task.label_id = form.label.data
        db.session.add(task)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        labels = Label.query.all()
        form.label.choices = [(label.id, label.name) for label in labels]

        form.description.data = task.description

        return render_template("create_task.html", form=form)

@app.route("/delete/<int:id>")
def delete(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/complete/<int:id>")
def complete(id):
    task = Task.query.get(id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/incomplete/<int:id>")
def incomplete(id):
    task = Task.query.get(id)
    task.completed = False
    db.session.add(task)
    db.session.commit()

    return redirect(url_for("home"))

    