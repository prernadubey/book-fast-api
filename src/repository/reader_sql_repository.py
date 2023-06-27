import typing as t
import logging
from ..domain.reader import Reader, ReaderPostResponse, ReaderGetResponse
from .. import db

log = logging.getLogger(__name__)


class ReaderSQLRepository:

    async def add_reader(self, reader: Reader) -> ReaderPostResponse:
        reader_id = (await db.connection.execute_insert(
            """
            INSERT INTO readers
                (name)
            VALUES (?)
            """,
            (reader.name,),
        ))[0]
        log.debug(f"Reader added {reader.name}")
        return ReaderPostResponse(reader_id=reader_id)

    async def get_readers(self) -> t.List[ReaderGetResponse]:
        async with db.connection.execute(
                """
                SELECT
                    id,
                    name
                FROM
                    readers
                """
        ) as cursor:
            rows = await cursor.fetchall()

        return [
            ReaderGetResponse(id=item[0], name=item[1],) for item in rows
        ]

    async def is_reader_exist(self, reader_id: int) -> t.Optional[bool]:
        async with db.connection.execute(
                """
                SELECT
                    *
                FROM
                    readers
                WHERE readers.id = ?
                """,
                (reader_id,)
        ) as cursor:
            row = await cursor.fetchone()
        if row:
            return True
        return None
