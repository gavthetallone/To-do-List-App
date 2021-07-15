from . import app, db
from .models import Task
from .forms import TaskForm
from flask import redirect, url_for, request, render_template

@app.route("/")
def home():
    tasks = Task.query.all()

    return render_template("home.html", tasks=tasks)

@app.route("/create", methods=["GET", "POST"])
def create():
    form = TaskForm()

    if request.method == "POST":
        new_task = Task(description=form.description.data)
        db.session.add(new_task)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return render_template("create.html", form=form)

@app.route("/update/<int:id>/", methods=["GET", "POST"])
def update(id):
    task = Task.query.get(id)
    form = TaskForm()

    if request.method == "POST":
        task.description = form.description.data
        db.session.add(task)
        db.session.commit()

        return redirect(url_for("home"))
    else:
        return render_template("create.html", form=form)

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

    