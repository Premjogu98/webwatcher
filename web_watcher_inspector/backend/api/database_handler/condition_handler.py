from dataclasses import dataclass
from api.database_handler.query_handler import queryHandler
from api.logger import console_logger
import sys
from fastapi import Depends, HTTPException

def getTotalDataCount():
    _, data = queryHandler.getQueryAndExecute("SELECT COUNT(data.id) AS count FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y';",fetchone=True)
    return data

def fetchDataCompleteData(offset:int,limit:int):
    try:
        _status, data = queryHandler.getQueryAndExecute(
            # query=f"""SET @row_number = 0; SELECT (@row_number:=@row_number + 1) AS sr_no, data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath,data.LastCompareChangedOn,links.tender_link FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' ORDER BY data.id LIMIT {limit} OFFSET {offset};""",
            query=f"""SELECT data.id, data.tlid, data.title, links.tender_link,data.CompareChangedOn,data.LastCompareChangedOn FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' ORDER BY data.id LIMIT {limit} OFFSET {offset};""",
            fetchall=True,
        )
        if _status:
            headers = [{"Header":keys.title(), "accessor":keys} for keys in list(data[0].keys())]
            data_count = getTotalDataCount()
            complete_details = {"headers":headers,"data": data}
            complete_details.update(data_count)
            return complete_details
    except Exception as e:
        console_logger.error('ERROR: {} Error on line {}'.format(e,sys.exc_info()[-1].tb_lineno))
        raise HTTPException(status_code=500, detail=str(e))

def getDataFromID(id):
    try:
        status, data = queryHandler.getQueryAndExecute(
                query=f"""SELECT data.ID,data.tlid,data.Title,data.XPath,data.oldHtmlPath,data.newHtmlPath,data.compare_per,data.CompareBy,data.entrydone,data.changes_count,data.entry_lockby,data.CompareChangedOn,data.LastCompareChangedOn,data.EntryDate,data.UpdatedOn,links.tender_link AS Url FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id  WHERE links.id="{id}";""",
                fetchone=True,
            )
        if status:
            return data
    except Exception as e:
        console_logger.error('ERROR: {} Error on line {}'.format(e,sys.exc_info()[-1].tb_lineno))
        raise HTTPException(status_code=500, detail=str(e))

def updateXpath(xpath,tlid):
    try:
        status, data = queryHandler.getQueryAndExecute(
                query=f"""UPDATE `dms_wpw_tenderlinksdata` SET XPath = "{xpath}" WHERE tlid = "{tlid}";""",
                fetchone=True,
            )
        if status:
            return "success"
    except Exception as e:
        console_logger.error('ERROR: {} Error on line {}'.format(e,sys.exc_info()[-1].tb_lineno))
        raise HTTPException(status_code=500, detail=str(e))