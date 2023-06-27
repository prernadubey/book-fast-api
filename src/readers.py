import logging

from fastapi import APIRouter, Depends

from .repository.reader_sql_repository import ReaderSQLRepository
from .domain.reader import Reader
from .dependencies import get_reader_repository


log = logging.getLogger(__name__)
router = APIRouter()


@router.post("/v1/readers")
async def add_reader(reader: Reader, reader_repo: ReaderSQLRepository = Depends(get_reader_repository)):
    return await reader_repo.add_reader(reader)


@router.get("/v1/readers")
async def get_readers(reader_repo: ReaderSQLRepository = Depends(get_reader_repository)):
    res = await reader_repo.get_readers()
    return {"readers": res}
