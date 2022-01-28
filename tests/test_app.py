import pytest

def test_home(client):
    assert client.get("/").status_code == 200


def test_404(client):
    assert client.get("/does-not-exist").status_code == 404
