from dataclasses import dataclass
from main.logger import console_logger
from datetime import datetime
import mysql.connector.cursor as MySQL_cursor
import mysql.connector.connection as MySQL_connection

@dataclass
class QueryHandler:
    connection: MySQL_connection
    cur: MySQL_cursor

    def requestForData(self, limit: int, offset: int):
        query = f"""SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.compare_changed_on, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.compare_by, data.last_compare_changed_on,links.tender_link FROM dms_wpw_tenderlinksdata_test AS data JOIN dms_wpw_tenderlinks AS links ON data.tlid = links.id WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' ORDER BY data.id LIMIT {limit} OFFSET {offset};"""
        _, data = self.getQueryAndExecute(query=query, fetchall=True)
        if not isinstance(data, list):
            return []
        return data

    def getQueryAndExecute(self, query, fetchone: bool = False, fetchall: bool = False):
        console_logger.info(f"QUERY ==> {query}")
        if fetchone or fetchall:
            self.cur.execute(query)
            if fetchone:
                return True, self.cur.fetchone()
            elif fetchall:
                return True, self.cur.fetchall()
        else:
            console_logger.warning("Please select fetchone OR fetchall")
            return False, {}

    def executeQuery(self, query):
        console_logger.debug(f"QUERY ==> {query}")
        self.cur.execute(query)

    def error_log(self, error, id):
        self.executeQuery(
            query=f"""UPDATE dms_wpw_tenderlinksdata_test SET compare_error ="{error.replace("'","")}", error_date="{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}" WHERE id = {id}"""
        )
