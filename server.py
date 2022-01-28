import sqlite3
from app import createApp 

connection = sqlite3.connect('books.db')
createApp(connection).run()
