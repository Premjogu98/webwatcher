from dataclasses import dataclass
from main.logger import console_logger
from datetime import datetime
import mysql.connector
from main.env_handler import EnvHandler
from main.db_connection import DbConnection
import time
from typing import Any, Dict, List, Tuple, Optional


@dataclass
class QueryHandler:
    DATABASE_DETAILS = EnvHandler.DB_CONNECTION

    def connectAgain(
        self,
    ) -> Tuple[
        mysql.connector.connection.MySQLConnection, mysql.connector.cursor.MySQLCursor
    ]:
        db_connection = DbConnection(CONNECTION_DETAILS=self.DATABASE_DETAILS)
        return db_connection.connection, db_connection.cur

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
        _, query_data = self.getQueryAndExecute(
            query="SELECT QUERY FROM `tend_dms`.`dms_wpw_query` LIMIT 1;", fetchone=True
        )
        query = f'{query_data["QUERY"].strip()} LIMIT {limit} OFFSET {offset};'
        _, data = self.getQueryAndExecute(query=query, fetchall=True)

        console_logger.debug(query)
        return data if isinstance(data, list) else []

    def getQueryAndExecute(
        self, query: str, fetchone: bool = False, fetchall: bool = False
    ) -> Tuple[bool, Any]:
        for _ in range(3):
            try:
                if not (fetchone or fetchall):
                    console_logger.warning("Please select fetchone OR fetchall")
                    return False, {}

                connection, cursor = self.connectAgain()
                console_logger.info(" ===== Connection created ===== ")
                cursor.execute(query)
                data = (
                    cursor.fetchone()
                    if fetchone
                    else cursor.fetchall() if fetchall else None
                )
                self._close_connection(cursor, connection)
                return True, data
            except mysql.connector.Error as e:
                self._handle_error(e)

    def executeQuery(self, query: str, params: Tuple[Any, ...] = None) -> None:
        self._execute_with_retry(query, params)

    def insertQuery(self, query: str, value: tuple) -> None:
        self._execute_with_retry(query, value)

    def error_log(self, error: str, id: int) -> None:
        query = f"""UPDATE dms_wpw_tenderlinksdata SET compare_error = %s, error_date = %s WHERE id = %s"""
        self.executeQuery(
            query,
            (error.replace("'", ""), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), id),
        )

    def _execute_with_retry(self, query: str, value: Optional[tuple] = None) -> None:
        for _ in range(3):
            try:
                connection, cursor = self.connectAgain()
                console_logger.info(" ===== Connection created ===== ")
                cursor.execute(query, value) if value else cursor.execute(query)
                self._close_connection(cursor, connection)
                return
            except mysql.connector.Error as e:
                self._handle_error(e)

    @staticmethod
    def _close_connection(
        cursor: mysql.connector.cursor.MySQLCursor,
        connection: mysql.connector.connection.MySQLConnection,
    ) -> None:
        console_logger.info(" ===== Connection started closing ===== ")
        cursor.close()
        connection.close()
        console_logger.info(" ===== Connection closed ===== ")

    @staticmethod
    def _handle_error(e: mysql.connector.Error) -> None:
        if e.errno == 2013:  # Lost connection error
            console_logger.error(
                f"Lost connection: {e} reconnect in 5 sec AND max retry 3 times"
            )
            time.sleep(5)
        else:
            raise Exception(e)
