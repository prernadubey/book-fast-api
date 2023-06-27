import logging

from fastapi import APIRouter, Depends
from .repository.book_sql_repository import BooksSQLRepository
from .domain.book import Book

from .dependencies import get_book_repository

log = logging.getLogger(__name__)
router = APIRouter()


@router.post("/v1/books")
async def add_book(book: Book, book_repo: BooksSQLRepository = Depends(get_book_repository)):
    return await book_repo.add_book(book)


@router.get("/v1/books")
async def get_books(book_repo: BooksSQLRepository = Depends(get_book_repository)):
    res = await book_repo.get_books()
    return {"books": res}
