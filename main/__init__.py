from dataclasses import dataclass
from main.db_connection import DbConnection
from main.db_connection.condition_handler import ConditionHandler
from main.db_connection.query_handler import QueryHandler
from main.env_handler import EnvHandler
from main.scraping import Scraping
from main.global_variables import GlobalVariable
import os


@dataclass
class Main:
    DATABASE_DETAILS = EnvHandler.DB_CONNECTION
    DB_CONNECTION = DbConnection(CONNECTION_DETAILS=DATABASE_DETAILS)
    BATCH_SIZE = int(os.getenv("THREAD", 3))
    LIMIT = os.getenv("DB_DATA_LIMIT", 100)
    OFFSET = os.getenv("DB_DATA_OFFSET", 0)
    QUERY_HANDLER = QueryHandler(
        connection=DB_CONNECTION.connection, cur=DB_CONNECTION.cur
    )
    GLOBAL_VARIABLE = GlobalVariable()

    def __𝐩𝐨𝐬𝐭_ini𝐭__ (self):
        CONDITION_HANDLER = ConditionHandler(
            QUERY_HANDLER=self.QUERY_HANDLER, GLOBAL_VARIABLE=self.GLOBAL_VARIABLE
        )
        Scraping(
            BATCH_SIZE=self.BATCH_SIZE,
            LIMIT=self.LIMIT,
            OFFSET=self.OFFSET,
            CONDITION_HANDLER=CONDITION_HANDLER,
            QUERY_HANDLER=self.QUERY_HANDLER,
            GLOBAL_VARIABLE=self.GLOBAL_VARIABLE,
        )
