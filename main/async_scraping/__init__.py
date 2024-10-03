from dataclasses import dataclass, field
import asyncio
import re
import sys
import datetime
from playwright.async_api import async_playwright, TimeoutError
from main.logger import console_logger
from main.db_connection.query_handler import QueryHandler
from main.db_connection.condition_handler import ConditionHandler
from main.global_variables import GlobalVariable, extractStringFromHTML
from main.db_connection.logs_handler import LogHandler
from typing import List, Dict, Any

@dataclass
class AsyncScraping:
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

    def ManageVariables(self) -> None:
        self.FETCHED_DATA = self.QUERY_HANDLER.requestForData(limit=self.LIMIT, offset=self.OFFSET)
        self.TOTAL_DATA_COUNT = len(self.FETCHED_DATA)

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self) -> None:
        self.ManageVariables()
        asyncio.run(self.manageConcurrency())
        self.infoLog(processEnd=True)

    def infoLog(self, processEnd: bool = False, method_start_time: str = "", method_end_time: str = "", count: int = 0) -> None:
        if processEnd:
            self.MAIN_END_TIME = self.getCurrentTime()
            diff_time = self.getDatetimeDifference(self.MAIN_START_TIME, self.MAIN_END_TIME)
            text = f"\033[92m TOTAL Execution START|END|DIFF(MIN) =>{self.MAIN_START_TIME} | {self.MAIN_END_TIME} | {diff_time}\033[00m"
            console_logger.debug(text)
            LogHandler(
                QUERY_HANDLER=self.QUERY_HANDLER,
                GLOBAL_VARIABLE=self.GLOBAL_VARIABLE,
                START_TIME=self.MAIN_START_TIME,
                END_TIME=self.MAIN_END_TIME,
                GROUP_ID=self.GROUP_ID,
                TOTAL_DATA=self.TOTAL_DATA_COUNT,
                BATCH_SIZE=self.BATCH_SIZE,
                DIFF_TIME=round(float(diff_time), 2),
            )
        else:
            # console_logger.debug(
            #     f"Execution START/END => {method_start_time} / {method_end_time}"
            # )
            text = f"""Total : {count}/{self.TOTAL_DATA_COUNT} | \033[92m Compared \033[00m: {self.GLOBAL_VARIABLE.compared} | \033[93m Nothing Changed \033[00m: {self.GLOBAL_VARIABLE.nothing_changed} | \033[91m Path Error \033[00m: {self.GLOBAL_VARIABLE.path_error} | \033[91m Timeout Error \033[00m: {self.GLOBAL_VARIABLE.timeout_error} | \033[91m Url Error \033[00m: {self.GLOBAL_VARIABLE.url_error} | \033[91m Exceptions \033[00m: {self.GLOBAL_VARIABLE.exceptions}\n"""
            console_logger.debug(text)

    async def manageConcurrency(self) -> None:
        total_completed_loop = 0
        in_progress_tasks = set()
        detail_index = 0

        while total_completed_loop < self.TOTAL_DATA_COUNT or in_progress_tasks:
            while len(in_progress_tasks) < self.BATCH_SIZE and detail_index < self.TOTAL_DATA_COUNT:
                task = asyncio.create_task(
                    self.browseManagement(**self.FETCHED_DATA[detail_index]),
                    name=f"{self.FETCHED_DATA[detail_index]['id']}-{self.LIMIT}-{self.OFFSET}",
                )
                in_progress_tasks.add(task)
                detail_index += 1
            
            done, _ = await asyncio.wait(in_progress_tasks, return_when=asyncio.FIRST_COMPLETED, timeout=25)
            
            for task in done:
                in_progress_tasks.remove(task)
                total_completed_loop += 1

            if detail_index == self.TOTAL_DATA_COUNT or total_completed_loop == self.TOTAL_DATA_COUNT - 1:
                console_logger.debug(f"total_completed_loop: {total_completed_loop} | in_progress_tasks: {len(in_progress_tasks)} | detail_index: {detail_index}")
                if len(in_progress_tasks) == 1:
                    self.GLOBAL_VARIABLE.url_error += 1
                    break

    @staticmethod
    def getCurrentTime() -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def getDatetimeDifference(first: str, second: str) -> float:
        time_difference = datetime.datetime.strptime(second, "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(first, "%Y-%m-%d %H:%M:%S")
        return time_difference.total_seconds() / 60

    async def browseManagement(self, **details: Dict[str, Any]) -> None:
        start_time = self.getCurrentTime()
        COUNT = self.COUNT
        console_logger.debug(f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mWORKING ON IT ......\033[00m")
        self.COUNT += 1
        
        try:
            async with async_playwright() as playwright:
                browser = await playwright.chromium.launch(channel="chrome", handle_sighup=False, headless=True, chromium_sandbox=False)
                context = await browser.new_context(ignore_https_errors=True, bypass_csp=True)
                page = await context.new_page()
                
                try:
                    await page.goto(details["tender_link"], timeout=25000)
                except asyncio.TimeoutError as error:
                    self.GLOBAL_VARIABLE.timeout_error += 1
                    raise Exception(error)
                except Exception as e:
                    console_logger.error(e)
                    self.GLOBAL_VARIABLE.url_error += 1
                    raise Exception(f"Unable to load url {details['tender_link']}")
                
                await self.process_element(page, **details)
        except Exception as error:
            console_logger.error(f"\033[91m EXCEPTION: Error on line {sys.exc_info()[-1].tb_lineno}  EXCEPTION: {error} \033[00m")
            self.GLOBAL_VARIABLE.exceptions += 1
        finally:
            try:
                await browser.close()
            except Exception as e:
                console_logger.error(f"Error closing browser: {e}")
            self.infoLog(method_start_time=start_time, method_end_time=self.getCurrentTime(), count=COUNT)

    async def process_element(self, page, **details: Dict[str, Any]) -> None:
        try:
            xpath = details["XPath"].replace("/", "//", 1).replace("///", "//")
            order_sent = page.locator(xpath)
            
            if await order_sent.count() == 0:
                console_logger.error(f'XPath error {details["XPath"]}')
                self.QUERY_HANDLER.error_log(error=f'XPath error {details["XPath"]}', id=details["id"])
                self.GLOBAL_VARIABLE.path_error += 1
                return

            element_html = await page.evaluate(f"""() => {{
                const element = document.evaluate(`{xpath}`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                return element ? element.outerHTML : false;
            }}""")

            if element_html:
                details["onlyhtml"] = re.sub(r"\s\s+", " ", element_html.replace("\n", " ").replace("\t", " "))
                details["onlytext"] = extractStringFromHTML(details["onlyhtml"])
                self.CONDITION_HANDLER.checkConditionBeforeTextComparison(**details)
            else:
                raise Exception("Unable to fetch OUTER HTML")
        except Exception as e:
            console_logger.error(f"\033[91m EXCEPTION: Error on line {sys.exc_info()[-1].tb_lineno}  EXCEPTION: {e} \033[00m")
            raise Exception(e)