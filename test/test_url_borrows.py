import requests
from datetime import date


TODAY_DATE = str(date.today())
GET_BORROWS = {
    "borrows": [
        {
            "reader": "test_reader1",
            "title": "test_book1",
            "author": "Arthur C. Clarke",
            "borrow_time": TODAY_DATE
        },
        {
            "reader": "test_reader2",
            "title": "test_book2",
            "author": "Stephen Hawking",
            "borrow_time": TODAY_DATE
        }
    ]
}

RES_BOOK_BORROWED = {
    "detail": "Requested book is already borrowed. Please try with other book."
}

RES_BOOK_READER_NOT_EXIST = {
    "detail": "Requested reader or book does not exist. Please check the data."
}


def test_add_borrows(app):
    result = requests.post("http://127.0.0.1:8000/v1/borrows", json={"reader_id": 1, "book_id": 1})
    assert result.ok

    result = requests.post("http://127.0.0.1:8000/v1/borrows", json={"reader_id": 2, "book_id": 2})
    assert result.ok

    # CASE: When reader exist but not book.
    result = requests.post("http://127.0.0.1:8000/v1/borrows", json={"reader_id": 3, "book_id": 5})
    assert result.json() == RES_BOOK_READER_NOT_EXIST
    assert result.status_code == 404

    # CASE: When reader and book both does not exist.
    result = requests.post("http://127.0.0.1:8000/v1/borrows", json={"reader_id": 5, "book_id": 5})
    assert result.json() == RES_BOOK_READER_NOT_EXIST
    assert result.status_code == 404

    # CASE: When book booked by someone else.
    result = requests.post("http://127.0.0.1:8000/v1/borrows", json={"reader_id": 3, "book_id": 1})
    assert result.json() == RES_BOOK_BORROWED
    assert result.status_code == 403

    # CASE: When book already borrowed by same reader.
    result = requests.post("http://127.0.0.1:8000/v1/borrows", json={"reader_id": 1, "book_id": 1})
    assert result.ok

    result = requests.get("http://127.0.0.1:8000/v1/borrows")
    assert result.json() == GET_BORROWS
