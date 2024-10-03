from dataclasses import dataclass, field
import asyncio
import re
import datetime
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from main.logger import console_logger
from main.db_connection.query_handler import QueryHandler
from main.db_connection.condition_handler import ConditionHandler
from main.global_variables import GlobalVariable, extractStringFromHTML
from typing import List, Dict, Any

chrome_options = Options()
chrome_options.page_load_strategy = "eager"
chrome_options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors", "enable-logging"])
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

@dataclass
class SeleniumScraping:
    BATCH_SIZE: int
    LIMIT: int
    OFFSET: int
    QUERY_HANDLER: QueryHandler
    CONDITION_HANDLER: ConditionHandler
    GLOBAL_VARIABLE: GlobalVariable
    GROUP_ID: int
    FETCHED_DATA: List[Dict[str, Any]] = field(default_factory=list)
    TOTAL_DATA_COUNT: int = 0
    COUNT: int = 0
    MAIN_START_TIME: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    MAIN_END_TIME: str = field(default_factory=lambda: datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    FILE_PATH: str = ""

    def FetchData(self) -> None:
        self.FETCHED_DATA = self.QUERY_HANDLER.requestForData(limit=self.LIMIT, offset=self.OFFSET)
        self.TOTAL_DATA_COUNT = len(self.FETCHED_DATA)

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self) -> None:
        self.FetchData()
        self.run()

    def infoLog(self, processEnd: bool = False, method_start_time: str = "", method_end_time: str = "", count: int = 0) -> None:
        if processEnd:
            self.MAIN_END_TIME = self.getCurrentTime()
            diff_time = self.getDatetimeDifference(self.MAIN_START_TIME, self.MAIN_END_TIME)
            text = f"\033[92m TOTAL Execution START|END|DIFF(MIN) =>  {self.MAIN_START_TIME} | {self.MAIN_END_TIME} | {diff_time}\033[00m"
            console_logger.debug(text)
        else:
            text = f"""Total : {count}/{self.TOTAL_DATA_COUNT} | \033[92m Compared \033[00m: {self.GLOBAL_VARIABLE.compared} | \033[93m Nothing Changed \033[00m: {self.GLOBAL_VARIABLE.nothing_changed} | \033[91m Path Error \033[00m: {self.GLOBAL_VARIABLE.path_error} | \033[91m Timeout Error \033[00m: {self.GLOBAL_VARIABLE.timeout_error} | \033[91m Url Error \033[00m: {self.GLOBAL_VARIABLE.url_error} | \033[91m Exceptions \033[00m: {self.GLOBAL_VARIABLE.exceptions}\n"""
            console_logger.debug(text)

    @staticmethod
    def getCurrentTime() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def getDatetimeDifference(first: str, second: str) -> float:
        time_difference = datetime.datetime.strptime(second, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(first, "%Y-%m-%d %H:%M:%S")
        return time_difference.total_seconds() / 60

    def run(self) -> None:
        self.COUNT += 1
        browser = webdriver.Chrome(options=chrome_options)
        browser.set_page_load_timeout(15)

        try:
            for details in self.FETCHED_DATA:
                start_time = self.getCurrentTime()
                COUNT = self.COUNT

                try:
                    console_logger.debug(details["tender_link"])
                    browser.get(details["tender_link"])
                    self.process_element(browser, **details)
                except TimeoutException as error:
                    self.GLOBAL_VARIABLE.timeout_error += 1
                    console_logger.error(f"Timeout Exception: {error}")
                except Exception as error:
                    console_logger.error(f"\033[91m {COUNT} Error \033[00m: {str(error).lower()}")
                    self.GLOBAL_VARIABLE.url_error += 1

                self.COUNT += 1
                self.infoLog(method_start_time=start_time, method_end_time=self.getCurrentTime(), count=COUNT)

        except Exception as error:
            console_logger.error(f"Exception: {error}")
            self.GLOBAL_VARIABLE.exceptions += 1
        finally:
            browser.quit()

    def process_element(self, browser: webdriver.Chrome, **details: Dict[str, Any]) -> None:
        element_found = False
        for element in browser.find_elements(By.XPATH, details["XPath"]):
            element_found = True
            details["onlyhtml"] = re.sub(r"\s\s+", " ", element.get_attribute("outerHTML").strip().replace("\n", " ").replace("\t", " "))
            details["onlytext"] = extractStringFromHTML(details["onlyhtml"])
            # Uncomment the following line if you want to use CONDITION_HANDLER
            # self.CONDITION_HANDLER.checkConditionBeforeTextComparison(**details)

        if not element_found:
            self.GLOBAL_VARIABLE.path_error += 1
            # Uncomment the following lines if you want to log XPath errors
            # self.QUERY_HANDLER.error_log(
            #     error=f'XPath error {details["XPath"].replace("/", "//", 1)}',
            #     id=details["id"],
            # )