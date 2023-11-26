from dataclasses import dataclass
import mysql.connector
from main.logger import console_logger


@dataclass
class DbConnection:
    CONNECTION_DETAILS: dict
    connection = None
    cur = None

    def __post_init__(self):
        console_logger.debug(self.CONNECTION_DETAILS)
        self.connection = mysql.connector.connect(
            host=self.CONNECTION_DETAILS["DB_HOST"],
            user=self.CONNECTION_DETAILS["DB_USERNAME"],
            password=self.CONNECTION_DETAILS["DB_PASSWORD"],
            database=self.CONNECTION_DETAILS["DB_NAME"],
        )
        self.cur = self.connection.cursor(dictionary=True)
        console_logger.info("===== DATABASE CONNECTED SUCCESSFULLY =====")

    
