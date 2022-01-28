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

