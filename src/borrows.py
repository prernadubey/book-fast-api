import logging

from fastapi import APIRouter, Depends, HTTPException

from .domain.borrow import Borrow
from .repository.borrow_sql_repository import BorrowSQLRepository
from .repository.reader_sql_repository import ReaderSQLRepository
from .repository.book_sql_repository import BooksSQLRepository

from .dependencies import get_borrow_repository, get_reader_repository, get_book_repository

log = logging.getLogger(__name__)
router = APIRouter()


@router.post("/v1/borrows")
async def add_borrow(borrow: Borrow, borrow_repo: BorrowSQLRepository = Depends(get_borrow_repository),
                     reader_repo: ReaderSQLRepository = Depends(get_reader_repository),
                     book_repo: BooksSQLRepository = Depends(get_book_repository)):
    is_reader_exist = await reader_repo.is_reader_exist(borrow.reader_id)
    is_book_exist = await book_repo.is_book_exist(borrow.book_id)

    if is_book_exist and is_reader_exist:
        book_borrowed = await borrow_repo.book_borrowed(borrow.book_id)
        if book_borrowed:
            if book_borrowed.reader_id != borrow.reader_id:
                raise HTTPException(status_code=403, detail="Requested book is already borrowed. "
                                                            "Please try with other book.")
            else:
                log.debug("Book is already borrowed by same reader.")
                return
        else:
            return await borrow_repo.add_borrow(borrow)

    raise HTTPException(status_code=404, detail="Requested reader or book does not exist. Please check the data.")


@router.delete("/v1/borrows/{book_id}")
async def del_borrow(book_id: int, borrow_repo: BorrowSQLRepository = Depends(get_borrow_repository)):
    return await borrow_repo.delete_borrow(book_id)


@router.get("/v1/borrows")
async def get_borrows(borrow_repo: BorrowSQLRepository = Depends(get_borrow_repository)):
    res = await borrow_repo.get_borrows()
    return {"borrows": res}

