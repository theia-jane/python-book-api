import os
import pytest
import tempfile
import sqlite3

from app import createApp, dictionaryRowFactory

@pytest.fixture
def client(db):
    yield createApp(db).test_client()
    db.close()

@pytest.fixture
def db(records):

    connection = sqlite3.connect(':memory:')
    cursor = connection.cursor()
    cursor.executescript("""
CREATE TABLE books (
       id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
       published INT,
       author VARCHAR,
       title VARCHAR,       
       first_sentence VARCHAR
       );

INSERT INTO books (published, author, title, first_sentence)
VALUES 
    {};
    """.format(", ".join([ "{}".format(r) for r in records ]))
    )

    connection.row_factory = dictionaryRowFactory
    return connection

@pytest.fixture
def records():
    return [
        (2010, 'Jax Talon', 'Asking questions', 'This is a test book.'),
        (1995, 'Water Lit', 'Again and again', 'Here we go again.'),
        (1971, 'Me', 'I think, therefore', 'Hello there dear friend.')
    ]
