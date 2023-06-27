from pydantic import BaseModel


class Reader(BaseModel):
    name: str


class ReaderPostResponse(BaseModel):
    reader_id: int


class ReaderGetResponse(BaseModel):
    name: str
    id: int
