import logging

from fastapi import APIRouter, Depends
from .repository.author_sql_repository import AuthorSQLRepository
from .domain.author import Author

from .dependencies import get_author_repository


log = logging.getLogger(__name__)
router = APIRouter()


@router.post("/v1/authors")
async def add_author(author: Author, author_repo: AuthorSQLRepository = Depends(get_author_repository)):
    return await author_repo.add_author(author)


@router.get("/v1/authors")
async def get_authors(author_repo: AuthorSQLRepository = Depends(get_author_repository)):
    res = await author_repo.get_authors()
    return {"authors": res}


