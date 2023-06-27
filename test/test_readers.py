import requests

GET_READERS = {
    "readers": [
        {
            "name": "test_reader1",
            "id": 1
        },
        {
            "name": "test_reader2",
            "id": 2
        },
        {
            "name": "test_reader3",
            "id": 3
        }
    ]
}


def test_add_readers(app):
    result = requests.post("http://127.0.0.1:8000/v1/readers", json={"name": "test_reader1"})
    assert result.ok

    result = requests.post("http://127.0.0.1:8000/v1/readers", json={"name": "test_reader2"})
    assert result.json() == {"reader_id": 2}

    result = requests.post("127.0.0.1:8000/v1/readers", json={"name": "test_reader3"})
    assert result.json() == {"reader_id": 3}

    result = requests.get("http://127.0.0.1:8000/v1/readers")
    assert result.json() == GET_READERS
