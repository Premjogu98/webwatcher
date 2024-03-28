from main.db_connection import DbConnection
from main.db_connection.condition_handler import ConditionHandler
from main.db_connection.query_handler import QueryHandler
from main.env_handler import EnvHandler
from main.sync_scraping import SyncScraping
from main.async_scraping import AsyncScraping

from main.selenium_scraping import SeleniumScraping
from main.global_variables import GlobalVariable

import os, random
from dataclasses import dataclass


@dataclass
class Main:
    DATABASE_DETAILS = EnvHandler.DB_CONNECTION
    DB_CONNECTION = DbConnection(CONNECTION_DETAILS=DATABASE_DETAILS)
    BATCH_SIZE = int(os.getenv("THREAD", 1))
    LIMIT = os.getenv("DB_DATA_LIMIT", 500)
    OFFSET = os.getenv("DB_DATA_OFFSET", 0)
    GROUP_ID = os.getenv("GROUP_ID")
    QUERY_HANDLER = QueryHandler(
        connection=DB_CONNECTION.connection, cur=DB_CONNECTION.cur
    )
    GLOBAL_VARIABLE = GlobalVariable()

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self):
        CONDITION_HANDLER = ConditionHandler(
            QUERY_HANDLER=self.QUERY_HANDLER, GLOBAL_VARIABLE=self.GLOBAL_VARIABLE
        )
        # SyncScraping(
        #     BATCH_SIZE=self.BATCH_SIZE,
        #     LIMIT=self.LIMIT,
        #     OFFSET=self.OFFSET,
        #     CONDITION_HANDLER=CONDITION_HANDLER,
        #     QUERY_HANDLER=self.QUERY_HANDLER,
        #     GLOBAL_VARIABLE=self.GLOBAL_VARIABLE,
        # )

        AsyncScraping(
            BATCH_SIZE=self.BATCH_SIZE,
            LIMIT=self.LIMIT,
            OFFSET=self.OFFSET,
            CONDITION_HANDLER=CONDITION_HANDLER,
            QUERY_HANDLER=self.QUERY_HANDLER,
            GLOBAL_VARIABLE=self.GLOBAL_VARIABLE,
            GROUP_ID=self.GROUP_ID,
        )

        # SeleniumScraping(
        #     BATCH_SIZE=self.BATCH_SIZE,
        #     LIMIT=self.LIMIT,
        #     OFFSET=self.OFFSET,
        #     CONDITION_HANDLER=CONDITION_HANDLER,
        #     QUERY_HANDLER=self.QUERY_HANDLER,
        #     GLOBAL_VARIABLE=self.GLOBAL_VARIABLE,
        #     GROUP_ID=self.GROUP_ID,
        # )
