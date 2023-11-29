from dataclasses import dataclass, field
import asyncio
import re
import os
import time
import random
import datetime
from playwright.async_api import async_playwright, TimeoutError
from playwright.sync_api import sync_playwright, Playwright
from main.logger import console_logger
from main.db_connection.query_handler import QueryHandler
from main.db_connection.condition_handler import ConditionHandler
from main.global_variables import GlobalVariable


@dataclass
class Scraping:
    BATCH_SIZE: int
    LIMIT: int
    OFFSET: int
    QUERY_HANDLER: QueryHandler
    CONDITION_HANDLER: ConditionHandler
    GLOBAL_VARIABLE: GlobalVariable
    FETCHED_DATA: list = field(default_factory=list)
    TOTAL_DATA_COUNT: int = 0
    COUNT: int = 0
    MAIN_START_TIME: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    MAIN_END_TIME: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    FILE_PATH = ""
    def ManageVariables(self):
        self.FILE_PATH = os.path.join(os.getcwd(),"logs",f'{self.OFFSET}-{self.LIMIT}.txt')
        open(self.FILE_PATH,'w').write("PROCESS START\n")
        self.FETCHED_DATA = self.QUERY_HANDLER.requestForData(
            limit=self.LIMIT, offset=self.OFFSET
        )
        self.TOTAL_DATA_COUNT = len(self.FETCHED_DATA)

    def __𝐩𝐨𝐬𝐭_ini𝐭__ (self):
        self.ManageVariables()
        self.manageConcurrency()
        self.infoLog(processEnd=True)

        # loop = asyncio.get_event_loop()
        # try:
        #     loop.run_until_complete(self.manageConcurrency())
        # finally:
        #     self.infoLog(processEnd=True)
        #     loop.close()

    def infoLog(
        self,
        processEnd: bool = False,
        method_start_time: str = "",
        method_end_time: str = "",
    ):
        text = ""
        if processEnd:
            self.MAIN_END_TIME = self.getCurrentTime()
            text = f"\nTOTAL Execution START|END|DIFF(MIN) =>{self.MAIN_START_TIME} | {self.MAIN_END_TIME} | {self.getDatetimeDifference(self.MAIN_START_TIME, self.MAIN_END_TIME)}\n"
            console_logger.debug(text)
            
        else:
            console_logger.debug(
                f"Execution START/END => {method_start_time} / {method_end_time}"
            )
            text = f"""Total : {self.COUNT}/{self.TOTAL_DATA_COUNT} | \033[92m Compared \033[00m: {self.GLOBAL_VARIABLE.compared} | \033[93m Nothing Changed \033[00m: {self.GLOBAL_VARIABLE.nothing_changed} | \033[91m Path Error \033[00m: {self.GLOBAL_VARIABLE.path_error} | \033[91m Timeout Error \033[00m: {self.GLOBAL_VARIABLE.timeout_error} | \033[91m Url Error \033[00m: {self.GLOBAL_VARIABLE.url_error} | \033[91m Exceptions \033[00m: {self.GLOBAL_VARIABLE.exceptions}\n"""
            console_logger.debug(text)
        with open(self.FILE_PATH, 'a') as f:
            f.write(text)
    def manageConcurrency(self):
        total_completed_loop = 0
        running_tasks = set()
        in_progress_tasks = set()
        detail_index = 0

        while detail_index < self.TOTAL_DATA_COUNT:
            self.browseManagement(**self.FETCHED_DATA[detail_index])
            detail_index += 1

        # while total_completed_loop < self.TOTAL_DATA_COUNT or in_progress_tasks:
        #     while detail_index < self.TOTAL_DATA_COUNT:
                # task = asyncio.create_task(
                #     self.browseManagement(**self.FETCHED_DATA[detail_index])
                # )
                # running_tasks.add(task)
                # in_progress_tasks.add(task)
                # detail_index += 1

            # done, _ = await asyncio.wait(
            #     in_progress_tasks, return_when=asyncio.FIRST_COMPLETED
            # )

            # for task in done:
            #     in_progress_tasks.remove(task)
            #     total_completed_loop += 1

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def getDatetimeDifference(self, first, second):
        start_time = datetime.datetime.strptime(first, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(second, "%Y-%m-%d %H:%M:%S")
        time_difference = end_time - start_time
        return time_difference.total_seconds() / 60

    def browseManagement(self, **details):
        start_time = self.getCurrentTime()
        COUNT = self.COUNT
        console_logger.debug(
            f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mWORKING ON IT ......\033[00m:"
        )
        self.COUNT += 1
        try:
            with sync_playwright() as playwright:
                chromium = playwright.chromium
                browser = chromium.launch(headless=True)
                page = browser.new_page()
                page.set_default_timeout(15000)
                try:
                    try:
                        page.goto(details["tender_link"], timeout=15000)
                    except Exception as e:
                        console_logger.debug(e)
                        self.GLOBAL_VARIABLE.url_error += 1
                        raise Exception(
                            f"Unable to load url {details['tender_link']}"
                        )
                except TimeoutError as error:
                    self.GLOBAL_VARIABLE.timeout_error += 1
                    raise Exception(error)
                except Exception as error:
                    error = str(error).lower()
                    console_logger.error(f"Error: {error}")
                    self.QUERY_HANDLER.error_log(error=error, id=details["id"])
                else:
                    self.process_element(page, **details)
        except Exception as error:
            console_logger.error(f"Exception: {error}")
            self.GLOBAL_VARIABLE.exceptions += 1
        finally:
            try:
                browser.close()
            except Exception as e:
                console_logger.warning(e)
            self.infoLog(
                method_start_time=start_time,
                method_end_time=self.getCurrentTime(),
            )
        console_logger.debug(
            f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mCOMPLETED\033[00m"
        )

    def process_element(self, page, **details):
        element = page.query_selector(details["XPath"].replace("/", "//", 1))

        if element:
            element_html = page.evaluate(
                "(element) => element.outerHTML", element
            )
            element_text = page.evaluate(
                "(element) => element.innerText", element
            )
            details["onlyhtml"] = re.sub(
                "\s\s+", " ", element_html.replace("\n", " ").replace("\t", " ")
            )
            details["onlytext"] = re.sub(
                "\s\s+", " ", element_text.replace("\n", " ").replace("\t", " ")
            )
            self.CONDITION_HANDLER.checkConditionBeforeTextComparison(**details)
        else:
            self.GLOBAL_VARIABLE.path_error += 1
            self.QUERY_HANDLER.error_log(error=f'XPath error {details["XPath"].replace("/", "//", 1)}', id=details["id"])
