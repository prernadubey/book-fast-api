from .repository.book_sql_repository import BooksSQLRepository
from .repository.author_sql_repository import AuthorSQLRepository
from .repository.reader_sql_repository import ReaderSQLRepository
from .repository.borrow_sql_repository import BorrowSQLRepository


async def get_book_repository():
    return BooksSQLRepository()


async def get_author_repository():
    yield AuthorSQLRepository()


async def get_reader_repository():
    return ReaderSQLRepository()


async def get_borrow_repository():
    return BorrowSQLRepository()
