from dataclasses import dataclass
from main.db_connection.query_handler import QueryHandler
from main.global_variables import GlobalVariable
import os

@dataclass
class LogHandler:
    QUERY_HANDLER: QueryHandler
    GLOBAL_VARIABLE: GlobalVariable
    START_TIME: str
    END_TIME: str
    GROUP_ID: int
    TOTAL_DATA: int
    BATCH_SIZE: int
    CONTAINER_NAME = os.getenv("CONTAINER_NAME")
    DIFF_TIME:float

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self):
        query = f"INSERT INTO dms_wpw_bot_run_log (docker_containers,group_id,total_data,batch_run,changes_found,changes_not_found,timeout,xpath_not_found,error_timeout,others,start_time,end_time,diff_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        value = (
            self.CONTAINER_NAME,
            self.GROUP_ID,
            self.TOTAL_DATA,
            self.BATCH_SIZE,
            self.GLOBAL_VARIABLE.compared,
            self.GLOBAL_VARIABLE.nothing_changed,
            self.GLOBAL_VARIABLE.url_error,
            self.GLOBAL_VARIABLE.path_error,
            self.GLOBAL_VARIABLE.timeout_error,
            self.GLOBAL_VARIABLE.exceptions,
            self.START_TIME,
            self.END_TIME,
            self.DIFF_TIME
        )
        self.QUERY_HANDLER.insertQuery(query, value)
