from dataclasses import dataclass
from api.database_handler.query_handler import queryHandler
from api.logger import console_logger
import sys
from fastapi import Depends, HTTPException

def getTotalDataCount():
    _, data = queryHandler.getQueryAndExecute("SELECT COUNT(data.id) AS count FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y';",fetchone=True)
    return data

def getTotalTenderlinksCount():
    try:
        status, data = queryHandler.getQueryAndExecute(
                query=f"""SELECT COUNT(id) AS count FROM dms_wpw_tenderlinks WHERE process_type = 'Web Watcher'""",
                fetchone=True,
            )
        if status:
            return data
    except Exception as e:
        console_logger.error('ERROR: {} Error on line {}'.format(e,sys.exc_info()[-1].tb_lineno))
        raise HTTPException(status_code=500, detail=str(e))

def fetchDataCompleteData(offset:int,limit:int,tenderlink=None):
    try:
        if tenderlink != "null":
            _status, data = queryHandler.getQueryAndExecute(query= f"""
                SELECT wpwlink.id,wpwtender.tlid, wpwlink.tender_link, wpwlink.added_WPW, wpwtender.compare_error, wpwlink.added_on 
                FROM dms_wpw_tenderlinks AS wpwlink 
                LEFT JOIN dms_wpw_tenderlinksdata AS wpwtender ON wpwlink.tender_link = wpwtender.Url 
                WHERE wpwlink.tender_link = '{tenderlink}' 
                GROUP BY wpwlink.tender_link; 
            """,
            fetchall=True
            )
        else:
            _status, data = queryHandler.getQueryAndExecute(
                # query=f"""SET @row_number = 0; SELECT (@row_number:=@row_number + 1) AS sr_no, data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath,data.LastCompareChangedOn,links.tender_link FROM dms_wpw_tenderlinksdata AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' ORDER BY data.id LIMIT {limit} OFFSET {offset};""",
                query=f"""
                    SELECT wpwlink.id,wpwtender.tlid, wpwlink.tender_link, wpwlink.added_WPW, wpwtender.compare_error, wpwlink.added_on 
                    FROM dms_wpw_tenderlinks AS wpwlink 
                    LEFT JOIN dms_wpw_tenderlinksdata AS wpwtender ON wpwlink.tender_link = wpwtender.Url 
                    WHERE wpwlink.process_type = 'Web Watcher' 
                    GROUP BY wpwlink.id 
                    ORDER BY wpwlink.id 
                    LIMIT {limit} OFFSET {offset};
                """,
                fetchall=True,
            )
        if _status:
            headers = [{"Header":keys.title(), "accessor":keys} for keys in list(data[0].keys())]
            if tenderlink == "null":
                data_count = getTotalTenderlinksCount()
            else:
                data_count = {"count":len(data)}
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
    
def getLinkFromID(id):
    try:
        status, data = queryHandler.getQueryAndExecute(
                query=f"""SELECT tender_link AS url FROM dms_wpw_tenderlinks WHERE id = '{id}';""",
                fetchone=True,
            )
        if status:
            return data['url']
    except Exception as e:
        console_logger.error('ERROR: {} Error on line {}'.format(e,sys.exc_info()[-1].tb_lineno))
        raise HTTPException(status_code=500, detail=str(e))
    
def conditionONE(xpath,url):
    try:
        console_logger.info("CONDITION 1 ......")
        _, data = queryHandler.getQueryAndExecute(
                query=f"""SELECT CASE
                        WHEN EXISTS (
                            SELECT 1
                            FROM dms_wpw_tenderlinksdata
                            WHERE Url = '{url}'
                            )
                        THEN 'True'
                        ELSE 'False'
                    END AS found;
                """,
                fetchone=True,
            )
        found = eval(data["found"])
        if found:
            _, data = queryHandler.getQueryAndExecute(
                    query=f"""UPDATE `dms_wpw_tenderlinksdata` SET XPath = "{xpath}", entrydone="Y" WHERE Url = "{url}";""",
                    fetchone=True,
                )
        return found
        
    except Exception as e:
        console_logger.error('ERROR: {} Error on line {}'.format(e,sys.exc_info()[-1].tb_lineno))
        raise HTTPException(status_code=500, detail=str(e))
    
def tendersLinksTableData(url):
    _, data = queryHandler.getQueryAndExecute(
                query=f"""SELECT * FROM dms_wpw_tenderlinks WHERE tender_link = '{url}';""",
                fetchone=True,
            )
    if _:
        return data
    
def conditionTWO(xpath,url):
    try:
        console_logger.info("CONDITION 2 ......")
        #=================================================================================

        console_logger.debug("Fetching Data From Tenderslinks Table")
        tenderUrlData = tendersLinksTableData(url)

        #=================================================================================

        console_logger.debug("Inserting New Entry To Table")
        query = f"INSERT INTO dms_wpw_tenderlinksdata (tlid,Url,XPath,entrydone,CompareBy) VALUES (%s,%s,%s,%s,%s)"
        value = (
            tenderUrlData["id"],
            url,
            xpath,
            "Y",
            "Text"
        )
        queryHandler.insertQuery(query, value)

        #=================================================================================

        console_logger.debug("Updating dms_wpw_tenderlinks added_WPW Flag to 'Y' ")
        queryHandler.executeQuery(query=f"""UPDATE `dms_wpw_tenderlinks` SET added_WPW = "Y" WHERE tender_link = "{url}";""",)

        #=================================================================================
        return "New Entry Added to table and added_WPW Flaged `Y`"
    except Exception as e:
        console_logger.error('ERROR: {} Error on line {}'.format(e,sys.exc_info()[-1].tb_lineno))
        raise HTTPException(status_code=500, detail=str(e))
    
def updateXpath(xpath,tlid):
    url = getLinkFromID(tlid)
    console_logger.debug(f"XPATH: {xpath} | tlid: {tlid} | Url: {url}")
    
    status = conditionONE(xpath,url)
    if not status:
        return conditionTWO(xpath,url)
    return "success"


