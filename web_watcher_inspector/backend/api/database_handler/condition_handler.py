from dataclasses import dataclass
from api.database_handler.query_handler import queryHandler
from api.logger import console_logger


    
def fetchDataCompleteData(headers=False):
    _status, data = queryHandler.getQueryAndExecute(
        query=f"""SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy, data.LastCompareChangedOn,links.tender_link FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' ORDER BY data.id LIMIT 100 OFFSET 0;""",
        fetchall=True,
    )
    # console_logger.debug(data)
    if _status:
        # if headers:
        #     data[0].keys()
        headers = list(data[0].keys())
        return {"headers":headers,"data": data}

    