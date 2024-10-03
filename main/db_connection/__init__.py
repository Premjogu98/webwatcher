from dataclasses import dataclass
import mysql.connector
import mysql.connector.cursor as MySQL_cursor
import mysql.connector.connection as MySQL_connection
from main.logger import console_logger


@dataclass
class DbConnection:
    CONNECTION_DETAILS: dict
    connection: MySQL_connection = None
    cur: MySQL_cursor = None

    def __post_init__(self):
        self.connection = mysql.connector.connect(
            host=self.CONNECTION_DETAILS["DB_HOST"],
            user=self.CONNECTION_DETAILS["DB_USERNAME"],
            password=self.CONNECTION_DETAILS["DB_PASSWORD"],
            database=self.CONNECTION_DETAILS["DB_NAME"],
        )
        self.cur = self.connection.cursor(dictionary=True)
