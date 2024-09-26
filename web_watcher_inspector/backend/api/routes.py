from fastapi import APIRouter
import asyncio
from fastapi.responses import HTMLResponse
from api.scraping import Scraping
from api.container_handler import containerHandler
from api.logger import console_logger
from api.database_handler.condition_handler import *

router = APIRouter()
scraping = Scraping()
from api.serializers import *


@router.get("/test")
async def test(url: str):
    return {"detail": url}


@router.get("/get/html", response_class=HTMLResponse)
async def endpoint_to_get_html_data(url: str = None, id: int = None):
    result, status = await scraping.get_html(url, id)
    return HTMLResponse(content=result, status_code=status)


@router.get(
    "/get/data",
)
async def endpoint_to_get_pagination_data(
    offset: int, limit: int, tenderlink=None, tenderid=None, wpwflag=None
):
    data = fetchDataCompleteData(offset, limit, tenderlink, tenderid, wpwflag)
    return {"detail": data}


@router.get(
    "/addition/data",
)
async def endpoint_to_get_addition_data(id: int):
    data = getDataFromID(id)
    return {"detail": data}


@router.patch(
    "/update/xpath",
)
async def endpoint_to_update_xpath(payload: UpdateXpath):
    data = updateXpath(payload.xpath, payload.tlid)
    return {"detail": data}


@router.get("/compared/html", response_class=HTMLResponse)
async def endpoint_to_get_addition_data(id: int, old: bool = False):
    result, status = scraping.get_compared_html(id, old)
    return HTMLResponse(content=result, status_code=status)


@router.get("/containers")
async def endpoint_to_get_addition_data():

    return {"detail": containerHandler.get_container_names()}
