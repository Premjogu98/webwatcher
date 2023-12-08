from dataclasses import dataclass
from bs4 import BeautifulSoup


@dataclass
class GlobalVariable:
    path_error: int = 0
    exceptions: int = 0
    timeout_error: int = 0
    success: int = 0
    compared: int = 0
    total_data: int = 0
    nothing_changed: int = 0
    url_error: int = 0

def extractStringFromHTML(htmlString: str):
    soup = BeautifulSoup(htmlString, "html.parser")

    # Remove custom tags
    for style_tag in soup("style"):
        style_tag.decompose()
    for style_tag in soup("script"):
        style_tag.decompose()
    for style_tag in soup("noscript"):
        style_tag.decompose()
    for style_tag in soup("svg"):
        style_tag.decompose()
    for style_tag in soup("link"):
        style_tag.decompose()
    for style_tag in soup("meta"):
        style_tag.decompose()
    for style_tag in soup("title"):
        style_tag.decompose()
    # Get the inner text
    inner_text = soup.get_text(separator=" ", strip=True)
    return inner_text