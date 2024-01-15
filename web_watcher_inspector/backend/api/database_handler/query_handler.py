from dataclasses import dataclass
from api.logger import console_logger
import mysql.connector.cursor as MySQL_cursor
import mysql.connector.connection as MySQL_connection
from api.globvar import globVar
from fastapi import Depends, HTTPException
import sys

@dataclass
class QueryHandler:
    connection: MySQL_connection = None
    cursor: MySQL_cursor = None

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self):
        self.reconnect()
    def reconnect(self):
        self.connection, self.cursor = globVar.connectDB()
        console_logger.debug(f"connection OBJ : {self.connection} | cursor OBJ : {self.cursor}")
        
    def getQueryAndExecute(self, query, fetchone: bool = False, fetchall: bool = False):
        try:
            console_logger.info(f"QUERY ==> {query}")
            if fetchone or fetchall:
                self.cursor.execute(query)
                if fetchone:
                    return True, self.cursor.fetchone()
                elif fetchall:
                    return True, self.cursor.fetchall()
            else:
                console_logger.warning("Please select fetchone OR fetchall")
                return False, {}
        except Exception as e:
            if "Lost connection" in str(e):
                console_logger.debug("Reconnecting Connenction")
                self.reconnect()
                self.getQueryAndExecute(query =query,fetchone=fetchone,fetchall=fetchall)
            else:
                console_logger.error('ERROR: {} Error on line {}'.format(e,sys.exc_info()[-1].tb_lineno))
                raise HTTPException(status_code=404,detail="Data Not found")

    def executeQuery(self, query):
        # console_logger.debug(f"QUERY ==> {query}")
        self.cursor.execute(query)

    def insertQuery(self, query: str, value: tuple):
        console_logger.debug(f"QUERY ==> {query}")
        console_logger.debug(f"VALUE ==> {value}")
        self.cursor.execute(query, value)


queryHandler = QueryHandler()
