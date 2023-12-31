from fastapi import APIRouter
import asyncio
from fastapi.responses import HTMLResponse
from api.scraping import Scraping
from api.logger import console_logger
from api.database_handler.condition_handler import (fetchDataCompleteData)
router = APIRouter()
scraping = Scraping()


@router.get("/test")
async def test(url: str):
    return {"detail": url}

@router.get("/get/html", response_class=HTMLResponse)
async def test(url: str=None,id:int=None):
    result, status = scraping.get_html(url,id)
    return HTMLResponse(content=result, status_code=status)


@router.get("/get/data",)
async def test(offset:int,limit:int):
    data = fetchDataCompleteData(offset,limit)
    return {"detail": data}
