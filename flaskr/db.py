import click
from flask import current_app, g
from flask.cli import with_appcontext

from .base import Session, engine, Base


def close_session(e=None):
    session = g.pop('session', None)

    if session is not None:
        session.close()


def get_session():
    if 'session' not in g:
        Base.metadata.create_all(engine)
        g.session = Session()

    return g.session


def init_session():
    session = get_session()

@click.command('init-session')
@with_appcontext
def init_session_command():
    """Clear the existing data and create new tables."""
    init_session()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_session)
    app.cli.add_command(init_session_command)

