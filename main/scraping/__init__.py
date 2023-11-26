from dataclasses import dataclass, field
import asyncio
import re
import os
import time
import random
from playwright.async_api import async_playwright
from main.logger import console_logger


@dataclass
class Scraping:
    BATCH_SIZE: int
    LIMIT: int
    OFFSET: int
    QUERY_HANDLER: any
    CONDITION_HANDLER: any
    FETCHED_DATA: list = field(default_factory=list)
    TOTAL_DATA_COUNT: int = 0
    COUNT: int = 0

    def ManageVariables(self):
        console_logger.debug(self.QUERY_HANDLER)
        console_logger.debug(self.CONDITION_HANDLER)
        console_logger.debug(self.FETCHED_DATA)
        self.FETCHED_DATA = self.QUERY_HANDLER.requestForData(
            limit=self.LIMIT, offset=self.OFFSET
        )
        self.TOTAL_DATA_COUNT = len(self.FETCHED_DATA)

    def __𝐩𝐨𝐬𝐭_ini𝐭__ (self):
        self.ManageVariables()

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self.manageConcurrency())
        finally:
            # self.stop()
            loop.close()

    def stop(self):
        end_time = self.getCurrentTime()
        console_logger.debug(
            f"\nTOTAL Execution START|END|DIFF(MIN) =>{self.start_time} | {end_time} | {self.getDatetimeDifference(self.start_time,end_time)}\n"
        )

    async def manageConcurrency(self):
        total_completed_loop = 0
        running_tasks = set()
        in_progress_tasks = set()
        next_index = 0

        while total_completed_loop < self.TOTAL_DATA_COUNT or in_progress_tasks:
            tasks_to_run = self.BATCH_SIZE - len(running_tasks)
            if tasks_to_run > 0 and total_completed_loop < self.TOTAL_DATA_COUNT:
                batch_details = [
                    detail
                    for detail in self.FETCHED_DATA[
                        total_completed_loop : total_completed_loop + tasks_to_run
                    ]
                ]

                for detail in batch_details:
                    task = asyncio.create_task(self.browseManagement(**detail))
                    running_tasks.add(task)
                    in_progress_tasks.add(task)
                next_index += tasks_to_run

            done, _ = await asyncio.wait(
                in_progress_tasks, return_when=asyncio.FIRST_COMPLETED
            )
            for task in done:
                running_tasks.remove(task)
                in_progress_tasks.remove(task)
                new_index = next_index + len(in_progress_tasks)

                if new_index < self.TOTAL_DATA_COUNT:
                    detail = self.FETCHED_DATA[new_index]
                    new_task = asyncio.create_task(self.browseManagement(**detail))
                    running_tasks.add(new_task)
                    in_progress_tasks.add(new_task)

    async def browseManagement(self, **details):
        COUNT = self.COUNT
        console_logger.debug(
            f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mWORKING ON IT ......\033[00m:"
        )
        self.COUNT += 1
        while True:
            async with async_playwright() as playwrigh:
                browser = await playwrigh.chromium.launch(headless=True)
                context = await browser.new_context()
                page = await context.new_page()
                page.set_default_timeout(10000)
                try:
                    await page.goto(details["tender_link"], timeout=15000)
                    await self.process_element(page, **details)
                except asyncio.TimeoutError:
                    console_logger.error(
                        f"Timeout occurred for URL {details['tender_link']}"
                    )
                except Exception as e:
                    console_logger.error(f"Error: {str(e)}")
                finally:
                    await browser.close()
                    break

        console_logger.debug(
            f"{COUNT}/{self.TOTAL_DATA_COUNT} == {details['tender_link']}  \033[93mCOMPLETED\033[00m"
        )

    async def process_element(self, page, **details):
        element = await page.query_selector(details["XPath"].replace("/", "//", 1))

        if element:
            element_html = await page.evaluate(
                "(element) => element.outerHTML", element
            )
            element_text = await page.evaluate(
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
            console_logger.error(
                f'XPath error {details["XPath"].replace("/", "//", 1)}'
            )
            return False
