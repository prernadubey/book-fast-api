from pydantic import BaseModel
from datetime import date


class Borrow(BaseModel):
    reader_id: int
    book_id: int


class BorrowGetResponse(BaseModel):
    reader: str
    title: str
    author: str
    borrow_time: date
