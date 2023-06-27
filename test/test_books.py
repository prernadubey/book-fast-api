import requests

GET_BOOKS = {
    "books": [
        {
            "author_name": "Arthur C. Clarke",
            "title": "test_book1",
            "id": 1
        },
        {
            "author_name": "Stephen Hawking",
            "title": "test_book2",
            "id": 2
        }
    ]
}


def test_add_books(app):
    result = requests.post("http://127.0.0.1:8000/v1/books", json={"author_id": 1, "title": "test_book1"})
    assert result.ok

    result = requests.post("http://127.0.0.1:8000/v1/books", json={"author_id": 2, "title": "test_book2"})
    assert result.json() == {"book_id": 2}

    result = requests.get("http://127.0.0.1:8000/v1/books")
    assert result.json() == GET_BOOKS

