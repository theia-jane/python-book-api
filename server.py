from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['DEBUG'] = True

books = [
    {'id': 0,
     'title': 'A Fire Upon the Deep',
     'author': 'Vernor Vinge',
     'first_sentence': 'The coldsleep itself was dreamless.',
     'year_published': '1992'},
    {'id': 1,
     'title': 'The Ones Who Walk Away From Omelas',
     'author': 'Ursula K. Le Guin',
     'first_sentence': 'With a clamor of bells that set the swallows soaring, the Festival of Summer came to the city Omelas, bright-towered by the sea.',
     'year_published': '1973'},
    {'id': 2,
     'title': 'Dhalgren',
     'author': 'Samual R. Delany',
     'first_sentence': 'to wound the autumnal city.',
     'year_published': '1975'}
]


@app.route('/', methods = ['GET'])
def home():
    return '<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>'

@app.route('/api/v1/resources/books/all', methods = ['GET'])
def api_all():
    return jsonify(books)

@app.route('/api/v1/resources/books', methods = ['GET'])
def api_id():
    # Check if an id was provided
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return 'Error: No id field provided. Please specify an id.'
    
    return jsonify([ b for b in books if b['id'] == id ])

app.run()

