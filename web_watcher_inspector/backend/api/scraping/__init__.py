import requests
from urllib.parse import urlparse,urljoin
from bs4 import BeautifulSoup
from api.logger import console_logger
import re
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
class Scraping:

    def __init__(self) -> None:
        pass

    def get_html(self,url):
        try:
            response = requests.get(url,verify=False)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # Make relative URLs absolute
                for tag in soup.find_all(['a', 'img', 'script']):
                    for attr in ['href', 'src']:
                        if attr in tag.attrs:
                            tag[attr] = urljoin(url, tag[attr])

                html_content = soup.prettify()
                for script in re.findall(r"(?<=<script).*?(?=</script>)", response.text):
                    html_content = html_content.replace(f"<header{script}</script>","")
                # console_logger.debug(soup.find_all(['header']))
                # for header in soup.find_all(['header']):
                #     console_logger.de(header)
                #     html_content = html_content.replace(f"<header {header}</header>","")
                html_content = html_content.replace('href="',f'style="pointer-events: none;cursor: default;" href="')
                return (html_content,200)
            else:
                console_logger.error(f"Failed to retrieve the page. Status code: {response.status_code}")
                return ("Failed to retrieve the page",response.status_code)
        except requests.RequestException as e:
            console_logger.error(e)
            return ("Please enter valid url",400)
        except Exception as e:
            console_logger.error(e)
            return ("Something went wrong",500)