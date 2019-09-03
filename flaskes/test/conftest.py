import os
import pytest
from flaskes.main import app as flask_app
from flaskes.main import db

from flask_migrate import upgrade

@pytest.yield_fixture(scope='session')
def app():
    """
    Setup our flask test app, this only gets executed once.

    :return: Flask app
    """
    params = {
        'DEBUG': False,
        'TESTING': True,
    }
    _app = flask_app
    print(_app)
    _app.config['TESTING'] = True
    _app.config['DEBUG'] = False

    basedir = os.path.abspath(os.path.dirname(__file__))

    _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.sqlite')

    with _app.app_context():
        upgrade()

    ctx = _app.app_context()
    ctx.push()

    yield _app
    db.drop_all()
    db.engine.execute("DROP TABLE alembic_version")
    ctx.pop()
    
    


@pytest.yield_fixture(scope='function')
def client(app):
    """
    Setup an app client, this gets executed for each test function.

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()


