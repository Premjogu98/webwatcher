import difflib
from difflib import SequenceMatcher
from dataclasses import dataclass
from main.logger import console_logger
from bs4 import BeautifulSoup

@dataclass
class OpticalCharacterRecognition:
    OLD_TEXT: str
    NEW_TEXT: str
    
    def extractInnerText(self,html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        inner_text = soup.get_text(separator=' ', strip=True)
        return inner_text
    
    def calculateSimilarity(self):
        sequence_matcher = SequenceMatcher(None, self.extractInnerText(self.OLD_TEXT), self.extractInnerText(self.NEW_TEXT))
        similarity_ratio = sequence_matcher.ratio()
        percentage_change = round((1 - similarity_ratio) * 100, 2)
        console_logger.info(f"Calculated Similarity: {percentage_change} %")
        if percentage_change == 0.00:
            return False, percentage_change
        return True, percentage_change

    # Print differences with highlighting
    def highlightDifference(self):
        differ = difflib.Differ()
        diff = list(differ.compare(self.OLD_TEXT, self.NEW_TEXT))
        for item in diff:
            if item.startswith("- "):  # Deletion
                console_logger.debug("\033[91m" + item[2:] + "\033[0m", end="")
            elif item.startswith("+ "):  # Addition
                pass
                console_logger.debug("\033[92m" + item[2:] + "\033[0m", end="")
            else:
                console_logger.debug(item[2:], end="")