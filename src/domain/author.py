from pydantic import BaseModel


class Author(BaseModel):
    name: str


class AuthorPostResponse(BaseModel):
    author_id: int


class AuthorGetResponse(BaseModel):
    name: str
    id: int
