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


def generate_html_response(url):
    result, status = scraping.get_html(url)
    return HTMLResponse(content=result, status_code=status)


@router.get("/get/html", response_class=HTMLResponse)
async def test(url: str):
    return generate_html_response(url)


@router.get("/get/data",)
async def test():
    data = fetchDataCompleteData()
    return {"detail": data}
