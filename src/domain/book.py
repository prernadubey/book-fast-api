from pydantic import BaseModel


class Book(BaseModel):
    author_id: int
    title: str


class BookPostResponse(BaseModel):
    book_id: int


class BookGetResponse(BaseModel):
    author_name: str
    title: str
    id: int
