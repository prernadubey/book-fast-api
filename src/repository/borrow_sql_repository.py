import typing as t
import logging
from ..domain.borrow import Borrow, BorrowGetResponse
from .. import db

log = logging.getLogger(__name__)


class BorrowSQLRepository:

    async def add_borrow(self, borrow: Borrow):
        await db.connection.execute(
            """
            INSERT INTO borrows
                (reader_id, book_id, borrow_time, return_time)
            VALUES
                (?, ?, DATE('now'), NULL)
            """,
            (borrow.reader_id, borrow.book_id),
        )
        log.debug(f"New borrow from reader id {borrow.reader_id}")
        return

    async def delete_borrow(self, book_id: int):
        await db.connection.execute(
            """
            UPDATE
                borrows
            SET
                return_time = DATE('now')
            WHERE
                book_id = ?
                AND return_time IS NULL;
            """,
            (book_id,),
        )
        log.debug(f"Book {book_id} returned.")
        return

    async def get_borrows(self) -> t.List[BorrowGetResponse]:
        async with db.connection.execute(
                """
                SELECT
                    readers.name,
                    books.title,
                    authors.name,
                    borrows.borrow_time
                FROM
                    borrows
                LEFT JOIN
                    books ON books.id = borrows.book_id
                LEFT JOIN
                    authors ON authors.id = books.author_id
                LEFT JOIN
                    readers ON readers.id = borrows.reader_id
                WHERE
                    borrows.return_time IS NULL
                """
        ) as cursor:
            rows = await cursor.fetchall()

        return [BorrowGetResponse(reader=item[0], title=item[1], author=item[2],
                                  borrow_time=item[3]) for item in rows]

    async def book_borrowed(self, book_id: int) -> t.Optional[Borrow]:
        async with db.connection.execute(
                """
                SELECT
                    borrows.book_id,
                    borrows.reader_id
                FROM
                    borrows
                WHERE
                    borrows.book_id = ? 
                AND 
                    borrows.return_time IS NULL
                """,
                (book_id,),
        ) as cursor:
            row = await cursor.fetchone()
        if row:
            return Borrow(book_id=row[0], reader_id=row[1])
        return None
