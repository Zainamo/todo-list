import os

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.views import MethodView
from sqlalchemy.orm import validates
from dotenv import load_dotenv

from src.utils import TodoUtils, transaction

load_dotenv()
app = Flask(__name__)
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}' \
                                        f'@postgres:{DB_PORT}/{DB_HOST}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
db.init_app(app)
migrate = Migrate(app, db)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


class TodoView(MethodView, TodoUtils):
    init_every_request = False
    methods = ["GET", "POST"]

    def __init__(self, model):
        self.model = model
        self.validator = self.validate_title

    def get(self):
        if request.args.get('add'):
            return render_template('add_todo.html')
        else:
            todos = self.model.query.all()
            return render_template('todo.html', todos=todos)

    @transaction(db)
    @validates('title')
    def post(self):
        # validate the title
        title = request.values['title']
        self.validator(title)

        # create an instance of the to do model with the validated data
        item = self.model(title=title)

        # commit the item to the database
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('todo'))


def register_api(application, model):
    item = TodoView.as_view("todo", model)
    application.add_url_rule("/", view_func=item)


register_api(app, Todo)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
