import difflib
import cdifflib
from dataclasses import dataclass
from main.logger import console_logger
from bs4 import BeautifulSoup
import re
from typing import Tuple

@dataclass
class OpticalCharacterRecognition:
    OLD_TEXT: str
    NEW_TEXT: str

    @staticmethod
    def extractInnerText(html_string: str) -> str:
        return BeautifulSoup(html_string, "html.parser").get_text(separator=" ", strip=True)

    @staticmethod
    def removeMultSpaces(txt: str) -> str:
        return re.sub(r"\s+", "", re.sub(" +", " ", txt))

    @staticmethod
    def removeNewline(text: str) -> str:
        return " ".join(text.splitlines())

    def calculateSimilarity(self) -> Tuple[bool, int]:
        old_text = self.removeMultSpaces(self.removeNewline(self.OLD_TEXT))
        new_text = self.removeMultSpaces(self.removeNewline(self.NEW_TEXT))

        similarity_ratio = cdifflib.CSequenceMatcher(a=old_text, b=new_text).quick_ratio()
        percentage_change = int(round((1 - similarity_ratio) * 100, 2))

        console_logger.info(f"Calculated Similarity: {percentage_change} % per should be greater than 3")
        # highlightDifference()
        return percentage_change > 3, percentage_change

    def highlightDifference(self) -> None:
        for item in difflib.Differ().compare(self.OLD_TEXT.splitlines(), self.NEW_TEXT.splitlines()):
            if item.startswith("- "):  # Deletion
                print(f"\033[91m{item[2:]}\033[0m")
            elif item.startswith("+ "):  # Addition
                print(f"\033[92m{item[2:]}\033[0m")
            elif not item.startswith("? "):  # Unchanged and not a hint line
                print(item[2:])