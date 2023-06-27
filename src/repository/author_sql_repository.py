import typing as t
import logging
from ..domain.author import Author, AuthorGetResponse, AuthorPostResponse
from .. import db

log = logging.getLogger(__name__)


class AuthorSQLRepository:

    async def add_author(self, author: Author) -> AuthorPostResponse:
        author_id = (await db.connection.execute_insert(
            """
            INSERT INTO authors (name) VALUES (?)
            """,
            (author.name,),
        ))[0]
        log.debug(f"Author added {author.name}")

        return AuthorPostResponse(author_id=author_id)

    async def get_authors(self) -> t.List[AuthorGetResponse]:
        async with db.connection.execute(
                """
                SELECT
                    id, name
                FROM
                    authors
                ORDER BY id ASC
                """
        ) as cursor:
            rows = await cursor.fetchall()

        return [
            AuthorGetResponse(id=item[0], name=item[1],) for item in rows
        ]

    async def get_author(self, author_id: int) -> t.Optional[AuthorGetResponse]:
        async with db.connection.execute(
                """
                SELECT
                    id, name
                FROM
                    authors
                WHERE authors.id = ?
                """,
                (author_id,),
        ) as cursor:
            row = await cursor.one_or_none()

        if row:
            return AuthorGetResponse(id=row[0], name=row[1], )
        return None
