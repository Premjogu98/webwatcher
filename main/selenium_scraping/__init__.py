from dataclasses import dataclass, field
import asyncio
import re
import datetime
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.options import Options

from main.logger import console_logger
from main.db_connection.query_handler import QueryHandler
from main.db_connection.condition_handler import ConditionHandler
from main.global_variables import GlobalVariable
from main.db_connection.logs_handler import LogHandler
from main.global_variables import extractStringFromHTML

chrome_options = Options()
chrome_options.page_load_strategy = (
    "eager"  # WebDriver waits until DOMContentLoaded event fire is returned.
)
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors", "enable-logging"]
)
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--headless")
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
    FETCHED_DATA: list = field(default_factory=list)
    TOTAL_DATA_COUNT: int = 0
    COUNT: int = 0
    MAIN_START_TIME: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    MAIN_END_TIME: str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    FILE_PATH = ""

    def FetchData(self):
        # self.FILE_PATH = os.path.join(
        #     os.getcwd(), "logs", f"{self.OFFSET}-{self.LIMIT}.txt"
        # )
        # open(self.FILE_PATH, "w").write("PROCESS START\n")
        self.FETCHED_DATA = self.QUERY_HANDLER.requestForData(
            limit=self.LIMIT, offset=self.OFFSET
        )
        self.TOTAL_DATA_COUNT = len(self.FETCHED_DATA)

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self):
        self.FetchData()
        self.run()

        # loop = asyncio.get_event_loop()
        # # loop.run_until_complete(asyncio.wait_for(self.manageConcurrency(),timeout=5400)) # 1.5 hrs
        # loop.run_until_complete(
        #     self.manageConcurrency(),
        # )
        # loop.close()
        # self.infoLog(processEnd=True)

    def infoLog(
        self,
        processEnd: bool = False,
        method_start_time: str = "",
        method_end_time: str = "",
        count: int = 0,
    ):
        text = ""
        if processEnd:
            self.MAIN_END_TIME = self.getCurrentTime()
            text = f"\033[92m TOTAL Execution START|END|DIFF(MIN) =>  {self.MAIN_START_TIME} | {self.MAIN_END_TIME} | {self.getDatetimeDifference(self.MAIN_START_TIME, self.MAIN_END_TIME)}\033[00m"
            console_logger.debug(text)
            # LogHandler(
            #     QUERY_HANDLER=self.QUERY_HANDLER,
            #     GLOBAL_VARIABLE=self.GLOBAL_VARIABLE,
            #     START_TIME=self.MAIN_START_TIME,
            #     END_TIME=self.MAIN_END_TIME,
            #     GROUP_ID=self.GROUP_ID,
            #     TOTAL_DATA=self.TOTAL_DATA_COUNT,
            #     BATCH_SIZE=self.BATCH_SIZE,
            #     DIFF_TIME=round(
            #         float(
            #             self.getDatetimeDifference(
            #                 first=self.MAIN_START_TIME, second=self.MAIN_END_TIME
            #             )
            #         ),
            #         2,
            #     ),
            # )
        else:
            # console_logger.debug(
            #     f"Execution START/END => {method_start_time} / {method_end_time}"
            # )
            text = f"""Total : {count}/{self.TOTAL_DATA_COUNT} | \033[92m Compared \033[00m: {self.GLOBAL_VARIABLE.compared} | \033[93m Nothing Changed \033[00m: {self.GLOBAL_VARIABLE.nothing_changed} | \033[91m Path Error \033[00m: {self.GLOBAL_VARIABLE.path_error} | \033[91m Timeout Error \033[00m: {self.GLOBAL_VARIABLE.timeout_error} | \033[91m Url Error \033[00m: {self.GLOBAL_VARIABLE.url_error} | \033[91m Exceptions \033[00m: {self.GLOBAL_VARIABLE.exceptions}\n"""
            console_logger.debug(text)

    async def manageConcurrency(self):
        total_completed_loop = 0
        running_tasks = set()
        in_progress_tasks = set()
        detail_index = 0

        while total_completed_loop < self.TOTAL_DATA_COUNT or in_progress_tasks:
            while (
                len(in_progress_tasks) < self.BATCH_SIZE
                and detail_index < self.TOTAL_DATA_COUNT
            ):
                task = asyncio.create_task(
                    self.browseManagement(**self.FETCHED_DATA[detail_index]),
                    name=f"{self.FETCHED_DATA[detail_index]['id']}-{self.LIMIT}-{self.OFFSET}",
                )
                running_tasks.add(task)
                in_progress_tasks.add(task)
                detail_index += 1
            done, _ = await asyncio.wait(
                in_progress_tasks, return_when=asyncio.FIRST_COMPLETED, timeout=25
            )
            for task in done:
                in_progress_tasks.remove(task)
                total_completed_loop += 1
            # console_logger.debug(f"total_completed_loop: {total_completed_loop} | running_tasks: {len(running_tasks)} | in_progress_tasks: {len(in_progress_tasks)} | detail_index: {detail_index}")

            if (
                detail_index == self.TOTAL_DATA_COUNT
                or total_completed_loop == self.TOTAL_DATA_COUNT - 1
            ):
                console_logger.debug(
                    f"total_completed_loop: {total_completed_loop} | running_tasks: {len(running_tasks)} | in_progress_tasks: {len(in_progress_tasks)} | detail_index: {detail_index}"
                )
                if len(in_progress_tasks) == 1:
                    self.GLOBAL_VARIABLE.url_error += 1
                    break

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def getDatetimeDifference(self, first, second):
        start_time = datetime.datetime.strptime(first, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(second, "%Y-%m-%d %H:%M:%S")
        time_difference = end_time - start_time
        return time_difference.total_seconds() / 60

    async def browseManagement(self, **details):
        start_time = self.getCurrentTime()
        COUNT = self.COUNT
        # console_logger.debug(
        #     f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mWORKING ON IT ......\033[00m"
        # )
        self.COUNT += 1
        try:
            browser = webdriver.Chrome(options=chrome_options)
            browser.set_page_load_timeout(15)
            try:
                try:
                    browser.get(details["tender_link"])
                    # await asyncio.sleep(5)
                except Exception as e:
                    console_logger.error(e)
                    self.GLOBAL_VARIABLE.url_error += 1
                    raise Exception(f"Unable to load url {details['tender_link']}")
            except asyncio.TimeoutError as error:
                self.GLOBAL_VARIABLE.timeout_error += 1
                raise Exception(error)
            except TimeoutException as error:
                self.GLOBAL_VARIABLE.timeout_error += 1
                raise Exception(error)
            except Exception as error:
                error = str(error).lower()
                # console_logger.error(f"\033[91m {COUNT} Error \033[00m: {error}")
                self.QUERY_HANDLER.error_log(error=error, id=details["id"])
            else:
                await self.process_element(browser, **details)
        except Exception as error:
            console_logger.error(f"Exception: {error}")
            self.GLOBAL_VARIABLE.exceptions += 1
        finally:
            try:
                browser.quit()
            except Exception as e:
                console_logger.error(f"\033[91m Error \033[00m: {e}")
            self.infoLog(
                method_start_time=start_time,
                method_end_time=self.getCurrentTime(),
                count=COUNT,
            )
        # console_logger.debug(
        #     f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mCOMPLETED\033[00m"
        # )

    def run(self):

        # console_logger.debug(
        #     f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mWORKING ON IT ......\033[00m"
        # )
        self.COUNT += 1
        try:
            browser = webdriver.Chrome(options=chrome_options)
            browser.set_page_load_timeout(15)
            for details in self.FETCHED_DATA:
                try:

                    start_time = self.getCurrentTime()
                    COUNT = self.COUNT
                    try:
                        console_logger.debug(details["tender_link"])
                        browser.get(details["tender_link"])
                        console_logger.debug(details["tender_link"])

                    except Exception as e:
                        console_logger.error(e)
                        self.GLOBAL_VARIABLE.url_error += 1
                        raise Exception(f"Unable to load url {details['tender_link']}")

                    self.process_element(browser, **details)
                    self.COUNT += 1
                    self.infoLog(
                        method_start_time=start_time,
                        method_end_time=self.getCurrentTime(),
                        count=COUNT,
                    )
                    # except asyncio.TimeoutError as error:
                    #     self.GLOBAL_VARIABLE.timeout_error += 1
                    # raise Exception(error)
                except TimeoutException as error:
                    self.GLOBAL_VARIABLE.timeout_error += 1
                    raise Exception(error)
                except Exception as error:
                    error = str(error).lower()
                    console_logger.error(f"\033[91m {COUNT} Error \033[00m: {error}")
                    # self.QUERY_HANDLER.error_log(error=error, id=details["id"])
        except Exception as error:
            console_logger.error(f"Exception: {error}")
            self.GLOBAL_VARIABLE.exceptions += 1

        # finally:
        # try:
        #     browser.quit()
        # except Exception as e:
        #     console_logger.error(f"\033[91m Error \033[00m: {e}")
        # self.infoLog(
        #     method_start_time=start_time,
        #     method_end_time=self.getCurrentTime(),
        #     count=COUNT,
        # )

        # console_logger.debug(
        #     f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mCOMPLETED\033[00m"
        # )

    def process_element(self, browser, **details):
        element_found = False
        for element in browser.find_elements(By.XPATH, details["XPath"]):
            element_found = True
            details["onlyhtml"] = re.sub(
                "\s\s+",
                " ",
                element.get_attribute("outerHTML")
                .strip()
                .replace("\n", " ")
                .replace("\t", " "),
            )
            details["onlytext"] = extractStringFromHTML(details["onlyhtml"])
            # console_logger.debug(details["onlytext"])
            # self.CONDITION_HANDLER.checkConditionBeforeTextComparison(**details)

        if not element_found:
            self.GLOBAL_VARIABLE.path_error += 1
            # self.QUERY_HANDLER.error_log(
            #     error=f'XPath error {details["XPath"].replace("/", "//", 1)}',
            #     id=details["id"],
            # )
