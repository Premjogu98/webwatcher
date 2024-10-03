from dataclasses import dataclass, field
from bs4 import BeautifulSoup
from typing import Set

@dataclass
class GlobalVariable:
    path_error: int = field(default=0)
    exceptions: int = field(default=0)
    timeout_error: int = field(default=0)
    success: int = field(default=0)
    compared: int = field(default=0)
    total_data: int = field(default=0)
    nothing_changed: int = field(default=0)
    url_error: int = field(default=0)

def extractStringFromHTML(htmlString: str) -> str:
    soup = BeautifulSoup(htmlString, "html.parser")
    tags_to_remove: Set[str] = {'style', 'script', 'noscript', 'svg', 'link', 'meta', 'title'}
    for tag in tags_to_remove:
        for element in soup(tag):
            element.decompose()
    return soup.get_text(separator=" ", strip=True)