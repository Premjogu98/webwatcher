from dataclasses import dataclass
from main.logger import console_logger
from datetime import datetime
import mysql.connector.cursor as MySQL_cursor
import mysql.connector.connection as MySQL_connection
from main.env_handler import EnvHandler
from main.db_connection import DbConnection
from mysql.connector import Error
import time


@dataclass
class QueryHandler:
    connection: MySQL_connection = None
    cur: MySQL_cursor = None
    DATABASE_DETAILS = EnvHandler.DB_CONNECTION

    def connectAgain(self):
        db_connection = DbConnection(CONNECTION_DETAILS=self.DATABASE_DETAILS)
        connection = db_connection.connection
        cur = db_connection.cur
        return connection, cur

    def requestForData(self, limit: int, offset: int):

        # query = f"""
        #     SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy, data.LastCompareChangedOn,links.tender_link
        #     FROM dms_wpw_tenderlinks links
        #     INNER JOIN dms_wpw_tenderlinksdata data ON links.id = data.tlid
        #     INNER JOIN tbl_region re ON links.country = re.Country_Short_Code
        #     WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' AND data.entrydone = 'Y' AND (re.Region_Code LIKE '102%' OR re.Region_Code LIKE '104%' OR re.Region_Code LIKE '105%' OR re.Region_Code LIKE '103304%')
        #     ORDER BY links.id ASC LIMIT {limit} OFFSET {offset};"""

        # query = f"""
        #     SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy, data.LastCompareChangedOn,links.tender_link
        #     FROM dms_wpw_tenderlinks links
        #     INNER JOIN dms_wpw_tenderlinksdata data ON links.id = data.tlid
        #     INNER JOIN tbl_region re ON links.country = re.Country_Short_Code
        #     WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y' AND data.entrydone = 'Y' AND (re.Region_Code LIKE '101%' OR re.Region_Code LIKE '102%' OR re.Region_Code LIKE '104%' OR re.Region_Code LIKE '105%' OR re.Region_Code LIKE '103304%')
        #     ORDER BY links.id ASC LIMIT {limit} OFFSET {offset};"""

        # query = f"""
        #     SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy, data.LastCompareChangedOn,links.tender_link
        #     FROM dms_wpw_tenderlinks links
        #     INNER JOIN dms_wpw_tenderlinksdata data ON links.id = data.tlid
        #     INNER JOIN tbl_region re ON links.country = re.Country_Short_Code
        #     WHERE data.tlid= 38112;"""

        # query = f"""
        #         SELECT data.id, data.tlid, data.title, data.XPath, data.compare_per, data.CompareChangedOn, data.oldHtmlPath, data.newHtmlPath, data.oldImagePath, data.newImagePath, data.CompareBy, data.LastCompareChangedOn, links.tender_link
        #         FROM dms_wpw_tenderlinks links
        #         INNER JOIN dms_wpw_tenderlinksdata data ON links.id = data.tlid
        #         INNER JOIN tbl_region re ON links.country = re.Country_Short_Code
        #         WHERE links.process_type = 'Web Watcher' AND links.added_WPW = 'Y'
        #         ORDER BY links.id ASC LIMIT {limit} OFFSET {offset};"""

        # query = """
        #         SELECT COUNT(*) AS record_count
        #         FROM dms_wpw_tenderlinks tl
        #         INNER JOIN dms_wpw_tenderlinksdata td ON tl.id = td.tlid
        #         INNER JOIN tbl_region re ON tl.country = re.Country_Short_Code
        #         WHERE tl.process_type = 'Web Watcher' AND tl.added_WPW = 'Y'
        #         ORDER BY tl.id ASC
        #     """
        _, data = self.getQueryAndExecute(
            query="SELECT QUERY FROM `tend_dms`.`dms_wpw_query` LIMIT 1;", fetchone=True
        )
        query = f'{data["QUERY"].strip()} LIMIT {limit} OFFSET {offset};'
        _, data = self.getQueryAndExecute(query=query, fetchall=True)

        console_logger.debug(query)
        if not isinstance(data, list):

            return []

        return data

    def getQueryAndExecute(self, query, fetchone: bool = False, fetchall: bool = False):
        # console_logger.info(f"QUERY ==> {query}")
        connection, cursor = None, None
        for _ in range(3):
            try:
                if fetchone or fetchall:
                    connection, cursor = self.connectAgain()
                    console_logger.info(" ===== Connection created ===== ")
                    cursor.execute(query)
                    if fetchone:
                        data = cursor.fetchone()
                    elif fetchall:
                        data = cursor.fetchall()
                    console_logger.info(" ===== Connection started closing ===== ")
                    cursor.close()
                    connection.close()
                    # console_logger.info(" ===== Connection closed ===== ")
                    return True, data
                else:
                    console_logger.warning("Please select fetchone OR fetchall")
                    return False, {}
            except Error as e:
                if connection and cursor:
                    console_logger.info(" ===== Connection started closing ===== ")
                    cursor.close()
                    connection.close()
                    console_logger.info(" ===== Connection closed ===== ")
                if e.errno == 2013:  # Lost connection error
                    console_logger.error(
                        f"Lost connection: {e} reconnect in 5 sec AND max retry 3 times"
                    )
                    time.sleep(5)
                else:
                    raise Exception(e)

    def executeQuery(self, query):
        # console_logger.debug(f"QUERY ==> {query}")
        connection, cursor = None, None
        for _ in range(3):
            try:
                connection, cursor = self.connectAgain()
                console_logger.info(" ===== Connection created ===== ")
                cursor.execute(query)
                console_logger.info(" ===== Connection started closing ===== ")
                cursor.close()
                connection.close()
                console_logger.info(" ===== Connection closed ===== ")
                return None
            except Error as e:
                if connection and cursor:
                    console_logger.info(" ===== Connection started closing ===== ")
                    cursor.close()
                    connection.close()
                    console_logger.info(" ===== Connection closed ===== ")
                if e.errno == 2013:  # Lost connection error
                    console_logger.error(
                        f"Lost connection: {e} reconnect in 5 sec AND max retry 3 times"
                    )
                    time.sleep(5)
                else:
                    raise Exception(e)

    def insertQuery(self, query: str, value: tuple):
        # console_logger.debug(f"QUERY ==> {query}")
        # console_logger.debug(f"VALUE ==> {value}")
        connection, cursor = None, None
        for _ in range(3):
            try:
                connection, cursor = self.connectAgain()
                console_logger.info(" ===== Connection created ===== ")
                cursor.execute(query, value)
                console_logger.info(" ===== Connection started closing ===== ")
                cursor.close()
                connection.close()
                console_logger.info(" ===== Connection closed ===== ")
                return None
            except Error as e:
                if connection and cursor:
                    console_logger.info(" ===== Connection started closing ===== ")
                    cursor.close()
                    connection.close()
                    console_logger.info(" ===== Connection closed ===== ")
                if e.errno == 2013:  # Lost connection error
                    console_logger.error(
                        f"Lost connection: {e} reconnect in 5 sec AND max retry 3 times"
                    )
                    time.sleep(5)
                else:
                    raise Exception(e)

    def error_log(self, error, id):
        self.executeQuery(
            query=f"""UPDATE dms_wpw_tenderlinksdata SET compare_error ="{error.replace("'","")}", error_date="{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}" WHERE id = {id}"""
        )
