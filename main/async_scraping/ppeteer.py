from dataclasses import dataclass, field
import asyncio
from async_timeout import timeout
import re
import sys
import datetime
import pyppeteer
from pyppeteer import launch, errors
import html

from main.logger import console_logger
from main.db_connection.query_handler import QueryHandler
from main.db_connection.condition_handler import ConditionHandler
from main.global_variables import GlobalVariable
from main.db_connection.logs_handler import LogHandler
from main.global_variables import extractStringFromHTML


@dataclass
class Ppeteer:
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

    def __𝐩𝐨𝐬𝐭_ini𝐭__(self):
        try:
            self.ManageVariables()
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                self.manageConcurrency(),
            )
            loop.close()
            self.infoLog(processEnd=True)
        except Exception as e:
            console_logger.warning(e)

    def ManageVariables(self):
        self.FETCHED_DATA = self.QUERY_HANDLER.requestForData(
            limit=self.LIMIT, offset=self.OFFSET
        )
        self.TOTAL_DATA_COUNT = len(self.FETCHED_DATA)

    def getCurrentTime(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def getDatetimeDifference(self, first, second):
        start_time = datetime.datetime.strptime(first, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(second, "%Y-%m-%d %H:%M:%S")
        time_difference = end_time - start_time
        return time_difference.total_seconds() / 60

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
            text = f"TOTAL Execution START|END|DIFF(MIN) =>{self.MAIN_START_TIME} | {self.MAIN_END_TIME} | {self.getDatetimeDifference(self.MAIN_START_TIME, self.MAIN_END_TIME)}"
            console_logger.info(text)
            LogHandler(
                QUERY_HANDLER=self.QUERY_HANDLER,
                GLOBAL_VARIABLE=self.GLOBAL_VARIABLE,
                START_TIME=self.MAIN_START_TIME,
                END_TIME=self.MAIN_END_TIME,
                GROUP_ID=self.GROUP_ID,
                TOTAL_DATA=self.TOTAL_DATA_COUNT,
                BATCH_SIZE=self.BATCH_SIZE,
                DIFF_TIME=round(
                    float(
                        self.getDatetimeDifference(
                            first=self.MAIN_START_TIME, second=self.MAIN_END_TIME
                        )
                    ),
                    2,
                ),
            )
        else:
            # console_logger.debug(
            #     f"Execution START/END => {method_start_time} / {method_end_time}"
            # )
            text = f"""Total : {count}/{self.TOTAL_DATA_COUNT} | \033[92m Compared \033[00m: {self.GLOBAL_VARIABLE.compared} | \033[93m Nothing Changed \033[00m: {self.GLOBAL_VARIABLE.nothing_changed} | \033[91m Path Error \033[00m: {self.GLOBAL_VARIABLE.path_error} | \033[91m Timeout Error \033[00m: {self.GLOBAL_VARIABLE.timeout_error} | \033[91m Url Error \033[00m: {self.GLOBAL_VARIABLE.url_error} | \033[91m Exceptions \033[00m: {self.GLOBAL_VARIABLE.exceptions}\n"""
            console_logger.debug(text)

    async def manageConcurrency(self):
        # # Add this line in your script to ensure Chromium is updated
        # pyppeteer.chromium_downloader.download_chromium()
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

    async def browseManagement(self, **details):
        start_time = self.getCurrentTime()
        COUNT = self.COUNT
        console_logger.warning(
            f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']} WORKING ON IT ......"
        )
        self.COUNT += 1
        try:

            browser = await launch(
                headless=True,
                autoClose=False,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-notifications",
                ],
            )
            try:
                context = await browser.createIncognitoBrowserContext()
                page = await context.newPage()
                try:
                    async with timeout(15):
                        await page.goto(details["tender_link"])
                        await asyncio.sleep(2)
                except asyncio.TimeoutError as error:
                    error_text = f"Unable to load url {details['tender_link']}"
                    console_logger.error(error_text)
                    self.GLOBAL_VARIABLE.url_error += 1
                    self.QUERY_HANDLER.error_log(
                        error=error_text.lower(), id=details["id"]
                    )
                except Exception as error:
                    console_logger.error(error)
                    self.GLOBAL_VARIABLE.url_error += 1
                    self.QUERY_HANDLER.error_log(
                        error=str(error).lower(), id=details["id"]
                    )
                else:
                    page.on(
                        "dialog", lambda dialog: asyncio.ensure_future(dialog.dismiss())
                    )
                    await page.setBypassCSP(True)  # Content Security Policy
                    await self.process_element(page, **details)

            except Exception as error:
                console_logger.error(
                    "EXCEPTION: Error on line {}  EXCEPTION: {}".format(
                        sys.exc_info()[-1].tb_lineno, error
                    )
                )
                self.GLOBAL_VARIABLE.exceptions += 1
            finally:
                await page.close()
                await context.close()
                await browser.close()
        except Exception as error:
            console_logger.error(
                "EXCEPTION: Error on line {}  EXCEPTION: {}".format(
                    sys.exc_info()[-1].tb_lineno, error
                )
            )
            self.GLOBAL_VARIABLE.exceptions += 1
        finally:
            self.infoLog(
                method_start_time=start_time,
                method_end_time=self.getCurrentTime(),
                count=COUNT,
            )

    async def process_element(self, page, **details):
        try:
            xpath = details["XPath"].replace("/", "//", 1).replace("///", "//")
            elements = await page.xpath(xpath)
            if not elements:
                console_logger.error(f'XPath error {details["XPath"]}')
                self.QUERY_HANDLER.error_log(
                    error=f'XPath error {details["XPath"]}',
                    id=details["id"],
                )
                self.GLOBAL_VARIABLE.path_error += 1
                return
            else:
                element_html = await page.evaluate(
                    f"""() => {{
                        const element = document.evaluate(`{xpath}`, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        return element ? element.outerHTML : false;
                    }}"""
                )
                if element_html:
                    details["onlyhtml"] = html.unescape(
                        re.sub(
                            "\s\s+",
                            " ",
                            element_html.replace("\n", " ").replace("\t", " "),
                        )
                    )
                    details["onlytext"] = extractStringFromHTML(details["onlyhtml"])
                    self.CONDITION_HANDLER.checkConditionBeforeTextComparison(**details)
                else:
                    raise Exception("Unable to fetch OUTER HTML")
        except Exception as e:
            console_logger.error(
                "EXCEPTION: Error on line {}  EXCEPTION: {}".format(
                    sys.exc_info()[-1].tb_lineno, e
                )
            )
            raise Exception(e)
