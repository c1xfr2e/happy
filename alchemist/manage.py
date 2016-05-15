# coding: utf-8

from flask import Flask
from flask.ext.script import Manager, Shell

app = Flask(__name__)
manager = Manager(app)


@app.route('/')
def index():
    return '<h1>Run! Now!</h1>'


@manager.shell
def make_shell_context():
    return dict(app=app)


if __name__ == '__main__':
    manager.run()
