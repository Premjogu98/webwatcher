import difflib
import cdifflib
# import difflib
from dataclasses import dataclass
from main.logger import console_logger
from bs4 import BeautifulSoup
import re

@dataclass
class OpticalCharacterRecognition:
    OLD_TEXT: str
    NEW_TEXT: str
    
    def extractInnerText(self,html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        inner_text = soup.get_text(separator=' ', strip=True)
        return inner_text
    
    def removeMultSpaces(self,txt:str):
        return re.sub(r"\s+", "", re.sub(' +', ' ', txt))
    
    def removeNewline(self,text:str):
        return " ".join(text.splitlines())
    
    def calculateSimilarity(self):
        old_text = self.removeMultSpaces(self.removeNewline(self.OLD_TEXT))
        new_text = self.removeMultSpaces(self.removeNewline(self.NEW_TEXT))

        # console_logger.debug("OLD TEXT "+ "="*40)
        # console_logger.debug(old_text)
        # console_logger.debug("NEW TEXT "+ "="*40)
        # console_logger.debug(new_text)
        # console_logger.debug("="*40)
        csequencematcher = cdifflib.CSequenceMatcher(a=old_text,  b=new_text)
        # console_logger.debug("="*40)
        similarity_ratio = csequencematcher.quick_ratio()

        percentage_change = int(round((1 - similarity_ratio) * 100, 2))
        console_logger.info(f"Calculated Similarity: {percentage_change} %")
        # console_logger.debug("="*40)
        if percentage_change == 0:
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