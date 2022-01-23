from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
app.config['DEBUG'] = True

def dictionaryRowFactory(cursor, row):
    return { column[0]: row[i] for i, column in enumerate(cursor.description) }

def fetchAllBooks(query, params={}):
    conn = sqlite3.connect('books.db')
    conn.row_factory = dictionaryRowFactory
    return conn.cursor().execute(query, params).fetchall()

@app.route('/', methods = ['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>This site is a prototype API for distant reading of science fiction novels.</p>'''

@app.errorhandler(404)
def pageNotFound(e):
    return '<h1>404</h1><p>The resource could not be found.</p>', 404

### Book APIs
@app.route('/api/v1/resources/books/all', methods = ['GET'])
def apiBooksAll():
    books = fetchAllBooks('SELECT * FROM books;')
    return jsonify(books)

@app.route('/api/v1/resources/books', methods = ['GET'])
def apiBooksFilter():
    # Fields we want to filter on
    fields = [ 'id', 'published', 'author' ] 

    # Make filter dictionary based on which request args
    # are sent
    queryFilter = {
        f: request.args[f]
        for f in fields
        if request.args.get(f)
    }

    # Build up our where clause
    whereClause = ' AND '.join([
        '{0}=:{0}'.format(f)
        for f in queryFilter.keys()
    ])

    query = "SELECT * FROM books WHERE {};".format(whereClause)
    books = fetchAllBooks(query, queryFilter)
    return jsonify(books)

app.run()

