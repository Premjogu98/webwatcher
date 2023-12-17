from dataclasses import dataclass
from api.database_handler.query_handler import queryHandler
from api.logger import console_logger



def getTotalDataCount():
    _, data = queryHandler.getQueryAndExecute("SELECT COUNT(*) as count FROM dms_wpw_tenderlinksdata",fetchone=True)
    return data

def fetchDataCompleteData(offset:int,limit:int):
    _status, data = queryHandler.getQueryAndExecute(
        query=f"""SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath,data.LastCompareChangedOn,links.tender_link FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' ORDER BY data.id LIMIT {limit} OFFSET {offset};""",
        fetchall=True,
    )
    # console_logger.debug(data)
    if _status:
        headers = [{"Header":keys.title(), "accessor":keys} for keys in list(data[0].keys())]
        data_count = getTotalDataCount()
        complete_details = {"headers":headers,"data": data}
        complete_details.update(data_count)
        return complete_details

    