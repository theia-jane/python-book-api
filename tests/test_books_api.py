import pytest

def test_all(client, db):
    response = client.get("/api/v1/resources/books/all")
    assert response.status_code == 200
    allBooks = response.get_json()

    expectedBooks = db.cursor().execute("SELECT * FROM books;").fetchall();
    assert len(allBooks) == len(expectedBooks)

    ## Make sure our data is in the same order
    allBooks = sorted(allBooks, key=lambda b: b['id'])
    expectedBooks = sorted(expectedBooks, key=lambda b: b['id'])

    for i in range(len(allBooks)):
        actualBook = allBooks[i]
        expectedBook = expectedBooks[i]

        # Spot check some important keys
        keys = ['id', 'author', 'title']
        for key in keys:
            assert actualBook[key] == expectedBook[key]

def test_id_filter(client):
    """
    When using the `id=?` filter this api should only return zero or one 
    """
    response = client.get("/api/v1/resources/books", query_string='id=1')
    assert response.status_code == 200
    filteredBooks = response.get_json()
    assert len(filteredBooks) == 1 

    response = client.get("/api/v1/resources/books", query_string='id=1&author=FAKEAUTHOR')
    assert response.status_code == 200 
    filteredBooks = response.get_json()
    assert len(filteredBooks) == 0 


def test_author_filter(client, db):
    author = "Me" # Well known author...........
    expectedBooks = db.cursor().execute("SELECT * FROM books WHERE author = ?;", [author]).fetchall();
    expectedBooks = sorted(expectedBooks, key=lambda b: b['id'])

    response = client.get("/api/v1/resources/books", query_string='author={}'.format(author))
    assert response.status_code == 200

    filteredBooks = response.get_json()
    filteredBooks = sorted(filteredBooks, key=lambda b: b['id'])
    assert len(filteredBooks) == len(expectedBooks) 

    for i in range(len(filteredBooks)):
        actualBook = filteredBooks[i]
        expectedBook = expectedBooks[i]

        # Spot check some important keys
        keys = ['id', 'author', 'title']
        for key in keys:
            assert actualBook[key] == expectedBook[key]

def test_published_filter(client, db):
    published = 2010 # Well something was published this year
    expectedBooks = db.cursor().execute("SELECT * FROM books WHERE published = ?;", [published]).fetchall();
    expectedBooks = sorted(expectedBooks, key=lambda b: b['id'])

    response = client.get("/api/v1/resources/books", query_string='published={}'.format(published))
    assert response.status_code == 200

    filteredBooks = response.get_json()
    filteredBooks = sorted(filteredBooks, key=lambda b: b['id'])
    assert len(filteredBooks) == len(expectedBooks) 

    for i in range(len(filteredBooks)):
        actualBook = filteredBooks[i]
        expectedBook = expectedBooks[i]

        # Spot check some important keys
        keys = ['id', 'author', 'title']
        for key in keys:
            assert actualBook[key] == expectedBook[key]


def test_combined_filter(client, db):
    testBooks = db.cursor().execute("SELECT * FROM books LIMIT 1;").fetchall();
    testBook = testBooks[0]
    values = [testBook['published'], testBook['author']] 

    queryString = 'published={}&author={}'.format(*values)
    response = client.get("/api/v1/resources/books", query_string=queryString)
    assert response.status_code == 200

    expectedBooks = db.cursor().execute("SELECT * FROM books WHERE published = ? AND author = ?;", values).fetchall();
    expectedBooks = sorted(expectedBooks, key=lambda b: b['id'])

    filteredBooks = response.get_json()
    filteredBooks = sorted(filteredBooks, key=lambda b: b['id'])
    assert len(filteredBooks) == len(expectedBooks) 

    for i in range(len(filteredBooks)):
        actualBook = filteredBooks[i]
        expectedBook = expectedBooks[i]

        # Spot check some important keys
        keys = ['id', 'author', 'title']
        for key in keys:
            assert actualBook[key] == expectedBook[key]
