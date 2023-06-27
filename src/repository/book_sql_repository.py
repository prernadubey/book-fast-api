import typing as t
import logging
from .. domain.book import Book, BookPostResponse, BookGetResponse
from .. import db
log = logging.getLogger(__name__)


class BooksSQLRepository:

    async def add_book(self, book: Book) -> BookPostResponse:

        book_id = (await db.connection.execute_insert(
            """
            INSERT INTO books
                (author_id, title)
            VALUES (?, ?)
            """,
            (book.author_id, book.title),
        ))[0]

        log.debug(f"Book added {book.title}")

        return BookPostResponse(book_id=book_id)

    async def get_books(self) -> t.List[BookGetResponse]:
        async with db.connection.execute(
                """
                SELECT
                    books.id,
                    books.title,
                    authors.name
                FROM
                    books
                JOIN
                    authors ON authors.id = books.author_id
                """
        ) as cursor:
            rows = await cursor.fetchall()
        return [
            BookGetResponse(id=item[0], title=item[1], author_name=item[2],)
            for item in rows
        ]

    async def is_book_exist(self, book_id: int) -> t.Optional[bool]:
        async with db.connection.execute(
                """
                SELECT
                    *
                FROM
                    books
                WHERE
                    books.id = ?
                """,
                (book_id,),
        ) as cursor:
            row = await cursor.fetchone()
        if row:
            return True
        return None
