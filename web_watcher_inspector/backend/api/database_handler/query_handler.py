from dataclasses import dataclass
from api.logger import console_logger
import mysql.connector.cursor as MySQL_cursor
import mysql.connector.connection as MySQL_connection
from api.globvar import globVar


@dataclass
class QueryHandler:
    connection: MySQL_connection = None
    cursor: MySQL_cursor = None

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self):
        self.connection, self.cursor = globVar.connectDB()

    def getQueryAndExecute(self, query, fetchone: bool = False, fetchall: bool = False):
        # console_logger.info(f"QUERY ==> {query}")
        if fetchone or fetchall:
            self.cursor.execute(query)
            if fetchone:
                return True, self.cursor.fetchone()
            elif fetchall:
                return True, self.cursor.fetchall()
        else:
            console_logger.warning("Please select fetchone OR fetchall")
            return False, {}

    def executeQuery(self, query):
        # console_logger.debug(f"QUERY ==> {query}")
        self.cursor.execute(query)

    def insertQuery(self, query: str, value: tuple):
        # console_logger.debug(f"QUERY ==> {query}")
        # console_logger.debug(f"VALUE ==> {value}")
        self.cursor.execute(query, value)


queryHandler = QueryHandler()
