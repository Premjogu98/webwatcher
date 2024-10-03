from dataclasses import dataclass, field
import re
import os
import datetime
from playwright.sync_api import sync_playwright
from main.logger import console_logger
from main.db_connection.query_handler import QueryHandler
from main.db_connection.condition_handler import ConditionHandler
from main.global_variables import GlobalVariable, extractStringFromHTML
from typing import List, Dict, Any

@dataclass
class SyncScraping:
    BATCH_SIZE: int
    LIMIT: int
    OFFSET: int
    QUERY_HANDLER: QueryHandler
    CONDITION_HANDLER: ConditionHandler
    GLOBAL_VARIABLE: GlobalVariable
    FETCHED_DATA: List[Dict[str, Any]] = field(default_factory=list)
    TOTAL_DATA_COUNT: int = 0
    COUNT: int = 0
    MAIN_START_TIME: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    MAIN_END_TIME: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    FILE_PATH: str = ""

    def ManageVariables(self) -> None:
        self.FILE_PATH = os.path.join(os.getcwd(), "logs", f"{self.OFFSET}-{self.LIMIT}.txt")
        with open(self.FILE_PATH, "w") as f:
            f.write("PROCESS START\n")
        self.FETCHED_DATA = self.QUERY_HANDLER.requestForData(limit=self.LIMIT, offset=self.OFFSET)
        self.TOTAL_DATA_COUNT = len(self.FETCHED_DATA)

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self) -> None:
        self.ManageVariables()
        self.manageConcurrency()
        self.infoLog(processEnd=True)

    def infoLog(self, processEnd: bool = False, method_start_time: str = "", method_end_time: str = "") -> None:
        if processEnd:
            self.MAIN_END_TIME = self.getCurrentTime()
            text = f"\nTOTAL Execution START|END|DIFF(MIN) =>{self.MAIN_START_TIME} | {self.MAIN_END_TIME} | {self.getDatetimeDifference(self.MAIN_START_TIME, self.MAIN_END_TIME)}\n"
            console_logger.debug(text)
            with open(self.FILE_PATH, "a") as f:
                f.write(text)
        else:
            console_logger.debug(f"Execution START/END => {method_start_time} / {method_end_time}")
            text = f"""Total : {self.COUNT}/{self.TOTAL_DATA_COUNT} | \033[92m Compared \033[00m: {self.GLOBAL_VARIABLE.compared} | \033[93m Nothing Changed \033[00m: {self.GLOBAL_VARIABLE.nothing_changed} | \033[91m Path Error \033[00m: {self.GLOBAL_VARIABLE.path_error} | \033[91m Timeout Error \033[00m: {self.GLOBAL_VARIABLE.timeout_error} | \033[91m Url Error \033[00m: {self.GLOBAL_VARIABLE.url_error} | \033[91m Exceptions \033[00m: {self.GLOBAL_VARIABLE.exceptions}\n"""
            console_logger.debug(text)

    def manageConcurrency(self) -> None:
        for details in self.FETCHED_DATA:
            self.browseManagement(**details)

    @staticmethod
    def getCurrentTime() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def getDatetimeDifference(first: str, second: str) -> float:
        time_difference = datetime.datetime.strptime(second, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(first, "%Y-%m-%d %H:%M:%S")
        return time_difference.total_seconds() / 60

    def browseManagement(self, **details: Dict[str, Any]) -> None:
        start_time = self.getCurrentTime()
        COUNT = self.COUNT
        console_logger.debug(f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mWORKING ON IT ......\033[00m:")
        self.COUNT += 1

        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=True)
            page = browser.new_page()
            page.set_default_timeout(15000)

            try:
                page.goto(details["tender_link"], timeout=15000)
                self.process_element(page, **details)
            except Exception as error:
                self._handle_error(error, details)
            finally:
                browser.close()

        self.infoLog(method_start_time=start_time, method_end_time=self.getCurrentTime())
        console_logger.debug(f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mCOMPLETED\033[00m")

    def process_element(self, page, **details: Dict[str, Any]) -> None:
        console_logger.debug(details["XPath"])
        element = page.query_selector(details["XPath"].replace("/", "//", 1))

        if element:
            element_html = page.evaluate("(element) => element.outerHTML", element)
            details["onlyhtml"] = re.sub(r"\s\s+", " ", element_html.replace("\n", " ").replace("\t", " "))
            details["onlytext"] = extractStringFromHTML(element_html)
            self.CONDITION_HANDLER.checkConditionBeforeTextComparison(**details)
        else:
            self._handle_xpath_error(details)

    def _handle_error(self, error: Exception, details: Dict[str, Any]) -> None:
        error_str = str(error).lower()
        if isinstance(error, TimeoutError):
            self.GLOBAL_VARIABLE.timeout_error += 1
        else:
            self.GLOBAL_VARIABLE.url_error += 1
        console_logger.error(f"Error: {error_str}")
        self.QUERY_HANDLER.error_log(error=error_str, id=details["id"])
        self.GLOBAL_VARIABLE.exceptions += 1

    def _handle_xpath_error(self, details: Dict[str, Any]) -> None:
        self.GLOBAL_VARIABLE.path_error += 1
        error_message = f'XPath error {details["XPath"].replace("/", "//", 1)}'
        self.QUERY_HANDLER.error_log(error=error_message, id=details["id"])