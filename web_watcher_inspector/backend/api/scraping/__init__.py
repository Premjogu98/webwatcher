import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from api.logger import console_logger
import re
from fastapi import Depends, HTTPException
from api.database_handler.condition_handler import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from playwright.async_api import async_playwright

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Scraping:

    def __init__(self) -> None:
        pass

    async def get_html_from_playwight(self, url, id):
        url = getLinkFromID(id)
        console_logger.debug(url)
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            # context = await browser.new_context()
            page = await browser.new_page()
            await page.goto(url, timeout=20000)
            await page.wait_for_timeout(10000)  # Wait for 10 seconds
            html_content = await page.content()
            await browser.close()
            return self.manageOuterHtml(html_content, url)

    def manageOuterHtml(self, html, url):
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup.find_all(["a", "img", "script", "link"]):
            for attr in ["href", "src"]:
                if attr in tag.attrs:
                    tag[attr] = urljoin(url, tag[attr])
        html_content = soup.prettify()
        for script in re.findall(r"(?<=<script).*?(?=</script>)", html):
            html_content = html_content.replace(f"<script{script}</script>", "")
        # console_logger.debug(soup.find_all(['header']))
        # for header in soup.find_all(['header']):
        #     console_logger.de(header)
        #     html_content = html_content.replace(f"<header {header}</header>","")
        html_content = html_content.replace(
            'href="', f'style="pointer-events: none;cursor: default;" href="'
        )
        return html_content

    async def get_html(self, url, id):
        try:
            if not url and not id:
                return HTTPException(content="url or id not found", status_code=400)
            if id:
                return (await self.get_html_from_playwight(url, id), 200)
                url = getLinkFromID(id)
                console_logger.debug(url)
            response = requests.get(url, verify=False, timeout=20)
            self.get_html_from_playwight(url, id)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                # Make relative URLs absolute
                for tag in soup.find_all(["a", "img", "script", "link"]):
                    for attr in ["href", "src"]:
                        if attr in tag.attrs:
                            tag[attr] = urljoin(url, tag[attr])
                            # console_logger.debug(tag[attr])
                html_content = soup.prettify()
                for script in re.findall(
                    r"(?<=<script).*?(?=</script>)", response.text
                ):
                    html_content = html_content.replace(f"<script{script}</script>", "")
                # console_logger.debug(soup.find_all(['header']))
                # for header in soup.find_all(['header']):
                #     console_logger.de(header)
                #     html_content = html_content.replace(f"<header {header}</header>","")
                html_content = html_content.replace(
                    'href="', f'style="pointer-events: none;cursor: default;" href="'
                )
                return (html_content, 200)
            else:
                console_logger.error(
                    f"Failed to retrieve the page. Status code: {response.status_code}"
                )
                return ("Failed to retrieve the page", response.status_code)
        except requests.Timeout:
            return ("Request Timeout", 408)
        except requests.RequestException as e:
            console_logger.error(e)
            return ("Unable to load url please check url first", 400)
        except Exception as e:
            console_logger.error(
                "ERROR: {} Error on line {}".format(e, sys.exc_info()[-1].tb_lineno)
            )
            return ("Something went wrong", 500)

    def get_compared_html(self, id, old):
        try:
            headers = {"Content-Type": "text/html; charset=utf-8"}
            # https://s3.nl.geostorage.net/tottestupload3/webpagewatcher/70588-newhtmlfile.html
            # https://s3.nl.geostorage.net/tottestupload3/webpagewatcher/70588-oldhtmlfile.html
            # f"http://185.15.209.234/compared/files/{id}-{'oldhtmlfile' if old else 'newhtmlfile'}.html"
            console_logger.info(
                f"https://s3.nl.geostorage.net/tottestupload3/webpagewatcher/{id}-{'oldhtmlfile' if old else 'newhtmlfile'}.html"
            )
            response = requests.get(
                f"https://s3.nl.geostorage.net/tottestupload3/webpagewatcher/{id}-{'oldhtmlfile' if old else 'newhtmlfile'}.html"
            )
            if response.status_code == 200:
                response.encoding = "utf-8"
                html_content = response.text
                return (html_content, 200)  # Display the HTML content
            else:
                console_logger.debug(
                    f"Failed to retrieve HTML. Status code: {response.status_code}"
                )
                return (response.text, response.status_code)
        except requests.Timeout:
            return ("Request Timeout", 408)
        except requests.RequestException as e:
            console_logger.error(e)
            return ("Unable to load url please check url first", 400)
        except Exception as e:
            console_logger.error(e)
            return ("Something went wrong", 500)
