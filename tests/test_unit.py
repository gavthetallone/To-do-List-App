from flask import url_for
from flask_testing import TestCase
from application import app, db
from application.models import Label, Task

class TestBase(TestCase):
    def create_app(self):
        app.config.update(
            SQLALCHEMY_DATABASE_URI="sqlite:///test.db",
            DEBUG=True,
            WTF_CSRF_ENABLED=False
        )
        return app

    def setUp(self):
        db.create_all()

        db.session.add(Task(description="Run unit tests"))
        db.session.add(Task(description="Do something else", completed=True))

        db.session.commit()

    def tearDown(self):
        db.drop_all()

class TestViews(TestBase):
    def test_home(self):
        response = self.client.get(url_for("home"))
        self.assert200(response)
    
    def test_create(self):
        response = self.client.get(url_for("create"))
        self.assert200(response)
    
    def test_update(self):
        response = self.client.get(url_for("update", id=1))
        self.assert200(response)


class TestRead(TestBase):
    def test_home(self):
        response = self.client.get(url_for("home"))
        assert "Run unit tests" in response.data.decode()
        assert "Do something else" in response.data.decode()

class TestCreate(TestBase):
    def test_create(self):
        response = self.client.post(
            url_for("create"),
            data={"description" : "Check create is working"},
            follow_redirects=True
            )
        
        assert "Check create is working" in response.data.decode()

    def test_create_label(self):
        response = self.client.post(
            url_for("create_label"),
            data={"name" : "Example label"},
            follow_redirects=True
            )
        
        assert Label.query.filter_by(name="Example label").first() != None

class TestUpdate(TestBase):
    def test_update(self):
        response = self.client.post(
            url_for("update", id=1),
            data={"description" : "Check update is working"},
            follow_redirects=True
            )
        
        assert "Check update is working" in response.data.decode()
        assert "Do something else" in response.data.decode()
        assert "Run unit tests" not in response.data.decode()
    
    def test_complete(self):
        response = self.client.get(
            url_for("complete", id=1),
            follow_redirects=True
            )
        assert "Run unit tests - ✔️" in response.data.decode()
        assert "Do something else - ✔️" in response.data.decode()
    
    def test_incomplete(self):
        response = self.client.get(
            url_for("incomplete", id=2),
            follow_redirects=True
            )
        assert "Run unit tests - ❌" in response.data.decode()
        assert "Do something else - ❌" in response.data.decode()


class TestDelete(TestBase):
    def test_delete(self):
        response = self.client.get(
            url_for("delete", id=1),
            follow_redirects=True
            )

        assert "Do something else" in response.data.decode()
        assert "Run unit tests" not in response.data.decode()
        
