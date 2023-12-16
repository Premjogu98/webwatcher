from dataclasses import dataclass
from dotenv import load_dotenv
from pathlib import Path
import os
import mysql.connector
from api.logger import console_logger

dotenv_path = Path(os.path.join(os.getcwd(),'.env'))
load_dotenv(dotenv_path=dotenv_path)

@dataclass
class GlobVar:

    MARK = "ww".upper()
    DB_HOST = os.getenv(f"{MARK}_DB_IP")
    DB_USERNAME = os.getenv(f"{MARK}_DB_USERNAME")
    DB_PASSWORD = os.getenv(f"{MARK}_DB_PASSWORD")
    DB_NAME = os.getenv(f"{MARK}_DB_NAME")
    CONNECTION_DETAILS = None
    
    def __𝐩𝐨𝐬𝐭_ini𝐭__ (self):
        self.CONNECTION_DETAILS = {
            "DB_HOST" : self.DB_HOST,
            "DB_USERNAME" : self.DB_USERNAME,
            "DB_PASSWORD" : self.DB_PASSWORD,
            "DB_NAME" : self.DB_NAME,
        }


    def connectDB(self):
        console_logger.info("=========== CONNECTING DATABASE ===========")
        CONNECTION = mysql.connector.connect(
            host=self.CONNECTION_DETAILS["DB_HOST"],
            user=self.CONNECTION_DETAILS["DB_USERNAME"],
            password=self.CONNECTION_DETAILS["DB_PASSWORD"],
            database=self.CONNECTION_DETAILS["DB_NAME"],
        )
        CURSOR = CONNECTION.cursor(dictionary=True)
        console_logger.info("=========== CONNECTED ===========")
        return (CONNECTION,CURSOR)

globVar = GlobVar()